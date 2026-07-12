from fastapi import APIRouter

router = APIRouter(prefix="/mcp", tags=["MCP"])


@router.get("/status")
async def status():
    return {
        "connected": False,
        "servers": [],
    }