from copy import deepcopy
import time


class ManualOverride:
    """
    Enterprise Manual Override

    Allows a human operator to override
    automatic agent decisions.

    Features

    ✓ Enable Override
    ✓ Disable Override
    ✓ Approve
    ✓ Reject
    ✓ Force Decision
    ✓ Reset
    ✓ Statistics

    Used by

    - Approval Manager
    - Human Approval
    - Agent Service
    - Workflow Engine
    """

    APPROVE = "approve"
    REJECT = "reject"
    FORCE = "force"

    def __init__(self):

        self.clear()

    # -------------------------------------------------
    # Enable Override
    # -------------------------------------------------

    def enable(
        self,
        operator="human",
        reason="",
    ):

        self._enabled = True

        self._operator = operator

        self._reason = reason

        self._enabled_at = time.time()

        return True

    # -------------------------------------------------
    # Disable Override
    # -------------------------------------------------

    def disable(
        self,
    ):

        self._enabled = False

        self._decision = None

        self._enabled_at = None

        return True

    # -------------------------------------------------
    # Approve
    # -------------------------------------------------

    def approve(
        self,
    ):

        if not self._enabled:

            return False

        self._decision = self.APPROVE

        self._decision_at = time.time()

        return True

    # -------------------------------------------------
    # Reject
    # -------------------------------------------------

    def reject(
        self,
    ):

        if not self._enabled:

            return False

        self._decision = self.REJECT

        self._decision_at = time.time()

        return True

    # -------------------------------------------------
    # Force Decision
    # -------------------------------------------------

    def force(
        self,
        value,
    ):

        if not self._enabled:

            return False

        self._decision = self.FORCE

        self._forced_value = deepcopy(value)

        self._decision_at = time.time()

        return True

    # -------------------------------------------------
    # Enabled
    # -------------------------------------------------

    def enabled(
        self,
    ):

        return self._enabled

    # -------------------------------------------------
    # Decision
    # -------------------------------------------------

    def decision(
        self,
    ):

        return self._decision

    # -------------------------------------------------
    # Forced Value
    # -------------------------------------------------

    def forced_value(
        self,
    ):

        return deepcopy(self._forced_value)

    # -------------------------------------------------
    # Statistics
    # -------------------------------------------------

    def statistics(
        self,
    ):

        return {

            "enabled": self._enabled,

            "decision": self._decision,

            "operator": self._operator,

            "forced": self._decision == self.FORCE,

        }

    # -------------------------------------------------
    # Export
    # -------------------------------------------------

    def export(
        self,
    ):

        return {

            "enabled": self._enabled,

            "operator": self._operator,

            "reason": self._reason,

            "decision": self._decision,

            "forced_value": deepcopy(self._forced_value),

            "enabled_at": self._enabled_at,

            "decision_at": self._decision_at,

        }

    # -------------------------------------------------
    # Clear
    # -------------------------------------------------

    def clear(
        self,
    ):

        self._enabled = False

        self._operator = ""

        self._reason = ""

        self._decision = None

        self._forced_value = None

        self._enabled_at = None

        self._decision_at = None

    # -------------------------------------------------
    # Empty
    # -------------------------------------------------

    @staticmethod
    def empty():

        return ManualOverride()