# Executive Agent - Priority Action Items & Implementation Roadmap

**Generated**: May 14, 2026
**Status**: Ready for Implementation
**Owner**: Development Team

---

## PRIORITY CHECKLIST

### 🔴 CRITICAL - Start Immediately (Days 1-3)

- [ ] **Day 1 - Component Initialization**
  - [ ] Modify `api/main.py` to initialize Memory, Events, Orchestrator on startup
  - [ ] Remove silent failures in Temporal client connection
  - [ ] Add healthcheck endpoint that verifies all connections
  - **Files**: `api/main.py`, `core/orchestrator/orchestrator.py`
  - **Time**: 2 hours
  - **Owner**: Backend Lead

- [ ] **Day 1 - Fix Credentials Exposure**
  - [ ] Create `.env` template with all required variables
  - [ ] Update `docker-compose.yml` to use environment variables
  - [ ] Generate secure random defaults
  - [ ] Add `.env` to `.gitignore`
  - **Files**: `docker-compose.yml`, `.env.example`, `.gitignore`
  - **Time**: 1 hour
  - **Owner**: DevOps/Backend

- [ ] **Day 2 - Plan Persistence**
  - [ ] Add `execution_plans` table to `init.sql`
  - [ ] Modify orchestrator to write plans to database
  - [ ] Create database migration script
  - [ ] Update `GET /api/v1/goals/` to query database
  - **Files**: `init.sql`, `core/orchestrator/orchestrator.py`, `api/routes/goals.py`
  - **Time**: 3 hours
  - **Owner**: Backend Lead

- [ ] **Day 2 - Input Validation**
  - [ ] Add Pydantic request models to all API endpoints
  - [ ] Add middleware for request size validation
  - [ ] Validate all path parameters (goal_id, task_id, approval_id)
  - **Files**: `api/routes/*.py`, `api/middleware/*.py`
  - **Time**: 2 hours
  - **Owner**: Backend Engineer

- [ ] **Day 3 - CORS Security**
  - [ ] Change `allow_origins=["*"]` to specific domains
  - [ ] Set up environment-based CORS config
  - [ ] Remove `allow_credentials=True` unless needed
  - **Files**: `api/main.py`
  - **Time**: 30 minutes
  - **Owner**: Backend Lead

- [ ] **Day 3 - Path Traversal Fix**
  - [ ] Update `workers/filesystem/worker.py` to use `Path.resolve()`
  - [ ] Add symlink attack prevention
  - [ ] Add unit tests for path validation
  - **Files**: `workers/filesystem/worker.py`, `tests/test_filesystem_worker.py`
  - **Time**: 1 hour
  - **Owner**: Security Engineer

---

### 🟠 HIGH - Weeks 2-4

#### Authentication & Authorization (Week 2)

- [ ] **Create Security Module**
  ```
  core/security/
  ├── auth.py           # JWT implementation
  ├── rbac.py           # Role-based access control
  ├── permissions.py    # Permission checks
  └── tokens.py         # Token management
  ```
  - **Effort**: 8 hours
  - **Owner**: Backend Lead + Security Engineer

- [ ] **Implement JWT Authentication**
  - [ ] JWT token generation with expiration
  - [ ] Token refresh endpoint
  - [ ] Token validation middleware
  - [ ] User model with roles/permissions
  - **Time**: 6 hours
  - **Test**: 2 hours

- [ ] **Protect All Endpoints**
  - [ ] Add `Depends(verify_token)` to all routes
  - [ ] Add 401/403 error handlers
  - [ ] Implement rate limiting per user
  - [ ] Add request logging for audit
  - **Time**: 4 hours

- [ ] **User Management API**
  - [ ] `POST /api/v1/auth/register`
  - [ ] `POST /api/v1/auth/login`
  - [ ] `POST /api/v1/auth/refresh`
  - [ ] `GET /api/v1/users/me`
  - **Time**: 3 hours

#### Approval Workflow Implementation (Week 2-3)

- [ ] **Database Schema**
  - [ ] Create `agent_core.approval_requests` table with full tracking
  - [ ] Create `agent_core.approval_actions` for audit trail
  - [ ] Add indexes for common queries
  - **Time**: 1 hour

