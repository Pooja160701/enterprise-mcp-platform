from fastapi import APIRouter
from pydantic import BaseModel

from core.mcp.manager import MCPManager

router = APIRouter(
    prefix="/mcp",
    tags=["MCP"],
)

manager = MCPManager()


class ToolRequest(BaseModel):
    tool: str
    arguments: dict


@router.get("/tools")
async def list_tools():
    return {
        "server": "filesystem",
        "tools": await manager.list_tools(),
    }


@router.post("/execute")
async def execute_tool(request: ToolRequest):
    result = await manager.execute_tool(
        request.tool,
        request.arguments,
    )

    return result