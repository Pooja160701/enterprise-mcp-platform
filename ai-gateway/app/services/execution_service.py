from app.services.tool_router import ToolRouter
from app.services.variable_resolver import VariableResolver


class ExecutionService:

    def __init__(self):
        self.router = ToolRouter()

    async def execute_plan(
        self,
        plan,
    ):

        results = []

        for step in plan:

            #
            # Resolve variables using previous results
            #
            resolved_plan = VariableResolver.resolve(
                [step],
                [
                    item["output"]
                    for item in results
                ],
            )

            resolved_step = resolved_plan[0]

            response = await self.router.execute(
                server=resolved_step["server"],
                tool=resolved_step["tool"],
                arguments=resolved_step["arguments"],
            )

            #
            # Convert MCP response into something reusable
            #
            output = self.extract_output(response)

            results.append(
                {
                    "server": resolved_step["server"],
                    "tool": resolved_step["tool"],
                    "arguments": resolved_step["arguments"],
                    "result": response,
                    "output": output,
                }
            )

        return results

    def extract_output(
        self,
        response,
    ):

        #
        # MCP normally returns content blocks.
        #

        if hasattr(response, "content"):

            for block in response.content:

                #
                # Text
                #

                if hasattr(block, "text"):

                    return {
                        "text": block.text,
                        "first_match": block.text,
                    }

        #
        # Dict
        #

        if isinstance(response, dict):

            return response

        #
        # List
        #

        if isinstance(response, list):

            if response:

                return {
                    "first_match": response[0]
                }

        return {
            "value": str(response)
        }