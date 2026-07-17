import json

from app.memory.semantic_memory import SemanticMemory


print("\n=== Semantic Memory Test ===\n")

#
# ----------------------------------------
# Clear
# ----------------------------------------
#

SemanticMemory.clear()

print("Initial Semantic Memory\n")

print(
    json.dumps(
        SemanticMemory.all(),
        indent=2,
    )
)

#
# ----------------------------------------
# Add Memories
# ----------------------------------------
#

print("\nAdding Semantic Memories\n")

m1 = SemanticMemory.add(
    content="Enterprise MCP Platform uses FastAPI.",
    tags=[
        "fastapi",
        "backend",
    ],
    importance=90,
    metadata={
        "source": "documentation",
    },
)

m2 = SemanticMemory.add(
    content="GitHub server exposes list_branches tool.",
    tags=[
        "github",
        "tool",
    ],
    importance=80,
    metadata={
        "source": "github",
    },
)

m3 = SemanticMemory.add(
    content="AWS server supports Lambda deployment.",
    tags=[
        "aws",
        "cloud",
    ],
    importance=70,
    metadata={
        "source": "aws",
    },
)

print(
    json.dumps(
        SemanticMemory.all(),
        indent=2,
        default=str,
    )
)

#
# ----------------------------------------
# Similarity Search
# ----------------------------------------
#

print("\nSimilarity Search: 'github branches'\n")

print(
    json.dumps(
        SemanticMemory.search(
            "github branches",
        ),
        indent=2,
        default=str,
    )
)

#
# ----------------------------------------
# Keyword Search
# ----------------------------------------
#

print("\nKeyword Search: 'FastAPI'\n")

print(
    json.dumps(
        SemanticMemory.keyword(
            "FastAPI",
        ),
        indent=2,
        default=str,
    )
)

#
# ----------------------------------------
# Tag Search
# ----------------------------------------
#

print("\nTag Search: 'github'\n")

print(
    json.dumps(
        SemanticMemory.tag(
            "github",
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

SemanticMemory.update(
    m1["id"],
    importance=100,
)

print(
    json.dumps(
        SemanticMemory.all()[0],
        indent=2,
        default=str,
    )
)

#
# ----------------------------------------
# Delete
# ----------------------------------------
#

print("\nDelete AWS Memory\n")

SemanticMemory.delete(
    m3["id"],
)

print(
    json.dumps(
        SemanticMemory.all(),
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
        SemanticMemory.stats(),
        indent=2,
    )
)

#
# ----------------------------------------
# Clear
# ----------------------------------------
#

print("\nClearing Semantic Memory\n")

SemanticMemory.clear()

print(
    json.dumps(
        SemanticMemory.stats(),
        indent=2,
    )
)

print("\nSemantic Memory Test Passed")