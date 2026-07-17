from __future__ import annotations

import pytest

from app.rag.citation_engine import CitationEngine
from app.rag.models import (
    ChunkMetadata,
    Citation,
    CitationResult,
    DocumentChunk,
    RetrievalResult,
)


# ---------------------------------------------------------
# Fixtures
# ---------------------------------------------------------


@pytest.fixture
def engine():
    return CitationEngine()


@pytest.fixture
def retrieval_results():
    return [
        RetrievalResult(
            chunk=DocumentChunk(
                id="chunk1",
                document_id="doc1",
                text="Python basics",
                metadata=ChunkMetadata(
                    document_id="doc1",
                    filename="python.pdf",
                    page=10,
                    source="Book A",
                ),
            ),
            score=0.98,
        ),
        RetrievalResult(
            chunk=DocumentChunk(
                id="chunk2",
                document_id="doc1",
                text="Advanced Python",
                metadata=ChunkMetadata(
                    document_id="doc1",
                    filename="python.pdf",
                    page=15,
                    source="Book A",
                ),
            ),
            score=0.95,
        ),
        RetrievalResult(
            chunk=DocumentChunk(
                id="chunk3",
                document_id="doc2",
                text="Docker Guide",
                metadata=ChunkMetadata(
                    document_id="doc2",
                    filename="docker.pdf",
                    page=4,
                    source="Book B",
                ),
            ),
            score=0.91,
        ),
    ]


# ---------------------------------------------------------
# Generate
# ---------------------------------------------------------


def test_generate(engine, retrieval_results):
    result = engine.generate(retrieval_results)

    assert isinstance(result, CitationResult)
    assert len(result.citations) == 3


def test_generate_empty(engine):
    result = engine.generate([])

    assert result.citations == []


def test_generate_deduplicates(engine):
    duplicate = RetrievalResult(
        chunk=DocumentChunk(
            id="chunk1",
            document_id="doc1",
            text="Duplicate",
            metadata=ChunkMetadata(
                document_id="doc1",
                filename="python.pdf",
                page=20,
            ),
        ),
        score=0.80,
    )

    results = [
        duplicate,
        duplicate,
    ]

    citations = engine.generate(results)

    assert len(citations.citations) == 1


def test_generate_indexes(engine, retrieval_results):
    citations = engine.generate(retrieval_results)

    indexes = [
        citation.index
        for citation in citations.citations
    ]

    assert indexes == [1, 2, 3]


# ---------------------------------------------------------
# Citation Content
# ---------------------------------------------------------


def test_citation_fields(engine, retrieval_results):
    citation = engine.generate(
        retrieval_results
    ).citations[0]

    assert citation.document_id == "doc1"
    assert citation.filename == "python.pdf"
    assert citation.chunk_id == "chunk1"
    assert citation.page == 10
    assert citation.source == "Book A"
    assert citation.score == pytest.approx(0.98)


# ---------------------------------------------------------
# Formatting
# ---------------------------------------------------------


def test_format(engine):
    citation = Citation(
        index=1,
        document_id="doc1",
        filename="paper.pdf",
        chunk_id="chunk1",
        page=5,
        source="Research",
        score=0.99,
    )

    formatted = engine.format(citation)

    assert "[1]" in formatted
    assert "paper.pdf" in formatted
    assert "Page 5" in formatted
    assert "Research" in formatted


def test_format_without_page(engine):
    citation = Citation(
        index=1,
        document_id="doc1",
        filename="paper.pdf",
        chunk_id="chunk1",
        page=None,
        source="Research",
        score=0.9,
    )

    formatted = engine.format(citation)

    assert "Page" not in formatted
    assert "Research" in formatted


def test_format_without_source(engine):
    citation = Citation(
        index=1,
        document_id="doc1",
        filename="paper.pdf",
        chunk_id="chunk1",
        page=2,
        source=None,
        score=0.9,
    )

    formatted = engine.format(citation)

    assert "Page 2" in formatted
    assert "paper.pdf" in formatted


def test_format_minimal(engine):
    citation = Citation(
        index=1,
        document_id="doc1",
        filename="paper.pdf",
        chunk_id="chunk1",
        score=0.5,
    )

    formatted = engine.format(citation)

    assert formatted == "[1] | paper.pdf"


def test_format_all(engine, retrieval_results):
    citations = engine.generate(retrieval_results)

    formatted = engine.format_all(citations)

    assert len(formatted) == 3
    assert all(isinstance(item, str) for item in formatted)


def test_format_all_empty(engine):
    result = CitationResult()

    assert engine.format_all(result) == []


# ---------------------------------------------------------
# Statistics
# ---------------------------------------------------------


def test_statistics(engine, retrieval_results):
    engine.generate(retrieval_results)

    stats = engine.statistics()

    assert stats["requests"] == 1
    assert stats["generated"] == 3


def test_multiple_generations(engine, retrieval_results):
    for _ in range(5):
        engine.generate(retrieval_results)

    stats = engine.statistics()

    assert stats["requests"] == 5
    assert stats["generated"] == 15


def test_clear_statistics(engine, retrieval_results):
    engine.generate(retrieval_results)

    engine.clear_statistics()

    assert engine.statistics() == {}


def test_reset(engine, retrieval_results):
    engine.generate(retrieval_results)

    engine.reset()

    assert engine.statistics() == {}


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------


def test_configuration(engine):
    config = engine.configuration()

    assert config["deduplicate"] is True
    assert config["format"] == "default"


# ---------------------------------------------------------
# Dunder
# ---------------------------------------------------------


def test_len(engine):
    assert len(engine) == 2


def test_iter(engine):
    config = dict(engine)

    assert config["deduplicate"] is True
    assert config["format"] == "default"


# ---------------------------------------------------------
# Unicode
# ---------------------------------------------------------


def test_unicode_filename(engine):
    result = RetrievalResult(
        chunk=DocumentChunk(
            id="1",
            document_id="doc",
            text="தமிழ்",
            metadata=ChunkMetadata(
                document_id="doc",
                filename="தமிழ்_日本語😀.pdf",
                page=1,
                source="Unicode",
            ),
        ),
        score=0.8,
    )

    citation = engine.generate([result]).citations[0]

    assert "தமிழ்" in citation.filename


# ---------------------------------------------------------
# Edge Cases
# ---------------------------------------------------------


def test_large_number_of_results(engine):
    results = []

    for i in range(1000):
        results.append(
            RetrievalResult(
                chunk=DocumentChunk(
                    id=f"chunk{i}",
                    document_id=f"doc{i // 10}",
                    text=f"text {i}",
                    metadata=ChunkMetadata(
                        document_id=f"doc{i // 10}",
                        filename=f"file{i}.txt",
                    ),
                ),
                score=1.0,
            )
        )

    citations = engine.generate(results)

    assert len(citations.citations) == 1000


def test_duplicate_document_different_chunks(engine):
    results = [
        RetrievalResult(
            chunk=DocumentChunk(
                id="chunk1",
                document_id="doc1",
                text="A",
                metadata=ChunkMetadata(
                    document_id="doc1",
                    filename="file.txt",
                ),
            ),
            score=0.9,
        ),
        RetrievalResult(
            chunk=DocumentChunk(
                id="chunk2",
                document_id="doc1",
                text="B",
                metadata=ChunkMetadata(
                    document_id="doc1",
                    filename="file.txt",
                ),
            ),
            score=0.8,
        ),
    ]

    citations = engine.generate(results)

    # Deduplication is by (document_id, chunk_id),
    # so different chunks from the same document remain.
    assert len(citations.citations) == 2