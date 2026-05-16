from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import structlog
import os
from core.orchestrator.orchestrator import Orchestrator
from api.routes import goals, tasks, agents, approvals, monitoring, auth

# Configure structured logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

app = FastAPI(
    title="Executive Agent Platform",
    description="Autonomous Operational Infrastructure Platform",
    version="1.0.0"
)

# CORS middleware - configure allowed origins properly
allowed_origins = os.getenv(
    "ALLOWED_ORIGINS",
    "http://localhost:3000,http://localhost:8000"
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Initialize core components
orchestrator = Orchestrator()
app.state.orchestrator = orchestrator

# Include routers
app.include_router(auth.router)  # Auth routes - no prefix, includes /api/v1/auth
app.include_router(goals.router, prefix="/api/v1/goals", tags=["goals"])
app.include_router(tasks.router, prefix="/api/v1/tasks", tags=["tasks"])
app.include_router(agents.router, prefix="/api/v1/agents", tags=["agents"])
app.include_router(approvals.router, prefix="/api/v1/approvals", tags=["approvals"])
app.include_router(monitoring.router, prefix="/api/v1/monitoring", tags=["monitoring"])

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "components": {
            "memory": app.state.memory_initialized if hasattr(app.state, 'memory_initialized') else False,
            "events": app.state.events_initialized if hasattr(app.state, 'events_initialized') else False,
            "temporal": app.state.temporal_initialized if hasattr(app.state, 'temporal_initialized') else False,
        }
    }

@app.on_event("startup")
async def startup_event():
    """Initialize core components on application startup"""
    logger = structlog.get_logger()
    logger.info("startup_event_triggered")

    try:
        # Initialize memory manager
        logger.info("initializing_memory_manager")
        redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
        postgres_url = os.getenv(
            "DATABASE_URL",
            os.getenv("POSTGRES_URL", "postgresql://user:password@localhost:5432/executive_agent")
        )

        await app.state.orchestrator.memory.initialize(redis_url, postgres_url)
        app.state.memory_initialized = True
        logger.info("memory_manager_initialized")

    except Exception as e:
        logger.warning("memory_manager_initialization_failed", error=str(e))
        app.state.memory_initialized = False

    try:
        # Initialize event publisher
        logger.info("initializing_event_publisher")
        rabbitmq_url = os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost:5672/")

        await app.state.orchestrator.events.initialize(rabbitmq_url)
        app.state.events_initialized = True
        logger.info("event_publisher_initialized")

    except Exception as e:
        logger.warning("event_publisher_initialization_failed", error=str(e))
        app.state.events_initialized = False

    try:
        # Initialize Temporal client
        logger.info("initializing_temporal_client")
        temporal_server_url = os.getenv("TEMPORAL_ADDRESS", os.getenv("TEMPORAL_SERVER_URL", "localhost:7233"))

        # Temporal worker startup is intentionally kept out of the API process for now.
        # Mark this false unless a client has already been attached.
        logger.info("temporal_client_not_started_in_api_process", server=temporal_server_url)
        app.state.temporal_initialized = app.state.orchestrator.temporal_client is not None

    except Exception as e:
        logger.warning("temporal_client_initialization_failed", error=str(e))
        app.state.temporal_initialized = False

    logger.info("startup_complete", components={
        "memory": app.state.memory_initialized,
        "events": app.state.events_initialized,
        "temporal": app.state.temporal_initialized,
    })

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup resources on shutdown"""
    logger = structlog.get_logger()
    logger.info("shutdown_event_triggered")

    try:
        # Close memory connections
        if hasattr(app.state, 'orchestrator') and app.state.orchestrator.memory:
            await app.state.orchestrator.memory.close()
            logger.info("memory_manager_closed")
    except Exception as e:
        logger.warning("memory_manager_closure_failed", error=str(e))

    try:
        # Close event publisher
        if hasattr(app.state, 'orchestrator') and app.state.orchestrator.events:
            await app.state.orchestrator.events.close()
            logger.info("event_publisher_closed")
    except Exception as e:
        logger.warning("event_publisher_closure_failed", error=str(e))

    logger.info("shutdown_complete")
