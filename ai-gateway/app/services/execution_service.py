import json

from app.planner.circuit_breaker import CircuitBreaker
from app.planner.dependency_executor import DependencyExecutor
from app.planner.result_cache import ResultCache
from app.planner.retry_engine import RetryEngine
from app.planner.timeout_manager import TimeoutManager
from app.planner.streaming_executor import StreamingExecutor

from app.services.tool_router import ToolRouter


class ExecutionService:

    def __init__(self):

        self.router = ToolRouter()

    async def execute_plan(
        self,
        plan,
    ):

        stream = StreamingExecutor()

        results = await stream.execute(
            plan=plan,
            executor=self,
        )

        print("\nExecution Stream\n")

        print(
            json.dumps(
                stream.history(),
                indent=2,
                default=str,
            )
        )

        print("\nExecution Results\n")

        print(
            json.dumps(
                results,
                indent=2,
                default=str,
            )
        )

        print("\nCache Statistics\n")

        print(
            json.dumps(
                ResultCache.stats(),
                indent=2,
            )
        )

        print("\nCircuit Breakers\n")

        print(
            json.dumps(
                CircuitBreaker.all_stats(),
                indent=2,
                default=str,
            )
        )

        return results

    async def execute_step(
        self,
        step,
        previous_results,
    ):
        """
        Execution Pipeline

            Resolve Arguments
                    ↓
               Cache Lookup
                    ↓
             Circuit Breaker
                    ↓
              Timeout Manager
                    ↓
                Retry Engine
                    ↓
              Execute MCP Tool
                    ↓
              Store In Cache
                    ↓
                 Return Result
        """

        #
        # Resolve placeholders
        #

        arguments = DependencyExecutor.resolve_arguments(
            step.get(
                "arguments",
                {},
            ),
            previous_results,
        )

        #
        # Cache lookup
        #

        cached = ResultCache.get(
            server=step["server"],
            tool=step["tool"],
            arguments=arguments,
        )

        if cached is not None:

            print(
                f"[CACHE HIT] {step['server']} -> {step['tool']}"
            )

            return {

                "id": step["id"],

                "server": step["server"],

                "tool": step["tool"],

                "result": cached,

                "cached": True,

            }

        print(
            f"[EXECUTE] {step['server']} -> {step['tool']}"
        )

        try:

            #
            # Circuit Breaker
            #

            response = await CircuitBreaker.execute(

                server=step["server"],

                coro=TimeoutManager.execute(

                    RetryEngine.execute(

                        self.router.execute,

                        server=step["server"],

                        tool=step["tool"],

                        arguments=arguments,

                    ),

                    server=step["server"],

                ),

            )

            output = self.extract_output(
                response
            )

            #
            # Store successful result
            #

            ResultCache.put(

                server=step["server"],

                tool=step["tool"],

                arguments=arguments,

                result=output,

            )

            return {

                "id": step["id"],

                "server": step["server"],

                "tool": step["tool"],

                "result": output,

                "cached": False,

            }

        except Exception as exc:

            return {

                "id": step["id"],

                "server": step["server"],

                "tool": step["tool"],

                "result": str(exc),

                "cached": False,

                "error": True,

            }

    def extract_output(
        self,
        response,
    ):

        #
        # MCP Content Blocks
        #

        if hasattr(
            response,
            "content",
        ):

            values = []

            for block in response.content:

                if hasattr(
                    block,
                    "text",
                ):

                    values.append(
                        block.text
                    )

            #
            # Single Block
            #

            if len(values) == 1:

                try:

                    return json.loads(
                        values[0]
                    )

                except Exception:

                    return values[0]

            #
            # Multiple Blocks
            #

            parsed = []

            for value in values:

                try:

                    parsed.append(
                        json.loads(value)
                    )

                except Exception:

                    parsed.append(value)

            return parsed

        #
        # Dictionary
        #

        if isinstance(
            response,
            dict,
        ):

            return response

        #
        # List
        #

        if isinstance(
            response,
            list,
        ):

            return response

        #
        # JSON String
        #

        if isinstance(
            response,
            str,
        ):

            try:

                return json.loads(
                    response
                )

            except Exception:

                return response

        #
        # Fallback
        #

        return str(response)