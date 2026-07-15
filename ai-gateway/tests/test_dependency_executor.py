import asyncio
import json

from app.planner.dependency_executor import DependencyExecutor


#
# Fake executor
#

class FakeExecutor:

    async def execute_step(
        self,
        step,
        previous_results,
    ):

        print(
            f"Executing Step {step['id']} -> {step['tool']}"
        )

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

    print("\nExecution Plan\n")

    print(
        json.dumps(
            plan,
            indent=2,
        )
    )

    print("\nDependency Levels\n")

    levels = DependencyExecutor.execution_levels(
        plan
    )

    print(levels)

    print("\nExecuting Plan\n")

    executor = FakeExecutor()

    results = await DependencyExecutor.execute(

        plan=plan,

        executor=executor,

    )

    print("\nResults\n")

    print(
        json.dumps(
            results,
            indent=2,
        )
    )


if __name__ == "__main__":

    asyncio.run(main())