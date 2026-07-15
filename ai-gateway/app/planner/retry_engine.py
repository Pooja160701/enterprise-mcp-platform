import asyncio
import random


class RetryEngine:
    """
    Enterprise Retry Engine

    Features

    ✓ Exponential Backoff
    ✓ Random Jitter
    ✓ Configurable Retries
    ✓ Async Compatible
    ✓ Retry on Selected Exceptions
    """

    DEFAULT_RETRIES = 3

    BASE_DELAY = 1.0

    MAX_DELAY = 10.0

    @classmethod
    async def execute(
        cls,
        func,
        *args,
        retries=None,
        retry_exceptions=(Exception,),
        **kwargs,
    ):
        """
        Execute an async function with retries.

        Example

            result = await RetryEngine.execute(
                some_async_function,
                arg1,
                arg2,
            )
        """

        retries = retries or cls.DEFAULT_RETRIES

        attempt = 0

        last_error = None

        while attempt <= retries:

            try:

                return await func(
                    *args,
                    **kwargs,
                )

            except retry_exceptions as exc:

                last_error = exc

                if attempt >= retries:

                    break

                delay = cls.calculate_delay(
                    attempt,
                )

                print(
                    f"[RETRY] Attempt {attempt + 1}/{retries} "
                    f"after {delay:.2f}s "
                    f"({type(exc).__name__})"
                )

                await asyncio.sleep(
                    delay,
                )

                attempt += 1

        raise last_error

    @classmethod
    def calculate_delay(
        cls,
        attempt,
    ):
        """
        Exponential Backoff

        1
        2
        4
        8
        """

        delay = min(
            cls.BASE_DELAY * (2 ** attempt),
            cls.MAX_DELAY,
        )

        #
        # Random jitter
        #

        delay += random.uniform(
            0,
            0.5,
        )

        return delay

    @classmethod
    async def execute_with_result(
        cls,
        func,
        *args,
        retries=None,
        retry_exceptions=(Exception,),
        **kwargs,
    ):
        """
        Returns metadata together with result.
        """

        retries = retries or cls.DEFAULT_RETRIES

        attempt = 0

        while True:

            try:

                result = await func(
                    *args,
                    **kwargs,
                )

                return {

                    "success": True,

                    "attempts": attempt + 1,

                    "result": result,

                }

            except retry_exceptions as exc:

                if attempt >= retries:

                    return {

                        "success": False,

                        "attempts": attempt + 1,

                        "error": str(exc),

                    }

                delay = cls.calculate_delay(
                    attempt,
                )

                print(
                    f"[RETRY] {attempt + 1}/{retries} "
                    f"waiting {delay:.2f}s"
                )

                await asyncio.sleep(
                    delay,
                )

                attempt += 1