import json

from context.context_manager import ContextManager
from app.memory.conversation_history import ConversationHistory
from app.memory.session_memory import SessionMemory
from app.memory.long_term_memory import LongTermMemory
from app.memory.semantic_memory import SemanticMemory


CONVERSATION_ID = "conv_001"
USER_ID = "pooja"

ConversationHistory.clear()
SessionMemory.clear()
LongTermMemory.clear()
SemanticMemory.clear()

#
# Populate memories
#

ConversationHistory.add_user(
    CONVERSATION_ID,
    "List all GitHub repositories.",
)

ConversationHistory.add_assistant(
    CONVERSATION_ID,
    "Fetching repositories.",
)

ConversationHistory.add_tool_result(
    CONVERSATION_ID,
    "github",
    "list_repositories",
    "Found 12 repositories.",
)

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

LongTermMemory.add(
    USER_ID,
    content="Preferred cloud provider is AWS.",
    category="preferences",
    importance=95,
)

LongTermMemory.add(
    USER_ID,
    content="Working on Enterprise MCP Platform.",
    category="projects",
    importance=90,
)

SemanticMemory.add(
    text="Enterprise MCP Platform uses FastAPI.",
    importance=90,
)

SemanticMemory.add(
    text="GitHub exposes list_branches.",
    importance=80,
)

print("\n=== Context Manager Test ===")

prompt = ContextManager.build_context(

    conversation_id=CONVERSATION_ID,

    user_id=USER_ID,

    query="Show branches of enterprise-mcp-platform.",

)

print("\nGenerated Prompt\n")

print(prompt)

print("\nPrompt Statistics\n")

print(

    json.dumps(

        ContextManager.statistics(

            prompt,

        ),

        indent=2,

    )

)

print("\nEstimated Tokens")

print(

    ContextManager.tokens(

        prompt,

    )

)

print("\nEmpty Context")

empty = ContextManager.build_context(

    conversation_id=None,

    user_id=None,

    query="Hello",

)

print(empty)

print("\nContext Manager Test Passed ✓")