from __future__ import annotations

import re
from pathlib import Path

try:
    import markdown
except ImportError:
    markdown = None

try:
    from bs4 import BeautifulSoup
except ImportError:
    BeautifulSoup = None


class MarkdownProcessor:
    """
    Production-ready Markdown utility.

    Responsibilities
    ----------------
    - Read Markdown files
    - Convert Markdown to HTML
    - Extract plain text
    - Parse headings
    - Provide document statistics

    Future extensions:
        - Table extraction
        - Link extraction
        - Image extraction
        - Front matter parsing
        - TOC generation
    """

    HEADING_PATTERN = re.compile(r"^(#{1,6})\s+(.+)$", re.MULTILINE)

    def __init__(self):

        self._statistics: dict[str, int] = {}

    # ---------------------------------------------------------
    # Reading
    # ---------------------------------------------------------

    def read(
        self,
        path: str | Path,
        encoding: str = "utf-8",
    ) -> str:

        path = Path(path)

        if not path.exists():
            raise FileNotFoundError(path)

        text = path.read_text(encoding=encoding)

        self._statistics["documents"] = (
            self._statistics.get("documents", 0) + 1
        )

        self._statistics["characters"] = (
            self._statistics.get("characters", 0)
            + len(text)
        )

        return text

    # ---------------------------------------------------------
    # HTML Conversion
    # ---------------------------------------------------------

    def to_html(
        self,
        markdown_text: str,
    ) -> str:

        if markdown is None:
            raise ImportError(
                "markdown package is required."
            )

        return markdown.markdown(
            markdown_text,
            extensions=[
                "tables",
                "fenced_code",
                "toc",
            ],
        )

    # ---------------------------------------------------------
    # Plain Text
    # ---------------------------------------------------------

    def to_text(
        self,
        markdown_text: str,
    ) -> str:

        html = self.to_html(markdown_text)

        if BeautifulSoup is None:
            raise ImportError(
                "beautifulsoup4 package is required."
            )

        soup = BeautifulSoup(
            html,
            "html.parser",
        )

        return soup.get_text(
            separator="\n",
            strip=True,
        )

    # ---------------------------------------------------------
    # Headings
    # ---------------------------------------------------------

    def headings(
        self,
        markdown_text: str,
    ) -> list[dict]:

        headings = []

        for match in self.HEADING_PATTERN.finditer(
            markdown_text
        ):
            headings.append(
                {
                    "level": len(match.group(1)),
                    "title": match.group(2).strip(),
                }
            )

        return headings

    # ---------------------------------------------------------
    # Statistics
    # ---------------------------------------------------------

    def statistics(
        self,
        markdown_text: str,
    ) -> dict:

        headings = self.headings(markdown_text)

        return {
            "characters": len(markdown_text),
            "lines": len(markdown_text.splitlines()),
            "words": len(markdown_text.split()),
            "headings": len(headings),
        }

    # ---------------------------------------------------------
    # Runtime Statistics
    # ---------------------------------------------------------

    def runtime_statistics(self):

        return dict(self._statistics)

    def clear_statistics(self):

        self._statistics.clear()

    def reset(self):

        self.clear_statistics()

    # ---------------------------------------------------------
    # Configuration
    # ---------------------------------------------------------

    def configuration(self):

        return {
            "backend": "markdown",
            "html_enabled": markdown is not None,
            "text_enabled": BeautifulSoup is not None,
        }

    # ---------------------------------------------------------
    # Dunder
    # ---------------------------------------------------------

    def __len__(self):

        return 3

    def __iter__(self):

        yield from self.configuration().items()