from mcp import ClientSession
from mcp.client.stdio import stdio_client

from core.mcp.transport import create_stdio_params


class MCPSession:

    def __init__(self, server):
        self.server = server

    async def list_tools(self):

        params = create_stdio_params(self.server)

        async with stdio_client(params) as (
            read_stream,
            write_stream,
        ):

            async with ClientSession(
                read_stream,
                write_stream,
            ) as session:

                await session.initialize()

                result = await session.list_tools()

                return result.tools

    async def call_tool(
        self,
        tool_name: str,
        arguments: dict,
    ):

        params = create_stdio_params(self.server)

        async with stdio_client(params) as (
            read_stream,
            write_stream,
        ):

            async with ClientSession(
                read_stream,
                write_stream,
            ) as session:

                await session.initialize()

                return await session.call_tool(
                    tool_name,
                    arguments,
                )