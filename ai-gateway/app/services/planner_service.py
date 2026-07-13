import json

from app.services.openai_service import OpenAIService
from app.services.prompt_builder import PromptBuilder
from app.services.plan_validator import PlanValidator


class PlannerService:

    def __init__(self):

        self.openai = OpenAIService()

    async def create_plan(
        self,
        message: str,
        tools: list[dict],
    ):

        prompt = PromptBuilder.build_planner_prompt(
            message,
            tools,
        )

        response = await self.openai.chat(prompt)

        print("\nPlanner Raw Output\n")
        print(response)

        return PlanValidator.validate(response)