- [ ] **Approval Logic**
  - [ ] Create `ApprovalManager` class
  - [ ] Implement approval state machine (pending → approved/rejected)
  - [ ] Add permission checks for who can approve
  - [ ] Implement escalation rules
  - **Time**: 4 hours

- [ ] **API Endpoints** (Replace stubs)
  - [ ] `GET /api/v1/approvals/` - List pending
  - [ ] `GET /api/v1/approvals/{id}` - Get details
  - [ ] `POST /api/v1/approvals/{id}/approve` - Approve
  - [ ] `POST /api/v1/approvals/{id}/reject` - Reject
  - [ ] `GET /api/v1/approvals/{id}/history` - Audit trail
  - **Time**: 3 hours

- [ ] **Dashboard Integration**
  - [ ] Create `ApprovalsPanel.tsx` component
  - [ ] Add WebSocket support for real-time updates
  - [ ] Implement approval UI forms
  - **Time**: 4 hours (Frontend)

#### Task Execution Endpoints (Week 3-4)

- [ ] **Task API**
  - [ ] `GET /api/v1/tasks/` - List with filters
  - [ ] `GET /api/v1/tasks/{id}` - Get details
  - [ ] `POST /api/v1/tasks/{id}/execute` - Trigger execution
  - [ ] `GET /api/v1/tasks/{id}/history` - Execution history
  - **Time**: 3 hours

- [ ] **Task Status Tracking**
  - [ ] Update task status in database
  - [ ] Store execution results
  - [ ] Track execution timeline
  - **Time**: 2 hours

- [ ] **Dashboard Task Display**
  - [ ] Complete `TasksPanel.tsx`
  - [ ] Real-time status updates
  - [ ] Execution history view
  - **Time**: 3 hours (Frontend)

---

### 🟡 MEDIUM - Weeks 5-8

#### Temporal Workflow Implementation (Week 5)

- [ ] **Create Workflow File**
  ```python
  # core/orchestrator/workflows.py
  @workflow.defn
  class GoalExecutionWorkflow:
      @workflow.run
      async def run(self, plan_id: str) -> dict:
          # Orchestrate task execution
  ```
  - **Effort**: 6 hours

- [ ] **Activity Definitions**
  - [ ] `execute_task_activity` - Execute single task
  - [ ] `update_status_activity` - Update plan/task status
  - [ ] `handle_approval_activity` - Request approval
  - **Effort**: 4 hours

- [ ] **Workflow Logic**
  - [ ] Parallel task execution with dependencies
  - [ ] Retry logic with exponential backoff
  - [ ] Error handling and recovery
  - [ ] Timeout management
  - **Effort**: 6 hours

- [ ] **Integration**
  - [ ] Register workflow with Temporal client
  - [ ] Start workflow when plan created
  - [ ] Monitor workflow status
  - **Effort**: 3 hours

- [ ] **Testing**
  - [ ] Unit tests for workflow
  - [ ] Integration tests with workers
  - [ ] Failure scenario testing
  - **Effort**: 4 hours

#### Worker Completion (Week 6-7)

**Browser Worker** (40% → 100%)
- [ ] Implement page navigation
- [ ] Form filling and interaction
- [ ] Screenshot capture
- [ ] Error recovery
- [ ] Time estimate: 8 hours

**API Worker** (30% → 100%)
- [ ] HTTP client with timeout
- [ ] Request/response validation
- [ ] Auth header handling
- [ ] Retry logic
- [ ] Time estimate: 6 hours

**Email Worker** (0% → 100%)
- [ ] SMTP integration
- [ ] Email templating
- [ ] Attachment support
- [ ] Delivery tracking
- [ ] Time estimate: 6 hours

**Deployment Worker** (50% → 100%)
- [ ] Docker image building
- [ ] Kubernetes deployment
- [ ] Health check integration
- [ ] Rollback support
- [ ] Time estimate: 8 hours

#### Real-time Dashboard (Week 7-8)

