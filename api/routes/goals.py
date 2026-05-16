from fastapi import APIRouter, HTTPException, Depends, Request
from shared.models import Goal
from core.orchestrator.orchestrator import Orchestrator
from core.security.auth import verify_token, UserContext
from core.security.rbac import RBAC
import structlog

router = APIRouter()
logger = structlog.get_logger()

# Dependency to get orchestrator from app state
def get_orchestrator(request: Request):
    return request.app.state.orchestrator

@router.post("/", response_model=dict)
async def create_goal(
    goal: Goal,
    orchestrator: Orchestrator = Depends(get_orchestrator),
    user: UserContext = Depends(verify_token)
):
    """
    Create a new goal and start execution

    Requires: GOALS_CREATE permission
    """
    # Check permission
    if not RBAC.can_access_goal(user.roles, "create"):
        logger.warning(
            "goal_creation_permission_denied",
            user_id=user.user_id,
            roles=user.roles
        )
        raise HTTPException(status_code=403, detail="Permission denied")

    try:
        logger.info(
            "goal_creation_requested",
            user_id=user.user_id,
            goal_description=goal.description[:50] if goal.description else None
        )

        plan_id = await orchestrator.receive_goal(goal)
        plan = orchestrator.get_plan(plan_id)

        return {
            "plan_id": plan_id,
            "status": "accepted",
            "learning_insights": plan.learning_insights if plan else None
        }
    except Exception as e:
        logger.error(
            "goal_creation_failed",
            error=str(e),
            user_id=user.user_id
        )
        raise HTTPException(status_code=500, detail="Failed to process goal")

@router.get("/{goal_id}")
async def get_goal_status(
    goal_id: str,
    orchestrator: Orchestrator = Depends(get_orchestrator),
    user: UserContext = Depends(verify_token)
):
    """
    Get goal execution status

    Requires: GOALS_READ permission
    """
    # Check permission
    if not RBAC.can_access_goal(user.roles, "read"):
        logger.warning(
            "goal_read_permission_denied",
            user_id=user.user_id,
            goal_id=goal_id
        )
        raise HTTPException(status_code=403, detail="Permission denied")

    plan = await orchestrator.get_plan_by_goal_async(goal_id)
    if not plan:
        raise HTTPException(status_code=404, detail="Goal not found")

    return {
        "goal_id": goal_id,
        "plan_id": plan.id,
        "status": "approval_pending" if plan.approval_required and not plan.approved else "executing",
        "learning_insights": plan.learning_insights,
        "task_count": len(plan.tasks)
    }

@router.get("/")
async def list_goals(
    orchestrator: Orchestrator = Depends(get_orchestrator),
    user: UserContext = Depends(verify_token)
):
    """
    List all goals

    Requires: GOALS_READ permission
    """
    # Check permission
    if not RBAC.can_access_goal(user.roles, "read"):
        logger.warning(
            "goals_list_permission_denied",
            user_id=user.user_id
        )
        raise HTTPException(status_code=403, detail="Permission denied")

    return {"goals": await orchestrator.list_goal_summaries()}
