import json

from core.mcp.manager import MCPManager

from app.services.argument_resolver import ArgumentResolver
from app.services.context_extractor import ContextExtractor
from app.services.context_store import ContextStore
from app.services.conversation_service import ConversationService
from app.services.execution_service import ExecutionService
from app.services.intent_classifier import IntentClassifier
from app.services.memory_service import MemoryService
from app.services.openai_service import OpenAIService
from app.services.planner_service import PlannerService
from app.services.result_aggregator import ResultAggregator
from app.services.telemetry_service import TelemetryService
from app.services.tool_selector import ToolSelector


class AgentService:
    """
    Enterprise AI Agent

    Pipeline

    User
        ↓
    Intent Detection
        ↓
    Tool Discovery
        ↓
    Tool Ranking
        ↓
    Planner (if required)
        ↓
    Argument Resolution
        ↓
    Tool Execution
        ↓
    Context Update
        ↓
    Result Aggregation
        ↓
    OpenAI Response
    """

    def __init__(self):

        self.openai = OpenAIService()

        self.mcp = MCPManager()

        self.planner = PlannerService()

        self.executor = ExecutionService()

        self.intent_classifier = IntentClassifier()

        self.context_store = ContextStore()

        self.context_extractor = ContextExtractor()

    async def chat(
        self,
        message: str,
    ):

        #
        # ---------------------------------------------
        # Conversation
        # ---------------------------------------------
        #

        conversation = ConversationService.create()

        conversation_id = conversation["id"]

        #
        # ---------------------------------------------
        # Telemetry
        # ---------------------------------------------
        #

        telemetry = TelemetryService()

        telemetry.begin()

        #
        # ---------------------------------------------
        # Conversation Context
        # ---------------------------------------------
        #

        ContextStore.update(
            conversation_id,
            **ContextExtractor.extract(message),
        )

        memory = ContextStore.get(conversation_id)

        print("\nConversation Context\n")
        print(json.dumps(memory, indent=2))

        #
        # ---------------------------------------------
        # Tool Discovery
        # ---------------------------------------------
        #

        telemetry.start_step("tool_selection")

        all_tools = []

        servers = [
            "filesystem",
            "docker",
            "github",
            "kubernetes",
            "postgres",
            "prometheus",
            "grafana",
            "aws",
        ]

        for server in servers:

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

            except Exception:

                #
                # Ignore offline servers
                #
                pass

        print("\nDiscovered Tools\n")

        for tool in all_tools:

            print(f'{tool["server"]} -> {tool["name"]}')

        #
        # ---------------------------------------------
        # Rank candidate tools
        # ---------------------------------------------
        #

        candidate_tools = ToolSelector.select(
            message,
            all_tools,
        )

        print("\nCandidate Tools\n")

        for tool in candidate_tools:

            print(f'{tool["server"]} -> {tool["name"]}')

        #
        # ------------------------------------------------
        # Fast Intent Detection
        # ------------------------------------------------
        #

        intent = self.intent_classifier.classify(message)

        if intent:

            print("\nIntent Match\n")
            print(json.dumps(intent, indent=2))

            plan = [
                {
                    "id": 1,
                    **intent,
                }
            ]

        else:

            print("\nUsing Planner...\n")

        plan = await self.planner.create_plan(
            user_message=message,
            candidate_tools=candidate_tools,
        )

        print("\nPlanner Output\n")

        print(
            json.dumps(
                plan,
                indent=2,
            )
        )

        telemetry.end_step("tool_selection")

        #
        # ------------------------------------------------
        # Execute Plan
        # ------------------------------------------------
        #

        telemetry.start_step("tool_execution")

        results = await self.executor.execute_plan(plan)

        telemetry.end_step("tool_execution")

        print("\nExecution Results\n")

        print(
            json.dumps(
                results,
                indent=2,
                default=str,
            )
        )

        #
        # ------------------------------------------------
        # Update Context
        # ------------------------------------------------
        #

        for step, result in zip(plan, results):

            ContextStore.update(
                conversation_id,
                last_server=step["server"],
                last_tool=step["tool"],
            )

        MemoryService.save(
            conversation_id,
            "last_message",
            message,
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

        #
        # ------------------------------------------------
        # Aggregate Tool Results
        # ------------------------------------------------
        #

        aggregated = ResultAggregator.aggregate(results)

        tool_text = aggregated["prompt"]

        print("\nAggregated Prompt\n")

        print(tool_text)

        #
        # ------------------------------------------------
        # Generate Response
        # ------------------------------------------------
        #

        telemetry.start_step("response_generation")

        answer = await self.openai.summarize_result(
            user_message=message,
            tool_name=", ".join(step["tool"] for step in plan),
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
                "server": ", ".join(step["server"] for step in plan),
                "tool": ", ".join(step["tool"] for step in plan),
                "started_at": execution["started_at"],
                "completed_at": execution["completed_at"],
            },
            "steps": [
                {
                    "id": 1,
                    "title": "Planning",
                    "description": f"Planned {len(plan)} step(s).",
                    "status": "completed",
                    "duration_ms": execution["steps"]["tool_selection"],
                },
                {
                    "id": 2,
                    "title": "Execution",
                    "description": f"Executed {len(results)} tool(s).",
                    "status": "completed",
                    "duration_ms": execution["steps"]["tool_execution"],
                },
                {
                    "id": 3,
                    "title": "Response",
                    "description": "Generated final AI response.",
                    "status": "completed",
                    "duration_ms": execution["steps"]["response_generation"],
                },
            ],
        }
