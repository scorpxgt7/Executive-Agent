from datetime import datetime, timezone

from fastapi.testclient import TestClient

from api.main import app
from shared.models import ApprovalRequest, ExecutionPlan, Task


def _auth_headers(client: TestClient) -> dict[str, str]:
    response = client.post(
        "/api/v1/auth/login",
        json={"username": "admin", "password": "admin"},
    )
    assert response.status_code == 200
    return {"Authorization": f"Bearer {response.json()['access_token']}"}


def test_agents_endpoint_returns_registered_agents():
    client = TestClient(app)
    headers = _auth_headers(client)

    response = client.get("/api/v1/agents/", headers=headers)

    assert response.status_code == 200
    payload = response.json()
    assert payload["count"] >= 4
    assert {agent["id"] for agent in payload["agents"]} >= {
        "planner_agent",
        "research_agent",
        "marketing_agent",
        "analytics_agent",
    }


def test_tasks_endpoint_reads_in_memory_plan_store():
    client = TestClient(app)
    headers = _auth_headers(client)
    task = Task(
        id="api-task-test",
        goal_id="api-goal-test",
        description="Validate task API",
        type="research",
        parameters={"priority": 1},
        assigned_agent="research_agent",
        dependencies=[],
    )
    app.state.orchestrator.plan_store["api-plan-test"] = ExecutionPlan(
        id="api-plan-test",
        goal_id="api-goal-test",
        tasks=[task],
        created_at=datetime.now(timezone.utc),
    )

    list_response = client.get("/api/v1/tasks/", headers=headers)
    detail_response = client.get("/api/v1/tasks/api-task-test", headers=headers)

    assert list_response.status_code == 200
    assert any(item["id"] == "api-task-test" for item in list_response.json()["tasks"])
    assert detail_response.status_code == 200
    assert detail_response.json()["id"] == "api-task-test"


def test_approval_decision_updates_in_memory_state():
    client = TestClient(app)
    headers = _auth_headers(client)
    plan = ExecutionPlan(
        id="api-approval-plan",
        goal_id="api-approval-goal",
        tasks=[],
        approval_required=True,
        created_at=datetime.now(timezone.utc),
    )
    approval = ApprovalRequest(
        id="api-approval-request",
        plan_id=plan.id,
        type="sensitive",
        reason="Test approval flow",
        requested_by="test",
    )
    app.state.orchestrator.plan_store[plan.id] = plan
    app.state.orchestrator.approval_store[approval.id] = approval

    list_response = client.get("/api/v1/approvals/", headers=headers)
    approve_response = client.post(
        f"/api/v1/approvals/{approval.id}/approve",
        headers=headers,
        json={"decision": "approved", "notes": "Looks good"},
    )

    assert list_response.status_code == 200
    assert any(item["id"] == approval.id for item in list_response.json()["approvals"])
    assert approve_response.status_code == 200
    assert approve_response.json()["status"] == "approved"
    assert app.state.orchestrator.plan_store[plan.id].approved is True
    assert app.state.orchestrator.plan_store[plan.id].approval_required is False
