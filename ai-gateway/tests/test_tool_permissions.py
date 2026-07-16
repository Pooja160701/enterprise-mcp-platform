import json

from app.governance.tool_permissions import ToolPermissions


def pretty(data):
    print(
        json.dumps(
            data,
            indent=2,
        )
    )


print("\n=== Tool Permissions Test ===\n")

# -------------------------------------------------
# Initialize
# -------------------------------------------------

permissions = ToolPermissions()

print("Initializing Tool Permissions\n")

pretty(
    permissions.statistics()
)

# -------------------------------------------------
# Register Tools
# -------------------------------------------------

print("\nRegistering Tools\n")

print(
    permissions.register(
        "github.list_repositories",
        roles=["admin", "developer"],
        users=["alice"],
    )
)

print(
    permissions.register(
        "database.delete",
        roles=["admin"],
    )
)

print(
    permissions.register(
        "filesystem.search",
        roles=["admin", "developer", "viewer"],
    )
)

pretty(
    permissions.statistics()
)

# -------------------------------------------------
# Tool Exists
# -------------------------------------------------

print("\nTool Exists\n")

print("github.list_repositories")

print(
    permissions.exists(
        "github.list_repositories"
    )
)

print("\nunknown.tool")

print(
    permissions.exists(
        "unknown.tool"
    )
)

# -------------------------------------------------
# Roles
# -------------------------------------------------

print("\nAllowed Roles\n")

print("github.list_repositories")

pretty(
    permissions.roles(
        "github.list_repositories"
    )
)

print("\ndatabase.delete")

pretty(
    permissions.roles(
        "database.delete"
    )
)

# -------------------------------------------------
# Users
# -------------------------------------------------

print("\nAllowed Users\n")

print("github.list_repositories")

pretty(
    permissions.users(
        "github.list_repositories"
    )
)

# -------------------------------------------------
# Permission Checks
# -------------------------------------------------

print("\nPermission Checks\n")

print("Admin -> database.delete")

print(
    permissions.allowed(
        "database.delete",
        role="admin",
    )
)

print("\nDeveloper -> database.delete")

print(
    permissions.allowed(
        "database.delete",
        role="developer",
    )
)

print("\nAlice -> github.list_repositories")

print(
    permissions.allowed(
        "github.list_repositories",
        user="alice",
    )
)

print("\nBob -> github.list_repositories")

print(
    permissions.allowed(
        "github.list_repositories",
        user="bob",
    )
)

# -------------------------------------------------
# Allow Role
# -------------------------------------------------

print("\nAllow Role\n")

print(
    permissions.allow_role(
        "database.delete",
        "developer",
    )
)

pretty(
    permissions.roles(
        "database.delete"
    )
)

print("\nDeveloper -> database.delete")

print(
    permissions.allowed(
        "database.delete",
        role="developer",
    )
)

# -------------------------------------------------
# Deny Role
# -------------------------------------------------

print("\nDeny Role\n")

print(
    permissions.deny_role(
        "database.delete",
        "developer",
    )
)

pretty(
    permissions.roles(
        "database.delete"
    )
)

# -------------------------------------------------
# Allow User
# -------------------------------------------------

print("\nAllow User\n")

print(
    permissions.allow_user(
        "database.delete",
        "bob",
    )
)

pretty(
    permissions.users(
        "database.delete"
    )
)

print("\nBob -> database.delete")

print(
    permissions.allowed(
        "database.delete",
        user="bob",
    )
)

# -------------------------------------------------
# Deny User
# -------------------------------------------------

print("\nDeny User\n")

print(
    permissions.deny_user(
        "database.delete",
        "bob",
    )
)

pretty(
    permissions.users(
        "database.delete"
    )
)

# -------------------------------------------------
# Remove Tool
# -------------------------------------------------

print("\nRemoving Tool\n")

print(
    permissions.remove(
        "filesystem.search"
    )
)

pretty(
    permissions.statistics()
)

# -------------------------------------------------
# Export
# -------------------------------------------------

print("\nExport\n")

pretty(
    permissions.export()
)

# -------------------------------------------------
# Cleanup
# -------------------------------------------------

print("\nCleanup\n")

permissions.clear()

pretty(
    permissions.statistics()
)

print("\nTool Permissions Test Passed ✓")