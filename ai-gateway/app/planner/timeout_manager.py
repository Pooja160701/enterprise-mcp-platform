import asyncio


class TimeoutManager:
    """
    Enterprise Timeout Manager

    Features

    ✓ Per Tool Timeout
    ✓ Global Default Timeout
    ✓ Async Compatible
    ✓ Graceful Failure
    ✓ Timeout Metadata
    """

    DEFAULT_TIMEOUT = 30

    TOOL_TIMEOUTS = {

        #
        # Fast
        #

        "github": 15,

        "docker": 15,

        "filesystem": 15,

        #
        # Medium
        #

        "postgres": 20,

        "kubernetes": 20,

        "prometheus": 20,

        "grafana": 20,

        #
        # Slow
        #

        "aws": 30,

    }

    @classmethod
    async def execute(
        cls,
        coro,
        server=None,
        timeout=None,
    ):
        """
        Execute coroutine with timeout.

        Example

            result = await TimeoutManager.execute(
                self.router.execute(...),
                server="github",
            )
        """

        if timeout is None:

            timeout = cls.TOOL_TIMEOUTS.get(

                server,

                cls.DEFAULT_TIMEOUT,

            )

        try:

            result = await asyncio.wait_for(

                coro,

                timeout=timeout,

            )

            return result

        except asyncio.TimeoutError:

            raise TimeoutError(

                f"{server} exceeded timeout ({timeout}s)"

            )

    @classmethod
    async def execute_with_result(
        cls,
        coro,
        server=None,
        timeout=None,
    ):
        """
        Returns execution metadata.
        """

        if timeout is None:

            timeout = cls.TOOL_TIMEOUTS.get(

                server,

                cls.DEFAULT_TIMEOUT,

            )

        try:

            result = await asyncio.wait_for(

                coro,

                timeout=timeout,

            )

            return {

                "success": True,

                "timeout": False,

                "seconds": timeout,

                "result": result,

            }

        except asyncio.TimeoutError:

            return {

                "success": False,

                "timeout": True,

                "seconds": timeout,

                "error": f"Execution exceeded {timeout} seconds",

            }

    @classmethod
    def set_timeout(
        cls,
        server,
        seconds,
    ):

        cls.TOOL_TIMEOUTS[server] = seconds

    @classmethod
    def get_timeout(
        cls,
        server,
    ):

        return cls.TOOL_TIMEOUTS.get(

            server,

            cls.DEFAULT_TIMEOUT,

        )

    @classmethod
    def all_timeouts(
        cls,
    ):

        return dict(

            cls.TOOL_TIMEOUTS

        )