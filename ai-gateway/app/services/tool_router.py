from core.mcp.executor import MCPExecutor


class ToolRouter:

    def __init__(self):
        self.executor = MCPExecutor()

    async def execute(
        self,
        tool: str,
        arguments: dict,
        server: str,
    ):
        return await self.executor.execute(
            server=server,
            tool=tool,
            arguments=arguments,
        )