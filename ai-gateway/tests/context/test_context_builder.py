import json

from context.context_builder import ContextBuilder
from app.memory.conversation_history import ConversationHistory
from app.memory.session_memory import SessionMemory
from app.memory.semantic_memory import SemanticMemory
from app.memory.long_term_memory import LongTermMemory


CONVERSATION_ID = "conv_001"
USER_ID = "pooja"


def pretty(obj):
    print(
        json.dumps(
            obj,
            indent=2,
            default=str,
        )
    )


#
# Clean
#

ConversationHistory.clear()
SessionMemory.clear()
SemanticMemory.clear()
LongTermMemory.clear()

print("\n=== Context Builder Test ===")

#
# Populate Conversation
#

ConversationHistory.add_user(
    CONVERSATION_ID,
    "List my GitHub repositories.",
)

ConversationHistory.add_assistant(
    CONVERSATION_ID,
    "Fetching repositories.",
)

ConversationHistory.add_tool_call(
    CONVERSATION_ID,
    "github",
    "list_repositories",
    {},
)

ConversationHistory.add_tool_result(
    CONVERSATION_ID,
    "github",
    "list_repositories",
    "Found 12 repositories.",
)

#
# Populate Session
#

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

#
# Populate Long-Term Memory
#

LongTermMemory.add(
    user_id=USER_ID,
    content="Preferred cloud provider is AWS.",
    category="preferences",
    importance=95,
)

LongTermMemory.add(
    user_id=USER_ID,
    content="Working on Enterprise MCP Platform.",
    category="projects",
    importance=90,
)

#
# Populate Semantic Memory
#

SemanticMemory.add(
    text="Enterprise MCP Platform uses FastAPI.",
    tags=["fastapi"],
    importance=90,
)

SemanticMemory.add(
    text="GitHub exposes list_branches.",
    tags=["github"],
    importance=80,
)

#
# Build Context
#

print("\nBuilt Context\n")

context = ContextBuilder.build(
    conversation_id=CONVERSATION_ID,
    user_id=USER_ID,
)

pretty(context)

#
# Conversation
#

print("\nConversation\n")

pretty(
    context["conversation"]
)

#
# Session
#

print("\nSession\n")

pretty(
    context["session"]
)

#
# Long-Term
#

print("\nLong-Term Memory\n")

pretty(
    context["long_term"]
)

#
# Semantic
#

print("\nSemantic Memory\n")

pretty(
    context["semantic"]
)

#
# Statistics
#

print("\nStatistics\n")

pretty(
    ContextBuilder.statistics(
        context,
    )
)

#
# Has Context
#

print("\nHas Context\n")

print(
    ContextBuilder.has_context(
        context,
    )
)

#
# Empty Context
#

print("\nEmpty Context\n")

pretty(
    ContextBuilder.empty()
)

print("\nContext Builder Test Passed")