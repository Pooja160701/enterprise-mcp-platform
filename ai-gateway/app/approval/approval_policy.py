from copy import deepcopy


class ApprovalPolicy:
    """
    Enterprise Approval Policy

    Determines whether a request requires
    human approval before execution.

    Features

    ✓ Automatic Approval
    ✓ Manual Approval
    ✓ Risk-Based Policies
    ✓ Tool Policies
    ✓ Confidence Policies
    ✓ Statistics

    Used by

    - Human Approval
    - Reasoning Manager
    - Workflow Engine
    - Agent Service
    """

    AUTO = "auto"
    MANUAL = "manual"

    def __init__(self):

        self.clear()

    # -------------------------------------------------
    # Configure Policy
    # -------------------------------------------------

    def configure(
        self,
        default=AUTO,
        confidence_threshold=70,
        protected_tools=None,
    ):

        self._default = default

        self._confidence_threshold = confidence_threshold

        self._protected_tools = set(
            protected_tools or []
        )

        return self

    # -------------------------------------------------
    # Evaluate Request
    # -------------------------------------------------

    def evaluate(
        self,
        *,
        tool=None,
        confidence=100,
        risk="low",
        requires_human=False,
    ):
        """
        Returns True if approval is required.
        """

        self._last = {

            "tool": tool,

            "confidence": confidence,

            "risk": risk,

            "requires_human": requires_human,

            "approval_required": False,

            "reason": "Automatic approval.",

        }

        #
        # Explicit request
        #

        if requires_human:

            self._last["approval_required"] = True
            self._last["reason"] = "Human approval requested."
            return True

        #
        # Manual policy
        #

        if self._default == self.MANUAL:

            self._last["approval_required"] = True
            self._last["reason"] = "Manual approval policy."
            return True

        #
        # Protected tool
        #

        if tool in self._protected_tools:

            self._last["approval_required"] = True
            self._last["reason"] = "Protected tool."
            return True

        #
        # Confidence
        #

        if confidence < self._confidence_threshold:

            self._last["approval_required"] = True
            self._last["reason"] = "Low confidence."
            return True

        #
        # High Risk
        #

        if str(risk).lower() == "high":

            self._last["approval_required"] = True
            self._last["reason"] = "High-risk operation."
            return True

        return False

    # -------------------------------------------------
    # Approval Required
    # -------------------------------------------------

    def approval_required(
        self,
    ):

        return self._last["approval_required"]

    # -------------------------------------------------
    # Reason
    # -------------------------------------------------

    def reason(
        self,
    ):

        return self._last["reason"]

    # -------------------------------------------------
    # Statistics
    # -------------------------------------------------

    def statistics(
        self,
    ):

        return {

            "default_policy": self._default,

            "confidence_threshold": self._confidence_threshold,

            "protected_tools": len(
                self._protected_tools
            ),

            "approval_required": self._last[
                "approval_required"
            ],

        }

    # -------------------------------------------------
    # Export
    # -------------------------------------------------

    def export(
        self,
    ):

        return {

            "default_policy": self._default,

            "confidence_threshold": self._confidence_threshold,

            "protected_tools": list(
                self._protected_tools
            ),

            "last_evaluation": deepcopy(
                self._last
            ),

        }

    # -------------------------------------------------
    # Clear
    # -------------------------------------------------

    def clear(
        self,
    ):

        self._default = self.AUTO

        self._confidence_threshold = 70

        self._protected_tools = set()

        self._last = {

            "tool": None,

            "confidence": 100,

            "risk": "low",

            "requires_human": False,

            "approval_required": False,

            "reason": "",

        }

    # -------------------------------------------------
    # Empty
    # -------------------------------------------------

    @staticmethod
    def empty():

        return ApprovalPolicy()