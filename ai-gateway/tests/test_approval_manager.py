import json

from app.approval.approval_manager import ApprovalManager


print("\n=== Approval Manager Test ===\n")

# -------------------------------------------------
# Initialize
# -------------------------------------------------

manager = ApprovalManager()

print("Initializing Approval Manager\n")

print(
    json.dumps(
        manager.statistics(),
        indent=2,
    )
)

# -------------------------------------------------
# Configure Policy
# -------------------------------------------------

print("\nConfiguring Policy\n")

manager.policy.configure(
    default="auto",
    confidence_threshold=80,
    protected_tools=[
        "database.delete",
        "filesystem.remove",
    ],
)

print(
    json.dumps(
        manager.policy.statistics(),
        indent=2,
    )
)

# -------------------------------------------------
# Create Approval Request
# -------------------------------------------------

print("\nCreating Approval Request\n")

request = manager.request(
    title="Delete Production Database",
    description="Requires human approval.",
    user="agent",
)

request_id = manager.requests.id()

print("\nRequest ID\n")
print(request_id)

# -------------------------------------------------
# Approve
# -------------------------------------------------

print("\nApproving Request\n")

print(
    manager.approve(
        request_id,
        user="admin",
    )
)

print("\nRequest Statistics\n")

print(
    json.dumps(
        manager.requests.statistics(),
        indent=2,
    )
)

# -------------------------------------------------
# Pause / Resume
# -------------------------------------------------

print("\nPausing Execution\n")

manager.pause_execution(
    reason="Waiting for maintenance window",
)

print(
    json.dumps(
        manager.pause.statistics(),
        indent=2,
    )
)

print("\nResuming Execution\n")

manager.resume_execution()

print(
    json.dumps(
        manager.pause.statistics(),
        indent=2,
    )
)

# -------------------------------------------------
# Manual Override
# -------------------------------------------------

print("\nManual Override\n")

manager.override.enable(
    operator="admin",
    reason="Emergency maintenance",
)

manager.override.force(
    {
        "status": "approved",
    }
)

manager.audit.manual_override(
    action="force",
    user="admin",
)

print(
    json.dumps(
        manager.override.statistics(),
        indent=2,
    )
)

# -------------------------------------------------
# Policy Evaluation
# -------------------------------------------------

print("\nPolicy Evaluation\n")

print(
    manager.requires_approval(
        tool="database.delete",
    )
)

print(
    json.dumps(
        manager.policy.export(),
        indent=2,
    )
)

# -------------------------------------------------
# Statistics
# -------------------------------------------------

print("\nStatistics\n")

print(
    json.dumps(
        manager.statistics(),
        indent=2,
    )
)

# -------------------------------------------------
# Export
# -------------------------------------------------

print("\nExport\n")

print(
    json.dumps(
        manager.export(),
        indent=2,
    )
)

# -------------------------------------------------
# Cleanup
# -------------------------------------------------

print("\nCleanup\n")

manager.clear()

print(
    json.dumps(
        manager.statistics(),
        indent=2,
    )
)

print("\nApproval Manager Test Passed ✓")