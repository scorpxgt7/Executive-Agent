# Executive Agent Platform

A production-grade Autonomous Operational Infrastructure platform capable of planning, delegating, executing, monitoring, learning, and coordinating multiple AI agents safely.

## Architecture

This platform implements a modular autonomous operational system with strict separation between reasoning and execution. The core components include:

- **Central Orchestrator**: AI-powered CEO that analyzes goals, generates plans, and coordinates execution
- **Durable Task System**: Temporal.io-based workflow engine for reliable task orchestration
- **Agent Registry**: Dynamic registration system for specialized AI agents
- **Memory Architecture**: Multi-layer memory system (short-term, episodic, semantic, organizational)
- **Permission & Governance**: Controlled autonomy with approval workflows
- **Execution Workers**: Isolated worker systems for safe task execution
- **Event-Driven System**: Kafka-based event streaming for observability
- **Observability Stack**: OpenTelemetry, Grafana, Prometheus for monitoring

## Quick Start

1. Clone the repository
2. Set up infrastructure: `docker-compose up -d`
3. Install dependencies: `pip install -r requirements.txt`
4. Start the API: `uvicorn api.main:app --reload`
5. Access dashboard at `http://localhost:3000`

## Development Philosophy

Prioritizes infrastructure, orchestration, memory, governance, recoverability, and observability over hype and fake autonomy. Designed for enterprise deployment readiness with controlled autonomy.

## Project Structure

```
/core              # Core platform components
  /orchestrator    # Central coordination logic
  /planner         # Goal decomposition and planning
  /scheduler       # Task scheduling and prioritization
  /memory          # Multi-layer memory system
  /approvals       # Permission and approval workflows
  /events          # Event publishing and streaming
  /governance      # Safety and compliance policies

/agents            # Specialized AI agents
  /planner         # Strategic planning agent
  /research        # Information gathering agent
  /marketing       # Marketing and content agent
  /analytics       # Data analysis agent
  /coding          # Software development agent

/workers           # Execution workers
  /browser         # Web automation worker
  /filesystem      # File system operations
  /deployment      # CI/CD and deployment
  /email           # Email communication
  /api             # External API integration

/ui                # Frontend dashboard
  /dashboard       # Main operations dashboard
  /monitoring      # Observability interface
  /approvals       # Approval management UI

/api               # REST API endpoints
/logs              # Centralized logging
/shared            # Common utilities and models
/tests             # Test suites
/docs              # Documentation
```

## Core Principles

1. **Reasoning ≠ Execution**: LLMs only reason and plan; workers execute safely
2. **Controlled Autonomy**: All sensitive actions require approval
3. **Reliable Infrastructure**: Durable workflows with retry and recovery
4. **Modular Architecture**: Components scale independently
5. **Enterprise Ready**: Built for production deployment and monitoring