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
from app.memory.memory_manager import MemoryManager


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
        # Memory
        # ---------------------------------------------
        #

        user_id = "default"

        MemoryManager.add_message(
            conversation_id=conversation_id,
            role="user",
            content=message,
        )

        MemoryManager.set_session(
            conversation_id,
            "last_user_message",
            message,
        )

        relevant_memory = MemoryManager.search(
            query=message,
            conversation_id=conversation_id,
            user_id=user_id,
            top_k=5,
        )

        print("\nRelevant Memory\n")

        print(
            json.dumps(
                relevant_memory,
                indent=2,
                default=str,
            )
        )

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
        # ---------------------------------------------
        # Memory Summary
        # ---------------------------------------------
        #

        memory_summary = MemoryManager.brief_summary(
            conversation_id,
        )

        print("\nConversation Summary\n")

        print(memory_summary)

        #
        # ------------------------------------------------
        # Fast Intent Detection
        # ------------------------------------------------
        #

        intent = self.intent_classifier.classify(message)

        #
        # ------------------------------------------------
        # Rule-based intent
        # ------------------------------------------------
        #

        if intent:

            print("\nIntent Match\n")
            print(json.dumps(intent, indent=2))

            plan = [
                {
                    "id": 1,
                    **intent,
                }
            ]

            planner_result = {

                "plan": plan,

                "confidence": {

                    "score": 100,

                    "grade": "A+",

                    "status": "Rule Match",

                },

                "validation": {

                    "valid": True,

                    "errors": [],

                    "warnings": [],

                },

                "repairs": [],

                "optimizations": [],

                "estimated_cost": 0,

            }

        else:

            print("\nUsing Planner...\n")

            planner_result = await self.planner.create_plan(

                user_message=message,

                candidate_tools=candidate_tools,

            )

            plan = planner_result["plan"]

        #
        # ------------------------------------------------
        # Planner Diagnostics
        # ------------------------------------------------
        #

        print("\nPlanner Output\n")

        print(
            json.dumps(
                plan,
                indent=2,
            )
        )

        print("\nPlanner Confidence\n")

        print(
            json.dumps(
                planner_result["confidence"],
                indent=2,
            )
        )

        print("\nPlanner Validation\n")

        print(
            json.dumps(
                planner_result["validation"],
                indent=2,
            )
        )

        print("\nPlanner Repairs\n")

        print(
            json.dumps(
                planner_result["repairs"],
                indent=2,
            )
        )

        print("\nPlanner Optimizations\n")

        print(
            json.dumps(
                planner_result["optimizations"],
                indent=2,
            )
        )

        print(
            f"\nEstimated Cost: {planner_result['estimated_cost']}"
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
        # ---------------------------------------------
        # Save Tool Results
        # ---------------------------------------------
        #

        MemoryManager.set_session(
            conversation_id,
            "last_results",
            results,
        )

        MemoryManager.add_semantic(
            text=tool_text if "tool_text" in locals() else str(results),
            metadata={
                "conversation": conversation_id,
            },
            tags=[
                "execution",
                "tool_result",
            ],
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

        #
        # ---------------------------------------------
        # Store Assistant Response
        # ---------------------------------------------
        #

        MemoryManager.add_message(
            conversation_id=conversation_id,
            role="assistant",
            content=answer,
        )

        MemoryManager.set_session(
            conversation_id,
            "last_answer",
            answer,
        )

        MemoryManager.remember(
            user_id=user_id,
            content=message,
            category="conversation",
            importance=60,
        )

        telemetry.end_step("response_generation")

        execution = telemetry.finish()

        return {
            "conversation": conversation,
            "answer": answer,
            "memory": {
                "summary": MemoryManager.summary(
                    conversation_id,
                ),
                "statistics": MemoryManager.stats(
                    conversation_id=conversation_id,
                    user_id=user_id,
                ),
            },
            "planner": {
                "confidence": planner_result["confidence"],
                "validation": planner_result["validation"],
                "repairs": planner_result["repairs"],
                "optimizations": planner_result["optimizations"],
                "estimated_cost": planner_result["estimated_cost"],
            },
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
