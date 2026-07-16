import json

from app.governance.governance_manager import GovernanceManager


def pretty(data):
    print(
        json.dumps(
            data,
            indent=2,
        )
    )


print("\n=== Governance Manager Test ===\n")

# -------------------------------------------------
# Initialize
# -------------------------------------------------

manager = GovernanceManager()

print("Initializing Governance Manager\n")

pretty(
    manager.statistics()
)

# -------------------------------------------------
# Configure Policy Engine
# -------------------------------------------------

print("\nConfiguring Policy Engine\n")


manager.policy.register(
    "Allow All",
    lambda ctx: True,
    priority=10,
)

pretty(
    manager.policy.statistics()
)

# -------------------------------------------------
# Configure RBAC
# -------------------------------------------------

print("\nConfiguring RBAC\n")

manager.rbac.add_role(
    "admin",
    permissions=[
        "database.delete",
        "github.list_repositories",
    ],
)

manager.rbac.assign(
    "alice",
    "admin",
)

pretty(
    manager.rbac.statistics()
)

# -------------------------------------------------
# Configure Tool Permissions
# -------------------------------------------------

print("\nConfiguring Tool Permissions\n")

manager.permissions.register(
    "database.delete",
    roles=[
        "admin",
    ],
)

manager.permissions.register(
    "github.list_repositories",
    roles=[
        "admin",
    ],
)

pretty(
    manager.permissions.statistics()
)

# -------------------------------------------------
# Configure Secret Access
# -------------------------------------------------

print("\nConfiguring Secret Access\n")

manager.secrets.register(
    "OPENAI_API_KEY",
    roles=[
        "admin",
    ],
)

pretty(
    manager.secrets.statistics()
)

# -------------------------------------------------
# Configure Rate Limits
# -------------------------------------------------

print("\nConfiguring Rate Limits\n")

manager.rate_limits.configure(
    global_limit=5,
    user_limit=5,
    tool_limit=5,
)

pretty(
    manager.rate_limits.statistics()
)

# -------------------------------------------------
# Configure Compliance Rules
# -------------------------------------------------

print("\nConfiguring Compliance Rules\n")

manager.compliance.configure(
    restricted_tools=[
        "filesystem.remove",
    ],
    protected_environments=[
        "production",
    ],
    blocked_keywords=[
        "password",
    ],
)

pretty(
    manager.compliance.statistics()
)

# -------------------------------------------------
# Governance Evaluation
# -------------------------------------------------

print("\nGovernance Evaluation\n")

result = manager.evaluate(
    user="alice",
    role="admin",
    tool="github.list_repositories",
    secret="OPENAI_API_KEY",
    environment="development",
    query="List all repositories.",
)

print(result["allowed"])

print("\nResults\n")

pretty(
    result["results"]
)

# -------------------------------------------------
# Compliance Failure
# -------------------------------------------------

print("\nCompliance Failure\n")

result = manager.evaluate(
    user="alice",
    role="admin",
    tool="filesystem.remove",
    environment="production",
    query="delete password",
)

print(result["allowed"])

pretty(result)

# -------------------------------------------------
# Statistics
# -------------------------------------------------

print("\nStatistics\n")

pretty(
    manager.statistics()
)

# -------------------------------------------------
# Export
# -------------------------------------------------

print("\nExport\n")

pretty(
    manager.export()
)

# -------------------------------------------------
# Cleanup
# -------------------------------------------------

print("\nCleanup\n")

manager.clear()

pretty(
    manager.statistics()
)

print("\nGovernance Manager Test Passed ✓")