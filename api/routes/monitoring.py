from fastapi import APIRouter, HTTPException, Depends
from core.security.auth import verify_token, UserContext
from core.security.rbac import RBAC
import structlog

logger = structlog.get_logger()
router = APIRouter()


@router.get("/health")
async def health_check(user: UserContext = Depends(verify_token)):
    """
    System health check

    Requires: MONITORING_READ permission
    """
    if not RBAC.has_permission(user.roles, "monitoring:read"):
        logger.warning(
            "monitoring_permission_denied",
            user_id=user.user_id
        )
        raise HTTPException(status_code=403, detail="Permission denied")

    return {"status": "healthy", "checked_by": user.user_id}


@router.get("/metrics")
async def get_metrics(user: UserContext = Depends(verify_token)):
    """
    Get system metrics

    Requires: MONITORING_READ permission
    """
    if not RBAC.has_permission(user.roles, "monitoring:read"):
        logger.warning(
            "metrics_access_denied",
            user_id=user.user_id
        )
        raise HTTPException(status_code=403, detail="Permission denied")

    logger.info("metrics_requested", user_id=user.user_id)

    # TODO: Collect metrics from system components
    return {
        "metrics": {},
        "timestamp": None,
        "collected_by": user.user_id
    }