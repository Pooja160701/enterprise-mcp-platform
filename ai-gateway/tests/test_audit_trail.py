import json

from app.approval.audit_trail import AuditTrail


print("\n=== Audit Trail Test ===\n")

# -------------------------------------------------
# Initialize
# -------------------------------------------------

audit = AuditTrail()

print("Initializing Audit Trail\n")

print(
    json.dumps(
        audit.statistics(),
        indent=2,
    )
)

# -------------------------------------------------
# Approval Requested
# -------------------------------------------------

print("\nApproval Requested\n")

audit.approval_requested(
    request_id="REQ-001",
    user="agent",
)

# -------------------------------------------------
# Approved
# -------------------------------------------------

print("\nApproved\n")

audit.approved(
    request_id="REQ-001",
    user="admin",
)

# -------------------------------------------------
# Rejected
# -------------------------------------------------

print("\nRejected\n")

audit.rejected(
    request_id="REQ-002",
    user="security",
)

# -------------------------------------------------
# Manual Override
# -------------------------------------------------

print("\nManual Override\n")

audit.manual_override(
    action="Force Approve",
    user="super-admin",
)

# -------------------------------------------------
# Pause
# -------------------------------------------------

print("\nPause\n")

audit.paused(
    reason="Awaiting human approval",
)

# -------------------------------------------------
# Resume
# -------------------------------------------------

print("\nResume\n")

audit.resumed()

# -------------------------------------------------
# Statistics
# -------------------------------------------------

print("\nStatistics\n")

print(
    json.dumps(
        audit.statistics(),
        indent=2,
    )
)

# -------------------------------------------------
# Latest Event
# -------------------------------------------------

print("\nLatest Event\n")

print(
    json.dumps(
        audit.latest(),
        indent=2,
    )
)

# -------------------------------------------------
# Approval Events
# -------------------------------------------------

print("\nApproved Events\n")

print(
    json.dumps(
        audit.find("approved"),
        indent=2,
    )
)

# -------------------------------------------------
# All Events
# -------------------------------------------------

print("\nAll Events\n")

print(
    json.dumps(
        audit.events(),
        indent=2,
    )
)

# -------------------------------------------------
# Export
# -------------------------------------------------

print("\nExport\n")

print(
    json.dumps(
        audit.export(),
        indent=2,
    )
)

# -------------------------------------------------
# Cleanup
# -------------------------------------------------

print("\nCleanup\n")

audit.clear()

print(
    json.dumps(
        audit.statistics(),
        indent=2,
    )
)

print("\nAudit Trail Test Passed ✓")