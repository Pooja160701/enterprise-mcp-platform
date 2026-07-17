import json

from app.governance.secret_access_rules import SecretAccessRules


def pretty(data):
    print(
        json.dumps(
            data,
            indent=2,
        )
    )


print("\n=== Secret Access Rules Test ===\n")

# -------------------------------------------------
# Initialize
# -------------------------------------------------

rules = SecretAccessRules()

print("Initializing Secret Access Rules\n")

pretty(
    rules.statistics()
)

# -------------------------------------------------
# Register Secrets
# -------------------------------------------------

print("\nRegistering Secrets\n")

print(
    rules.register(
        "OPENAI_API_KEY",
        roles=["admin", "developer"],
        users=["alice"],
        permissions=[
            SecretAccessRules.READ,
            SecretAccessRules.WRITE,
        ],
    )
)

print(
    rules.register(
        "DATABASE_PASSWORD",
        roles=["admin"],
        permissions=[
            SecretAccessRules.READ,
        ],
    )
)

print(
    rules.register(
        "JWT_SECRET",
        roles=["admin"],
        users=["security"],
        permissions=[
            SecretAccessRules.READ,
            SecretAccessRules.WRITE,
        ],
    )
)

pretty(
    rules.statistics()
)

# -------------------------------------------------
# Exists
# -------------------------------------------------

print("\nSecret Exists\n")

print("OPENAI_API_KEY")

print(
    rules.exists(
        "OPENAI_API_KEY"
    )
)

print("\nUNKNOWN_SECRET")

print(
    rules.exists(
        "UNKNOWN_SECRET"
    )
)

# -------------------------------------------------
# Roles
# -------------------------------------------------

print("\nAllowed Roles\n")

print("OPENAI_API_KEY")

pretty(
    rules.roles(
        "OPENAI_API_KEY"
    )
)

print("\nDATABASE_PASSWORD")

pretty(
    rules.roles(
        "DATABASE_PASSWORD"
    )
)

# -------------------------------------------------
# Users
# -------------------------------------------------

print("\nAllowed Users\n")

print("OPENAI_API_KEY")

pretty(
    rules.users(
        "OPENAI_API_KEY"
    )
)

# -------------------------------------------------
# Permissions
# -------------------------------------------------

print("\nPermissions\n")

print("OPENAI_API_KEY")

pretty(
    rules.permissions(
        "OPENAI_API_KEY"
    )
)

print("\nDATABASE_PASSWORD")

pretty(
    rules.permissions(
        "DATABASE_PASSWORD"
    )
)

# -------------------------------------------------
# Permission Checks
# -------------------------------------------------

print("\nPermission Checks\n")

print("Admin READ DATABASE_PASSWORD")

print(
    rules.allowed(
        "DATABASE_PASSWORD",
        role="admin",
        permission=SecretAccessRules.READ,
    )
)

print("\nDeveloper READ DATABASE_PASSWORD")

print(
    rules.allowed(
        "DATABASE_PASSWORD",
        role="developer",
        permission=SecretAccessRules.READ,
    )
)

print("\nAlice WRITE OPENAI_API_KEY")

print(
    rules.allowed(
        "OPENAI_API_KEY",
        user="alice",
        permission=SecretAccessRules.WRITE,
    )
)

print("\nBob WRITE OPENAI_API_KEY")

print(
    rules.allowed(
        "OPENAI_API_KEY",
        user="bob",
        permission=SecretAccessRules.WRITE,
    )
)

# -------------------------------------------------
# Grant Permission
# -------------------------------------------------

print("\nGrant Permission\n")

print(
    rules.grant(
        "DATABASE_PASSWORD",
        SecretAccessRules.WRITE,
    )
)

pretty(
    rules.permissions(
        "DATABASE_PASSWORD"
    )
)

print("\nAdmin WRITE DATABASE_PASSWORD")

print(
    rules.allowed(
        "DATABASE_PASSWORD",
        role="admin",
        permission=SecretAccessRules.WRITE,
    )
)

# -------------------------------------------------
# Revoke Permission
# -------------------------------------------------

print("\nRevoke Permission\n")

print(
    rules.revoke(
        "DATABASE_PASSWORD",
        SecretAccessRules.WRITE,
    )
)

pretty(
    rules.permissions(
        "DATABASE_PASSWORD"
    )
)

# -------------------------------------------------
# Allow Role
# -------------------------------------------------

print("\nAllow Role\n")

print(
    rules.allow_role(
        "DATABASE_PASSWORD",
        "developer",
    )
)

pretty(
    rules.roles(
        "DATABASE_PASSWORD"
    )
)

# -------------------------------------------------
# Deny Role
# -------------------------------------------------

print("\nDeny Role\n")

print(
    rules.deny_role(
        "DATABASE_PASSWORD",
        "developer",
    )
)

pretty(
    rules.roles(
        "DATABASE_PASSWORD"
    )
)

# -------------------------------------------------
# Allow User
# -------------------------------------------------

print("\nAllow User\n")

print(
    rules.allow_user(
        "DATABASE_PASSWORD",
        "bob",
    )
)

pretty(
    rules.users(
        "DATABASE_PASSWORD"
    )
)

print("\nBob READ DATABASE_PASSWORD")

print(
    rules.allowed(
        "DATABASE_PASSWORD",
        user="bob",
        permission=SecretAccessRules.READ,
    )
)

# -------------------------------------------------
# Deny User
# -------------------------------------------------

print("\nDeny User\n")

print(
    rules.deny_user(
        "DATABASE_PASSWORD",
        "bob",
    )
)

pretty(
    rules.users(
        "DATABASE_PASSWORD"
    )
)

# -------------------------------------------------
# Remove Secret
# -------------------------------------------------

print("\nRemoving Secret\n")

print(
    rules.remove(
        "JWT_SECRET"
    )
)

pretty(
    rules.statistics()
)

# -------------------------------------------------
# Export
# -------------------------------------------------

print("\nExport\n")

pretty(
    rules.export()
)

# -------------------------------------------------
# Cleanup
# -------------------------------------------------

print("\nCleanup\n")

rules.clear()

pretty(
    rules.statistics()
)

print("\nSecret Access Rules Test Passed")