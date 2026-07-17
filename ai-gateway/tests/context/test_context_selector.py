import json

from context.context_selector import ContextSelector


context = {

    "conversation": [

        {
            "role": "user",
            "content": "List GitHub repositories.",
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

            "id": 1,

            "content": "Preferred cloud provider is AWS.",

            "importance": 95,

        },

        {

            "id": 2,

            "content": "Working on Enterprise MCP Platform.",

            "importance": 90,

        },

    ],

    "semantic": [

        {

            "id": 1,

            "content": "Enterprise MCP Platform uses FastAPI.",

            "importance": 90,

        },

        {

            "id": 2,

            "content": "GitHub exposes list_branches.",

            "importance": 80,

        },

    ],

}

print("\n=== Context Selector Test ===")

selected = ContextSelector.select(context)

print("\nSelected Context\n")

print(

    json.dumps(

        selected,

        indent=2,

    )

)

print("\nConversation\n")

print(

    json.dumps(

        selected["conversation"],

        indent=2,

    )

)

print("\nSession\n")

print(

    json.dumps(

        selected["session"],

        indent=2,

    )

)

print("\nLong-Term\n")

print(

    json.dumps(

        selected["long_term"],

        indent=2,

    )

)

print("\nSemantic\n")

print(

    json.dumps(

        selected["semantic"],

        indent=2,

    )

)

print("\nStatistics\n")

print(

    json.dumps(

        ContextSelector.statistics(

            selected,

        ),

        indent=2,

    )

)

print("\nEmpty Context\n")

empty = ContextSelector.select(

    {

        "conversation": [],

        "session": {},

        "long_term": [],

        "semantic": [],

    }

)

print(

    json.dumps(

        empty,

        indent=2,

    )

)

print("\nContext Selector Test Passed")