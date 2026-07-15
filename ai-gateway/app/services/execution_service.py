import asyncio

from app.services.tool_router import ToolRouter
from app.services.dependency_executor import DependencyExecutor
from app.services.argument_resolver import ArgumentResolver


class ExecutionService:

    def __init__(self):
        self.router = ToolRouter()

    async def execute_plan(
        self,
        plan,
    ):

        execution_levels = DependencyExecutor.build(plan)

        print("\nExecution Levels\n")
        print(execution_levels)

        results = []

        for level in execution_levels:

            #
            # Resolve arguments using outputs
            # from previous execution levels.
            #

            resolved_level = []

            for step in level:

                resolved_step = step.copy()

                resolved_step["arguments"] = ArgumentResolver.resolve(
                    step.get(
                        "arguments",
                        {},
                    ),
                    results,
                )

                resolved_level.append(
                    resolved_step
                )

            print("\nExecuting Level\n")
            print(resolved_level)

            tasks = [
                self.execute_step(step)
                for step in resolved_level
            ]

            level_results = await asyncio.gather(
                *tasks,
                return_exceptions=False,
            )

            results.extend(level_results)

        print("\nExecution Results\n")
        print(results)

        return results

    async def execute_step(
        self,
        step,
    ):

        response = await self.router.execute(
            server=step["server"],
            tool=step["tool"],
            arguments=step.get(
                "arguments",
                {},
            ),
        )

        output = self.extract_output(response)

        return {
            "id": step["id"],
            "server": step["server"],
            "tool": step["tool"],
            "result": output,
        }

    def extract_output(
        self,
        response,
    ):

        #
        # MCP Content blocks
        #

        if hasattr(response, "content"):

            values = []

            for block in response.content:

                if hasattr(block, "text"):

                    values.append(block.text)

            #
            # Single object
            #

            if len(values) == 1:

                return values[0]

            return values

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

        return str(response)