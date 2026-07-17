import json

from app.memory.memory_store import MemoryStore


CONVERSATION_ID = "conv_001"

print("\n=== Memory Store Test ===\n")

#
# -----------------------------------------
# Clear
# -----------------------------------------
#

MemoryStore.clear()

print("Initial Statistics\n")

print(
    json.dumps(
        MemoryStore.stats(),
        indent=2,
    )
)

#
# -----------------------------------------
# Add Memories
# -----------------------------------------
#

print("\nAdding Memories\n")

m1 = MemoryStore.add(
    conversation_id=CONVERSATION_ID,
    content="User prefers Python",
    memory_type="session",
    importance=80,
    tags=["python", "preference"],
)

m2 = MemoryStore.add(
    conversation_id=CONVERSATION_ID,
    content="Uses FastAPI",
    memory_type="semantic",
    importance=70,
    tags=["fastapi"],
)

m3 = MemoryStore.add(
    conversation_id=CONVERSATION_ID,
    content="Working on Enterprise MCP",
    memory_type="long_term",
    importance=95,
    tags=["project"],
)

print(
    json.dumps(
        MemoryStore.get(CONVERSATION_ID),
        indent=2,
        default=str,
    )
)

#
# -----------------------------------------
# Get By ID
# -----------------------------------------
#

print("\nGet By ID\n")

print(
    json.dumps(
        MemoryStore.get_by_id(
            CONVERSATION_ID,
            m1["id"],
        ),
        indent=2,
        default=str,
    )
)

#
# -----------------------------------------
# Update
# -----------------------------------------
#

print("\nUpdate Memory\n")

MemoryStore.update(
    CONVERSATION_ID,
    m1["id"],
    importance=100,
)

print(
    json.dumps(
        MemoryStore.get_by_id(
            CONVERSATION_ID,
            m1["id"],
        ),
        indent=2,
        default=str,
    )
)

#
# -----------------------------------------
# Search by Tag
# -----------------------------------------
#

print("\nSearch By Tag\n")

print(
    json.dumps(
        MemoryStore.by_tag(
            CONVERSATION_ID,
            "python",
        ),
        indent=2,
        default=str,
    )
)

#
# -----------------------------------------
# Search by Type
# -----------------------------------------
#

print("\nSearch By Type\n")

print(
    json.dumps(
        MemoryStore.by_type(
            CONVERSATION_ID,
            "semantic",
        ),
        indent=2,
        default=str,
    )
)

#
# -----------------------------------------
# Delete
# -----------------------------------------
#

print("\nDelete Memory\n")

MemoryStore.delete(
    CONVERSATION_ID,
    m2["id"],
)

print(
    json.dumps(
        MemoryStore.get(
            CONVERSATION_ID,
        ),
        indent=2,
        default=str,
    )
)

#
# -----------------------------------------
# Statistics
# -----------------------------------------
#

print("\nStatistics\n")

print(
    json.dumps(
        MemoryStore.stats(),
        indent=2,
    )
)

#
# -----------------------------------------
# Clear
# -----------------------------------------
#

print("\nClearing Memory Store\n")

MemoryStore.clear()

print(
    json.dumps(
        MemoryStore.stats(),
        indent=2,
    )
)

print("\nMemory Store Test Passed")