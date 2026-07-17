from __future__ import annotations

from pathlib import Path

import pytest

from app.rag.document_loader import DocumentLoader
from app.rag.models import DocumentType


# ---------------------------------------------------------
# Fixtures
# ---------------------------------------------------------


@pytest.fixture
def loader():
    return DocumentLoader()


@pytest.fixture
def text_file(tmp_path):
    file = tmp_path / "sample.txt"
    file.write_text(
        "Hello\nWorld\n",
        encoding="utf-8",
    )
    return file


@pytest.fixture
def markdown_file(tmp_path):
    file = tmp_path / "notes.md"
    file.write_text(
        "# Heading\n\nSome content",
        encoding="utf-8",
    )
    return file


@pytest.fixture
def html_file(tmp_path):
    file = tmp_path / "page.html"
    file.write_text(
        "<html><body>Hello</body></html>",
        encoding="utf-8",
    )
    return file


@pytest.fixture
def unknown_file(tmp_path):
    file = tmp_path / "data.xyz"
    file.write_text(
        "Unsupported",
        encoding="utf-8",
    )
    return file


# ---------------------------------------------------------
# Type Detection
# ---------------------------------------------------------


@pytest.mark.parametrize(
    ("filename", "expected"),
    [
        ("a.txt", DocumentType.TEXT),
        ("a.md", DocumentType.MARKDOWN),
        ("a.markdown", DocumentType.MARKDOWN),
        ("a.html", DocumentType.HTML),
        ("a.htm", DocumentType.HTML),
        ("a.pdf", DocumentType.PDF),
        ("a.docx", DocumentType.UNKNOWN),
        ("a.xyz", DocumentType.UNKNOWN),
    ],
)
def test_detect_type(loader, filename, expected):
    assert loader.detect_type(filename) == expected


# ---------------------------------------------------------
# TXT Loading
# ---------------------------------------------------------


def test_load_text(loader, text_file):
    document = loader.load(text_file)

    assert document.filename == "sample.txt"
    assert document.document_type == DocumentType.TEXT
    assert document.content == "Hello\nWorld"
    assert document.metadata["size"] > 0


# ---------------------------------------------------------
# Markdown Loading
# ---------------------------------------------------------


def test_load_markdown(loader, markdown_file):
    document = loader.load(markdown_file)

    assert document.document_type == DocumentType.MARKDOWN
    assert "# Heading" in document.content


# ---------------------------------------------------------
# HTML Loading
# ---------------------------------------------------------


def test_load_html(loader, html_file):
    document = loader.load(html_file)

    assert document.document_type == DocumentType.HTML
    assert "<html>" in document.content


# ---------------------------------------------------------
# Unsupported
# ---------------------------------------------------------


def test_load_unknown_extension(loader, unknown_file):
    with pytest.raises(ValueError):
        loader.load(unknown_file)


def test_missing_file(loader, tmp_path):
    missing = tmp_path / "missing.txt"

    with pytest.raises(FileNotFoundError):
        loader.load(missing)


# ---------------------------------------------------------
# Helpers
# ---------------------------------------------------------


def test_normalize(loader):
    text = "Hello  \r\nWorld   \r\n"

    normalized = loader._normalize(text)

    assert normalized == "Hello\nWorld"


def test_normalize_empty(loader):
    assert loader._normalize("") == ""


def test_load_text_direct(loader, text_file):
    content = loader._load_text(text_file)

    assert "Hello" in content


def test_load_html_direct(loader, html_file):
    content = loader._load_html(html_file)

    assert "<body>" in content


# ---------------------------------------------------------
# PDF
# ---------------------------------------------------------


def test_pdf_without_library(loader, monkeypatch, tmp_path):
    pdf = tmp_path / "sample.pdf"
    pdf.write_bytes(b"%PDF-1.4")

    monkeypatch.setattr(
        "app.rag.document_loader.pypdf",
        None,
    )

    with pytest.raises(ImportError):
        loader._load_pdf(pdf)


@pytest.mark.skipif(
    pytest.importorskip("pypdf", reason="pypdf not installed") is None,
    reason="pypdf unavailable",
)
def test_pdf_type_detection(loader):
    assert loader.detect_type("sample.pdf") == DocumentType.PDF


# ---------------------------------------------------------
# Statistics
# ---------------------------------------------------------


def test_statistics(loader, text_file):
    loader.load(text_file)

    stats = loader.statistics()

    assert stats["documents"] == 1


def test_clear_statistics(loader, text_file):
    loader.load(text_file)

    loader.clear_statistics()

    assert loader.statistics() == {}


def test_reset(loader, text_file):
    loader.load(text_file)

    loader.reset()

    assert loader.statistics() == {}


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------


def test_configuration(loader):
    config = loader.configuration()

    assert ".txt" in config["supported_extensions"]
    assert ".pdf" in config["supported_extensions"]
    assert "pdf_enabled" in config


# ---------------------------------------------------------
# Dunder Methods
# ---------------------------------------------------------


def test_len(loader):
    assert len(loader) == len(loader.SUPPORTED_EXTENSIONS)


def test_iter(loader):
    config = dict(loader)

    assert "supported_extensions" in config
    assert "pdf_enabled" in config


# ---------------------------------------------------------
# Unicode
# ---------------------------------------------------------


def test_unicode_loading(loader, tmp_path):
    file = tmp_path / "unicode.txt"

    file.write_text(
        "தமிழ் 日本語 😀",
        encoding="utf-8",
    )

    document = loader.load(file)

    assert "தமிழ்" in document.content
    assert "日本語" in document.content
    assert "😀" in document.content


# ---------------------------------------------------------
# Large File
# ---------------------------------------------------------


def test_large_file(loader, tmp_path):
    file = tmp_path / "large.txt"

    text = "hello\n" * 10000

    file.write_text(
        text,
        encoding="utf-8",
    )

    document = loader.load(file)

    assert len(document.content) > 10000


# ---------------------------------------------------------
# Metadata
# ---------------------------------------------------------


def test_metadata(loader, text_file):
    document = loader.load(text_file)

    assert Path(document.metadata["path"]).exists()
    assert document.metadata["size"] > 0


# ---------------------------------------------------------
# Case Insensitive Extension
# ---------------------------------------------------------


def test_uppercase_extension(loader, tmp_path):
    file = tmp_path / "README.TXT"

    file.write_text(
        "Hello",
        encoding="utf-8",
    )

    document = loader.load(file)

    assert document.document_type == DocumentType.TEXT