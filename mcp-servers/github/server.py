from mcp.server.fastmcp import FastMCP

from service import GitHubService

mcp = FastMCP("GitHub MCP")

service = GitHubService()


@mcp.tool()
def list_repositories():
    """
    List all repositories.
    """
    return service.list_repositories()


@mcp.tool()
def repository_info(repository: str):
    """
    Get repository information.

    Example:
    Pooja160701/enterprise-mcp-platform
    """
    return service.repository_info(repository)


@mcp.tool()
def list_branches(repository: str):
    """
    List repository branches.
    """
    return service.list_branches(repository)


@mcp.tool()
def latest_commit(repository: str):
    """
    Get latest commit.
    """
    return service.latest_commit(repository)


@mcp.tool()
def list_issues(repository: str):
    """
    List open issues.
    """
    return service.list_issues(repository)


@mcp.tool()
def create_issue(
    repository: str,
    title: str,
    body: str = "",
):
    """
    Create a GitHub issue.
    """
    return service.create_issue(
        repository,
        title,
        body,
    )


@mcp.tool()
def close_issue(
    repository: str,
    issue_number: int,
):
    """
    Close an issue.
    """
    return service.close_issue(
        repository,
        issue_number,
    )


@mcp.tool()
def list_pull_requests(repository: str):
    """
    List pull requests.
    """
    return service.list_pull_requests(repository)


@mcp.tool()
def list_workflows(repository: str):
    """
    List GitHub Actions workflows.
    """
    return service.list_workflows(repository)


if __name__ == "__main__":

    print("=" * 60)
    print("Starting GitHub MCP Server...")
    print("Transport : stdio")
    print("Server    : GitHub MCP")
    print("=" * 60)

    mcp.run(transport="stdio")