from dataclasses import dataclass
from pathlib import Path
import os


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DOCS_PATH = PROJECT_ROOT / "docs"

@dataclass
class MCPServer:
    name: str
    command: str
    args: list[str]

OPENAI_API_KEY: str = ""
OPENAI_MODEL: str = "gpt-5"

FILESYSTEM_SERVER = MCPServer(
    name="filesystem",
    command="npx",
    args=[
        "-y",
        "@modelcontextprotocol/server-filesystem",
        str(DOCS_PATH),
    ],
)