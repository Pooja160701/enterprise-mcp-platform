import json

from app.governance.compliance_rules import ComplianceRules


def pretty(data):
    print(
        json.dumps(
            data,
            indent=2,
        )
    )


print("\n=== Compliance Rules Test ===\n")

# -------------------------------------------------
# Initialize
# -------------------------------------------------

rules = ComplianceRules()

print("Initializing Compliance Rules\n")

pretty(
    rules.statistics()
)

# -------------------------------------------------
# Configure Rules
# -------------------------------------------------

print("\nConfiguring Compliance Rules\n")

rules.configure(
    restricted_tools=[
        "database.delete",
        "filesystem.remove",
    ],
    protected_environments=[
        "production",
        "staging",
    ],
    blocked_keywords=[
        "password",
        "secret",
        "token",
    ],
)

pretty(
    rules.statistics()
)

# -------------------------------------------------
# Compliant Request
# -------------------------------------------------

print("\nCompliant Evaluation\n")

print(
    rules.evaluate(
        tool="github.list_repositories",
        query="List all repositories.",
        environment="development",
    )
)

print("\nCompliant")

print(
    rules.compliant()
)

print("\nStatus")

print(
    rules.status()
)

print("\nReason")

print(
    rules.reason()
)

# -------------------------------------------------
# Restricted Tool
# -------------------------------------------------

print("\nRestricted Tool\n")

print(
    rules.evaluate(
        tool="database.delete",
        query="Delete old records.",
        environment="development",
    )
)

print("\nStatus")

print(
    rules.status()
)

print("\nReason")

print(
    rules.reason()
)

# -------------------------------------------------
# Protected Environment
# -------------------------------------------------

print("\nProtected Environment\n")

print(
    rules.evaluate(
        tool="github.list_repositories",
        query="List repositories.",
        environment="production",
    )
)

print("\nStatus")

print(
    rules.status()
)

print("\nReason")

print(
    rules.reason()
)

# -------------------------------------------------
# Sensitive Data
# -------------------------------------------------

print("\nSensitive Data Detection\n")

print(
    rules.evaluate(
        tool="github.list_repositories",
        query="List repositories.",
        contains_sensitive_data=True,
    )
)

print("\nStatus")

print(
    rules.status()
)

print("\nReason")

print(
    rules.reason()
)

# -------------------------------------------------
# Blocked Keyword
# -------------------------------------------------

print("\nBlocked Keyword\n")

print(
    rules.evaluate(
        tool="github.list_repositories",
        query="Show database password",
    )
)

print("\nStatus")

print(
    rules.status()
)

print("\nReason")

print(
    rules.reason()
)

# -------------------------------------------------
# Export
# -------------------------------------------------

print("\nExport\n")

pretty(
    rules.export()
)

# -------------------------------------------------
# Statistics
# -------------------------------------------------

print("\nStatistics\n")

pretty(
    rules.statistics()
)

# -------------------------------------------------
# Cleanup
# -------------------------------------------------

print("\nCleanup\n")

rules.clear()

pretty(
    rules.statistics()
)

print("\nCompliance Rules Test Passed ✓")