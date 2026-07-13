import json

from app.services.argument_resolver import ArgumentResolver
from app.services.conversation_service import ConversationService
from app.services.openai_service import OpenAIService
from app.services.telemetry_service import TelemetryService
from app.services.tool_router import ToolRouter
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

        #
        # -------------------------------
        # TOOL SELECTION
        # -------------------------------
        #

        telemetry.start_step("tool_selection")

        all_tools = []

        #
        # Filesystem Tools
        #
        filesystem_tools = await self.mcp.list_tools("filesystem")

        for tool in filesystem_tools:
            all_tools.append(
                {
                    "server": "filesystem",
                    "name": tool.name,
                    "description": tool.description or "",
                }
            )

        #
        # Docker Tools
        #
        docker_tools = await self.mcp.list_tools("docker")

        for tool in docker_tools:
            all_tools.append(
                {
                    "server": "docker",
                    "name": tool.name,
                    "description": tool.description or "",
                }
            )

        candidate_tools = ToolSelector.select(
            message,
            all_tools,
        )

        print("\nAvailable tools sent to GPT:\n")

        for tool in candidate_tools:
            print(
                tool["server"],
                "->",
                tool["name"],
            )

        decision = await self.openai.choose_tool(
            message,
            candidate_tools,
        )

        print("\nGPT Decision:\n")
        print(decision)

        telemetry.end_step("tool_selection")

        #
        # -------------------------------
        # PARSE LLM RESPONSE
        # -------------------------------
        #

        try:
            plan = json.loads(decision)

        except json.JSONDecodeError:

            raise ValueError(
                f"Invalid JSON returned by OpenAI:\n\n{decision}"
            )

        arguments = ArgumentResolver.resolve(
            plan["tool"],
            plan.get("arguments", {}),
        )

        #
        # -------------------------------
        # EXECUTE TOOL
        # -------------------------------
        #

        telemetry.start_step("tool_execution")

        result = await self.router.execute(
            tool=plan["tool"],
            arguments=arguments,
            server=plan["server"],
        )

        telemetry.end_step("tool_execution")

        #
        # -------------------------------
        # FORMAT TOOL OUTPUT
        # -------------------------------
        #

        tool_text = ""

        if hasattr(result, "content") and result.content:

            tool_text = "\n".join(

                block.text

                for block in result.content

                if hasattr(block, "text")

            )

        else:

            tool_text = str(result)

        #
        # -------------------------------
        # RESPONSE GENERATION
        # -------------------------------
        #

        telemetry.start_step("response_generation")

        answer = await self.openai.summarize_result(
            user_message=message,
            tool_name=plan["tool"],
            tool_result=tool_text,
        )

        telemetry.end_step("response_generation")

        execution = telemetry.finish()

        return {

            "conversation": conversation,

            "answer": answer,

            "execution": {

                "status": "success",

                "duration_ms": execution["total"],

                "server": plan["server"],

                "tool": plan["tool"],

                "started_at": execution["started_at"],

                "completed_at": execution["completed_at"],

            },

            "steps": [

                {
                    "id": 1,
                    "title": "Tool Selection",
                    "description": "AI selected the appropriate MCP server and tool.",
                    "status": "completed",
                    "duration_ms": execution["steps"]["tool_selection"],
                },

                {
                    "id": 2,
                    "title": "Tool Execution",
                    "description": f'Executed "{plan["tool"]}" on {plan["server"]}.',
                    "status": "completed",
                    "duration_ms": execution["steps"]["tool_execution"],
                },

                {
                    "id": 3,
                    "title": "Response Generation",
                    "description": "Generated the final response.",
                    "status": "completed",
                    "duration_ms": execution["steps"]["response_generation"],
                },

            ],
        }