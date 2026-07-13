import json

from app.services.openai_service import OpenAIService


class PlannerService:

    def __init__(self):
        self.openai = OpenAIService()

    async def create_plan(
        self,
        message: str,
        tools: list,
    ):

        decision = await self.openai.choose_tool(
            message,
            tools,
        )

        try:
            plan = json.loads(decision)

        except json.JSONDecodeError:

            raise ValueError(
                f"Invalid JSON returned by OpenAI:\n\n{decision}"
            )

        #
        # Allow GPT to return either:
        #
        # { ... }
        #
        # or
        #
        # [ ... ]
        #

        if isinstance(plan, dict):
            return [plan]

        return plan