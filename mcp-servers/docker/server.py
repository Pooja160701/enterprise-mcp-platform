from mcp.server.fastmcp import FastMCP

from service import DockerService

mcp = FastMCP("Docker MCP")

service = DockerService()


@mcp.tool()
def list_running_containers():
    """
    List all running Docker containers.
    """
    return service.list_running_containers()


@mcp.tool()
def list_images():
    """
    List all Docker images.
    """
    return service.list_images()

@mcp.tool()
def inspect_container(name: str):
    """
    Inspect one container.
    """
    return service.inspect_container(name)


@mcp.tool()
def container_logs(
    name: str,
    tail: int = 50,
):
    """
    Show logs.
    """
    return service.container_logs(name, tail)


@mcp.tool()
def start_container(name: str):
    """
    Start container.
    """
    return service.start_container(name)


@mcp.tool()
def stop_container(name: str):
    """
    Stop container.
    """
    return service.stop_container(name)

if __name__ == "__main__":
    print("=" * 60)
    print("Starting Docker MCP Server...")
    print("Transport : stdio")
    print("Server    : Docker MCP")
    print("=" * 60)

    mcp.run(transport="stdio")