from fastapi import APIRouter, HTTPException, Depends, Request
from core.orchestrator.orchestrator import Orchestrator
from core.security.auth import verify_token, UserContext
from core.security.rbac import RBAC
from pydantic import BaseModel
import structlog

logger = structlog.get_logger()
router = APIRouter()


def get_orchestrator(request: Request):
    return request.app.state.orchestrator


class ApprovalResponse(BaseModel):
    """Approval response model"""
    approval_id: str
    plan_id: str
    status: str
    requested_by: str
    reason: str


class ApproveRequest(BaseModel):
    """Approve/reject request"""
    decision: str  # "approved" or "rejected"
    notes: str = None


@router.get("/", response_model=dict)
async def list_approvals(
    user: UserContext = Depends(verify_token),
    orchestrator: Orchestrator = Depends(get_orchestrator),
):
    """
    List approval requests

    Requires: APPROVALS_READ permission
    """
    if not RBAC.has_permission(user.roles, "approvals:read"):
        logger.warning(
            "approvals_list_permission_denied",
            user_id=user.user_id
        )
        raise HTTPException(status_code=403, detail="Permission denied")

    logger.info("approvals_list_requested", user_id=user.user_id)

    approvals = await orchestrator.list_approvals()
    return {
        "approvals": approvals,
        "count": len(approvals)
    }


@router.post("/{approval_id}/approve", response_model=dict)
async def approve_request(
    approval_id: str,
    request: ApproveRequest,
    orchestrator: Orchestrator = Depends(get_orchestrator),
    user: UserContext = Depends(verify_token)
):
    """
    Approve or reject an approval request

    Requires: APPROVALS_APPROVE permission
    """
    if not RBAC.has_permission(user.roles, "approvals:approve"):
        logger.warning(
            "approvals_approve_permission_denied",
            user_id=user.user_id,
            approval_id=approval_id
        )
        raise HTTPException(status_code=403, detail="Permission denied")

    logger.info(
        "approval_decision_made",
        user_id=user.user_id,
        approval_id=approval_id,
        decision=request.decision
    )

    try:
        result = await orchestrator.decide_approval(approval_id, request.decision, user.user_id)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    if not result:
        raise HTTPException(status_code=404, detail="Approval not found")

    if request.notes:
        result["notes"] = request.notes
    return result


@router.get("/{approval_id}")
async def get_approval(
    approval_id: str,
    orchestrator: Orchestrator = Depends(get_orchestrator),
    user: UserContext = Depends(verify_token)
):
    """
    Get approval details

    Requires: APPROVALS_READ permission
    """
    if not RBAC.has_permission(user.roles, "approvals:read"):
        logger.warning(
            "approval_read_permission_denied",
            user_id=user.user_id,
            approval_id=approval_id
        )
        raise HTTPException(status_code=403, detail="Permission denied")

    approval = await orchestrator.get_approval(approval_id)
    if not approval:
        raise HTTPException(status_code=404, detail="Approval not found")
    return approval
