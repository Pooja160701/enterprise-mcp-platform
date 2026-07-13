import json

from app.services.argument_resolver import ArgumentResolver
from app.services.context_service import ContextService
from app.services.conversation_service import ConversationService
from app.services.execution_service import ExecutionService
from app.services.intent_service import IntentService
from app.services.memory_service import MemoryService
from app.services.openai_service import OpenAIService
from app.services.planner_service import PlannerService
from app.services.result_aggregator import ResultAggregator
from app.services.telemetry_service import TelemetryService
from app.services.tool_selector import ToolSelector

from core.mcp.manager import MCPManager


class AgentService:

    def __init__(self):

        self.openai = OpenAIService()

        self.mcp = MCPManager()

        self.planner = PlannerService()

        self.executor = ExecutionService()

        self.intent = IntentService()

    async def chat(
        self,
        message: str,
    ):

        conversation = ConversationService.create()

        conversation_id = conversation["id"]

        telemetry = TelemetryService()

        telemetry.begin()

        #
        # ---------------------------------------------------
        # Detect intent
        # ---------------------------------------------------
        #

        intent = await self.intent.detect(message)

        #
        # ---------------------------------------------------
        # Discover Tools
        # ---------------------------------------------------
        #

        telemetry.start_step("tool_selection")

        all_tools = []

        for server in intent:

            try:

                tools = await self.mcp.list_tools(server)

                for tool in tools:

                    all_tools.append(

                        {

                            "server": server,

                            "name": tool.name,

                            "description": tool.description or "",

                        }

                    )

            except Exception as e:

                print(f"Unable to load {server}: {e}")

        #
        # Rank tools
        #

        candidate_tools = ToolSelector.select(

            message,

            all_tools,

        )

        print("\nCandidate Tools\n")

        for tool in candidate_tools:

            print(

                f"{tool['server']} -> {tool['name']}"

            )

        #
        # ---------------------------------------------------
        # Planner
        # ---------------------------------------------------
        #

        plan = await self.planner.create_plan(

            message,

            candidate_tools,

        )

        print("\nExecution Plan\n")

        print(

            json.dumps(

                plan,

                indent=2,

            )

        )

        telemetry.end_step("tool_selection")

        #
        # ---------------------------------------------------
        # Resolve Arguments
        # ---------------------------------------------------
        #

        for step in plan:

            step["arguments"] = ArgumentResolver.resolve(

                step["tool"],

                step.get(

                    "arguments",

                    {},

                ),

            )

        #
        # ---------------------------------------------------
        # Execute
        # ---------------------------------------------------
        #

        telemetry.start_step("tool_execution")

        results = await self.executor.execute_plan(
            plan
        )

        memory = MemoryService.get_all(conversation_id)

        for step, item in zip(plan, results):

            ContextService.update(
                memory,
                step,
                item["output"],
            )

            MemoryService.save(
                conversation_id,
                "last_plan",
                plan,
            )

            MemoryService.save(
                conversation_id,
                "last_results",
                results,
            )

            MemoryService.save(
                conversation_id,
                "last_message",
                message,
            )

        telemetry.end_step("tool_execution")

        #
        # ---------------------------------------------------
        # Aggregate Results
        # ---------------------------------------------------
        #

        aggregated = ResultAggregator.aggregate(results)

        tool_text = aggregated["prompt"]

        #
        # ---------------------------------------------------
        # Generate Final Answer
        # ---------------------------------------------------
        #

        telemetry.start_step(

            "response_generation"

        )

        answer = await self.openai.summarize_result(

            user_message=message,

            tool_name=", ".join(

                step["tool"]

                for step in plan

            ),

            tool_result=tool_text,

        )

        telemetry.end_step(

            "response_generation"

        )

        execution = telemetry.finish()

        return {

            "conversation": conversation,

            "answer": answer,

            "execution": {

                "status": "success",

                "duration_ms": execution["total"],

                "server": ", ".join(

                    step["server"]

                    for step in plan

                ),

                "tool": ", ".join(

                    step["tool"]

                    for step in plan

                ),

                "started_at": execution["started_at"],

                "completed_at": execution["completed_at"],

            },

            "steps": [

                {

                    "id": 1,

                    "title": "Intent Detection & Planning",

                    "description": f"Detected '{intent}' intent and planned {len(plan)} tool(s).",

                    "status": "completed",

                    "duration_ms": execution["steps"]["tool_selection"],

                },

                {

                    "id": 2,

                    "title": "Tool Execution",

                    "description": f"Executed {len(plan)} MCP tool(s).",

                    "status": "completed",

                    "duration_ms": execution["steps"]["tool_execution"],

                },

                {

                    "id": 3,

                    "title": "Response Generation",

                    "description": "Generated the final AI response.",

                    "status": "completed",

                    "duration_ms": execution["steps"]["response_generation"],

                },

            ],

        }