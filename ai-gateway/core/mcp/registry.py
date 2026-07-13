from core.mcp.config import MCP_SERVERS


class MCPRegistry:

    @staticmethod
    def get(name: str):
        return MCP_SERVERS.get(name)

    @staticmethod
    def all():
        return list(MCP_SERVERS.values())

    @staticmethod
    def names():
        return list(MCP_SERVERS.keys())