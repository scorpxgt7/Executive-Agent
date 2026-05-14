from temporalio import workflow
from temporalio.common import RetryPolicy
from shared.models import ExecutionPlan, Task
import structlog

logger = structlog.get_logger()

@workflow.defn
class GoalExecutionWorkflow:
    @workflow.run
    async def run(self, plan: ExecutionPlan) -> Dict[str, Any]:
        logger.info("Starting goal execution workflow", plan_id=plan.id)

        results = {}

        # Execute tasks in dependency order
        for task in plan.tasks:
            if task.dependencies:
                # Wait for dependencies
                await workflow.wait_condition(
                    lambda: all(results[dep_id]["status"] == "completed" for dep_id in task.dependencies)
                )

            # Execute task with retry
            result = await workflow.execute_activity(
                "execute_task",
                args=[task],
                retry_policy=RetryPolicy(
                    initial_interval=1,
                    backoff_coefficient=2,
                    maximum_interval=100,
                    maximum_attempts=3,
                ),
                start_to_close_timeout=300,  # 5 minutes
            )

            results[task.id] = result

            # Check if workflow should continue
            if result["status"] == "failed":
                # Handle failure - could escalate, retry, etc.
                pass

        logger.info("Goal execution completed", plan_id=plan.id)
        return {"status": "completed", "results": results}