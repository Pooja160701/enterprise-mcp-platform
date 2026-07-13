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
    Name: {tool["name"]}

    Description:
    {tool.get("description", "No description")}

    """
            )

        prompt = f"""
    You are an Enterprise AI Agent.

    Your task is to select exactly ONE MCP tool.

    User Request:

    {message}


    Available Tools

    {''.join(tool_descriptions)}


    Rules

    1. Choose exactly ONE tool.

    2. Use:

    - list_directory
    -> when the user wants to list folder contents.

    - read_text_file
    -> when the user wants to open or read a file.

    - directory_tree
    -> when the user asks for folder hierarchy.

    - search_files
    -> when searching for filenames.

    - create_directory
    -> when creating folders.

    - write_file
    -> when creating new files.

    - edit_file
    -> when modifying existing files.

    - list_allowed_directories
    -> ONLY when the user explicitly asks
        which directories are accessible.

    Return ONLY valid JSON.

    Example

    {
        "server":"filesystem",
        "tool":"list_directory",
        "arguments":{
            "path":"/app/docs"
        }
    }

    Do not explain.

    Do not use markdown.

    Choose BOTH

    1. The` correct MCP server.

    2. The tool.

    Return valid` JSON only.
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

    The user asked:

    {user_message}


    The following tool was executed:

    {tool_name}


    Tool Result

    {tool_result}


    Instructions

    - Answer naturally.
    - Do not mention MCP.
    - Do not mention JSON.
    - Do not mention internal tools.
    - Speak directly to the user.
    - If the result contains filenames,
    present them as a clean list.
    - If the result is empty,
    explain that nothing was found.
    - Be concise but helpful.
    """

        response = await self.client.responses.create(
            model=self.model,
            input=prompt,
        )

        return response.output_text