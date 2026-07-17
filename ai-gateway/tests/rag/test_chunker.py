from __future__ import annotations

import pytest

from app.rag.chunker import Chunker
from app.rag.models import (
    Document,
    DocumentType,
)


# ---------------------------------------------------------
# Fixtures
# ---------------------------------------------------------


@pytest.fixture
def document():
    return Document(
        id="doc1",
        filename="sample.txt",
        content="This is a sample document for testing the chunker.",
        document_type=DocumentType.TEXT,
    )


@pytest.fixture
def large_document():
    text = " ".join(["word"] * 1000)

    return Document(
        id="large",
        filename="large.txt",
        content=text,
        document_type=DocumentType.TEXT,
    )


@pytest.fixture
def chunker():
    return Chunker(
        chunk_size=100,
        chunk_overlap=20,
    )


# ---------------------------------------------------------
# Initialization
# ---------------------------------------------------------


def test_default_initialization():
    c = Chunker()

    assert c.chunk_size == 500
    assert c.chunk_overlap == 50


def test_custom_initialization():
    c = Chunker(
        chunk_size=256,
        chunk_overlap=32,
    )

    assert c.chunk_size == 256
    assert c.chunk_overlap == 32


@pytest.mark.parametrize(
    ("size", "overlap"),
    [
        (0, 10),
        (-1, 5),
        (10, 10),
        (10, 15),
        (20, 20),
    ],
)
def test_invalid_initialization(size, overlap):
    with pytest.raises(ValueError):
        Chunker(
            chunk_size=size,
            chunk_overlap=overlap,
        )


# ---------------------------------------------------------
# Chunking
# ---------------------------------------------------------


def test_small_document(chunker, document):
    chunks = chunker.chunk(document)

    assert len(chunks) == 1
    assert chunks[0].text == document.content


def test_empty_document(chunker):
    document = Document(
        id="1",
        filename="empty.txt",
        content="",
        document_type=DocumentType.TEXT,
    )

    assert chunker.chunk(document) == []


def test_whitespace_document(chunker):
    document = Document(
        id="1",
        filename="space.txt",
        content="   \n\n\t ",
        document_type=DocumentType.TEXT,
    )

    assert chunker.chunk(document) == []


def test_large_document(chunker, large_document):
    chunks = chunker.chunk(large_document)

    assert len(chunks) > 1


def test_chunk_ids(chunker, large_document):
    chunks = chunker.chunk(large_document)

    assert chunks[0].id == "large_0"
    assert chunks[-1].id.startswith("large_")


def test_chunk_metadata(chunker, large_document):
    chunks = chunker.chunk(large_document)

    metadata = chunks[0].metadata

    assert metadata.document_id == "large"
    assert metadata.filename == "large.txt"
    assert metadata.document_type == DocumentType.TEXT
    assert metadata.chunk_index == 0


def test_chunk_lengths(chunker, large_document):
    chunks = chunker.chunk(large_document)

    for chunk in chunks[:-1]:
        assert len(chunk.text) <= chunker.chunk_size


# ---------------------------------------------------------
# Recursive Split
# ---------------------------------------------------------


def test_recursive_split_small(chunker):
    text = "hello"

    chunks = chunker._recursive_split(text)

    assert chunks == ["hello"]


def test_recursive_split_paragraphs(chunker):
    text = ("\n\n").join(
        [
            "Paragraph one.",
            "Paragraph two.",
            "Paragraph three.",
        ]
    )

    chunks = chunker._recursive_split(text)

    assert len(chunks) >= 1


def test_recursive_split_sentences():
    c = Chunker(
        chunk_size=30,
        chunk_overlap=5,
    )

    text = (
        "Sentence one. "
        "Sentence two. "
        "Sentence three. "
        "Sentence four."
    )

    chunks = c._recursive_split(text)

    assert len(chunks) >= 2


def test_recursive_split_words():
    c = Chunker(
        chunk_size=10,
        chunk_overlap=2,
    )

    text = " ".join(["word"] * 50)

    chunks = c._recursive_split(text)

    assert len(chunks) > 5


def test_recursive_split_long_token():
    c = Chunker(
        chunk_size=20,
        chunk_overlap=5,
    )

    text = "A" * 200

    chunks = c._recursive_split(text)

    assert len(chunks) > 1

    for chunk in chunks[:-1]:
        assert len(chunk) <= 20


# ---------------------------------------------------------
# Metadata
# ---------------------------------------------------------


def test_metadata_indexes(chunker, large_document):
    chunks = chunker.chunk(large_document)

    indexes = [
        c.metadata.chunk_index
        for c in chunks
    ]

    assert indexes == list(range(len(chunks)))


def test_metadata_character_positions(chunker, large_document):
    chunks = chunker.chunk(large_document)

    for chunk in chunks:
        assert chunk.metadata.start_char >= 0
        assert (
            chunk.metadata.end_char
            >= chunk.metadata.start_char
        )


# ---------------------------------------------------------
# Statistics
# ---------------------------------------------------------


def test_statistics(chunker, document):
    chunker.chunk(document)

    stats = chunker.statistics()

    assert stats["documents"] == 1
    assert stats["chunks"] == 1


def test_statistics_multiple(chunker, document):
    chunker.chunk(document)
    chunker.chunk(document)

    stats = chunker.statistics()

    assert stats["documents"] == 2
    assert stats["chunks"] == 2


def test_clear_statistics(chunker, document):
    chunker.chunk(document)

    chunker.clear_statistics()

    assert chunker.statistics() == {}


def test_reset(chunker, document):
    chunker.chunk(document)

    chunker.reset()

    assert chunker.statistics() == {}


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------


def test_configuration(chunker):
    config = chunker.configuration()

    assert config["chunk_size"] == 100
    assert config["chunk_overlap"] == 20
    assert config["algorithm"] == "recursive"


# ---------------------------------------------------------
# Dunder
# ---------------------------------------------------------


def test_len(chunker):
    assert len(chunker) == 3


def test_iter(chunker):
    config = dict(chunker)

    assert config["chunk_size"] == 100
    assert config["chunk_overlap"] == 20


# ---------------------------------------------------------
# Unicode
# ---------------------------------------------------------


def test_unicode(chunker):
    document = Document(
        id="unicode",
        filename="unicode.txt",
        content="தமிழ் 日本語 😀 مرحبا " * 20,
        document_type=DocumentType.TEXT,
    )

    chunks = chunker.chunk(document)

    assert len(chunks) > 0

    combined = " ".join(
        c.text for c in chunks
    )

    assert "தமிழ்" in combined
    assert "日本語" in combined
    assert "😀" in combined


# ---------------------------------------------------------
# Edge Cases
# ---------------------------------------------------------


def test_exact_chunk_size():
    c = Chunker(
        chunk_size=100,
        chunk_overlap=10,
    )

    document = Document(
        id="exact",
        filename="exact.txt",
        content="A" * 100,
        document_type=DocumentType.TEXT,
    )

    chunks = c.chunk(document)

    assert len(chunks) == 1
    assert chunks[0].text == "A" * 100


def test_single_character_chunks():
    c = Chunker(
        chunk_size=1,
        chunk_overlap=0,
    )

    document = Document(
        id="chars",
        filename="chars.txt",
        content="ABCDE",
        document_type=DocumentType.TEXT,
    )

    chunks = c.chunk(document)

    assert len(chunks) == 5
    assert chunks[0].text == "A"
    assert chunks[-1].text == "E"


def test_document_type_preserved(chunker, document):
    chunks = chunker.chunk(document)

    assert all(
        c.metadata.document_type == DocumentType.TEXT
        for c in chunks
    )