from copy import deepcopy

from app.approval.approval_request import ApprovalRequest
from app.approval.pause_resume import PauseResume
from app.approval.manual_override import ManualOverride
from app.approval.approval_policy import ApprovalPolicy
from app.approval.audit_trail import AuditTrail


class ApprovalManager:
    """
    Enterprise Approval Manager

                     Approval Manager
                            │
        ┌──────────────┬──────────────┬──────────────┐
        │              │              │              │
    Approval      Pause/Resume   Manual Override   Policy
        │              │              │              │
        └──────────────┴──────────────┴──────────────┘
                            │
                      Audit Trail

    Central entry point for all human approval workflows.

    Features

    ✓ Approval Requests
    ✓ Pause / Resume Execution
    ✓ Manual Overrides
    ✓ Approval Policies
    ✓ Audit Trail
    ✓ Statistics
    """

    def __init__(self):

        self.requests = ApprovalRequest()
        self.pause = PauseResume()
        self.override = ManualOverride()
        self.policy = ApprovalPolicy()
        self.audit = AuditTrail()

    # -------------------------------------------------
    # Create Approval Request
    # -------------------------------------------------

    def request(
        self,
        title,
        description="",
        user=None,
    ):

        request = self.requests.create(
            title=title,
            description=description,
            requested_by=user or "agent",
        )

        request_id = request.id()

        self.audit.approval_requested(
            request_id,
            user=user,
        )

        return request_id

    # -------------------------------------------------
    # Approve
    # -------------------------------------------------

    def approve(
        self,
        request_id,
        user=None,
    ):

        success = self.requests.approve(
            approved_by=user or "human",
        )

        if success:
            self.audit.approved(
                request_id,
                user=user,
            )

        return success

    # -------------------------------------------------
    # Reject
    # -------------------------------------------------

    def reject(
        self,
        request_id,
        user=None,
    ):

        success = self.requests.reject(
            rejected_by=user or "human",
        )

        if success:
            self.audit.rejected(
                request_id,
                user=user,
            )

        return success

    # -------------------------------------------------
    # Pause
    # -------------------------------------------------

    def pause_execution(self, reason=None):

        self.pause.pause()

        self.audit.paused(reason)

    # -------------------------------------------------
    # Resume
    # -------------------------------------------------

    def resume_execution(self):

        self.pause.resume()

        self.audit.resumed()

    # -------------------------------------------------
    # Manual Override
    # -------------------------------------------------

    def override_execution(self, action, user=None):

        self.override.enable(
            operator=user or "human",
        )

        if action == "approve":
            self.override.approve()

        elif action == "reject":
            self.override.reject()

        else:
            self.override.force(action)

        self.audit.manual_override(
            action,
            user=user,
        )

    # -------------------------------------------------
    # Policy Evaluation
    # -------------------------------------------------

    def requires_approval(
        self,
        *,
        tool=None,
        confidence=100,
        risk="low",
        requires_human=False,
    ):

        return self.policy.evaluate(

            tool=tool,

            confidence=confidence,

            risk=risk,

            requires_human=requires_human,

        )

    # -------------------------------------------------
    # Statistics
    # -------------------------------------------------

    def statistics(
        self,
    ):

        return {

            "requests": deepcopy(
                self.requests.statistics()
            ),

            "pause_resume": deepcopy(
                self.pause.statistics()
            ),

            "manual_override": deepcopy(
                self.override.statistics()
            ),

            "policy": deepcopy(
                self.policy.statistics()
            ),

            "audit": deepcopy(
                self.audit.statistics()
            ),

        }

    # -------------------------------------------------
    # Export
    # -------------------------------------------------

    def export(
        self,
    ):

        return {

            "requests": deepcopy(
                self.requests.export()
            ),

            "pause_resume": deepcopy(
                self.pause.export()
            ),

            "manual_override": deepcopy(
                self.override.export()
            ),

            "policy": deepcopy(
                self.policy.export()
            ),

            "audit": deepcopy(
                self.audit.export()
            ),

        }

    # -------------------------------------------------
    # Clear
    # -------------------------------------------------

    def clear(
        self,
    ):

        self.requests.clear()

        self.pause.reset()

        self.override.clear()

        self.policy.clear()

        self.audit.clear()

    # -------------------------------------------------
    # Empty
    # -------------------------------------------------

    @staticmethod
    def empty():

        return ApprovalManager()