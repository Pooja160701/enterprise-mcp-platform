from copy import deepcopy


class ComplianceRules:
    """
    Enterprise Compliance Rules

    Evaluates requests against organizational
    compliance and governance requirements.

    Features

    ✓ Compliance Validation
    ✓ Restricted Operations
    ✓ Sensitive Data Detection
    ✓ Environment Policies
    ✓ Regulatory Checks
    ✓ Statistics
    ✓ Export

    Used by

    - Policy Engine
    - Governance Manager
    - Approval Manager
    - Agent Service
    - Workflow Engine
    """

    COMPLIANT = "compliant"
    NON_COMPLIANT = "non_compliant"

    def __init__(self):

        self.clear()

    # -------------------------------------------------
    # Configure Rules
    # -------------------------------------------------

    def configure(
        self,
        *,
        restricted_tools=None,
        protected_environments=None,
        blocked_keywords=None,
    ):

        self._restricted_tools = set(
            restricted_tools or []
        )

        self._protected_environments = set(
            protected_environments or []
        )

        self._blocked_keywords = {

            keyword.lower()

            for keyword in (blocked_keywords or [])

        }

        return self

    # -------------------------------------------------
    # Evaluate Request
    # -------------------------------------------------

    def evaluate(
        self,
        *,
        tool=None,
        query="",
        environment="development",
        contains_sensitive_data=False,
    ):
        """
        Returns True if the request is compliant.
        """

        self._last = {

            "tool": tool,

            "environment": environment,

            "contains_sensitive_data": contains_sensitive_data,

            "status": self.COMPLIANT,

            "reason": "Compliant.",

        }

        #
        # Restricted Tool
        #

        if tool in self._restricted_tools:

            self._last["status"] = self.NON_COMPLIANT

            self._last["reason"] = (
                "Restricted tool."
            )

            return False

        #
        # Protected Environment
        #

        if str(environment).lower() in {

            env.lower()

            for env in self._protected_environments

        }:

            self._last["status"] = self.NON_COMPLIANT

            self._last["reason"] = (
                "Protected environment."
            )

            return False

        #
        # Sensitive Data
        #

        if contains_sensitive_data:

            self._last["status"] = self.NON_COMPLIANT

            self._last["reason"] = (
                "Sensitive data detected."
            )

            return False

        #
        # Blocked Keywords
        #

        query_lower = str(query).lower()

        for keyword in self._blocked_keywords:

            if keyword in query_lower:

                self._last["status"] = self.NON_COMPLIANT

                self._last["reason"] = (
                    f"Blocked keyword: {keyword}"
                )

                return False

        return True

    # -------------------------------------------------
    # Compliant
    # -------------------------------------------------

    def compliant(
        self,
    ):

        return self._last["status"] == self.COMPLIANT

    # -------------------------------------------------
    # Status
    # -------------------------------------------------

    def status(
        self,
    ):

        return self._last["status"]

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

            "restricted_tools": len(
                self._restricted_tools
            ),

            "protected_environments": len(
                self._protected_environments
            ),

            "blocked_keywords": len(
                self._blocked_keywords
            ),

            "status": self._last["status"],

        }

    # -------------------------------------------------
    # Export
    # -------------------------------------------------

    def export(
        self,
    ):

        return {

            "restricted_tools": sorted(
                self._restricted_tools
            ),

            "protected_environments": sorted(
                self._protected_environments
            ),

            "blocked_keywords": sorted(
                self._blocked_keywords
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

        self._restricted_tools = set()

        self._protected_environments = set()

        self._blocked_keywords = set()

        self._last = {

            "tool": None,

            "environment": "development",

            "contains_sensitive_data": False,

            "status": self.COMPLIANT,

            "reason": "",

        }

    # -------------------------------------------------
    # Empty
    # -------------------------------------------------

    @staticmethod
    def empty():

        return ComplianceRules()