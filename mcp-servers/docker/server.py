from mcp.server.fastmcp import FastMCP

from service import DockerService

mcp = FastMCP("Docker MCP")

service = DockerService()


@mcp.tool(
    description="List all running Docker containers."
)
def list_running_containers():
    return service.list_running_containers()


@mcp.tool(
    description="List every Docker container including stopped containers."
)
def list_all_containers():
    return service.list_all_containers()


@mcp.tool(
    description="List Docker images available on the host."
)
def list_images():
    return service.list_images()


@mcp.tool(
    description="Inspect a Docker container by name."
)
def inspect_container(name: str):
    return service.inspect_container(name)


@mcp.tool(
    description="Retrieve logs from a Docker container."
)
def container_logs(
    name: str,
    tail: int = 50,
):
    return service.container_logs(
        name=name,
        tail=tail,
    )


@mcp.tool(
    description="Start a stopped Docker container."
)
def start_container(name: str):
    return service.start_container(name)


@mcp.tool(
    description="Stop a running Docker container."
)
def stop_container(name: str):
    return service.stop_container(name)


if __name__ == "__main__":
    mcp.run()