from __future__ import annotations

from .models import (
    Document,
    DocumentChunk,
    ChunkMetadata,
)


class Chunker:
    """
    Production-ready text chunker.

    Supports:
    - Fixed-size chunking
    - Character overlap
    - Recursive splitting (paragraph/sentence fallback)
    - Metadata preservation
    """

    def __init__(
        self,
        chunk_size: int = 500,
        chunk_overlap: int = 50,
    ):

        if chunk_size <= 0:
            raise ValueError("chunk_size must be > 0")

        if chunk_overlap < 0:
            raise ValueError("chunk_overlap cannot be negative")

        if chunk_overlap >= chunk_size:
            raise ValueError(
                "chunk_overlap must be smaller than chunk_size"
            )

        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

        self._statistics: dict[str, int] = {}

    # ---------------------------------------------------------
    # Public API
    # ---------------------------------------------------------

    def chunk(
        self,
        document: Document,
    ) -> list[DocumentChunk]:

        if not document.content.strip():
            return []

        chunks = self._recursive_split(document.content)

        results: list[DocumentChunk] = []

        cursor = 0

        for index, text in enumerate(chunks):

            start = cursor
            end = start + len(text)

            metadata = ChunkMetadata(
                document_id=document.id,
                filename=document.filename,
                document_type=document.document_type,
                chunk_index=index,
                start_char=start,
                end_char=end,
            )

            results.append(
                DocumentChunk(
                    id=f"{document.id}_{index}",
                    document_id=document.id,
                    text=text,
                    metadata=metadata,
                )
            )

            cursor = max(
                end - self.chunk_overlap,
                end,
            )

        self._statistics["documents"] = (
            self._statistics.get("documents", 0) + 1
        )

        self._statistics["chunks"] = (
            self._statistics.get("chunks", 0)
            + len(results)
        )

        return results

    # ---------------------------------------------------------
    # Recursive Splitter
    # ---------------------------------------------------------

    def _recursive_split(
        self,
        text: str,
    ) -> list[str]:

        if len(text) <= self.chunk_size:
            return [text.strip()]

        separators = [
            "\n\n",
            "\n",
            ". ",
            " ",
        ]

        pieces = [text]

        for separator in separators:

            new_pieces = []

            for piece in pieces:

                if len(piece) <= self.chunk_size:

                    new_pieces.append(piece)

                    continue

                split = piece.split(separator)

                buffer = ""

                for item in split:

                    candidate = (
                        item
                        if not buffer
                        else buffer + separator + item
                    )

                    if len(candidate) <= self.chunk_size:

                        buffer = candidate

                    else:

                        if buffer:
                            new_pieces.append(buffer.strip())

                        buffer = item

                if buffer:
                    new_pieces.append(buffer.strip())

            pieces = new_pieces

        final_chunks = []

        for piece in pieces:

            if len(piece) <= self.chunk_size:

                final_chunks.append(piece)

                continue

            start = 0

            while start < len(piece):

                end = start + self.chunk_size

                final_chunks.append(piece[start:end])

                start = end - self.chunk_overlap

        return [c.strip() for c in final_chunks if c.strip()]

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
            "chunk_size": self.chunk_size,
            "chunk_overlap": self.chunk_overlap,
            "algorithm": "recursive",
        }

    # ---------------------------------------------------------
    # Dunder
    # ---------------------------------------------------------

    def __len__(self):

        return 3

    def __iter__(self):

        yield from self.configuration().items()