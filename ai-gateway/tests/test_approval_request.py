import json

from app.approval.approval_request import ApprovalRequest


print("\n=== Approval Request Test ===\n")

# -------------------------------------------------
# Initialize
# -------------------------------------------------

request = ApprovalRequest()

print("Initializing Approval Request\n")

print(
    json.dumps(
        request.statistics(),
        indent=2,
    )
)

# -------------------------------------------------
# Create Request
# -------------------------------------------------

print("\nCreating Approval Request\n")

request.create(
    title="Delete Production Database",
    description="Human approval required before deleting the production database.",
    requested_by="agent",
    metadata={
        "environment": "production",
        "risk": "high",
    },
)

print("Request ID\n")
print(request.id())

print("\nStatus\n")
print(request.status())

print("\nStatistics\n")

print(
    json.dumps(
        request.statistics(),
        indent=2,
    )
)

# -------------------------------------------------
# Export
# -------------------------------------------------

print("\nExport\n")

print(
    json.dumps(
        request.export(),
        indent=2,
    )
)

# -------------------------------------------------
# Approve
# -------------------------------------------------

print("\nApproving Request\n")

print(
    request.approve(
        approved_by="admin",
        comment="Approved after review.",
    )
)

print("\nApproved\n")
print(request.approved())

print("\nStatus\n")
print(request.status())

print("\nStatistics\n")

print(
    json.dumps(
        request.statistics(),
        indent=2,
    )
)

# -------------------------------------------------
# Reject After Approval
# -------------------------------------------------

print("\nReject After Approval\n")

print(request.reject())

# -------------------------------------------------
# Create Second Request
# -------------------------------------------------

print("\nCreating Second Request\n")

second = ApprovalRequest()

second.create(
    title="Shutdown Cluster",
    description="Approval required.",
)

print(
    second.reject(
        rejected_by="security-team",
        comment="Operation denied.",
    )
)

print("\nRejected\n")
print(second.rejected())

print(
    json.dumps(
        second.statistics(),
        indent=2,
    )
)

# -------------------------------------------------
# Create Third Request
# -------------------------------------------------

print("\nCreating Third Request\n")

third = ApprovalRequest()

third.create(
    title="Rotate Secrets",
    description="Approval timeout demo.",
)

print(
    third.expire()
)

print("\nExpired\n")
print(third.expired())

print(
    json.dumps(
        third.statistics(),
        indent=2,
    )
)

# -------------------------------------------------
# Cleanup
# -------------------------------------------------

print("\nCleanup\n")

request.clear()

print(
    json.dumps(
        request.statistics(),
        indent=2,
    )
)

print("\nApproval Request Test Passed ✓")