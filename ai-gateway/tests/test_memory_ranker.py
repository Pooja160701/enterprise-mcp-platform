import json
import time

from app.memory.memory_ranker import MemoryRanker


print("\n=== Memory Ranker Test ===\n")

#
# ----------------------------------------
# Sample Memories
# ----------------------------------------
#

now = time.time()

memories = [

    {
        "id": 1,
        "content": "User prefers AWS cloud.",
        "importance": 95,
        "category": "preference",
        "created_at": now - 60,
        "access_count": 5,
        "pinned": True,
    },

    {
        "id": 2,
        "content": "Uses FastAPI for backend.",
        "importance": 80,
        "category": "general",
        "created_at": now - 3600,
        "access_count": 2,
    },

    {
        "id": 3,
        "content": "Repository is enterprise-mcp-platform.",
        "importance": 70,
        "category": "fact",
        "created_at": now - 120,
        "access_count": 1,
    },

    {
        "id": 4,
        "content": "Working with Kubernetes clusters.",
        "importance": 100,
        "category": "profile",
        "created_at": now - 7200,
        "access_count": 0,
    },

]

print("Original Memories\n")

print(
    json.dumps(
        memories,
        indent=2,
        default=str,
    )
)

#
# ----------------------------------------
# Rank
# ----------------------------------------
#

print("\nRanking for Query: 'aws cloud'\n")

ranked = MemoryRanker.rank(
    query="aws cloud",
    memories=memories,
)

print(
    json.dumps(
        ranked,
        indent=2,
        default=str,
    )
)

#
# ----------------------------------------
# Best Match
# ----------------------------------------
#

print("\nBest Match\n")

best = MemoryRanker.best(
    query="aws cloud",
    memories=memories,
)

print(
    json.dumps(
        best,
        indent=2,
        default=str,
    )
)

#
# ----------------------------------------
# Touch Memory
# ----------------------------------------
#

print("\nTouch Best Memory\n")

updated = MemoryRanker.touch(best)

print(
    json.dumps(
        updated,
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
        MemoryRanker.statistics(
            ranked,
        ),
        indent=2,
    )
)

#
# ----------------------------------------
# Empty Ranking
# ----------------------------------------
#

print("\nEmpty Ranking\n")

print(
    json.dumps(
        MemoryRanker.rank(
            query="github",
            memories=[],
        ),
        indent=2,
    )
)

print("\nMemory Ranker Test Passed ✓")