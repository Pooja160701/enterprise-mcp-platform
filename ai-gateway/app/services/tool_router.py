from core.mcp.manager import MCPManager


class ToolRouter:

    def __init__(self):
        self.manager = MCPManager()

    async def execute(self, tool_name: str, arguments: dict):
        return await self.manager.execute_tool(
            tool_name,
            arguments,
        )