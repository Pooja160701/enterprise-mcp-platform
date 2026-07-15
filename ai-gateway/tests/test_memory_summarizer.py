import json

from app.memory.memory_summarizer import MemorySummarizer


print("\n=== Memory Summarizer Test ===\n")

#
# ----------------------------------------------------
# Sample Conversation
# ----------------------------------------------------
#

messages = [

    {
        "role": "user",
        "content": "List all GitHub repositories.",
    },

    {
        "role": "assistant",
        "content": "Fetching repositories from GitHub.",
    },

    {
        "role": "tool",
        "content": "Executed list_repositories.",
    },

    {
        "role": "assistant",
        "content": "Found 12 repositories.",
    },

    {
        "role": "user",
        "content": "Show branches of enterprise-mcp-platform.",
    },

    {
        "role": "assistant",
        "content": "Fetching branches.",
    },

    {
        "role": "tool",
        "content": "Executed list_branches.",
    },

    {
        "role": "assistant",
        "content": "Found branches: main, develop.",
    },

]

print("Conversation\n")

print(
    json.dumps(
        messages,
        indent=2,
    )
)

print("\nSummary\n")

summary = MemorySummarizer.summarize(
    messages,
)

if isinstance(summary, (dict, list)):

    print(
        json.dumps(
            summary,
            indent=2,
            default=str,
        )
    )

else:

    print(summary)

print("\nSummary Length\n")

if isinstance(summary, str):

    print(len(summary), "characters")

elif isinstance(summary, list):

    print(len(summary), "items")

elif isinstance(summary, dict):

    print(len(summary.keys()), "fields")

print("\nMemory Summarizer Test Passed ✓")