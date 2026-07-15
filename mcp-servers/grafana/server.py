from mcp.server.fastmcp import FastMCP

from tools import (
    health,
    list_dashboards,
    list_datasources,
    dashboard_info,
    list_alerts,
)

mcp = FastMCP("Grafana MCP")


@mcp.tool()
def health_tool():
    """Check Grafana health."""
    return health()


@mcp.tool()
def list_dashboards_tool():
    """List Grafana dashboards."""
    return list_dashboards()


@mcp.tool()
def list_datasources_tool():
    """List Grafana datasources."""
    return list_datasources()


@mcp.tool()
def dashboard_info_tool(uid: str):
    """Get dashboard details."""
    return dashboard_info(uid)


@mcp.tool()
def list_alerts_tool():
    """List Grafana alert rules."""
    return list_alerts()


if __name__ == "__main__":
    mcp.run()