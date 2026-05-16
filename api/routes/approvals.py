from fastapi import APIRouter, HTTPException, Depends, Request
from core.security.auth import verify_token, UserContext
from core.security.rbac import RBAC
from pydantic import BaseModel
import structlog

logger = structlog.get_logger()
router = APIRouter()


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
async def list_approvals(user: UserContext = Depends(verify_token)):
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

    # TODO: Query from database when persistence is implemented
    return {
        "approvals": [],
        "count": 0
    }


@router.post("/{approval_id}/approve", response_model=dict)
async def approve_request(
    approval_id: str,
    request: ApproveRequest,
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

    # TODO: Persist decision to database and trigger appropriate workflow
    return {
        "approval_id": approval_id,
        "status": request.decision,
        "decided_by": user.user_id,
        "notes": request.notes
    }


@router.get("/{approval_id}")
async def get_approval(
    approval_id: str,
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

    # TODO: Query from database when persistence is implemented
    raise HTTPException(status_code=404, detail="Approval not found")