- [ ] **WebSocket Implementation**
  - [ ] Set up Socket.io server
  - [ ] Goal status stream
  - [ ] Task execution events
  - [ ] Approval notifications
  - **Time**: 4 hours

- [ ] **Dashboard Components**
  - [ ] Live status indicators
  - [ ] Event feed
  - [ ] Real-time charts
  - [ ] Progress tracking
  - **Time**: 6 hours (Frontend)

- [ ] **Testing**
  - [ ] Unit tests (70%+ coverage)
  - [ ] Integration tests
  - [ ] Load testing (1000 concurrent)
  - [ ] Failure scenario tests
  - **Time**: 8 hours

---

## DETAILED IMPLEMENTATION GUIDE

### Phase 1: Critical Foundation (Days 1-3)

#### Task 1: Component Initialization Fix

**File**: `/workspaces/Executive-Agent/api/main.py`

```python
# ADD to top of file
import asyncio

# MODIFY: Add startup event
@app.on_event("startup")
async def startup_event():
    """Initialize all core components on startup"""
    try:
        # Initialize memory manager
        logger.info("Initializing memory manager...")
        await app.state.orchestrator.memory.initialize(
            redis_url=os.getenv("REDIS_URL", "redis://localhost:6379"),
            postgres_url=os.getenv("DATABASE_URL", "postgresql://agent_user:agent_password@localhost/executive_agent")
        )
        logger.info("Memory manager initialized successfully")

    except Exception as e:
        logger.warning("Memory manager initialization failed", error=str(e))
        logger.warning("Application will continue with limited memory features")

    try:
        # Initialize event publisher
        logger.info("Initializing event publisher...")
        await app.state.orchestrator.events.initialize(
            rabbitmq_url=os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost/")
        )
        logger.info("Event publisher initialized successfully")

    except Exception as e:
        logger.warning("Event publisher initialization failed", error=str(e))

    # Temporal client will be initialized when needed
    logger.info("Application startup complete")

@app.on_event("shutdown")
async def shutdown_event():
    """Clean up resources on shutdown"""
    await app.state.orchestrator.events.close()
```

---

#### Task 2: Plan Persistence

**File**: `/workspaces/Executive-Agent/init.sql` (ADD to end)

```sql
-- Execution Plans (if not exists)
CREATE TABLE IF NOT EXISTS agent_core.execution_plans (
    id VARCHAR(255) PRIMARY KEY,
    goal_id VARCHAR(255) REFERENCES agent_core.goals(id),
    tasks JSONB NOT NULL,
    approval_required BOOLEAN DEFAULT false,
    approved BOOLEAN DEFAULT false,
    learning_insights JSONB,
    status VARCHAR(50) DEFAULT 'planning',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    result JSONB,
    INDEX idx_execution_plans_goal_id (goal_id),
    INDEX idx_execution_plans_status (status)
);
```

**File**: `/workspaces/Executive-Agent/core/orchestrator/orchestrator.py` (MODIFY)

```python
# CHANGE THIS METHOD:
async def receive_goal(self, goal: Goal) -> str:
    """Receive and process a new goal"""
    logger.info("Received new goal", goal_id=goal.id, description=goal.description)

    # ... existing analysis and planning ...

    # ADD THIS LINE after plan creation:
    # Store plan to database (NEW)
    await self._persist_plan(plan)

    # ... rest of method ...

# ADD THIS NEW METHOD:
async def _persist_plan(self, plan: ExecutionPlan):
    """Persist execution plan to database"""
    if not self.memory or not self.memory.postgres:
        logger.warning("Database not available, plan not persisted", plan_id=plan.id)
        # Still store in memory for this session
        self.plan_store[plan.id] = plan
        return

    try:
        tasks_json = json.dumps([task.dict() for task in plan.tasks])
        insights_json = json.dumps(plan.learning_insights) if plan.learning_insights else None

        await self.memory.postgres.execute("""
            INSERT INTO agent_core.execution_plans
            (id, goal_id, tasks, approval_required, approved, learning_insights, status, created_at)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
            ON CONFLICT (id) DO UPDATE SET
                status = $7,
                learning_insights = $6,
                approved = $5
        """,
        plan.id, plan.goal_id, tasks_json,
        plan.approval_required, plan.approved,
        insights_json, "planning", plan.created_at)

        logger.info("Plan persisted", plan_id=plan.id)

    except Exception as e:
        logger.error("Failed to persist plan", plan_id=plan.id, error=str(e))
        # Fallback to memory
        self.plan_store[plan.id] = plan

# MODIFY: get_plan to check database first
def get_plan(self, plan_id: str) -> Optional[ExecutionPlan]:
    # First check memory
    if plan_id in self.plan_store:
        return self.plan_store[plan_id]

    # Could add database lookup here in future
    return None
```

