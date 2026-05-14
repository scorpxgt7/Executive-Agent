from fastapi import APIRouter, HTTPException, Depends, Request
from shared.models import Goal
from core.orchestrator.orchestrator import Orchestrator
import structlog

router = APIRouter()
logger = structlog.get_logger()

# Dependency to get orchestrator from app state
def get_orchestrator(request: Request):
    return request.app.state.orchestrator

@router.post("/", response_model=dict)
async def create_goal(goal: Goal, orchestrator: Orchestrator = Depends(get_orchestrator)):
    """Create a new goal and start execution"""
    try:
        plan_id = await orchestrator.receive_goal(goal)
        plan = orchestrator.get_plan(plan_id)
        return {
            "plan_id": plan_id,
            "status": "accepted",
            "learning_insights": plan.learning_insights if plan else None
        }
    except Exception as e:
        logger.error("Failed to create goal", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to process goal")

@router.get("/{goal_id}")
async def get_goal_status(goal_id: str, orchestrator: Orchestrator = Depends(get_orchestrator)):
    """Get goal execution status"""
    plan = orchestrator.get_plan_by_goal(goal_id)
    if not plan:
        raise HTTPException(status_code=404, detail="Goal not found")

    return {
        "goal_id": goal_id,
        "plan_id": plan.id,
        "status": "executing",
        "learning_insights": plan.learning_insights,
        "task_count": len(plan.tasks)
    }

@router.get("/")
async def list_goals(orchestrator: Orchestrator = Depends(get_orchestrator)):
    """List all goals"""
    return {
        "goals": [
            {
                "goal_id": plan.goal_id,
                "plan_id": plan.id,
                "status": "executing",
                "learning_insights": plan.learning_insights,
                "task_count": len(plan.tasks),
            }
            for plan in orchestrator.plan_store.values()
        ]
    }