import asyncio
import json

from app.planner.streaming_executor import StreamingExecutor


class FakeExecutor:

    async def execute_step(
        self,
        step,
        previous_results,
    ):

        await asyncio.sleep(0.5)

        return {

            "id": step["id"],

            "server": step["server"],

            "tool": step["tool"],

            "result": f"Completed {step['tool']}",

        }


plan = [

    {
        "id": 1,
        "server": "github",
        "tool": "list_repositories",
        "arguments": {},
        "depends_on": [],
    },

    {
        "id": 2,
        "server": "github",
        "tool": "list_branches",
        "arguments": {
            "repository": "enterprise-mcp-platform",
        },
        "depends_on": [1],
    },

    {
        "id": 3,
        "server": "github",
        "tool": "latest_commit",
        "arguments": {
            "repository": "enterprise-mcp-platform",
        },
        "depends_on": [1],
    },

    {
        "id": 4,
        "server": "github",
        "tool": "list_workflows",
        "arguments": {
            "repository": "enterprise-mcp-platform",
        },
        "depends_on": [2, 3],
    },

]


async def main():

    executor = StreamingExecutor()

    print("\nExecuting Streaming Plan\n")

    results = await executor.execute(

        plan,

        FakeExecutor(),

    )

    print("\nExecution Results\n")

    print(
        json.dumps(
            results,
            indent=2,
        )
    )

    print("\nStream Events\n")

    print(
        json.dumps(
            executor.history(),
            indent=2,
            default=str,
        )
    )

    print("\nStatistics\n")

    print(
        f"Total Events : {len(executor.history())}"
    )

    print(
        f"Total Results: {len(results)}"
    )


if __name__ == "__main__":

    asyncio.run(main())