from fastapi import APIRouter, HTTPException, Depends, Request
from core.orchestrator.orchestrator import Orchestrator
from core.security.auth import require_role, verify_token, UserContext
from core.security.rbac import RBAC
import structlog

logger = structlog.get_logger()
router = APIRouter()


def get_orchestrator(request: Request):
    return request.app.state.orchestrator


@router.get("/")
async def list_agents(
    user: UserContext = Depends(verify_token),
    orchestrator: Orchestrator = Depends(get_orchestrator),
):
    """
    List all agents

    Requires: AGENTS_READ permission
    """
    if not RBAC.has_permission(user.roles, "agents:read"):
        logger.warning(
            "agents_list_permission_denied",
            user_id=user.user_id
        )
        raise HTTPException(status_code=403, detail="Permission denied")

    logger.info("agents_list_requested", user_id=user.user_id)

    agents = await orchestrator.list_agents()
    return {"agents": agents, "count": len(agents)}


@router.post("/")
async def register_agent(user: UserContext = Depends(require_role(["admin", "operator"]))):
    """
    Register a new agent

    Requires: AGENTS_MANAGE permission
    """
    if not RBAC.has_permission(user.roles, "agents:manage"):
        logger.warning(
            "agent_registration_permission_denied",
            user_id=user.user_id
        )
        raise HTTPException(status_code=403, detail="Permission denied")

    logger.info("agent_registration_attempted", user_id=user.user_id)

    # TODO: Implement agent registration logic
    return {"status": "registered"}
