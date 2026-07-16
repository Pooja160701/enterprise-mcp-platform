from copy import deepcopy
import time
import uuid


class ApprovalRequest:
    """
    Enterprise Approval Request

    Represents a human approval request before the
    agent performs a sensitive action.

    Features

    ✓ Create Approval Request
    ✓ Approve
    ✓ Reject
    ✓ Expire
    ✓ Status Tracking
    ✓ Metadata
    ✓ Statistics

    Used by

    - Approval Manager
    - Human Approval
    - Agent Service
    - Workflow Engine
    """

    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    EXPIRED = "expired"

    def __init__(self):

        self.clear()

    # -------------------------------------------------
    # Create Request
    # -------------------------------------------------

    def create(
        self,
        title,
        description,
        requested_by="agent",
        metadata=None,
    ):

        self.clear()

        self._id = str(uuid.uuid4())

        self._title = title

        self._description = description

        self._requested_by = requested_by

        self._metadata = deepcopy(metadata or {})

        self._status = self.PENDING

        self._created_at = time.time()

        return self

    # -------------------------------------------------
    # Approve
    # -------------------------------------------------

    def approve(
        self,
        approved_by="human",
        comment=None,
    ):

        if self._status != self.PENDING:

            return False

        self._status = self.APPROVED

        self._approved_by = approved_by

        self._comment = comment

        self._resolved_at = time.time()

        return True

    # -------------------------------------------------
    # Reject
    # -------------------------------------------------

    def reject(
        self,
        rejected_by="human",
        comment=None,
    ):

        if self._status != self.PENDING:

            return False

        self._status = self.REJECTED

        self._approved_by = rejected_by

        self._comment = comment

        self._resolved_at = time.time()

        return True

    # -------------------------------------------------
    # Expire
    # -------------------------------------------------

    def expire(
        self,
    ):

        if self._status != self.PENDING:

            return False

        self._status = self.EXPIRED

        self._resolved_at = time.time()

        return True

    # -------------------------------------------------
    # ID
    # -------------------------------------------------

    def id(
        self,
    ):

        return self._id

    # -------------------------------------------------
    # Status
    # -------------------------------------------------

    def status(
        self,
    ):

        return self._status

    # -------------------------------------------------
    # Approved
    # -------------------------------------------------

    def approved(
        self,
    ):

        return self._status == self.APPROVED

    # -------------------------------------------------
    # Pending
    # -------------------------------------------------

    def pending(
        self,
    ):

        return self._status == self.PENDING

    # -------------------------------------------------
    # Rejected
    # -------------------------------------------------

    def rejected(
        self,
    ):

        return self._status == self.REJECTED

    # -------------------------------------------------
    # Expired
    # -------------------------------------------------

    def expired(
        self,
    ):

        return self._status == self.EXPIRED

    # -------------------------------------------------
    # Duration
    # -------------------------------------------------

    def duration(
        self,
    ):

        end = self._resolved_at or time.time()

        return round(
            end - self._created_at,
            3,
        )

    # -------------------------------------------------
    # Statistics
    # -------------------------------------------------

    def statistics(
        self,
    ):

        return {

            "id": self._id,

            "status": self._status,

            "pending": self.pending(),

            "approved": self.approved(),

            "rejected": self.rejected(),

            "expired": self.expired(),

            "duration": self.duration(),

        }

    # -------------------------------------------------
    # Export
    # -------------------------------------------------

    def export(
        self,
    ):

        return {

            "id": self._id,

            "title": self._title,

            "description": self._description,

            "requested_by": self._requested_by,

            "metadata": deepcopy(self._metadata),

            "status": self._status,

            "approved_by": self._approved_by,

            "comment": self._comment,

            "created_at": self._created_at,

            "resolved_at": self._resolved_at,

            "duration": self.duration(),

        }

    # -------------------------------------------------
    # Clear
    # -------------------------------------------------

    def clear(
        self,
    ):

        self._id = ""

        self._title = ""

        self._description = ""

        self._requested_by = ""

        self._metadata = {}

        self._status = self.PENDING

        self._approved_by = None

        self._comment = None

        self._created_at = time.time()

        self._resolved_at = None

    # -------------------------------------------------
    # Empty
    # -------------------------------------------------

    @staticmethod
    def empty():

        return ApprovalRequest()