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

Your task is to choose exactly ONE tool to satisfy the user's request.

User Request:

{message}

----------------------------------------------------
Available Tools
----------------------------------------------------

{''.join(tool_descriptions)}

----------------------------------------------------
Rules
----------------------------------------------------

1. Select exactly ONE server.

2. Select exactly ONE tool.

3. Return ONLY valid JSON.

4. Do not explain your reasoning.

5. Do not use markdown.

6. If no arguments are required, return an empty object.

----------------------------------------------------
Example
----------------------------------------------------

{{
  "server": "filesystem",
  "tool": "list_directory",
  "arguments": {{
    "path": "/app/docs"
  }}
}}

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