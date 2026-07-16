import time
from collections import defaultdict
from copy import deepcopy


class RateLimits:
    """
    Enterprise Rate Limits

    Controls request execution rates across users,
    tools and the entire platform.

    Features

    ✓ Global Rate Limits
    ✓ User Rate Limits
    ✓ Tool Rate Limits
    ✓ Sliding Time Window
    ✓ Reset
    ✓ Statistics
    ✓ Export

    Used by

    - Policy Engine
    - Governance Manager
    - API Gateway
    - Tool Executor
    - Workflow Engine
    """

    def __init__(self):

        self.clear()

    # -------------------------------------------------
    # Configure
    # -------------------------------------------------

    def configure(
        self,
        *,
        global_limit=1000,
        user_limit=100,
        tool_limit=200,
        window=60,
    ):

        self._global_limit = global_limit

        self._user_limit = user_limit

        self._tool_limit = tool_limit

        self._window = window

        return self

    # -------------------------------------------------
    # Internal Cleanup
    # -------------------------------------------------

    def _cleanup(self):

        now = time.time()

        cutoff = now - self._window

        self._global = [

            ts

            for ts in self._global

            if ts >= cutoff

        ]

        for user in list(self._users):

            self._users[user] = [

                ts

                for ts in self._users[user]

                if ts >= cutoff

            ]

            if not self._users[user]:

                del self._users[user]

        for tool in list(self._tools):

            self._tools[tool] = [

                ts

                for ts in self._tools[tool]

                if ts >= cutoff

            ]

            if not self._tools[tool]:

                del self._tools[tool]

    # -------------------------------------------------
    # Check Request
    # -------------------------------------------------

    def allowed(
        self,
        *,
        user=None,
        tool=None,
    ):

        self._cleanup()

        #
        # Global
        #

        if len(self._global) >= self._global_limit:

            self._last_reason = "Global rate limit exceeded."

            return False

        #
        # User
        #

        if user is not None:

            if len(self._users[user]) >= self._user_limit:

                self._last_reason = "User rate limit exceeded."

                return False

        #
        # Tool
        #

        if tool is not None:

            if len(self._tools[tool]) >= self._tool_limit:

                self._last_reason = "Tool rate limit exceeded."

                return False

        self._last_reason = "Allowed."

        return True

    # -------------------------------------------------
    # Record Request
    # -------------------------------------------------

    def record(
        self,
        *,
        user=None,
        tool=None,
    ):

        if not self.allowed(
            user=user,
            tool=tool,
        ):

            return False

        now = time.time()

        self._global.append(now)

        if user is not None:

            self._users[user].append(now)

        if tool is not None:

            self._tools[tool].append(now)

        return True

    # -------------------------------------------------
    # Remaining Global
    # -------------------------------------------------

    def remaining_global(self):

        self._cleanup()

        return max(

            0,

            self._global_limit - len(self._global),

        )

    # -------------------------------------------------
    # Remaining User
    # -------------------------------------------------

    def remaining_user(
        self,
        user,
    ):

        self._cleanup()

        return max(

            0,

            self._user_limit -

            len(self._users[user]),

        )

    # -------------------------------------------------
    # Remaining Tool
    # -------------------------------------------------

    def remaining_tool(
        self,
        tool,
    ):

        self._cleanup()

        return max(

            0,

            self._tool_limit -

            len(self._tools[tool]),

        )

    # -------------------------------------------------
    # Last Reason
    # -------------------------------------------------

    def reason(self):

        return self._last_reason

    # -------------------------------------------------
    # Statistics
    # -------------------------------------------------

    def statistics(self):

        self._cleanup()

        return {

            "global_requests": len(
                self._global
            ),

            "tracked_users": len(
                self._users
            ),

            "tracked_tools": len(
                self._tools
            ),

            "global_limit": self._global_limit,

            "user_limit": self._user_limit,

            "tool_limit": self._tool_limit,

            "window_seconds": self._window,

        }

    # -------------------------------------------------
    # Export
    # -------------------------------------------------

    def export(self):

        self._cleanup()

        return {

            "configuration": {

                "global_limit": self._global_limit,

                "user_limit": self._user_limit,

                "tool_limit": self._tool_limit,

                "window_seconds": self._window,

            },

            "usage": {

                "global_requests": len(
                    self._global
                ),

                "users": {

                    user: len(times)

                    for user, times

                    in self._users.items()

                },

                "tools": {

                    tool: len(times)

                    for tool, times

                    in self._tools.items()

                },

            },

            "last_reason": self._last_reason,

        }

    # -------------------------------------------------
    # Clear
    # -------------------------------------------------

    def clear(self):

        self._global_limit = 1000

        self._user_limit = 100

        self._tool_limit = 200

        self._window = 60

        self._global = []

        self._users = defaultdict(list)

        self._tools = defaultdict(list)

        self._last_reason = ""

    # -------------------------------------------------
    # Empty
    # -------------------------------------------------

    @staticmethod
    def empty():

        return RateLimits()