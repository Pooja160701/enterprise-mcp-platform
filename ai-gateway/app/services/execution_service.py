from app.services.tool_router import ToolRouter
from app.services.dependency_executor import DependencyExecutor
import json

class ExecutionService:

    def __init__(self):
        self.router = ToolRouter()

    async def execute_plan(
        self,
        plan,
    ):

        results = []

        for step in plan:

            resolved = DependencyExecutor.resolve(
                [step],
                results,
            )[0]

            response = await self.router.execute(
                server=resolved["server"],
                tool=resolved["tool"],
                arguments=resolved["arguments"],
            )

            output = self.extract_output(response)

            results.append(
                {
                    "server": resolved["server"],
                    "tool": resolved["tool"],
                    "result": output,
                }
            )

        print("\nExecution Results\n")
        from pprint import pprint
        pprint(results)

        return results

    def extract_output(
        self,
        response,
    ):
        """
        Convert MCP response into native Python objects.
        """

        #
        # FastMCP returns content blocks.
        #

        if hasattr(response, "content"):

            values = []

            for block in response.content:

                #
                # Structured JSON
                #

                if hasattr(block, "data"):

                    values.append(block.data)
                    continue

                #
                # Older MCP versions
                #

                if hasattr(block, "json"):

                    values.append(block.json)
                    continue

                #
                # Text response
                #

                if hasattr(block, "text"):

                    values.append(block.text)
                    continue

            if len(values) == 1:
                return values[0]

            return values

        #
        # Already decoded
        #

        return response