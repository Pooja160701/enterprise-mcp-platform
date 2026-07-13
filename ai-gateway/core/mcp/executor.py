from core.mcp.manager import MCPManager


class MCPExecutor:

    def __init__(self):
        self.manager = MCPManager()

    async def execute(
        self,
        server: str,
        tool: str,
        arguments: dict,
    ):

        return await self.manager.execute_tool(
            tool,
            arguments,
            server,
        )