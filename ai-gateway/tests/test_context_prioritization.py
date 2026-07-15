import json

from context.context_prioritization import ContextPrioritization


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

    ],

    "session": {

        "repository": "enterprise-mcp-platform",

        "branch": "main",

    },

    "long_term": [

        {

            "content": "Preferred cloud provider is AWS.",

            "importance": 95,

        },

        {

            "content": "Working on Enterprise MCP Platform.",

            "importance": 90,

        },

        {

            "content": "Uses FastAPI.",

            "importance": 80,

        },

    ],

    "semantic": [

        {

            "content": "Enterprise MCP Platform uses FastAPI.",

            "importance": 90,

        },

        {

            "content": "GitHub exposes list_branches.",

            "importance": 80,

        },

        {

            "content": "AWS Lambda deployment.",

            "importance": 70,

        },

    ],

}

print("\n=== Context Prioritization Test ===")

prioritized = ContextPrioritization.prioritize(
    context
)

print("\nPrioritized Context\n")

print(
    json.dumps(
        prioritized,
        indent=2,
    )
)

print("\nLong-Term Priority\n")

print(
    json.dumps(
        prioritized["long_term"],
        indent=2,
    )
)

print("\nSemantic Priority\n")

print(
    json.dumps(
        prioritized["semantic"],
        indent=2,
    )
)

print("\nStatistics\n")

print(
    json.dumps(
        ContextPrioritization.statistics(
            prioritized,
        ),
        indent=2,
    )
)

print("\nEmpty Context\n")

empty = ContextPrioritization.prioritize(
    {}
)

print(
    json.dumps(
        empty,
        indent=2,
    )
)

print("\nContext Prioritization Test Passed ✓")