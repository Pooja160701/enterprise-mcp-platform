from core.mcp.registry import MCPRegistry
from core.mcp.session import MCPSession


class MCPManager:

    def __init__(self):
        self.registry = MCPRegistry()

    async def list_tools(
        self,
        server_name: str = "filesystem",
    ):

        server = self.registry.get(server_name)

        if server is None:
            raise ValueError(f"Unknown server: {server_name}")

        session = MCPSession(server)

        return await session.list_tools()

    async def execute_tool(
        self,
        tool_name: str,
        arguments: dict,
        server_name: str = "filesystem",
    ):

        server = self.registry.get(server_name)

        if server is None:
            raise ValueError(f"Unknown server: {server_name}")

        session = MCPSession(server)

        return await session.call_tool(
            tool_name,
            arguments,
        )