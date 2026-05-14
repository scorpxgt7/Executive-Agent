from fastapi import APIRouter, HTTPException, Depends
from shared.models import Goal
from core.orchestrator.orchestrator import Orchestrator
import structlog

router = APIRouter()
logger = structlog.get_logger()

# Dependency to get orchestrator
def get_orchestrator():
    return Orchestrator()

@router.post("/", response_model=dict)
async def create_goal(goal: Goal, orchestrator: Orchestrator = Depends(get_orchestrator)):
    """Create a new goal and start execution"""
    try:
        plan_id = await orchestrator.receive_goal(goal)
        return {"plan_id": plan_id, "status": "accepted"}
    except Exception as e:
        logger.error("Failed to create goal", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to process goal")

@router.get("/{goal_id}")
async def get_goal_status(goal_id: str, orchestrator: Orchestrator = Depends(get_orchestrator)):
    """Get goal execution status"""
    # Query workflow status from Temporal
    return {"goal_id": goal_id, "status": "executing"}  # Placeholder

@router.get("/")
async def list_goals():
    """List all goals"""
    # Return from database
    return {"goals": []}