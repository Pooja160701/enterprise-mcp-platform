from openai import AsyncOpenAI

from app.core.config import settings


class OpenAIService:

    def __init__(self):
        self.client = AsyncOpenAI(
            api_key=settings.OPENAI_API_KEY
        )

        self.model = settings.OPENAI_MODEL

    async def choose_tool(
        self,
        message: str,
        tools: list,
    ):

        tool_descriptions = []

        for tool in tools:

            tool_descriptions.append(
                f"""
Server: {tool["server"]}

Tool: {tool["name"]}

Description:
{tool.get("description", "No description")}
"""
            )

        prompt = f"""
You are an Enterprise AI Agent.

Your task is to choose one or more tools to satisfy the user's request.

User Request:

{message}

----------------------------------------------------
Available Tools
----------------------------------------------------

{''.join(tool_descriptions)}

----------------------------------------------------
Rules
----------------------------------------------------

1. Select one or more servers.

2. Select one or more tools.

3. If one tool is enough, return a JSON object.

4. If multiple tools are needed, return a JSON array.

5. Return ONLY valid JSON.

6. Do not explain your reasoning.

7. Do not use markdown.

8. If no arguments are required, return an empty object.

----------------------------------------------------
Example
----------------------------------------------------

    [
        {{
            "server":"github",
            "tool":"repository_info",
            "arguments":{{
                "repository":"Pooja160701/enterprise-mcp-platform"
            }}
        }},
        {{
            "server":"docker",
            "tool":"list_running_containers",
            "arguments":{{}}
        }}
    ]

----------------------------------------------------
Response
----------------------------------------------------

Return ONLY the JSON object.
"""

        response = await self.client.responses.create(
            model=self.model,
            input=prompt,
        )

        return response.output_text

    async def summarize_result(
        self,
        user_message: str,
        tool_name: str,
        tool_result: str,
    ):

        prompt = f"""
You are an intelligent infrastructure assistant.

User Request:

{user_message}

Executed Tool:

{tool_name}

Tool Output:

{tool_result}

Instructions:

- Answer naturally.
- Do not mention MCP.
- Do not mention JSON.
- Do not mention internal tools.
- Speak directly to the user.
- If the output contains filenames, format them as a readable list.
- If the output is empty, clearly state that nothing was found.
- Keep the answer concise and professional.
"""

        response = await self.client.responses.create(
            model=self.model,
            input=prompt,
        )

        return response.output_text