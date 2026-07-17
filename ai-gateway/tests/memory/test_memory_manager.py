import json

from app.memory.memory_manager import MemoryManager


USER_ID = "pooja"
CONVERSATION_ID = "conv_001"

print("\n=== Memory Manager Test ===\n")

#
# --------------------------------------------------
# Reset
# --------------------------------------------------
#

MemoryManager.clear_all()

print("Initial Statistics\n")

print(
    json.dumps(
        MemoryManager.stats(
            conversation_id=CONVERSATION_ID,
            user_id=USER_ID,
        ),
        indent=2,
    )
)

#
# --------------------------------------------------
# Conversation History
# --------------------------------------------------
#

print("\nAdding Conversation Messages\n")

MemoryManager.add_message(
    conversation_id=CONVERSATION_ID,
    role="user",
    content="I prefer AWS for cloud deployments.",
)

MemoryManager.add_message(
    conversation_id=CONVERSATION_ID,
    role="assistant",
    content="I'll remember that AWS is your preferred cloud provider.",
)

print(
    json.dumps(
        MemoryManager.history(
            CONVERSATION_ID,
        ),
        indent=2,
    )
)

#
# --------------------------------------------------
# Session Memory
# --------------------------------------------------
#

print("\nSession Memory\n")

MemoryManager.set_session(
    CONVERSATION_ID,
    "repository",
    "enterprise-mcp-platform",
)

MemoryManager.set_session(
    CONVERSATION_ID,
    "branch",
    "main",
)

print(
    json.dumps(
        MemoryManager.session(
            CONVERSATION_ID,
        ),
        indent=2,
    )
)

#
# --------------------------------------------------
# Long-Term Memory
# --------------------------------------------------
#

print("\nLong-Term Memory\n")

MemoryManager.remember(
    user_id=USER_ID,
    content="Preferred cloud provider is AWS.",
    category="preferences",
    importance=95,
)

print(
    json.dumps(
        MemoryManager.memories(
            USER_ID,
        ),
        indent=2,
    )
)

#
# --------------------------------------------------
# Semantic Memory
# --------------------------------------------------
#

print("\nSemantic Memory\n")

MemoryManager.add_semantic(
    text="Enterprise MCP Platform uses FastAPI.",
    tags=[
        "fastapi",
        "backend",
    ],
)

print(
    json.dumps(
        MemoryManager.semantic(),
        indent=2,
    )
)

#
# --------------------------------------------------
# Search
# --------------------------------------------------
#

print("\nSearch: AWS\n")

print(
    json.dumps(
        MemoryManager.search(
            query="AWS",
            conversation_id=CONVERSATION_ID,
            user_id=USER_ID,
        ),
        indent=2,
        default=str,
    )
)

#
# --------------------------------------------------
# Best Match
# --------------------------------------------------
#

print("\nBest Match\n")

print(
    json.dumps(
        MemoryManager.best_match(
            query="AWS",
            conversation_id=CONVERSATION_ID,
            user_id=USER_ID,
        ),
        indent=2,
        default=str,
    )
)

#
# --------------------------------------------------
# Summary
# --------------------------------------------------
#

print("\nConversation Summary\n")

print(
    json.dumps(
        MemoryManager.summary(
            CONVERSATION_ID,
        ),
        indent=2,
        default=str,
    )
)

#
# --------------------------------------------------
# Export
# --------------------------------------------------
#

print("\nExport\n")

exported = MemoryManager.export(
    conversation_id=CONVERSATION_ID,
    user_id=USER_ID,
)

print(
    json.dumps(
        exported,
        indent=2,
        default=str,
    )
)

#
# --------------------------------------------------
# Statistics
# --------------------------------------------------
#

print("\nStatistics\n")

print(
    json.dumps(
        MemoryManager.stats(
            conversation_id=CONVERSATION_ID,
            user_id=USER_ID,
        ),
        indent=2,
    )
)

#
# --------------------------------------------------
# Clear Conversation
# --------------------------------------------------
#

print("\nClear Conversation\n")

MemoryManager.clear_conversation(
    CONVERSATION_ID,
)

print(
    json.dumps(
        MemoryManager.stats(
            conversation_id=CONVERSATION_ID,
            user_id=USER_ID,
        ),
        indent=2,
    )
)

#
# --------------------------------------------------
# Clear All
# --------------------------------------------------
#

print("\nClear All\n")

MemoryManager.clear_all()

print(
    json.dumps(
        MemoryManager.stats(),
        indent=2,
    )
)

print("\nMemory Manager Test Passed")