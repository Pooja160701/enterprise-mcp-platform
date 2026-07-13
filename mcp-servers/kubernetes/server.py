from mcp.server.fastmcp import FastMCP

from service import KubernetesService

mcp = FastMCP("Kubernetes MCP")

service = KubernetesService()


@mcp.tool()
def list_nodes():
    """
    List all Kubernetes nodes.
    """
    return service.list_nodes()


@mcp.tool()
def list_namespaces():
    """
    List all Kubernetes namespaces.
    """
    return service.list_namespaces()


@mcp.tool()
def list_pods(namespace: str = "default"):
    """
    List pods in a namespace.
    """
    return service.list_pods(namespace)


@mcp.tool()
def list_deployments(namespace: str = "default"):
    """
    List deployments.
    """
    return service.list_deployments(namespace)


@mcp.tool()
def list_services(namespace: str = "default"):
    """
    List services.
    """
    return service.list_services(namespace)


if __name__ == "__main__":

    print("=" * 60)
    print("Starting Kubernetes MCP Server...")
    print("Transport : stdio")
    print("Server    : Kubernetes MCP")
    print("=" * 60)

    mcp.run(transport="stdio")