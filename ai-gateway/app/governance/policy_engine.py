from copy import deepcopy
import time


class PolicyEngine:
    """
    Enterprise Policy Engine

    Central policy evaluation engine used across
    the Enterprise MCP Platform.

    Features

    ✓ Register Policies
    ✓ Enable / Disable Policies
    ✓ Evaluate Requests
    ✓ Priority Based Execution
    ✓ Audit Friendly Results
    ✓ Runtime Statistics

    Used by

    - Governance Manager
    - RBAC
    - Tool Permissions
    - Secret Access Rules
    - Compliance Rules
    - Rate Limits
    """

    ALLOW = "allow"
    DENY = "deny"

    def __init__(self):

        self.clear()

    # -------------------------------------------------
    # Register Policy
    # -------------------------------------------------

    def register(
        self,
        name,
        evaluator,
        priority=50,
        enabled=True,
    ):

        self._policies[name] = {

            "name": name,

            "priority": priority,

            "enabled": enabled,

            "evaluator": evaluator,

        }

        return self

    # -------------------------------------------------
    # Remove Policy
    # -------------------------------------------------

    def remove(
        self,
        name,
    ):

        return self._policies.pop(
            name,
            None,
        ) is not None

    # -------------------------------------------------
    # Enable Policy
    # -------------------------------------------------

    def enable(
        self,
        name,
    ):

        if name not in self._policies:
            return False

        self._policies[name]["enabled"] = True

        return True

    # -------------------------------------------------
    # Disable Policy
    # -------------------------------------------------

    def disable(
        self,
        name,
    ):

        if name not in self._policies:
            return False

        self._policies[name]["enabled"] = False

        return True

    # -------------------------------------------------
    # Evaluate
    # -------------------------------------------------

    def evaluate(
        self,
        context=None,
    ):

        context = context or {}

        self._evaluations += 1

        ordered = sorted(
            self._policies.values(),
            key=lambda p: p["priority"],
            reverse=True,
        )

        results = []

        allowed = True

        reason = "Allowed"

        for policy in ordered:

            if not policy["enabled"]:
                continue

            try:

                decision = bool(
                    policy["evaluator"](context)
                )

            except Exception as exc:

                decision = False

                results.append({

                    "policy": policy["name"],

                    "decision": self.DENY,

                    "reason": str(exc),

                })

                allowed = False

                reason = str(exc)

                break

            results.append({

                "policy": policy["name"],

                "decision": (
                    self.ALLOW
                    if decision
                    else self.DENY
                ),

            })

            if not decision:

                allowed = False

                reason = f"Denied by {policy['name']}"

                break

        self._last = {

            "timestamp": time.time(),

            "allowed": allowed,

            "reason": reason,

            "results": deepcopy(results),

        }

        if allowed:
            self._allowed += 1
        else:
            self._denied += 1

        return allowed

    # -------------------------------------------------
    # Allowed
    # -------------------------------------------------

    def allowed(
        self,
    ):

        return self._last["allowed"]

    # -------------------------------------------------
    # Reason
    # -------------------------------------------------

    def reason(
        self,
    ):

        return self._last["reason"]

    # -------------------------------------------------
    # Policies
    # -------------------------------------------------

    def policies(
        self,
    ):

        return list(

            self._policies.keys()

        )

    # -------------------------------------------------
    # Export
    # -------------------------------------------------

    def export(
        self,
    ):

        return {

            "policies": [

                {

                    "name": p["name"],

                    "priority": p["priority"],

                    "enabled": p["enabled"],

                }

                for p in sorted(
                    self._policies.values(),
                    key=lambda x: x["priority"],
                    reverse=True,
                )

            ],

            "last": deepcopy(
                self._last
            ),

        }

    # -------------------------------------------------
    # Statistics
    # -------------------------------------------------

    def statistics(
        self,
    ):

        return {

            "policies": len(
                self._policies
            ),

            "enabled": sum(
                p["enabled"]
                for p in self._policies.values()
            ),

            "disabled": sum(
                not p["enabled"]
                for p in self._policies.values()
            ),

            "evaluations": self._evaluations,

            "allowed": self._allowed,

            "denied": self._denied,

        }

    # -------------------------------------------------
    # Clear
    # -------------------------------------------------

    def clear(
        self,
    ):

        self._policies = {}

        self._evaluations = 0

        self._allowed = 0

        self._denied = 0

        self._last = {

            "timestamp": None,

            "allowed": True,

            "reason": "",

            "results": [],

        }

    # -------------------------------------------------
    # Empty
    # -------------------------------------------------

    @staticmethod
    def empty():

        return PolicyEngine()