from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


# =====================================================
# Approval Request
# =====================================================

@dataclass
class ApprovalRequestModel:

    id: str

    title: str

    description: str = ""

    status: str = "pending"

    created_at: Optional[float] = None

    approved_by: Optional[str] = None

    rejected_by: Optional[str] = None

    metadata: Dict[str, Any] = field(default_factory=dict)


# =====================================================
# Pause / Resume
# =====================================================

@dataclass
class PauseResumeModel:

    paused: bool = False

    reason: Optional[str] = None

    paused_at: Optional[float] = None

    resumed_at: Optional[float] = None


# =====================================================
# Manual Override
# =====================================================

@dataclass
class ManualOverrideModel:

    enabled: bool = False

    action: Optional[str] = None

    user: Optional[str] = None

    timestamp: Optional[float] = None


# =====================================================
# Approval Policy
# =====================================================

@dataclass
class ApprovalPolicyModel:

    default_policy: str = "auto"

    confidence_threshold: int = 70

    protected_tools: List[str] = field(default_factory=list)

    approval_required: bool = False

    reason: str = ""


# =====================================================
# Audit Event
# =====================================================

@dataclass
class AuditEventModel:

    id: int

    timestamp: float

    event: str

    status: Optional[str] = None

    user: Optional[str] = None

    details: Dict[str, Any] = field(default_factory=dict)


# =====================================================
# Approval Manager Export
# =====================================================

@dataclass
class ApprovalManagerModel:

    requests: List[ApprovalRequestModel] = field(default_factory=list)

    pause_resume: Optional[PauseResumeModel] = None

    manual_override: Optional[ManualOverrideModel] = None

    policy: Optional[ApprovalPolicyModel] = None

    audit: List[AuditEventModel] = field(default_factory=list)