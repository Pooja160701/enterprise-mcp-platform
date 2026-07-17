import json

from app.memory.conversation_history import ConversationHistory


CONVERSATION_ID = "conversation_001"

print("\n=== Conversation History Test ===\n")

#
# ----------------------------------------
# Clear
# ----------------------------------------
#

ConversationHistory.clear()

print("Initial History\n")

print(
    json.dumps(
        ConversationHistory.get(CONVERSATION_ID),
        indent=2,
    )
)

#
# ----------------------------------------
# Add Messages
# ----------------------------------------
#

print("\nAdding Messages\n")

ConversationHistory.add_user(
    CONVERSATION_ID,
    "List my GitHub repositories.",
)

ConversationHistory.add_assistant(
    CONVERSATION_ID,
    "Sure, I'll fetch your repositories.",
)

ConversationHistory.add_tool_call(
    conversation_id=CONVERSATION_ID,
    server="github",
    tool="list_repositories",
    arguments={},
)

ConversationHistory.add_tool_result(
    conversation_id=CONVERSATION_ID,
    server="github",
    tool="list_repositories",
    result="Found 12 repositories.",
)

ConversationHistory.add_assistant(
    CONVERSATION_ID,
    "Found 12 repositories.",
)

print(
    json.dumps(
        ConversationHistory.get(CONVERSATION_ID),
        indent=2,
        default=str,
    )
)

#
# ----------------------------------------
# Last Message
# ----------------------------------------
#

print("\nLast Message\n")

print(
    json.dumps(
        ConversationHistory.last(CONVERSATION_ID),
        indent=2,
        default=str,
    )
)

#
# ----------------------------------------
# Search
# ----------------------------------------
#

print("\nSearch 'github'\n")

print(
    json.dumps(
        ConversationHistory.search(
            CONVERSATION_ID,
            "github",
        ),
        indent=2,
        default=str,
    )
)

#
# ----------------------------------------
# Update Message
# ----------------------------------------
#

print("\nUpdate First Message\n")

first = ConversationHistory.get(CONVERSATION_ID)[0]

ConversationHistory.update(
    conversation_id=CONVERSATION_ID,
    message_id=first["id"],
    content="Show all GitHub repositories.",
)

print(
    json.dumps(
        ConversationHistory.get(CONVERSATION_ID)[0],
        indent=2,
        default=str,
    )
)

#
# ----------------------------------------
# Delete Message
# ----------------------------------------
#

print("\nDelete Last Message\n")

last = ConversationHistory.last(CONVERSATION_ID)

ConversationHistory.delete(
    conversation_id=CONVERSATION_ID,
    message_id=last["id"],
)

print(
    json.dumps(
        ConversationHistory.get(CONVERSATION_ID),
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
        ConversationHistory.stats(),
        indent=2,
    )
)

#
# ----------------------------------------
# Clear Conversation
# ----------------------------------------
#

print("\nClearing Conversation\n")

ConversationHistory.clear(CONVERSATION_ID)

print(
    json.dumps(
        ConversationHistory.get(CONVERSATION_ID),
        indent=2,
    )
)

print("\nConversation History Test Passed")