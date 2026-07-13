import json

from app.services.openai_service import OpenAIService
from app.services.tool_router import ToolRouter
from app.services.argument_resolver import ArgumentResolver
from app.services.conversation_service import ConversationService
from app.services.telemetry_service import TelemetryService
from app.services.tool_selector import ToolSelector
from core.mcp.manager import MCPManager


class AgentService:

    def __init__(self):
        self.openai = OpenAIService()
        self.mcp = MCPManager()
        self.router = ToolRouter()

    async def chat(self, message: str):

        conversation = ConversationService.create()

        telemetry = TelemetryService()
        telemetry.begin()
        telemetry.start_step("tool_selection")

        tools = await self.mcp.list_tools(
            server_name="filesystem"
        )

        candidate_tools = ToolSelector.select(
            message,
            tools,
        )

        decision = await self.openai.choose_tool(
            message,
            candidate_tools,
)

        telemetry.end_step("tool_selection")

        try:
            plan = json.loads(decision)
        except json.JSONDecodeError:
            raise ValueError(
                f"Invalid JSON returned by LLM: {decision}"
            )

        arguments = ArgumentResolver.resolve(
            plan["tool"],
            plan["arguments"],
        )

        telemetry.start_step("tool_execution")

        result = await self.router.execute(
            tool=plan["tool"],
            arguments=arguments,
            server=plan["server"],
        )

        telemetry.end_step("tool_execution")

        tool_text = ""

        if result.content:
            tool_text = "\n".join(
                block.text
                for block in result.content
                if hasattr(block, "text")
            )

        telemetry.start_step("response_generation")

        answer = await self.openai.summarize_result(
            message,
            plan["tool"],
            tool_text,
        )

        telemetry.end_step("response_generation")

        execution = telemetry.finish()

        return {

            "conversation": conversation,

            "answer": answer,

            "execution": {

                "status": "success",

                "duration_ms": execution["total"],

                "tool": plan["tool"],

                "server": plan["server"],

                "started_at": execution["started_at"],

                "completed_at": execution["completed_at"]

            },

            "steps": [

                {
                    "id": 1,
                    "title": "Tool Selection",
                    "description": "GPT selected the MCP tool.",
                    "status": "completed",
                    "duration_ms": execution["steps"]["tool_selection"]
                },

                {
                    "id": 2,
                    "title": "Tool Execution",
                    "description": f"Executed {plan['tool']} on {plan['server']} MCP.",
                    "status": "completed",
                    "duration_ms": execution["steps"]["tool_execution"]
                },

                {
                    "id": 3,
                    "title": "Response Generation",
                    "description": "Generated the final answer.",
                    "status": "completed",
                    "duration_ms": execution["steps"]["response_generation"]
                }

            ]
        }