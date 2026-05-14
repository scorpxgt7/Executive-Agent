import os
import json
import structlog
from typing import Dict, Any
from shared.models import ExecutionPlan, Goal

logger = structlog.get_logger()

class LearningManager:
    def __init__(self):
        self.logger = logger

    async def refine_execution_plan(self, plan: ExecutionPlan, goal: Goal, analysis: Dict[str, Any]) -> ExecutionPlan:
        """Refine the execution plan using learned insights and adaptive recommendations."""
        self.logger.info("Refining execution plan with learning insights", plan_id=plan.id, goal_id=goal.id)

        suggestions = await self._generate_learning_insights(goal, analysis, plan)
        plan.learning_insights = suggestions

        return plan

    async def _generate_learning_insights(self, goal: Goal, analysis: Dict[str, Any], plan: ExecutionPlan) -> Dict[str, Any]:
        """Generate adaptive guidance for plan optimization."""
        try:
            import openai
            client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

            prompt = f"""
            Based on this goal, analysis, and execution plan, provide a concise set of learning-based recommendations for optimization.

            Goal: {goal.description}
            Objectives: {', '.join(goal.objectives)}
            Analysis: {json.dumps(analysis)}
            Tasks: {[task.description for task in plan.tasks]}

            Return JSON with keys:
            - strategy_adjustments
            - risk_mitigations
            - performance_improvements
            - feedback_loops
            """

            response = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.4,
                max_tokens=500
            )

            content = response.choices[0].message.content
            json_text = content.strip('```json').strip('```').strip()
            return json.loads(json_text)
        except Exception as exc:
            self.logger.warning("Learning insights generation failed, using fallback", error=str(exc))
            return {
                "strategy_adjustments": ["Iterate quickly on the highest-impact tasks", "Use shorter feedback cycles for approval-sensitive work"],
                "risk_mitigations": ["Monitor external dependencies daily", "Limit agent budget for high-risk operations"],
                "performance_improvements": ["Cache repeated data analysis results", "Batch similar tasks for efficiency"],
                "feedback_loops": ["Capture task execution outcomes in semantic memory", "Review failed tasks within 1 hour"]
            }
