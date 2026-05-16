from fastapi import APIRouter, HTTPException, Depends
from core.security.auth import verify_token, UserContext
from core.security.rbac import RBAC
import structlog

logger = structlog.get_logger()
router = APIRouter()


@router.get("/")
async def list_tasks(user: UserContext = Depends(verify_token)):
    """
    List all tasks

    Requires: TASKS_READ permission
    """
    if not RBAC.has_permission(user.roles, "tasks:read"):
        logger.warning(
            "tasks_list_permission_denied",
            user_id=user.user_id
        )
        raise HTTPException(status_code=403, detail="Permission denied")

    logger.info("tasks_list_requested", user_id=user.user_id)

    # TODO: Query from database
    return {"tasks": [], "count": 0}


@router.get("/{task_id}")
async def get_task(task_id: str, user: UserContext = Depends(verify_token)):
    """
    Get task details

    Requires: TASKS_READ permission
    """
    if not RBAC.has_permission(user.roles, "tasks:read"):
        logger.warning(
            "task_read_permission_denied",
            user_id=user.user_id,
            task_id=task_id
        )
        raise HTTPException(status_code=403, detail="Permission denied")

    # TODO: Query from database
    raise HTTPException(status_code=404, detail="Task not found")