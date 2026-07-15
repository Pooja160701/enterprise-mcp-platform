import json

from context.prompt_context import PromptContext


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

user_query = "Show branches of enterprise-mcp-platform."

print("\n=== Prompt Context Test ===")

prompt_context = PromptContext.build(
    context=context,
    query=user_query,
)

prompt = PromptContext.render(
    prompt_context,
)

print("\nGenerated Prompt\n")

print(prompt)

print("\nPrompt Length")

print(len(prompt), "characters")

print("\nEstimated Tokens")

print(PromptContext.tokens(prompt))

print("\nPrompt Context Test Passed ✓")