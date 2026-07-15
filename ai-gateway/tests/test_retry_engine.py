import asyncio

from app.planner.retry_engine import RetryEngine


counter = {
    "attempts": 0
}


async def flaky_tool():

    counter["attempts"] += 1

    print(
        f"Attempt {counter['attempts']}"
    )

    #
    # Fail twice
    #

    if counter["attempts"] < 3:

        raise Exception("Temporary failure")

    return "SUCCESS"


async def main():

    print("\nRetry Engine Test\n")

    result = await RetryEngine.execute(
        flaky_tool
    )

    print("\nFinal Result\n")

    print(result)

    print("\nAttempts\n")

    print(counter["attempts"])


if __name__ == "__main__":

    asyncio.run(main())