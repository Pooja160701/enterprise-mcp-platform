from copy import deepcopy

from app.governance.policy_engine import PolicyEngine
from app.governance.rbac import RBAC
from app.governance.tool_permissions import ToolPermissions
from app.governance.secret_access_rules import SecretAccessRules
from app.governance.rate_limits import RateLimits
from app.governance.compliance_rules import ComplianceRules


class GovernanceManager:
    """
    Enterprise Governance Manager

                       Governance Manager
                               │
        ┌──────────────┬──────────────┬──────────────┐
        │              │              │              │
    Policy Engine      RBAC     Tool Permissions    Secrets
        │              │              │              │
        └──────────────┼──────────────┼──────────────┘
                       │
              Rate Limits
                       │
               Compliance Rules

    Central governance layer for the Enterprise MCP Platform.

    Responsibilities

    ✓ Policy Evaluation
    ✓ Role Based Access Control
    ✓ Tool Permissions
    ✓ Secret Access Rules
    ✓ Rate Limiting
    ✓ Compliance Validation
    ✓ Governance Statistics
    """

    def __init__(self):

        self.policy = PolicyEngine()

        self.rbac = RBAC()

        self.permissions = ToolPermissions()

        self.secrets = SecretAccessRules()

        self.rate_limits = RateLimits()

        self.compliance = ComplianceRules()

    # -------------------------------------------------
    # Governance Evaluation
    # -------------------------------------------------

    def evaluate(
        self,
        *,
        user=None,
        role=None,
        tool=None,
        secret=None,
        confidence=100,
        risk="low",
        environment="development",
        query="",
        contains_sensitive_data=False,
    ):
        """
        Complete governance evaluation.

        Returns

        {
            "allowed": bool,
            "results": {...}
        }
        """

        results = {}

        #
        # Policy Engine
        #

        policy_ok = self.policy.evaluate(
            {
                "tool": tool,
                "confidence": confidence,
                "risk": risk,
                "user": user,
                "role": role,
            }
        )
        results["policy"] = {

            "allowed": policy_ok,

            "details": deepcopy(
                self.policy.export()
            ),

        }

        #
        # RBAC
        #

        rbac_ok = True
        if user is not None and tool is not None:
            rbac_ok = self.rbac.allowed(
                user=user,
                permission=tool,
            )

        results["rbac"] = {

            "allowed": rbac_ok,

            "details": deepcopy(
                self.rbac.export()
            ),

        }

        #
        # Tool Permissions
        #

        permission_ok = True

        if tool is not None:

            permission_ok = self.permissions.allowed(
                tool=tool,
                role=role,
            )

        results["tool_permissions"] = {

            "allowed": permission_ok,

            "details": deepcopy(
                self.permissions.export()
            ),

        }

        #
        # Secret Access
        #

        secret_ok = True

        if secret is not None:

            secret_ok = self.secrets.allowed(
                secret=secret,
                role=role,
            )

        results["secret_access"] = {

            "allowed": secret_ok,

            "details": deepcopy(
                self.secrets.export()
            ),

        }

        #
        # Rate Limits
        #

        rate_ok = self.rate_limits.record(

            user=user,

            tool=tool,

        )

        results["rate_limits"] = {

            "allowed": rate_ok,

            "details": deepcopy(
                self.rate_limits.export()
            ),

        }

        #
        # Compliance
        #

        compliance_ok = self.compliance.evaluate(

            tool=tool,

            query=query,

            environment=environment,

            contains_sensitive_data=contains_sensitive_data,

        )

        results["compliance"] = {

            "allowed": compliance_ok,

            "details": deepcopy(
                self.compliance.export()
            ),

        }

        #
        # Final Decision
        #

        allowed = all(

            (

                policy_ok,

                rbac_ok,

                permission_ok,

                secret_ok,

                rate_ok,

                compliance_ok,

            )

        )

        return {

            "allowed": allowed,

            "results": results,

        }

    # -------------------------------------------------
    # Statistics
    # -------------------------------------------------

    def statistics(
        self,
    ):

        return {

            "policy_engine": deepcopy(
                self.policy.statistics()
            ),

            "rbac": deepcopy(
                self.rbac.statistics()
            ),

            "tool_permissions": deepcopy(
                self.permissions.statistics()
            ),

            "secret_access": deepcopy(
                self.secrets.statistics()
            ),

            "rate_limits": deepcopy(
                self.rate_limits.statistics()
            ),

            "compliance": deepcopy(
                self.compliance.statistics()
            ),

        }

    # -------------------------------------------------
    # Export
    # -------------------------------------------------

    def export(
        self,
    ):

        return {

            "policy_engine": deepcopy(
                self.policy.export()
            ),

            "rbac": deepcopy(
                self.rbac.export()
            ),

            "tool_permissions": deepcopy(
                self.permissions.export()
            ),

            "secret_access": deepcopy(
                self.secrets.export()
            ),

            "rate_limits": deepcopy(
                self.rate_limits.export()
            ),

            "compliance": deepcopy(
                self.compliance.export()
            ),

        }

    # -------------------------------------------------
    # Clear
    # -------------------------------------------------

    def clear(
        self,
    ):

        self.policy.clear()

        self.rbac.clear()

        self.permissions.clear()

        self.secrets.clear()

        self.rate_limits.clear()

        self.compliance.clear()

    # -------------------------------------------------
    # Empty
    # -------------------------------------------------

    @staticmethod
    def empty():

        return GovernanceManager()