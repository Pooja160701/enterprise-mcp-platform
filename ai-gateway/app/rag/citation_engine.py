from __future__ import annotations

from .models import (
    Citation,
    CitationResult,
    RetrievalResult,
)


class CitationEngine:
    """
    Production-ready citation engine.

    Responsibilities:
        - Generate citations from retrieval results
        - Deduplicate citations
        - Preserve source metadata
        - Format citations

    Future extensions:
        - APA / MLA / IEEE formatting
        - URL citations
        - Footnotes
        - Markdown references
        - HTML references
    """

    def __init__(self):

        self._statistics: dict[str, int] = {}

    # ---------------------------------------------------------
    # Public API
    # ---------------------------------------------------------

    def generate(
        self,
        results: list[RetrievalResult],
    ) -> CitationResult:

        citations: list[Citation] = []
        seen: set[tuple[str, str]] = set()

        index = 1

        for result in results:

            chunk = result.chunk
            metadata = chunk.metadata

            key = (
                chunk.document_id,
                chunk.id,
            )

            if key in seen:
                continue

            seen.add(key)

            citations.append(
                Citation(
                    index=index,
                    document_id=chunk.document_id,
                    filename=metadata.filename,
                    chunk_id=chunk.id,
                    page=metadata.page,
                    source=metadata.source,
                    score=result.score,
                )
            )

            index += 1

        self._statistics["generated"] = (
            self._statistics.get("generated", 0)
            + len(citations)
        )

        self._statistics["requests"] = (
            self._statistics.get("requests", 0)
            + 1
        )

        return CitationResult(
            citations=citations
        )

    # ---------------------------------------------------------
    # Formatting
    # ---------------------------------------------------------

    def format(
        self,
        citation: Citation,
    ) -> str:

        parts = [
            f"[{citation.index}]",
            citation.filename,
        ]

        if citation.page is not None:
            parts.append(f"Page {citation.page}")

        if citation.source:
            parts.append(citation.source)

        return " | ".join(parts)

    def format_all(
        self,
        result: CitationResult,
    ) -> list[str]:

        return [
            self.format(citation)
            for citation in result.citations
        ]

    # ---------------------------------------------------------
    # Statistics
    # ---------------------------------------------------------

    def statistics(self) -> dict:

        return dict(self._statistics)

    def clear_statistics(self):

        self._statistics.clear()

    def reset(self):

        self.clear_statistics()

    # ---------------------------------------------------------
    # Configuration
    # ---------------------------------------------------------

    def configuration(self) -> dict:

        return {
            "deduplicate": True,
            "format": "default",
        }

    # ---------------------------------------------------------
    # Dunder
    # ---------------------------------------------------------

    def __len__(self):

        return 2

    def __iter__(self):

        yield from self.configuration().items()