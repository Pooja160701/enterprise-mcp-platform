import asyncio

from app.planner.timeout_manager import TimeoutManager


async def slow_task():

    print("Task started...")

    await asyncio.sleep(20)      # should timeout

    return "Finished"


async def fast_task():

    print("Fast task started...")

    await asyncio.sleep(1)       # should succeed

    return "Success"


async def main():

    print("\n=== Fast Task ===\n")

    result = await TimeoutManager.execute(
        fast_task(),
        server="github",
    )

    print(result)

    print("\n=== Slow Task ===\n")

    try:

        result = await TimeoutManager.execute(
            slow_task(),
            server="github",
        )

        print(result)

    except Exception as e:

        print(type(e).__name__)
        print(e)


if __name__ == "__main__":
    asyncio.run(main())