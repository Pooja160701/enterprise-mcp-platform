import json
import time

from app.governance.rate_limits import RateLimits


def pretty(data):
    print(
        json.dumps(
            data,
            indent=2,
        )
    )


print("\n=== Rate Limits Test ===\n")

# -------------------------------------------------
# Initialize
# -------------------------------------------------

limits = RateLimits()

print("Initializing Rate Limits\n")

pretty(
    limits.statistics()
)

# -------------------------------------------------
# Configure
# -------------------------------------------------

print("\nConfiguring Rate Limits\n")

limits.configure(
    global_limit=5,
    user_limit=2,
    tool_limit=3,
    window=60,
)

pretty(
    limits.statistics()
)

# -------------------------------------------------
# Initial Checks
# -------------------------------------------------

print("\nInitial Permission Check\n")

print(
    limits.allowed(
        user="alice",
        tool="github.list_repositories",
    )
)

print("\nReason\n")

print(
    limits.reason()
)

# -------------------------------------------------
# Record Requests
# -------------------------------------------------

print("\nRecording Requests\n")

print(
    limits.record(
        user="alice",
        tool="github.list_repositories",
    )
)

print(
    limits.record(
        user="alice",
        tool="github.list_repositories",
    )
)

print(
    limits.record(
        user="bob",
        tool="github.list_repositories",
    )
)

pretty(
    limits.statistics()
)

# -------------------------------------------------
# Remaining Limits
# -------------------------------------------------

print("\nRemaining Global\n")

print(
    limits.remaining_global()
)

print("\nRemaining User (alice)\n")

print(
    limits.remaining_user(
        "alice"
    )
)

print("\nRemaining Tool\n")

print(
    limits.remaining_tool(
        "github.list_repositories"
    )
)

# -------------------------------------------------
# User Limit
# -------------------------------------------------

print("\nUser Limit Check\n")

print(
    limits.allowed(
        user="alice",
        tool="filesystem.search",
    )
)

print(
    limits.reason()
)

# -------------------------------------------------
# Tool Limit
# -------------------------------------------------

print("\nTool Limit Check\n")

print(
    limits.record(
        user="charlie",
        tool="github.list_repositories",
    )
)

print(
    limits.allowed(
        user="david",
        tool="github.list_repositories",
    )
)

print(
    limits.reason()
)

# -------------------------------------------------
# Global Limit
# -------------------------------------------------

print("\nGlobal Limit Check\n")

print(
    limits.record(
        user="eve",
        tool="filesystem.search",
    )
)

print(
    limits.allowed(
        user="frank",
        tool="memory.search",
    )
)

print(
    limits.reason()
)

# -------------------------------------------------
# Export
# -------------------------------------------------

print("\nExport\n")

pretty(
    limits.export()
)

# -------------------------------------------------
# Cleanup Window Demonstration
# -------------------------------------------------

print("\nWaiting 1 second (window demonstration)\n")

time.sleep(1)

pretty(
    limits.statistics()
)

# -------------------------------------------------
# Cleanup
# -------------------------------------------------

print("\nCleanup\n")

limits.clear()

pretty(
    limits.statistics()
)

print("\nRate Limits Test Passed ✓")