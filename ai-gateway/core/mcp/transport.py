import os

from mcp import StdioServerParameters


def create_stdio_params(server):

    return StdioServerParameters(
        command=server.command,
        args=server.args or [],
        env=os.environ.copy(),   
    )