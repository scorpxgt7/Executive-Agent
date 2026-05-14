from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
async def health_check():
    """System health check"""
    return {"status": "healthy"}

@router.get("/metrics")
async def get_metrics():
    """Get system metrics"""
    return {"metrics": {}}