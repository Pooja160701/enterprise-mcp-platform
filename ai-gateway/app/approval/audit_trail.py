import time
from copy import deepcopy


class AuditTrail:
    """
    Enterprise Audit Trail

    Records every human approval event.

    Features

    ✓ Approval Requests
    ✓ Decisions
    ✓ Manual Overrides
    ✓ Pause / Resume Events
    ✓ Timestamped Audit Log
    ✓ Search
    ✓ Export
    ✓ Statistics

    Used by

    - Approval Manager
    - Approval Policy
    - Manual Override
    - Pause Resume
    - Observability
    """

    def __init__(self):

        self.clear()

    # -------------------------------------------------
    # Add Event
    # -------------------------------------------------

    def add(
        self,
        event,
        user=None,
        status=None,
        details=None,
    ):

        entry = {

            "id": len(self._events) + 1,

            "timestamp": time.time(),

            "event": event,

            "user": user,

            "status": status,

            "details": deepcopy(details or {}),

        }

        self._events.append(entry)

        return entry["id"]

    # -------------------------------------------------
    # Approval Requested
    # -------------------------------------------------

    def approval_requested(
        self,
        request_id,
        user=None,
    ):

        return self.add(

            event="approval_requested",

            user=user,

            status="pending",

            details={

                "request_id": request_id,

            },

        )

    # -------------------------------------------------
    # Approved
    # -------------------------------------------------

    def approved(
        self,
        request_id,
        user=None,
    ):

        return self.add(

            event="approved",

            user=user,

            status="approved",

            details={

                "request_id": request_id,

            },

        )

    # -------------------------------------------------
    # Rejected
    # -------------------------------------------------

    def rejected(
        self,
        request_id,
        user=None,
    ):

        return self.add(

            event="rejected",

            user=user,

            status="rejected",

            details={

                "request_id": request_id,

            },

        )

    # -------------------------------------------------
    # Manual Override
    # -------------------------------------------------

    def manual_override(
        self,
        action,
        user=None,
    ):

        return self.add(

            event="manual_override",

            user=user,

            status="override",

            details={

                "action": action,

            },

        )

    # -------------------------------------------------
    # Pause
    # -------------------------------------------------

    def paused(
        self,
        reason=None,
    ):

        return self.add(

            event="paused",

            status="paused",

            details={

                "reason": reason,

            },

        )

    # -------------------------------------------------
    # Resume
    # -------------------------------------------------

    def resumed(
        self,
    ):

        return self.add(

            event="resumed",

            status="running",

        )

    # -------------------------------------------------
    # Events
    # -------------------------------------------------

    def events(
        self,
    ):

        return deepcopy(

            self._events

        )

    # -------------------------------------------------
    # Latest Event
    # -------------------------------------------------

    def latest(
        self,
    ):

        if not self._events:

            return None

        return deepcopy(

            self._events[-1]

        )

    # -------------------------------------------------
    # Find
    # -------------------------------------------------

    def find(
        self,
        event,
    ):

        return [

            deepcopy(item)

            for item in self._events

            if item["event"] == event

        ]

    # -------------------------------------------------
    # Statistics
    # -------------------------------------------------

    def statistics(
        self,
    ):

        return {

            "events": len(self._events),

            "approvals": len(

                self.find(

                    "approved"

                )

            ),

            "rejections": len(

                self.find(

                    "rejected"

                )

            ),

            "overrides": len(

                self.find(

                    "manual_override"

                )

            ),

            "pauses": len(

                self.find(

                    "paused"

                )

            ),

            "resumes": len(

                self.find(

                    "resumed"

                )

            ),

        }

    # -------------------------------------------------
    # Export
    # -------------------------------------------------

    def export(
        self,
    ):

        return deepcopy(

            self._events

        )

    # -------------------------------------------------
    # Clear
    # -------------------------------------------------

    def clear(
        self,
    ):

        self._events = []

    # -------------------------------------------------
    # Empty
    # -------------------------------------------------

    @staticmethod
    def empty():

        return AuditTrail()