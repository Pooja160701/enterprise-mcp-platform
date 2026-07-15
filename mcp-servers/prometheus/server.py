from mcp.server.fastmcp import FastMCP

from tools import (
    health,
    list_targets,
    list_alerts,
    list_rules,
    query,
    query_range,
)

mcp = FastMCP("Prometheus MCP")


@mcp.tool()
def health_tool():
    """
    Check Prometheus health.
    """
    return health()


@mcp.tool()
def list_targets_tool():
    """
    List all active Prometheus scrape targets.
    """
    return list_targets()


@mcp.tool()
def list_alerts_tool():
    """
    List active Prometheus alerts.
    """
    return list_alerts()


@mcp.tool()
def list_rules_tool():
    """
    List all Prometheus recording and alerting rules.
    """
    return list_rules()


@mcp.tool()
def query_tool(expression: str):
    """
    Execute an instant PromQL query.
    """
    return query(expression)


@mcp.tool()
def query_range_tool(
    expression: str,
    start: str,
    end: str,
    step: str = "60s",
):
    """
    Execute a PromQL range query.
    """
    return query_range(
        expression,
        start,
        end,
        step,
    )


if __name__ == "__main__":
    mcp.run()