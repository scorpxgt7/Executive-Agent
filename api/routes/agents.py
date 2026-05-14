from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def list_agents():
    """List all agents"""
    return {"agents": []}

@router.post("/")
async def register_agent():
    """Register a new agent"""
    return {"status": "registered"}