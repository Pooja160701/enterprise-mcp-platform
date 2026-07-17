import json

from app.memory.memory_compression import MemoryCompression


print("\n=== Memory Compression Test ===\n")

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

print("Original Messages\n")

print(
    json.dumps(
        messages,
        indent=2,
    )
)

print("\nTotal Messages :", len(messages))

#
# ----------------------------------------------------
# Compress
# ----------------------------------------------------
#

print("\nCompressed Memory\n")

compressed = MemoryCompression.compress(
    messages,
)

print(
    json.dumps(
        compressed,
        indent=2,
        default=str,
    )
)

#
# ----------------------------------------------------
# Statistics
# ----------------------------------------------------
#

print("\nCompression Statistics\n")

if isinstance(compressed, list):

    print("Original :", len(messages))
    print("Compressed :", len(compressed))
    print("Saved :", len(messages) - len(compressed))

elif isinstance(compressed, dict):

    print(
        json.dumps(
            compressed,
            indent=2,
            default=str,
        )
    )

else:

    print(compressed)

print("\nMemory Compression Test Passed")