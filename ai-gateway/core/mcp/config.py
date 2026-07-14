from dataclasses import dataclass
from typing import Optional


@dataclass
class MCPServerConfig:
    name: str
    type: str  # external | python
    command: Optional[str] = None
    args: Optional[list[str]] = None


MCP_SERVERS = {

    "filesystem": MCPServerConfig(
        name="filesystem",
        type="external",
        command="npx",
        args=[
            "-y",
            "@modelcontextprotocol/server-filesystem",
            "/app",
        ],
    ),

    "docker": MCPServerConfig(
        name="docker",
        type="external",
        command="python",
        args=[
            "/mcp-servers/docker/server.py",
        ],
    ),

    "github": MCPServerConfig(
        name="github",
        type="external",
        command="python",
        args=[
            "/mcp-servers/github/server.py",
        ],
    ),

    "kubernetes": MCPServerConfig(
        name="kubernetes",
        type="external",
        command="python",
        args=[
            "/mcp-servers/kubernetes/server.py",
        ],
    ),

    "postgres": MCPServerConfig(
        name="postgres",
        type="external",
        command="python",
        args=[
            "/mcp-servers/postgres/server.py",
        ],
    ),

    "prometheus": MCPServerConfig(
        name="prometheus",
        type="external",
        command="python",
        args=[
            "/mcp-servers/prometheus/server.py",
        ],
    ),

    "grafana": MCPServerConfig(
        name="grafana",
        type="external",
        command="python",
        args=[
            "/mcp-servers/grafana/server.py",
        ],
    ),

    "aws": MCPServerConfig(
        name="aws",
        type="external",
        command="python",
        args=[
            "/mcp-servers/aws/server.py",
        ],
    ),
}