import asyncio

from app.services.tool_router import ToolRouter


class ExecutionService:

    def __init__(self):
        self.router = ToolRouter()

    async def execute_plan(
        self,
        plan,
    ):

        tasks = []

        for step in plan:

            tasks.append(

                self.router.execute(

                    server=step["server"],

                    tool=step["tool"],

                    arguments=step["arguments"],

                )

            )

        responses = await asyncio.gather(
            *tasks
        )

        results = []

        for step, response in zip(
            plan,
            responses,
        ):

            results.append(

                {

                    "server": step["server"],

                    "tool": step["tool"],

                    "result": response,

                }

            )

        return results