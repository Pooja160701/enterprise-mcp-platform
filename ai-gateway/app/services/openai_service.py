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

        prompt = f"""
You are an AI agent.

User request:

{message}

Available MCP tools:

{tools}

Respond ONLY as JSON.

Example:

{{
 "tool":"list_directory",
 "arguments": {{
      "path":"/app/docs"
 }}
}}

Return valid JSON only.
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
    You are an AI assistant.

    User asked:

    {user_message}

    Tool Used:

    {tool_name}

    Tool Output:

    {tool_result}

    Answer naturally.

    Do not mention JSON.

    Do not mention MCP.

    Answer as if you performed the task yourself.
    """

        response = await self.client.responses.create(
            model=self.model,
            input=prompt,
        )

        return response.output_text    