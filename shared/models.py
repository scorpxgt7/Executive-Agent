from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime
from enum import Enum

class GoalStatus(str, Enum):
    PENDING = "pending"
    ANALYZING = "analyzing"
    PLANNING = "planning"
    APPROVAL_PENDING = "approval_pending"
    EXECUTING = "executing"
    COMPLETED = "completed"
    FAILED = "failed"

class TaskStatus(str, Enum):
    PENDING = "pending"
    ASSIGNED = "assigned"
    EXECUTING = "executing"
    COMPLETED = "completed"
    FAILED = "failed"

class Goal(BaseModel):
    id: str
    description: str
    objectives: List[str]
    constraints: Dict[str, Any]
    deadline: Optional[datetime]
    priority: int = 1
    status: GoalStatus = GoalStatus.PENDING
    created_at: datetime = datetime.utcnow()

class Task(BaseModel):
    id: str
    goal_id: str
    description: str
    type: str
    parameters: Dict[str, Any]
    assigned_agent: Optional[str]
    status: TaskStatus = TaskStatus.PENDING
    dependencies: List[str] = []
    created_at: datetime = datetime.utcnow()
    completed_at: Optional[datetime]

class ExecutionPlan(BaseModel):
    id: str
    goal_id: str
    tasks: List[Task]
    approval_required: bool = False
    approved: bool = False
    created_at: datetime

class Agent(BaseModel):
    id: str
    name: str
    role: str
    capabilities: List[str]
    tools: List[str]
    limits: Dict[str, Any]
    permissions: Dict[str, Any]
    active: bool = True

class ApprovalRequest(BaseModel):
    id: str
    plan_id: str
    type: str  # "safe", "sensitive", "critical"
    reason: str
    requested_by: str
    status: str = "pending"
    created_at: datetime

class MemoryEntry(BaseModel):
    id: str
    type: str  # "short_term", "episodic", "semantic", "organizational"
    content: Dict[str, Any]
    context: Dict[str, Any]
    timestamp: datetime
    expires_at: Optional[datetime]