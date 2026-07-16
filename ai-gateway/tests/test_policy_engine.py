import json

from app.governance.policy_engine import PolicyEngine


def pretty(data):
    print(
        json.dumps(
            data,
            indent=2,
        )
    )


print("\n=== Policy Engine Test ===\n")

# -------------------------------------------------
# Initialize
# -------------------------------------------------

engine = PolicyEngine()

print("Initializing Policy Engine\n")

pretty(
    engine.statistics()
)

# -------------------------------------------------
# Register Policies
# -------------------------------------------------

print("\nRegistering Policies\n")


def allow_all(context):
    return True


def deny_delete(context):
    return context.get("action") != "delete"


def admin_only(context):
    return context.get("role") == "admin"


engine.register(
    "Allow All",
    allow_all,
    priority=10,
)

engine.register(
    "No Delete",
    deny_delete,
    priority=100,
)

engine.register(
    "Admin Only",
    admin_only,
    priority=50,
)

pretty(
    engine.statistics()
)

print("\nPolicies\n")

pretty(
    engine.policies()
)

# -------------------------------------------------
# Allow Evaluation
# -------------------------------------------------

print("\nAllowed Evaluation\n")

allowed = engine.evaluate(

    {

        "action": "read",

        "role": "admin",

    }

)

print(allowed)

print("\nAllowed\n")

print(engine.allowed())

print("\nReason\n")

print(engine.reason())

print("\nExport\n")

pretty(
    engine.export()
)

# -------------------------------------------------
# Denied Evaluation
# -------------------------------------------------

print("\nDenied Evaluation\n")

allowed = engine.evaluate(

    {

        "action": "delete",

        "role": "admin",

    }

)

print(allowed)

print("\nAllowed\n")

print(engine.allowed())

print("\nReason\n")

print(engine.reason())

# -------------------------------------------------
# Disable Policy
# -------------------------------------------------

print("\nDisabling Policy\n")

print(

    engine.disable(

        "No Delete"

    )

)

pretty(
    engine.statistics()
)

# -------------------------------------------------
# Evaluate Again
# -------------------------------------------------

print("\nEvaluation After Disable\n")

allowed = engine.evaluate(

    {

        "action": "delete",

        "role": "admin",

    }

)

print(allowed)

print("\nReason\n")

print(engine.reason())

# -------------------------------------------------
# Enable Policy
# -------------------------------------------------

print("\nEnabling Policy\n")

print(

    engine.enable(

        "No Delete"

    )

)

pretty(
    engine.statistics()
)

# -------------------------------------------------
# Remove Policy
# -------------------------------------------------

print("\nRemoving Policy\n")

print(

    engine.remove(

        "Allow All"

    )

)

pretty(
    engine.statistics()
)

# -------------------------------------------------
# Final Export
# -------------------------------------------------

print("\nExport\n")

pretty(
    engine.export()
)

# -------------------------------------------------
# Cleanup
# -------------------------------------------------

print("\nCleanup\n")

engine.clear()

pretty(
    engine.statistics()
)

print("\nPolicy Engine Test Passed ✓")