from __future__ import annotations

from pathlib import Path

try:
    import pypdf
except ImportError:
    pypdf = None


class PDFReader:
    """
    Production-ready PDF utility.

    Responsibilities
    ----------------
    - Read PDF files
    - Extract page text
    - Extract full document text
    - Provide document metadata

    Future extensions:
        - OCR (Tesseract)
        - Table extraction
        - Image extraction
        - Layout parsing
    """

    def __init__(self):

        self._statistics: dict[str, int] = {}

    # ---------------------------------------------------------
    # Public API
    # ---------------------------------------------------------

    def read(
        self,
        path: str | Path,
    ) -> str:

        pages = self.read_pages(path)

        return "\n".join(pages)

    def read_pages(
        self,
        path: str | Path,
    ) -> list[str]:

        if pypdf is None:
            raise ImportError(
                "pypdf is required for PDF support."
            )

        path = Path(path)

        if not path.exists():
            raise FileNotFoundError(path)

        reader = pypdf.PdfReader(str(path))

        pages: list[str] = []

        for page in reader.pages:

            text = page.extract_text() or ""

            pages.append(text.strip())

        self._statistics["documents"] = (
            self._statistics.get("documents", 0)
            + 1
        )

        self._statistics["pages"] = (
            self._statistics.get("pages", 0)
            + len(pages)
        )

        return pages

    # ---------------------------------------------------------
    # Metadata
    # ---------------------------------------------------------

    def metadata(
        self,
        path: str | Path,
    ) -> dict:

        if pypdf is None:
            raise ImportError(
                "pypdf is required for PDF support."
            )

        path = Path(path)

        if not path.exists():
            raise FileNotFoundError(path)

        reader = pypdf.PdfReader(str(path))

        meta = reader.metadata or {}

        return {
            "title": getattr(meta, "title", None),
            "author": getattr(meta, "author", None),
            "subject": getattr(meta, "subject", None),
            "creator": getattr(meta, "creator", None),
            "producer": getattr(meta, "producer", None),
            "pages": len(reader.pages),
            "encrypted": reader.is_encrypted,
        }

    # ---------------------------------------------------------
    # Utility
    # ---------------------------------------------------------

    def page_count(
        self,
        path: str | Path,
    ) -> int:

        if pypdf is None:
            raise ImportError(
                "pypdf is required for PDF support."
            )

        path = Path(path)

        if not path.exists():
            raise FileNotFoundError(path)

        reader = pypdf.PdfReader(str(path))

        return len(reader.pages)

    # ---------------------------------------------------------
    # Statistics
    # ---------------------------------------------------------

    def statistics(self):

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
            "backend": "pypdf",
            "pdf_enabled": pypdf is not None,
        }

    # ---------------------------------------------------------
    # Dunder
    # ---------------------------------------------------------

    def __len__(self):

        return 2

    def __iter__(self):

        yield from self.configuration().items()