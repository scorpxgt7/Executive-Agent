import asyncio
import json
from typing import Dict, List, Any, Optional
from datetime import datetime, timezone
import structlog
from temporalio.client import Client
from temporalio import activity
from temporalio.worker import Worker
from core.memory.memory_manager import MemoryManager
from core.events.event_publisher import EventPublisher
from core.governance.permission_manager import PermissionManager
from core.learning.learning_manager import LearningManager
from agents.registry import AgentRegistry
from agents.planner.agent import PlannerAgent
from core.orchestrator.workflow import GoalExecutionWorkflow
from shared.models import Goal, Task, ExecutionPlan

logger = structlog.get_logger()

class Orchestrator:
    def __init__(self):
        self.memory = MemoryManager()
        self.events = EventPublisher()
        self.permissions = PermissionManager()
        self.agents = AgentRegistry()
        self.learning = LearningManager(memory=self.memory)
        self.temporal_client = None
        self.plan_store: Dict[str, ExecutionPlan] = {}

    async def initialize(self):
        # Initialize Temporal client
        self.temporal_client = await Client.connect("localhost:7233")

        # Register core agents
        await self._register_core_agents()

        # Start worker
        worker = Worker(
            self.temporal_client,
            task_queue="executive-agent-queue",
            workflows=[GoalExecutionWorkflow],
            activities=[self.execute_task_activity],
        )
        await worker.run()

    async def _register_core_agents(self):
        """Register core agents"""
        from shared.models import Agent

        # Register planner agent
        planner_agent = Agent(
            id="planner_agent",
            name="Strategic Planner",
            role="planner",
            capabilities=["goal_analysis", "strategy_planning", "task_decomposition", "risk_assessment"],
            tools=["openai", "analysis_frameworks"],
            limits={"daily_budget": 50, "max_parallel_tasks": 2},
            permissions={"requires_human_approval": False}
        )
        self.agents.register_agent(planner_agent)

        # Register research agent
        research_agent = Agent(
            id="research_agent",
            name="Research Analyst",
            role="research",
            capabilities=["market_research", "competitive_analysis", "data_gathering", "trend_analysis"],
            tools=["openai", "web_search", "data_analysis"],
            limits={"daily_budget": 30, "max_parallel_tasks": 3},
            permissions={"requires_human_approval": False}
        )
        self.agents.register_agent(research_agent)

        # Register marketing agent
        marketing_agent = Agent(
            id="marketing_agent",
            name="Content Marketer",
            role="marketing",
            capabilities=["content_creation", "social_media", "promotion_strategy", "brand_management"],
            tools=["openai", "content_tools", "social_platforms"],
            limits={"daily_budget": 40, "max_parallel_tasks": 2},
            permissions={"requires_human_approval": True}  # Content publishing needs approval
        )
        self.agents.register_agent(marketing_agent)

        # Register analytics agent
        analytics_agent = Agent(
            id="analytics_agent",
            name="Data Analyst",
            role="analytics",
            capabilities=["performance_analysis", "goal_tracking", "insight_generation", "reporting"],
            tools=["openai", "analytics_tools", "data_visualization"],
            limits={"daily_budget": 25, "max_parallel_tasks": 1},
            permissions={"requires_human_approval": False}
        )
        self.agents.register_agent(analytics_agent)

    async def receive_goal(self, goal: Goal) -> str:
        """Receive and process a new goal"""
        logger.info("Received new goal", goal_id=goal.id, description=goal.description)

        # Analyze goal
        analysis = await self._analyze_goal(goal)

        # Generate execution plan
        plan = await self._generate_plan(goal, analysis)

        # Refine plan using advanced learning insights
        plan = await self.learning.refine_execution_plan(plan, goal, analysis)

        # Check permissions and request approvals if needed
        approval_required = self.permissions.check_approval_required(plan)
        plan.approval_required = approval_required
        if approval_required:
            goal.status = "approval_pending"
        else:
            goal.status = "executing"

        # Store the execution plan locally and persist it when a database is available.
        self.plan_store[plan.id] = plan
        await self._persist_goal_plan_and_tasks(goal, plan)

        if approval_required:
            await self._request_approval(plan)
            return plan.id

        # Start execution workflow if the Temporal client is initialized
        if self.temporal_client is not None:
            await self.temporal_client.start_workflow(
                GoalExecutionWorkflow.run,
                args=[plan],
                id=f"goal-{goal.id}",
                task_queue="executive-agent-queue",
            )
        else:
            logger.info("Temporal client not initialized, skipping workflow start", plan_id=plan.id)

        # Emit event
        await self.events.publish("GOAL_RECEIVED", {"goal_id": goal.id, "plan_id": plan.id})

        return plan.id

    def get_plan(self, plan_id: str) -> Optional[ExecutionPlan]:
        return self.plan_store.get(plan_id)

    def get_plan_by_goal(self, goal_id: str) -> Optional[ExecutionPlan]:
        return next((plan for plan in self.plan_store.values() if plan.goal_id == goal_id), None)

    async def get_plan_by_goal_async(self, goal_id: str) -> Optional[ExecutionPlan]:
        """Get a plan by goal id, preferring memory and falling back to the database."""
        plan = self.get_plan_by_goal(goal_id)
        if plan:
            return plan

        row = await self._fetch_plan_row("goal_id", goal_id)
        if not row:
            return None
        return self._plan_from_row(row)

    async def list_goal_summaries(self) -> List[Dict[str, Any]]:
        """List goal summaries for the API, preferring database state when available."""
        if self.memory.postgres:
            try:
                rows = await self.memory.postgres.fetch("""
                    SELECT
                        p.id AS plan_id,
                        p.goal_id,
                        p.status,
                        p.learning_insights,
                        p.tasks,
                        g.priority
                    FROM agent_core.execution_plans p
                    LEFT JOIN agent_core.goals g ON g.id = p.goal_id
                    ORDER BY p.created_at DESC
                """)
                return [self._goal_summary_from_row(row) for row in rows]
            except Exception as e:
                logger.warning("Failed to list goals from database, using memory", error=str(e))

        return [
            {
                "goal_id": plan.goal_id,
                "plan_id": plan.id,
                "status": "approval_pending" if plan.approval_required and not plan.approved else "executing",
                "learning_insights": plan.learning_insights,
                "task_count": len(plan.tasks),
            }
            for plan in self.plan_store.values()
        ]

    async def _analyze_goal(self, goal: Goal) -> Dict[str, Any]:
        """Analyze goal using AI"""
        # Use OpenAI to analyze the goal
        import openai
        import os

        prompt = f"""
        Analyze this goal and provide a structured analysis:

        Goal: {goal.description}
        Objectives: {', '.join(goal.objectives)}
        Constraints: {goal.constraints}

        Provide analysis in JSON format:
        {{
            "complexity": "low|medium|high",
            "estimated_duration_days": number,
            "required_capabilities": ["list", "of", "capabilities"],
            "risk_level": "low|medium|high",
            "success_criteria": ["measurable", "criteria"],
            "potential_strategies": ["strategy1", "strategy2"],
            "required_agents": ["agent_type1", "agent_type2"]
        }}
        """

        try:
            client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=1000
            )

            analysis_text = response.choices[0].message.content
            # Parse JSON response
            import json
            analysis = json.loads(analysis_text.strip('```json').strip('```'))
            return analysis
        except Exception as e:
            logger.error("Failed to analyze goal with AI", error=str(e))
            # Fallback analysis when AI is unavailable or API key is missing
            return {
                "complexity": "medium",
                "estimated_duration_days": 30,
                "required_capabilities": ["research", "marketing", "analytics"],
                "risk_level": "medium",
                "success_criteria": ["earn $100 online"],
                "potential_strategies": ["content creation", "affiliate marketing", "freelancing"],
                "required_agents": ["planner", "research", "marketing", "analytics"]
            }

    async def _generate_plan(self, goal: Goal, analysis: Dict) -> ExecutionPlan:
        """Generate execution plan"""
        # Decompose goal into tasks
        tasks = await self._decompose_goal(goal, analysis)

        # Assign agents to tasks
        assigned_tasks = await self._assign_agents(tasks)

        plan = ExecutionPlan(
            id=f"plan-{goal.id}",
            goal_id=goal.id,
            tasks=assigned_tasks,
            created_at=datetime.now(timezone.utc)
        )

        return plan

    async def _decompose_goal(self, goal: Goal, analysis: Dict) -> List[Task]:
        """Break goal into executable tasks using planner agent"""
        planner = PlannerAgent()
        return await planner.create_execution_plan(goal, analysis)

    async def _assign_agents(self, tasks: List[Task]) -> List[Task]:
        """Assign appropriate agents to tasks"""
        for task in tasks:
            agent = self.agents.find_agent_for_task(task)
            task.assigned_agent = agent.id if agent else None
        return tasks

    async def _request_approval(self, plan: ExecutionPlan):
        """Request human approval for plan"""
        approval = self.permissions.create_approval_request(plan, requested_by="orchestrator")
        if self.memory.postgres:
            try:
                await self.memory.postgres.execute("""
                    INSERT INTO agent_core.approvals (
                        id, plan_id, type, reason, requested_by, status, created_at
                    )
                    VALUES ($1, $2, $3, $4, $5, $6, $7)
                    ON CONFLICT (id) DO UPDATE SET
                        status = EXCLUDED.status,
                        reason = EXCLUDED.reason
                """,
                approval.id,
                approval.plan_id,
                approval.type,
                approval.reason,
                approval.requested_by,
                approval.status,
                approval.created_at.replace(tzinfo=None) if approval.created_at.tzinfo else approval.created_at)
            except Exception as e:
                logger.warning("Failed to persist approval request", plan_id=plan.id, error=str(e))

        await self.events.publish(
            "APPROVAL_REQUESTED",
            {"approval_id": approval.id, "plan_id": plan.id, "type": approval.type}
        )

    async def _persist_goal_plan_and_tasks(self, goal: Goal, plan: ExecutionPlan) -> None:
        """Persist goal, execution plan, and tasks when Postgres is available."""
        if not self.memory.postgres:
            logger.debug("Postgres not initialized, keeping plan in memory", plan_id=plan.id)
            return

        try:
            async with self.memory.postgres.transaction():
                await self.memory.postgres.execute("""
                    INSERT INTO agent_core.goals (
                        id, description, objectives, constraints, deadline, priority, status, created_at, updated_at
                    )
                    VALUES ($1, $2, $3, $4, $5, $6, $7, $8, CURRENT_TIMESTAMP)
                    ON CONFLICT (id) DO UPDATE SET
                        description = EXCLUDED.description,
                        objectives = EXCLUDED.objectives,
                        constraints = EXCLUDED.constraints,
                        deadline = EXCLUDED.deadline,
                        priority = EXCLUDED.priority,
                        status = EXCLUDED.status,
                        updated_at = CURRENT_TIMESTAMP
                """,
                goal.id,
                goal.description,
                json.dumps(goal.objectives),
                json.dumps(goal.constraints),
                goal.deadline.replace(tzinfo=None) if goal.deadline and goal.deadline.tzinfo else goal.deadline,
                goal.priority,
                goal.status.value if hasattr(goal.status, "value") else str(goal.status),
                goal.created_at.replace(tzinfo=None) if goal.created_at.tzinfo else goal.created_at)

                tasks_json = json.dumps([task.model_dump(mode="json") for task in plan.tasks])
                insights_json = json.dumps(plan.learning_insights) if plan.learning_insights else None
                status = "approval_pending" if plan.approval_required and not plan.approved else "executing"

                await self.memory.postgres.execute("""
                    INSERT INTO agent_core.execution_plans (
                        id, goal_id, tasks, approval_required, approved, learning_insights, status, created_at
                    )
                    VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
                    ON CONFLICT (id) DO UPDATE SET
                        tasks = EXCLUDED.tasks,
                        approval_required = EXCLUDED.approval_required,
                        approved = EXCLUDED.approved,
                        learning_insights = EXCLUDED.learning_insights,
                        status = EXCLUDED.status
                """,
                plan.id,
                plan.goal_id,
                tasks_json,
                plan.approval_required,
                plan.approved,
                insights_json,
                status,
                plan.created_at.replace(tzinfo=None) if plan.created_at.tzinfo else plan.created_at)

                for task in plan.tasks:
                    await self.memory.postgres.execute("""
                        INSERT INTO agent_core.tasks (
                            id, goal_id, description, type, parameters, assigned_agent, status, dependencies, created_at
                        )
                        VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
                        ON CONFLICT (id) DO UPDATE SET
                            description = EXCLUDED.description,
                            type = EXCLUDED.type,
                            parameters = EXCLUDED.parameters,
                            assigned_agent = EXCLUDED.assigned_agent,
                            status = EXCLUDED.status,
                            dependencies = EXCLUDED.dependencies
                    """,
                    task.id,
                    task.goal_id,
                    task.description,
                    task.type,
                    json.dumps(task.parameters),
                    task.assigned_agent,
                    task.status.value if hasattr(task.status, "value") else str(task.status),
                    json.dumps(task.dependencies),
                    task.created_at.replace(tzinfo=None) if task.created_at.tzinfo else task.created_at)

            logger.info("Persisted goal execution plan", goal_id=goal.id, plan_id=plan.id)
        except Exception as e:
            logger.warning("Failed to persist execution plan, using memory fallback", plan_id=plan.id, error=str(e))

    async def _fetch_plan_row(self, column: str, value: str):
        if not self.memory.postgres:
            return None
        if column not in {"id", "goal_id"}:
            raise ValueError("Unsupported execution plan lookup")
        try:
            return await self.memory.postgres.fetchrow(
                f"SELECT * FROM agent_core.execution_plans WHERE {column} = $1",
                value
            )
        except Exception as e:
            logger.warning("Failed to fetch execution plan from database", column=column, value=value, error=str(e))
            return None

    def _plan_from_row(self, row) -> ExecutionPlan:
        tasks_data = self._json_value(row["tasks"], default=[])
        learning_insights = self._json_value(row["learning_insights"], default=None)
        plan = ExecutionPlan(
            id=row["id"],
            goal_id=row["goal_id"],
            tasks=[Task(**task) for task in tasks_data],
            approval_required=row["approval_required"],
            approved=row["approved"],
            learning_insights=learning_insights,
            created_at=row["created_at"],
        )
        self.plan_store[plan.id] = plan
        return plan

    def _goal_summary_from_row(self, row) -> Dict[str, Any]:
        tasks = self._json_value(row["tasks"], default=[])
        return {
            "goal_id": row["goal_id"],
            "plan_id": row["plan_id"],
            "status": row["status"],
            "learning_insights": self._json_value(row["learning_insights"], default=None),
            "task_count": len(tasks),
            "priority": row["priority"],
        }

    def _json_value(self, value, default):
        if value is None:
            return default
        if isinstance(value, str):
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                return default
        return value

    @activity.defn(name="execute_task")
    async def execute_task_activity(self, task: Task) -> Dict[str, Any]:
        """Activity to execute a task through appropriate agent"""
        logger.info("Executing task", task_id=task.id, task_type=task.type)

        try:
            # Route to appropriate agent based on task type
            result = await self._route_to_agent(task)

            # Update memory
            await self.memory.store_execution_result(task.id, result)

            # Emit event
            await self.events.publish("TASK_COMPLETED", {"task_id": task.id, "result": result})

            return result
        except Exception as e:
            logger.error("Task execution failed", task_id=task.id, error=str(e))
            await self.events.publish("TASK_FAILED", {"task_id": task.id, "error": str(e)})
            raise

    async def _route_to_agent(self, task: Task) -> Dict[str, Any]:
        """Route task to appropriate agent or worker"""
        task_type = task.type.lower()

        # Route to specialized agents
        if task_type in ["planning", "strategy", "analysis"]:
            from agents.planner.agent import PlannerAgent
            agent = PlannerAgent()
            if "analyze" in task.description.lower():
                return await agent.analyze_goal(self._get_goal_from_task(task), {})
            else:
                return await agent.create_execution_plan(self._get_goal_from_task(task), {})

        elif task_type in ["research", "market_research", "competitive_analysis"]:
            from agents.research.agent import ResearchAgent
            agent = ResearchAgent()
            if "competition" in task.description.lower():
                return await agent.analyze_competition(task)
            else:
                return await agent.conduct_research(task)

        elif task_type in ["marketing", "content", "promotion"]:
            from agents.marketing.agent import MarketingAgent
            agent = MarketingAgent()
            if "promote" in task.description.lower():
                return await agent.create_promotion_strategy(task)
            elif "optimize" in task.description.lower():
                return await agent.optimize_content(task)
            else:
                return await agent.create_content(task)

        elif task_type in ["analytics", "tracking", "insights"]:
            from agents.analytics.agent import AnalyticsAgent
            agent = AnalyticsAgent()
            if "track" in task.description.lower():
                return await agent.track_goals(task)
            elif "insight" in task.description.lower():
                return await agent.generate_insights(task)
            else:
                return await agent.analyze_performance(task)

        # Route to execution workers
        elif task_type in ["automation", "web", "browser"]:
            from workers.browser.worker import BrowserWorker
            worker = BrowserWorker()
            await worker.initialize()
            result = await worker.execute_task(task.parameters)
            await worker.cleanup()
            return result

        elif task_type in ["api", "webhook", "integration"]:
            from workers.api.worker import APIWorker
            worker = APIWorker()
            await worker.initialize()
            result = await worker.execute_task(task.parameters)
            await worker.cleanup()
            return result

        elif task_type in ["email", "notification"]:
            from workers.email.worker import EmailWorker
            worker = EmailWorker()
            result = await worker.execute_task(task.parameters)
            return result

        elif task_type in ["filesystem", "file", "storage"]:
            from workers.filesystem.worker import FilesystemWorker
            worker = FilesystemWorker()
            result = await worker.execute_task(task.parameters)
            return result

        elif task_type in ["deployment", "ci_cd", "infrastructure"]:
            from workers.deployment.worker import DeploymentWorker
            worker = DeploymentWorker()
            await worker.initialize()
            result = await worker.execute_task(task.parameters)
            await worker.cleanup()
            return result

        else:
            # Default fallback
            return {"status": "completed", "result": f"Task {task.id} executed via default handler"}

    def _get_goal_from_task(self, task: Task) -> Goal:
        """Get goal object from task (placeholder - would query database)"""
        # This would normally query the database for the goal
        return Goal(
            id=task.goal_id,
            description="Earn $100 online in 30 days",
            objectives=["Research opportunities", "Create content", "Monetize"]
        )

    async def monitor_execution(self, plan_id: str):
        """Monitor ongoing execution"""
        # Query Temporal for workflow status
        pass

    async def handle_failure(self, task_id: str, error: Exception):
        """Handle task failures"""
        logger.error("Task failed", task_id=task_id, error=str(error))

        # Implement retry logic, escalation, etc.
        await self.events.publish("TASK_FAILED", {"task_id": task_id, "error": str(error)})
