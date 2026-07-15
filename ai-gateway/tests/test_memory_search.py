import json
import time

from app.memory.semantic_memory import SemanticMemory
from app.memory.long_term_memory import LongTermMemory
from app.memory.memory_search import MemorySearch


print("\n=== Memory Search Test ===\n")

#
# ----------------------------------------------------
# Reset
# ----------------------------------------------------
#

SemanticMemory.clear()
LongTermMemory.clear()

USER = "pooja"

#
# ----------------------------------------------------
# Populate Semantic Memory
# ----------------------------------------------------
#

SemanticMemory.add(
    content="Enterprise MCP Platform uses FastAPI.",
    tags=["fastapi", "backend"],
    importance=90,
)

SemanticMemory.add(
    content="GitHub server exposes list_branches tool.",
    tags=["github"],
    importance=80,
)

SemanticMemory.add(
    content="AWS Lambda deployment supported.",
    tags=["aws"],
    importance=70,
)

#
# ----------------------------------------------------
# Populate Long-Term Memory
# ----------------------------------------------------
#

LongTermMemory.add(
    user_id=USER,
    content="Preferred cloud provider is AWS.",
    category="preferences",
    importance=95,
)

LongTermMemory.add(
    user_id=USER,
    content="Working on Enterprise MCP Platform.",
    category="projects",
    importance=90,
)

print("Search : 'aws'\n")

results = MemorySearch.search(
    query="aws",
    user_id=USER,
)

print(
    json.dumps(
        results,
        indent=2,
        default=str,
    )
)

print("\nSearch : 'github'\n")

results = MemorySearch.search(
    query="github",
    user_id=USER,
)

print(
    json.dumps(
        results,
        indent=2,
        default=str,
    )
)

print("\nSearch : 'fastapi'\n")

results = MemorySearch.search(
    query="fastapi",
    user_id=USER,
)

print(
    json.dumps(
        results,
        indent=2,
        default=str,
    )
)

print("\nSearch : 'enterprise'\n")

results = MemorySearch.search(
    query="enterprise",
    user_id=USER,
)

print(
    json.dumps(
        results,
        indent=2,
        default=str,
    )
)

print("\nSearch : 'unknown'\n")

results = MemorySearch.search(
    query="unknown",
    user_id=USER,
)

print(
    json.dumps(
        results,
        indent=2,
        default=str,
    )
)

print("\nMemory Search Test Passed ✓")