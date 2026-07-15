import time


class CircuitBreaker:
    """
    Enterprise Circuit Breaker

    States

        CLOSED
           │
           │ failures >= threshold
           ▼
         OPEN
           │
           │ recovery timeout
           ▼
      HALF_OPEN
           │
      success │ failure
           ▼      ▼
       CLOSED    OPEN

    Features

    ✓ Per-server breaker
    ✓ Automatic recovery
    ✓ Configurable thresholds
    ✓ Cooldown period
    ✓ Statistics
    """

    FAILURE_THRESHOLD = 3

    RECOVERY_TIMEOUT = 60

    _breakers = {}

    @classmethod
    def _get(cls, server):

        if server not in cls._breakers:

            cls._breakers[server] = {

                "state": "CLOSED",

                "failures": 0,

                "last_failure": None,

                "opened_at": None,

                "successes": 0,

            }

        return cls._breakers[server]

    @classmethod
    def allow_request(
        cls,
        server,
    ):

        breaker = cls._get(server)

        #
        # CLOSED
        #

        if breaker["state"] == "CLOSED":

            return True

        #
        # OPEN
        #

        if breaker["state"] == "OPEN":

            elapsed = time.time() - breaker["opened_at"]

            if elapsed >= cls.RECOVERY_TIMEOUT:

                breaker["state"] = "HALF_OPEN"

                return True

            return False

        #
        # HALF_OPEN
        #

        return True

    @classmethod
    def record_success(
        cls,
        server,
    ):

        breaker = cls._get(server)

        breaker["successes"] += 1

        breaker["failures"] = 0

        breaker["state"] = "CLOSED"

        breaker["opened_at"] = None

    @classmethod
    def record_failure(
        cls,
        server,
    ):

        breaker = cls._get(server)

        breaker["failures"] += 1

        breaker["last_failure"] = time.time()

        if breaker["failures"] >= cls.FAILURE_THRESHOLD:

            breaker["state"] = "OPEN"

            breaker["opened_at"] = time.time()

    @classmethod
    def state(
        cls,
        server,
    ):

        return cls._get(server)["state"]

    @classmethod
    def stats(
        cls,
        server,
    ):

        return dict(

            cls._get(server)

        )

    @classmethod
    def all_stats(
        cls,
    ):

        return {

            server: dict(data)

            for server, data in cls._breakers.items()

        }

    @classmethod
    def reset(
        cls,
        server=None,
    ):

        if server:

            cls._breakers.pop(
                server,
                None,
            )

        else:

            cls._breakers.clear()

    @classmethod
    async def execute(
        cls,
        server,
        coro,
    ):
        """
        Execute a coroutine through the breaker.

        Example

            result = await CircuitBreaker.execute(
                "github",
                some_coroutine,
            )
        """

        if not cls.allow_request(server):

            raise RuntimeError(

                f"Circuit OPEN for '{server}'. "

                "Requests temporarily blocked."

            )

        try:

            result = await coro

            cls.record_success(
                server,
            )

            return result

        except Exception:

            cls.record_failure(
                server,
            )

            raise