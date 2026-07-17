from __future__ import annotations

from pathlib import Path

try:
    import pypdf
except ImportError:
    pypdf = None

from .models import (
    Document,
    DocumentType,
)


class DocumentLoader:
    """
    Production-ready document loader.

    Supports:
    - TXT
    - Markdown
    - HTML
    - PDF

    Easily extensible for DOCX, CSV, etc.
    """

    SUPPORTED_EXTENSIONS = {
        ".txt": DocumentType.TEXT,
        ".md": DocumentType.MARKDOWN,
        ".markdown": DocumentType.MARKDOWN,
        ".html": DocumentType.HTML,
        ".htm": DocumentType.HTML,
        ".pdf": DocumentType.PDF,
    }

    def __init__(self):

        self._statistics: dict[str, int] = {}

    # ---------------------------------------------------------
    # Public API
    # ---------------------------------------------------------

    def load(
        self,
        path: str | Path,
    ) -> Document:

        path = Path(path)

        if not path.exists():
            raise FileNotFoundError(path)

        document_type = self.detect_type(path)

        if document_type == DocumentType.TEXT:
            content = self._load_text(path)

        elif document_type == DocumentType.MARKDOWN:
            content = self._load_text(path)

        elif document_type == DocumentType.HTML:
            content = self._load_html(path)

        elif document_type == DocumentType.PDF:
            content = self._load_pdf(path)

        else:
            raise ValueError(
                f"Unsupported document type: {path.suffix}"
            )

        content = self._normalize(content)

        self._statistics["documents"] = (
            self._statistics.get("documents", 0) + 1
        )

        return Document(
            id=path.stem,
            filename=path.name,
            content=content,
            document_type=document_type,
            metadata={
                "path": str(path.resolve()),
                "size": path.stat().st_size,
            },
        )

    # ---------------------------------------------------------
    # Type Detection
    # ---------------------------------------------------------

    def detect_type(
        self,
        path: str | Path,
    ) -> DocumentType:

        suffix = Path(path).suffix.lower()

        return self.SUPPORTED_EXTENSIONS.get(
            suffix,
            DocumentType.UNKNOWN,
        )

    # ---------------------------------------------------------
    # Loaders
    # ---------------------------------------------------------

    def _load_text(
        self,
        path: Path,
    ) -> str:

        return path.read_text(
            encoding="utf-8",
            errors="ignore",
        )

    def _load_html(
        self,
        path: Path,
    ) -> str:

        return path.read_text(
            encoding="utf-8",
            errors="ignore",
        )

    def _load_pdf(
        self,
        path: Path,
    ) -> str:

        if pypdf is None:
            raise ImportError(
                "pypdf is required for PDF support."
            )

        reader = pypdf.PdfReader(str(path))

        pages = []

        for page in reader.pages:

            text = page.extract_text()

            if text:
                pages.append(text)

        return "\n".join(pages)

    # ---------------------------------------------------------
    # Helpers
    # ---------------------------------------------------------

    def _normalize(
        self,
        text: str,
    ) -> str:

        return "\n".join(
            line.rstrip()
            for line in text.replace("\r\n", "\n").splitlines()
        ).strip()

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
            "supported_extensions": sorted(
                self.SUPPORTED_EXTENSIONS.keys()
            ),
            "pdf_enabled": pypdf is not None,
        }

    # ---------------------------------------------------------
    # Dunder
    # ---------------------------------------------------------

    def __len__(self):

        return len(self.SUPPORTED_EXTENSIONS)

    def __iter__(self):

        yield from self.configuration().items()