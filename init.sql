-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Create schemas
CREATE SCHEMA IF NOT EXISTS agent_core;
CREATE SCHEMA IF NOT EXISTS agent_memory;
CREATE SCHEMA IF NOT EXISTS agent_events;

-- Goals table
CREATE TABLE agent_core.goals (
    id VARCHAR(255) PRIMARY KEY,
    description TEXT NOT NULL,
    objectives JSONB,
    constraints JSONB,
    deadline TIMESTAMP,
    priority INTEGER DEFAULT 1,
    status VARCHAR(50) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tasks table
CREATE TABLE agent_core.tasks (
    id VARCHAR(255) PRIMARY KEY,
    goal_id VARCHAR(255) REFERENCES agent_core.goals(id),
    description TEXT NOT NULL,
    type VARCHAR(100) NOT NULL,
    parameters JSONB,
    assigned_agent VARCHAR(255),
    status VARCHAR(50) DEFAULT 'pending',
    dependencies JSONB DEFAULT '[]',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,
    result JSONB
);

-- Execution plans
CREATE TABLE agent_core.execution_plans (
    id VARCHAR(255) PRIMARY KEY,
    goal_id VARCHAR(255) REFERENCES agent_core.goals(id),
    tasks JSONB NOT NULL DEFAULT '[]',
    approval_required BOOLEAN DEFAULT false,
    approved BOOLEAN DEFAULT false,
    learning_insights JSONB,
    status VARCHAR(50) DEFAULT 'planning',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    result JSONB
);

-- Agents table
CREATE TABLE agent_core.agents (
    id VARCHAR(255) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    role VARCHAR(100) NOT NULL,
    capabilities JSONB DEFAULT '[]',
    tools JSONB DEFAULT '[]',
    limits JSONB DEFAULT '{}',
    permissions JSONB DEFAULT '{}',
    active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Approval requests
CREATE TABLE agent_core.approvals (
    id VARCHAR(255) PRIMARY KEY,
    plan_id VARCHAR(255) NOT NULL,
    type VARCHAR(50) NOT NULL,
    reason TEXT,
    requested_by VARCHAR(255),
    status VARCHAR(50) DEFAULT 'pending',
    approved_by VARCHAR(255),
    approved_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Memory tables
CREATE TABLE agent_memory.short_term (
    id SERIAL PRIMARY KEY,
    session_id VARCHAR(255),
    content JSONB NOT NULL,
    context JSONB,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP
);

CREATE TABLE agent_memory.episodic (
    id SERIAL PRIMARY KEY,
    task_id VARCHAR(255),
    content JSONB NOT NULL,
    outcome JSONB,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE agent_memory.semantic (
    id VARCHAR(255) PRIMARY KEY,
    content VECTOR(1536), -- OpenAI embedding dimension
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Events table
CREATE TABLE agent_events.events (
    id SERIAL PRIMARY KEY,
    event_type VARCHAR(100) NOT NULL,
    payload JSONB NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    source VARCHAR(255)
);

-- Indexes
CREATE INDEX idx_goals_status ON agent_core.goals(status);
CREATE INDEX idx_execution_plans_goal_id ON agent_core.execution_plans(goal_id);
CREATE INDEX idx_execution_plans_status ON agent_core.execution_plans(status);
CREATE INDEX idx_tasks_goal_id ON agent_core.tasks(goal_id);
CREATE INDEX idx_tasks_status ON agent_core.tasks(status);
CREATE INDEX idx_approvals_status ON agent_core.approvals(status);
CREATE INDEX idx_events_type ON agent_events.events(event_type);
CREATE INDEX idx_events_timestamp ON agent_events.events(timestamp);
CREATE INDEX idx_memory_short_term_expires ON agent_memory.short_term(expires_at);
CREATE INDEX idx_memory_episodic_task ON agent_memory.episodic(task_id);