---

#### Task 3: Input Validation

**Create**: `/workspaces/Executive-Agent/api/middleware/validation.py`

```python
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
import structlog

logger = structlog.get_logger()

class RequestValidationMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Validate request size
        content_length = request.headers.get('content-length')
        if content_length:
            try:
                size = int(content_length)
                if size > 10 * 1024 * 1024:  # 10MB limit
                    logger.warning("Request too large", size=size, path=request.url.path)
                    raise HTTPException(status_code=413, detail="Request payload too large")
            except ValueError:
                logger.warning("Invalid content-length header", path=request.url.path)

        response = await call_next(request)
        return response
```

**File**: `/workspaces/Executive-Agent/api/main.py` (ADD after CORS middleware)

```python
from api.middleware.validation import RequestValidationMiddleware

app.add_middleware(RequestValidationMiddleware)
```

---

### Phase 2: Security Hardening (Weeks 2-3)

#### Create Authentication Module

**Create**: `/workspaces/Executive-Agent/core/security/auth.py`

```python
from datetime import datetime, timedelta, timezone
from typing import Optional
import jwt
import os
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthCredentials
import structlog

logger = structlog.get_logger()

SECRET_KEY = os.getenv("JWT_SECRET_KEY", "change-me-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

security = HTTPBearer()

def create_access_token(user_id: str, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT token"""
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode = {
        "sub": user_id,
        "exp": expire,
        "iat": datetime.now(timezone.utc)
    }

    try:
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    except Exception as e:
        logger.error("Failed to create token", error=str(e))
        raise HTTPException(status_code=500, detail="Token creation failed")

async def verify_token(credentials: HTTPAuthCredentials = Depends(security)) -> str:
    """Verify JWT token and return user_id"""
    token = credentials.credentials

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user_id
    except jwt.ExpiredSignatureError:
        logger.warning("Token expired", token=token[:20])
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        logger.warning("Invalid token", token=token[:20])
        raise HTTPException(status_code=401, detail="Invalid token")
    except Exception as e:
        logger.error("Token verification failed", error=str(e))
        raise HTTPException(status_code=401, detail="Authentication failed")
```

#### Protect All Endpoints

**File**: `/workspaces/Executive-Agent/api/routes/goals.py` (UPDATE all endpoints)

```python
from fastapi import APIRouter, HTTPException, Depends, Request
from shared.models import Goal
from core.orchestrator.orchestrator import Orchestrator
from core.security.auth import verify_token
import structlog

router = APIRouter()
logger = structlog.get_logger()

def get_orchestrator(request: Request):
    return request.app.state.orchestrator

@router.post("/", response_model=dict)
async def create_goal(
    goal: Goal,
    user_id: str = Depends(verify_token),  # NEW: Require auth
    orchestrator: Orchestrator = Depends(get_orchestrator)
):
    """Create a new goal and start execution"""
    try:
        logger.info("create_goal_request", user_id=user_id, goal_id=goal.id)
        plan_id = await orchestrator.receive_goal(goal)
        plan = orchestrator.get_plan(plan_id)
        logger.info("create_goal_success", user_id=user_id, goal_id=goal.id, plan_id=plan_id)
        return {
            "plan_id": plan_id,
            "status": "accepted",
            "learning_insights": plan.learning_insights if plan else None
        }
    except Exception as e:
        logger.error("create_goal_failed", user_id=user_id, goal_id=goal.id, error=str(e))
        raise HTTPException(status_code=500, detail="Failed to process goal")

@router.get("/")
async def list_goals(
    user_id: str = Depends(verify_token),  # NEW: Require auth
    orchestrator: Orchestrator = Depends(get_orchestrator)
):
    """List all goals"""
    logger.info("list_goals_request", user_id=user_id)
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
```

