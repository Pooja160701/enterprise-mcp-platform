from fastapi import APIRouter

from core.mcp.registry import MCPRegistry
from core.mcp.manager import MCPManager

router = APIRouter(
    prefix="/servers",
    tags=["Servers"],
)


@router.get("")
async def list_servers():

    manager = MCPManager()

    servers = []

    for server in MCPRegistry.all():

        try:

            tools = await manager.list_tools(server.name)

            servers.append(
                {
                    "name": server.name,
                    "command": server.command,
                    "status": "connected",
                    "tool_count": len(tools),
                }
            )

        except Exception:

            servers.append(
                {
                    "name": server.name,
                    "command": server.command,
                    "status": "offline",
                    "tool_count": 0,
                }
            )

    return servers