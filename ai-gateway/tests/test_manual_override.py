import json

from app.approval.manual_override import ManualOverride


print("\n=== Manual Override Test ===\n")

# -------------------------------------------------
# Initialize
# -------------------------------------------------

override = ManualOverride()

print("Initializing Manual Override\n")

print(
    json.dumps(
        override.statistics(),
        indent=2,
    )
)

# -------------------------------------------------
# Enable Override
# -------------------------------------------------

print("\nEnabling Override\n")

print(
    override.enable(
        operator="admin",
        reason="Emergency maintenance",
    )
)

print("\nEnabled\n")

print(
    override.enabled()
)

print("\nStatistics\n")

print(
    json.dumps(
        override.statistics(),
        indent=2,
    )
)

# -------------------------------------------------
# Approve
# -------------------------------------------------

print("\nApprove Decision\n")

print(
    override.approve()
)

print("\nDecision\n")

print(
    override.decision()
)

print("\nStatistics\n")

print(
    json.dumps(
        override.statistics(),
        indent=2,
    )
)

# -------------------------------------------------
# Reject
# -------------------------------------------------

print("\nReject Decision\n")

print(
    override.reject()
)

print("\nDecision\n")

print(
    override.decision()
)

# -------------------------------------------------
# Force Decision
# -------------------------------------------------

print("\nForce Decision\n")

forced_result = {
    "status": "approved",
    "repositories": [
        "enterprise-mcp-platform",
        "agent-service",
    ],
}

print(
    override.force(
        forced_result,
    )
)

print("\nDecision\n")

print(
    override.decision()
)

print("\nForced Value\n")

print(
    json.dumps(
        override.forced_value(),
        indent=2,
    )
)

print("\nStatistics\n")

print(
    json.dumps(
        override.statistics(),
        indent=2,
    )
)

# -------------------------------------------------
# Export
# -------------------------------------------------

print("\nExport\n")

print(
    json.dumps(
        override.export(),
        indent=2,
    )
)

# -------------------------------------------------
# Disable Override
# -------------------------------------------------

print("\nDisabling Override\n")

print(
    override.disable()
)

print("\nStatistics\n")

print(
    json.dumps(
        override.statistics(),
        indent=2,
    )
)

# -------------------------------------------------
# Cleanup
# -------------------------------------------------

print("\nCleanup\n")

override.clear()

print(
    json.dumps(
        override.statistics(),
        indent=2,
    )
)

print("\nManual Override Test Passed ✓")