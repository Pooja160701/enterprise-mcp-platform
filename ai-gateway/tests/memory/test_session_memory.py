import json

from app.memory.session_memory import SessionMemory


CONVERSATION_ID = "conversation_001"

print("\n=== Session Memory Test ===\n")

#
# ----------------------------------------
# Clear
# ----------------------------------------
#

SessionMemory.clear()

print("Initial Session\n")

print(
    json.dumps(
        SessionMemory.all(CONVERSATION_ID),
        indent=2,
    )
)

#
# ----------------------------------------
# Store Values
# ----------------------------------------
#

print("\nAdding Session Values\n")

SessionMemory.set(
    CONVERSATION_ID,
    "repository",
    "enterprise-mcp-platform",
)

SessionMemory.set(
    CONVERSATION_ID,
    "branch",
    "main",
)

SessionMemory.set(
    CONVERSATION_ID,
    "server",
    "github",
)

SessionMemory.set(
    CONVERSATION_ID,
    "tool",
    "list_branches",
)

print(
    json.dumps(
        SessionMemory.all(CONVERSATION_ID),
        indent=2,
    )
)

#
# ----------------------------------------
# Get Values
# ----------------------------------------
#

print("\nGet Values\n")

print(
    "Repository :",
    SessionMemory.get(
        CONVERSATION_ID,
        "repository",
    ),
)

print(
    "Branch :",
    SessionMemory.get(
        CONVERSATION_ID,
        "branch",
    ),
)

print(
    "Server :",
    SessionMemory.get(
        CONVERSATION_ID,
        "server",
    ),
)

print(
    "Tool :",
    SessionMemory.get(
        CONVERSATION_ID,
        "tool",
    ),
)

#
# ----------------------------------------
# Update Value
# ----------------------------------------
#

print("\nUpdate Branch\n")

SessionMemory.set(
    CONVERSATION_ID,
    "branch",
    "develop",
)

print(
    SessionMemory.get(
        CONVERSATION_ID,
        "branch",
    )
)

#
# ----------------------------------------
# Exists
# ----------------------------------------
#

print("\nExists\n")

print(
    "repository ->",
    SessionMemory.exists(
        CONVERSATION_ID,
        "repository",
    ),
)

print(
    "cluster ->",
    SessionMemory.exists(
        CONVERSATION_ID,
        "cluster",
    ),
)

#
# ----------------------------------------
# Delete
# ----------------------------------------
#

print("\nDelete Tool\n")

SessionMemory.delete(
    CONVERSATION_ID,
    "tool",
)

print(
    json.dumps(
        SessionMemory.all(CONVERSATION_ID),
        indent=2,
    )
)

#
# ----------------------------------------
# Statistics
# ----------------------------------------
#

print("\nStatistics\n")

print(
    json.dumps(
        SessionMemory.stats(),
        indent=2,
    )
)

#
# ----------------------------------------
# Clear Conversation
# ----------------------------------------
#

print("\nClearing Session\n")

SessionMemory.clear(
    CONVERSATION_ID,
)

print(
    json.dumps(
        SessionMemory.all(CONVERSATION_ID),
        indent=2,
    )
)

print("\nSession Memory Test Passed")