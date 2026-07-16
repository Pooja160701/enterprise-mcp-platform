import json

from app.approval.approval_policy import ApprovalPolicy


print("\n=== Approval Policy Test ===\n")

# -------------------------------------------------
# Initialize
# -------------------------------------------------

policy = ApprovalPolicy()

print("Initializing Approval Policy\n")

print(
    json.dumps(
        policy.statistics(),
        indent=2,
    )
)

# -------------------------------------------------
# Configure Policy
# -------------------------------------------------

print("\nConfiguring Policy\n")

policy.configure(
    default=ApprovalPolicy.AUTO,
    confidence_threshold=80,
    protected_tools=[
        "github.delete_repository",
        "filesystem.delete",
    ],
)

print(
    json.dumps(
        policy.statistics(),
        indent=2,
    )
)

# -------------------------------------------------
# Automatic Approval
# -------------------------------------------------

print("\nAutomatic Approval\n")

print(
    policy.evaluate(
        tool="github.list_repositories",
        confidence=95,
        risk="low",
    )
)

print("\nApproval Required\n")
print(policy.approval_required())

print("\nReason\n")
print(policy.reason())

# -------------------------------------------------
# Protected Tool
# -------------------------------------------------

print("\nProtected Tool\n")

print(
    policy.evaluate(
        tool="github.delete_repository",
        confidence=100,
        risk="low",
    )
)

print("\nApproval Required\n")
print(policy.approval_required())

print("\nReason\n")
print(policy.reason())

# -------------------------------------------------
# Low Confidence
# -------------------------------------------------

print("\nLow Confidence\n")

print(
    policy.evaluate(
        tool="github.list_repositories",
        confidence=45,
        risk="low",
    )
)

print("\nApproval Required\n")
print(policy.approval_required())

print("\nReason\n")
print(policy.reason())

# -------------------------------------------------
# High Risk
# -------------------------------------------------

print("\nHigh Risk\n")

print(
    policy.evaluate(
        tool="filesystem.search",
        confidence=95,
        risk="high",
    )
)

print("\nApproval Required\n")
print(policy.approval_required())

print("\nReason\n")
print(policy.reason())

# -------------------------------------------------
# Explicit Human Approval
# -------------------------------------------------

print("\nExplicit Human Approval\n")

print(
    policy.evaluate(
        tool="memory.search",
        confidence=100,
        risk="low",
        requires_human=True,
    )
)

print("\nApproval Required\n")
print(policy.approval_required())

print("\nReason\n")
print(policy.reason())

# -------------------------------------------------
# Manual Policy
# -------------------------------------------------

print("\nManual Approval Policy\n")

policy.configure(
    default=ApprovalPolicy.MANUAL,
)

print(
    policy.evaluate(
        tool="github.list_repositories",
        confidence=100,
        risk="low",
    )
)

print("\nApproval Required\n")
print(policy.approval_required())

print("\nReason\n")
print(policy.reason())

# -------------------------------------------------
# Statistics
# -------------------------------------------------

print("\nStatistics\n")

print(
    json.dumps(
        policy.statistics(),
        indent=2,
    )
)

# -------------------------------------------------
# Export
# -------------------------------------------------

print("\nExport\n")

print(
    json.dumps(
        policy.export(),
        indent=2,
    )
)

# -------------------------------------------------
# Cleanup
# -------------------------------------------------

print("\nCleanup\n")

policy.clear()

print(
    json.dumps(
        policy.statistics(),
        indent=2,
    )
)

print("\nApproval Policy Test Passed ✓")