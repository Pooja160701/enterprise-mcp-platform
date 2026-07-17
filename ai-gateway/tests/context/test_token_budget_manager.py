import json

from context.token_budget_manager import TokenBudgetManager


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

print("\n=== Token Budget Manager Test ===")

print("\nOriginal Statistics\n")

print(

    json.dumps(

        TokenBudgetManager.statistics(

            context,

        ),

        indent=2,

    )

)

print("\nApplying Token Budget (100 tokens)\n")

reduced = TokenBudgetManager.fit(

    context,

    max_tokens=100,

)

print(

    json.dumps(

        reduced,

        indent=2,

    )

)

print("\nReduced Statistics\n")

print(

    json.dumps(

        TokenBudgetManager.statistics(

            reduced,

        ),

        indent=2,

    )

)

print("\nEstimated Tokens")

print(

    TokenBudgetManager.estimate_tokens(

        reduced,

    )

)

print("\nEmpty Context")

empty = TokenBudgetManager.fit(

    {},

    max_tokens=100,

)

print(

    json.dumps(

        empty,

        indent=2,

    )

)

print("\nToken Budget Manager Test Passed")