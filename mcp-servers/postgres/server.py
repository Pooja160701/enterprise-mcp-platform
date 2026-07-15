from mcp.server.fastmcp import FastMCP

from tools import (
    list_databases,
    list_tables,
    describe_table,
    table_row_count,
    database_size,
    run_select_query,
)

mcp = FastMCP("PostgreSQL MCP")


@mcp.tool()
def list_databases_tool():
    """
    List PostgreSQL databases.
    """
    return list_databases()


@mcp.tool()
def list_tables_tool(schema: str = "public"):
    """
    List tables in a schema.
    """
    return list_tables(schema)


@mcp.tool()
def describe_table_tool(table: str):
    """
    Describe table columns.
    """
    return describe_table(table)


@mcp.tool()
def table_row_count_tool(table: str):
    """
    Count rows in a table.
    """
    return table_row_count(table)


@mcp.tool()
def database_size_tool():
    """
    Show current database size.
    """
    return database_size()


@mcp.tool()
def run_select_query_tool(sql: str):
    """
    Execute a SELECT query.
    """
    return run_select_query(sql)


if __name__ == "__main__":
    mcp.run()