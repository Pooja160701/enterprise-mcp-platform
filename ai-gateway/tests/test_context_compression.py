import json

from context.context_compression import ContextCompression


context = {

    "conversation": [

        {
            "role": "user",
            "content": "List all GitHub repositories.",
        },

        {
            "role": "assistant",
            "content": "Fetching repositories.",
        },

        {
            "role": "tool_result",
            "content": "Found 12 repositories.",
        },

        {
            "role": "assistant",
            "content": "Repositories successfully retrieved.",
        },

        {
            "role": "user",
            "content": "Show branches of enterprise-mcp-platform.",
        },

        {
            "role": "assistant",
            "content": "Fetching branches.",
        },

    ],

    "session": {

        "repository": "enterprise-mcp-platform",

        "branch": "main",

    },

    "long_term": [

        {
            "content": "Preferred cloud provider is AWS.",
        },

        {
            "content": "Working on Enterprise MCP Platform.",
        },

    ],

    "semantic": [

        {
            "content": "Enterprise MCP Platform uses FastAPI.",
        },

        {
            "content": "GitHub exposes list_branches.",
        },

    ],

}

print("\n=== Context Compression Test ===")

print("\nOriginal Context\n")

print(
    json.dumps(
        context,
        indent=2,
    )
)

compressed = ContextCompression.compress(
    context,
)

print("\nCompressed Context\n")

print(
    json.dumps(
        compressed,
        indent=2,
    )
)

print("\nStatistics\n")

print(
    json.dumps(
        ContextCompression.statistics(
            context,
            compressed,
        ),
        indent=2,
    )
)

print("\nEmpty Context\n")

empty = ContextCompression.compress({})

print(
    json.dumps(
        empty,
        indent=2,
    )
)

print("\nContext Compression Test Passed ✓")