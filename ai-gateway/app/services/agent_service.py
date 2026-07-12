import json

from app.services.openai_service import OpenAIService
from app.services.tool_router import ToolRouter
from app.services.argument_resolver import ArgumentResolver
from app.services.conversation_service import ConversationService
from app.services.telemetry_service import TelemetryService
from core.mcp.manager import MCPManager


class AgentService:

    def __init__(self):
        self.openai = OpenAIService()
        self.mcp = MCPManager()
        self.router = ToolRouter()

    async def chat(self, message: str):

        tools = await self.mcp.list_tools()

        conversation = ConversationService.create()

        telemetry = TelemetryService()
        telemetry.begin()

        tools = await self.mcp.list_tools()

        decision = await self.openai.choose_tool(
            message,
            tools,
        )

        tool = json.loads(decision)

        arguments = ArgumentResolver.resolve(
            tool["tool"],
            tool["arguments"],
        )

        result = await self.router.execute(
            tool["tool"],
            arguments,
        )

        tool_text = ""

        if result.content:
            tool_text = "\n".join(
                block.text
                for block in result.content
                if hasattr(block, "text")
            )

        answer = await self.openai.summarize_result(
            message,
            tool["tool"],
            tool_text,
        )

        duration = telemetry.end()
        
        return {

            "conversation": conversation,

            "answer": answer,

            "execution": {

                "status": "success",

                "duration_ms": duration,

                "tool": tool["tool"],

                "server": "filesystem"

            },

            "steps": [

                {

                    "name": "LLM Tool Selection",

                    "status": "completed"

                },

                {

                    "name": "MCP Tool Execution",

                    "status": "completed"

                },

                {

                    "name": "LLM Response Generation",

                    "status": "completed"

                }

            ]

        }