---

### Environment Variables Configuration

**File**: `.env.example` (UPDATE)

```bash
# Database
DATABASE_URL=postgresql://agent_user:random_password_here@localhost:5432/executive_agent

# Redis
REDIS_URL=redis://localhost:6379
REDIS_PASSWORD=random_redis_password

# Temporal
TEMPORAL_ADDRESS=localhost:7233

# OpenAI
OPENAI_API_KEY=sk-your-api-key-here

# RabbitMQ
RABBITMQ_URL=amqp://guest:guest@localhost:5672/

# JWT Security
JWT_SECRET_KEY=generate-with-openssl-rand-hex-32
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30

# API Settings
API_RATE_LIMIT=100/hour
MAX_GOAL_BUDGET_USD=100

# Environment
ENVIRONMENT=development
LOG_LEVEL=INFO
DEBUG=false
```

---

## TESTING CHECKLIST

### Unit Tests to Create

- [ ] `tests/test_auth.py` - Authentication logic
- [ ] `tests/test_persistence.py` - Database operations
- [ ] `tests/test_validation.py` - Input validation
- [ ] `tests/test_workers.py` - Worker operations
- [ ] `tests/test_orchestrator_full.py` - Full flow

### Integration Tests

- [ ] End-to-end goal creation and execution
- [ ] Approval workflow
- [ ] Task execution with workers
- [ ] Error recovery scenarios

### Security Tests

- [ ] SQL injection attempts
- [ ] Path traversal attempts
- [ ] Authentication bypass attempts
- [ ] Rate limiting verification

---

## DEPLOYMENT STEPS

### Local Testing
1. Create `.env` from `.env.example` with test values
2. Run `docker-compose up -d`
3. Run `python -m pytest tests/` to validate
4. Start backend: `uvicorn api.main:app --reload`
5. Start dashboard: `npm start` in ui/dashboard

### Staging Deployment
1. Update environment variables for staging
2. Run migrations: `alembic upgrade head`
3. Deploy to staging Kubernetes cluster
4. Run smoke tests
5. Run load tests (100 concurrent users)

### Production Deployment
1. Complete security audit
2. Update production environment
3. Run migrations with backup
4. Deploy with canary release (10% traffic)
5. Monitor for 24 hours
6. Full rollout (100% traffic)

---

## METRICS & MONITORING

### Key Metrics to Track

- API response time (P50, P95, P99)
- OpenAI API call costs per hour
- Database connection pool utilization
- Task success/failure rate
- Approval workflow completion time
- Error rates by endpoint
- Concurrent active goals

### Alerts to Configure

- API latency > 500ms (P95)
- Error rate > 1%
- Database connections > 90%
- OpenAI API cost spike
- Task execution timeout
- Workflow failure rate

---

## Success Criteria

### By Day 3:
- [ ] All components initialize without errors
- [ ] Plans persist to database
- [ ] Credentials not exposed in code
- [ ] CORS properly restricted
- [ ] Path traversal fixed

### By Week 2:
- [ ] All endpoints require JWT authentication
- [ ] Rate limiting enforced
- [ ] Approval workflow logic implemented
- [ ] 50+ unit tests passing
- [ ] Zero critical security issues

### By Week 4:
- [ ] All approval endpoints functional
- [ ] Task execution endpoints working
- [ ] WebSocket real-time updates working
- [ ] 100+ tests passing (70%+ coverage)
- [ ] Load testing passed (1000 concurrent)

---

## Questions & Escalation

**For Security Issues**: Open GitHub Issue with label `security`
**For Architecture Decisions**: Schedule architecture review
**For Timeline Concerns**: Escalate to project manager
**For Blocker Issues**: Immediate Slack notification to #executive-agent channel

---

**Document Created**: May 14, 2026
**Last Updated**: May 14, 2026
**Owner**: Engineering Lead
**Distribution**: Development Team, Management
