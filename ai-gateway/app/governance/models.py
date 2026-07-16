from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


# =====================================================
# Policy Evaluation
# =====================================================

@dataclass
class PolicyResult:
    """
    Result produced by the Policy Engine.
    """

    allowed: bool = True

    reason: str = ""

    risk: str = "low"

    confidence: int = 100

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )


# =====================================================
# RBAC
# =====================================================

@dataclass
class Role:
    """
    RBAC Role
    """

    name: str

    permissions: List[str] = field(
        default_factory=list
    )


@dataclass
class UserRole:
    """
    User Role Assignment
    """

    user: str

    role: str


# =====================================================
# Tool Permissions
# =====================================================

@dataclass
class ToolPermission:
    """
    Tool Permission Rule
    """

    tool: str

    roles: List[str] = field(
        default_factory=list
    )

    enabled: bool = True


# =====================================================
# Secret Access
# =====================================================

@dataclass
class SecretRule:
    """
    Secret Access Rule
    """

    secret: str

    roles: List[str] = field(
        default_factory=list
    )

    enabled: bool = True


# =====================================================
# Rate Limits
# =====================================================

@dataclass
class RateLimitRule:
    """
    Rate Limit Configuration
    """

    global_limit: int = 1000

    user_limit: int = 100

    tool_limit: int = 200

    window_seconds: int = 60


@dataclass
class RateLimitUsage:
    """
    Current Rate Limit Usage
    """

    global_requests: int = 0

    tracked_users: int = 0

    tracked_tools: int = 0

    last_reason: str = ""


# =====================================================
# Compliance
# =====================================================

@dataclass
class ComplianceResult:
    """
    Compliance Evaluation Result
    """

    compliant: bool = True

    reason: str = ""

    environment: str = "development"

    tool: Optional[str] = None

    sensitive_data: bool = False


# =====================================================
# Governance Evaluation
# =====================================================

@dataclass
class GovernanceDecision:
    """
    Final Governance Decision
    """

    allowed: bool = True

    policy: Optional[PolicyResult] = None

    compliance: Optional[ComplianceResult] = None

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )


# =====================================================
# Governance Request
# =====================================================

@dataclass
class GovernanceRequest:
    """
    Request evaluated by Governance Manager.
    """

    user: Optional[str] = None

    role: Optional[str] = None

    tool: Optional[str] = None

    secret: Optional[str] = None

    confidence: int = 100

    risk: str = "low"

    environment: str = "development"

    query: str = ""

    contains_sensitive_data: bool = False


# =====================================================
# Governance Response
# =====================================================

@dataclass
class GovernanceResponse:
    """
    Response returned by Governance Manager.
    """

    allowed: bool

    results: Dict[str, Any] = field(
        default_factory=dict
    )


# =====================================================
# Governance Statistics
# =====================================================

@dataclass
class GovernanceStatistics:
    """
    Aggregated Governance Statistics.
    """

    policy_engine: Dict[str, Any] = field(
        default_factory=dict
    )

    rbac: Dict[str, Any] = field(
        default_factory=dict
    )

    tool_permissions: Dict[str, Any] = field(
        default_factory=dict
    )

    secret_access: Dict[str, Any] = field(
        default_factory=dict
    )

    rate_limits: Dict[str, Any] = field(
        default_factory=dict
    )

    compliance: Dict[str, Any] = field(
        default_factory=dict
    )