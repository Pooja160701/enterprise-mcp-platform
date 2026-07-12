from contextlib import AsyncExitStack

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from core.mcp.config import FILESYSTEM_SERVER


class MCPManager:
    def __init__(self):
        self.session = None
        self.exit_stack = AsyncExitStack()

    async def connect(self):
        if self.session:
            return self.session

        server_params = StdioServerParameters(
            command=FILESYSTEM_SERVER.command,
            args=FILESYSTEM_SERVER.args,
        )

        read_stream, write_stream = await self.exit_stack.enter_async_context(
            stdio_client(server_params)
        )

        self.session = await self.exit_stack.enter_async_context(
            ClientSession(read_stream, write_stream)
        )

        await self.session.initialize()

        return self.session

    async def list_tools(self):
        session = await self.connect()

        result = await session.list_tools()

        return [
            {
                "name": tool.name,
                "description": tool.description,
            }
            for tool in result.tools
        ]

    async def execute_tool(self, tool_name: str, arguments: dict):
        session = await self.connect()

        result = await session.call_tool(
            tool_name,
            arguments=arguments,
        )

        return result
    
    async def close(self):
        await self.exit_stack.aclose()
        self.session = None