import json

from app.governance.rbac import RBAC


def pretty(data):
    print(
        json.dumps(
            data,
            indent=2,
        )
    )


print("\n=== RBAC Test ===\n")

# -------------------------------------------------
# Initialize
# -------------------------------------------------

rbac = RBAC()

print("Initializing RBAC\n")

pretty(
    rbac.statistics()
)

# -------------------------------------------------
# Create Roles
# -------------------------------------------------

print("\nCreating Roles\n")

print(
    rbac.add_role(
        "admin",
        [
            "read",
            "write",
            "delete",
        ],
    )
)

print(
    rbac.add_role(
        "developer",
        [
            "read",
            "write",
        ],
    )
)

print(
    rbac.add_role(
        "viewer",
        [
            "read",
        ],
    )
)

pretty(
    rbac.statistics()
)

print("\nRoles\n")

pretty(
    rbac.roles()
)

# -------------------------------------------------
# Assign Users
# -------------------------------------------------

print("\nAssigning Users\n")

print(
    rbac.assign(
        "alice",
        "admin",
    )
)

print(
    rbac.assign(
        "bob",
        "developer",
    )
)

print(
    rbac.assign(
        "charlie",
        "viewer",
    )
)

print("\nUsers\n")

pretty(
    rbac.users()
)

# -------------------------------------------------
# User Roles
# -------------------------------------------------

print("\nUser Roles\n")

print("alice")

print(
    rbac.role(
        "alice",
    )
)

print("\nbob")

print(
    rbac.role(
        "bob",
    )
)

print("\ncharlie")

print(
    rbac.role(
        "charlie",
    )
)

# -------------------------------------------------
# Permissions
# -------------------------------------------------

print("\nUser Permissions\n")

print("alice")

pretty(
    rbac.permissions(
        "alice",
    )
)

print("\nbob")

pretty(
    rbac.permissions(
        "bob",
    )
)

print("\ncharlie")

pretty(
    rbac.permissions(
        "charlie",
    )
)

# -------------------------------------------------
# Permission Checks
# -------------------------------------------------

print("\nPermission Checks\n")

print("Alice Delete")

print(
    rbac.allowed(
        "alice",
        "delete",
    )
)

print("\nBob Delete")

print(
    rbac.allowed(
        "bob",
        "delete",
    )
)

print("\nCharlie Read")

print(
    rbac.allowed(
        "charlie",
        "read",
    )
)

# -------------------------------------------------
# Grant Permission
# -------------------------------------------------

print("\nGrant Permission\n")

print(
    rbac.grant(
        "developer",
        "delete",
    )
)

pretty(
    rbac.permissions(
        "bob",
    )
)

print("\nBob Delete")

print(
    rbac.allowed(
        "bob",
        "delete",
    )
)

# -------------------------------------------------
# Revoke Permission
# -------------------------------------------------

print("\nRevoke Permission\n")

print(
    rbac.revoke_permission(
        "developer",
        "delete",
    )
)

pretty(
    rbac.permissions(
        "bob",
    )
)

# -------------------------------------------------
# Revoke User
# -------------------------------------------------

print("\nRevoking User\n")

print(
    rbac.revoke(
        "charlie",
    )
)

pretty(
    rbac.users()
)

# -------------------------------------------------
# Remove Role
# -------------------------------------------------

print("\nRemoving Role\n")

print(
    rbac.remove_role(
        "viewer",
    )
)

pretty(
    rbac.roles()
)

# -------------------------------------------------
# Statistics
# -------------------------------------------------

print("\nStatistics\n")

pretty(
    rbac.statistics()
)

# -------------------------------------------------
# Export
# -------------------------------------------------

print("\nExport\n")

pretty(
    rbac.export()
)

# -------------------------------------------------
# Cleanup
# -------------------------------------------------

print("\nCleanup\n")

rbac.clear()

pretty(
    rbac.statistics()
)

print("\nRBAC Test Passed ✓")