import asyncio
import json

from app.planner.circuit_breaker import CircuitBreaker


counter = {
    "calls": 0
}


async def failing_tool():

    counter["calls"] += 1

    print(f"Call {counter['calls']}")

    raise Exception("Backend unavailable")


async def main():

    print("\nCircuit Breaker Test\n")

    CircuitBreaker.reset("github")

    for _ in range(6):

        try:

            if CircuitBreaker.allow_request("github"):

                await CircuitBreaker.execute(
                    "github",
                    failing_tool(),
                )

            else:

                raise RuntimeError(
                    "Circuit OPEN for 'github'. Requests temporarily blocked."
                )

        except Exception as e:

            print(type(e).__name__)
            print(e)

        print("-" * 40)

    print("\nCircuit State\n")

    print(
        json.dumps(
            CircuitBreaker.stats("github"),
            indent=2,
            default=str,
        )
    )


if __name__ == "__main__":

    asyncio.run(main())