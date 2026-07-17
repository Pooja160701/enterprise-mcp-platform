import json

from app.memory.long_term_memory import LongTermMemory


USER_ID = "pooja"

print("\n=== Long-Term Memory Test ===\n")

#
# ----------------------------------------
# Clear
# ----------------------------------------
#

LongTermMemory.clear()

print("Initial Long-Term Memory\n")

print(
    json.dumps(
        LongTermMemory.get(USER_ID),
        indent=2,
    )
)

#
# ----------------------------------------
# Add Memories
# ----------------------------------------
#

print("\nAdding Long-Term Memories\n")

m1 = LongTermMemory.add(
    user_id=USER_ID,
    content="Preferred cloud provider is AWS.",
    category="preferences",
    importance=95,
    pinned=True,
    metadata={
        "source": "user",
    },
)

m2 = LongTermMemory.add(
    user_id=USER_ID,
    content="Working on Enterprise MCP Platform.",
    category="projects",
    importance=90,
    metadata={
        "status": "active",
    },
)

m3 = LongTermMemory.add(
    user_id=USER_ID,
    content="Uses FastAPI for backend services.",
    category="skills",
    importance=80,
)

print(
    json.dumps(
        LongTermMemory.get(USER_ID),
        indent=2,
        default=str,
    )
)

#
# ----------------------------------------
# Get By ID
# ----------------------------------------
#

print("\nGet By ID\n")

print(
    json.dumps(
        LongTermMemory.get_by_id(
            USER_ID,
            m1["id"],
        ),
        indent=2,
        default=str,
    )
)

#
# ----------------------------------------
# By Category
# ----------------------------------------
#

print("\nCategory: projects\n")

print(
    json.dumps(
        LongTermMemory.by_category(
            USER_ID,
            "projects",
        ),
        indent=2,
        default=str,
    )
)

#
# ----------------------------------------
# Pin Memory
# ----------------------------------------
#

print("\nPin FastAPI Memory\n")

LongTermMemory.pin(
    USER_ID,
    m3["id"],
)

print(
    json.dumps(
        LongTermMemory.get_by_id(
            USER_ID,
            m3["id"],
        ),
        indent=2,
        default=str,
    )
)

#
# ----------------------------------------
# Search
# ----------------------------------------
#

print("\nSearch 'AWS'\n")

print(
    json.dumps(
        LongTermMemory.search(
            USER_ID,
            "AWS",
        ),
        indent=2,
        default=str,
    )
)

#
# ----------------------------------------
# Archive
# ----------------------------------------
#

print("\nArchive Project Memory\n")

LongTermMemory.archive(
    USER_ID,
    m2["id"],
)

print(
    json.dumps(
        LongTermMemory.get_by_id(
            USER_ID,
            m2["id"],
        ),
        indent=2,
        default=str,
    )
)

#
# ----------------------------------------
# Update
# ----------------------------------------
#

print("\nUpdate Memory\n")

LongTermMemory.update(
    USER_ID,
    m3["id"],
    importance=100,
)

print(
    json.dumps(
        LongTermMemory.get_by_id(
            USER_ID,
            m3["id"],
        ),
        indent=2,
        default=str,
    )
)

#
# ----------------------------------------
# Delete
# ----------------------------------------
#

print("\nDelete Project Memory\n")

LongTermMemory.delete(
    USER_ID,
    m2["id"],
)

print(
    json.dumps(
        LongTermMemory.get(
            USER_ID,
        ),
        indent=2,
        default=str,
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
        LongTermMemory.stats(),
        indent=2,
    )
)

#
# ----------------------------------------
# Clear
# ----------------------------------------
#

print("\nClearing Long-Term Memory\n")

LongTermMemory.clear()

print(
    json.dumps(
        LongTermMemory.stats(),
        indent=2,
    )
)

print("\nLong-Term Memory Test Passed")