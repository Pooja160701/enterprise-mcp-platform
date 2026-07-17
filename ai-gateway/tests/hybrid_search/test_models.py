import pytest

from app.hybrid_search.models import (
    HybridSearchResult,
    SearchDocument,
    SearchRequest,
    SearchResult,
    SearchType,
)


# ---------------------------------------------------------
# SearchType
# ---------------------------------------------------------


def test_search_type_values():

    assert SearchType.KEYWORD.value == "keyword"
    assert SearchType.BM25.value == "bm25"
    assert SearchType.VECTOR.value == "vector"
    assert SearchType.HYBRID.value == "hybrid"


def test_search_type_members():

    assert len(SearchType) == 4

    assert SearchType.KEYWORD in SearchType
    assert SearchType.BM25 in SearchType
    assert SearchType.VECTOR in SearchType
    assert SearchType.HYBRID in SearchType


# ---------------------------------------------------------
# SearchDocument
# ---------------------------------------------------------


def test_search_document_creation():

    document = SearchDocument(
        id="1",
        text="Hello World",
    )

    assert document.id == "1"
    assert document.text == "Hello World"
    assert document.metadata == {}
    assert document.embedding is None


def test_search_document_with_metadata():

    document = SearchDocument(
        id="2",
        text="Python",
        metadata={
            "source": "github",
            "language": "python",
        },
    )

    assert document.metadata["source"] == "github"
    assert document.metadata["language"] == "python"


def test_search_document_with_embedding():

    embedding = [0.1, 0.2, 0.3]

    document = SearchDocument(
        id="3",
        text="Embedding",
        embedding=embedding,
    )

    assert document.embedding == embedding


def test_search_document_empty_text():

    document = SearchDocument(
        id="4",
        text="",
    )

    assert document.text == ""


# ---------------------------------------------------------
# SearchRequest
# ---------------------------------------------------------


def test_search_request_defaults():

    request = SearchRequest(
        query="python"
    )

    assert request.query == "python"
    assert request.top_k == 10
    assert request.metadata_filter == {}
    assert request.search_type == SearchType.HYBRID


def test_search_request_custom_values():

    request = SearchRequest(
        query="docker",
        top_k=5,
        metadata_filter={
            "language": "python"
        },
        search_type=SearchType.BM25,
    )

    assert request.query == "docker"
    assert request.top_k == 5
    assert request.metadata_filter["language"] == "python"
    assert request.search_type == SearchType.BM25


# ---------------------------------------------------------
# SearchResult
# ---------------------------------------------------------


def test_search_result_defaults():

    document = SearchDocument(
        id="1",
        text="Example",
    )

    result = SearchResult(
        document=document,
        source=SearchType.KEYWORD,
    )

    assert result.document == document
    assert result.score == 0.0
    assert result.rank == 0
    assert result.source == SearchType.KEYWORD


def test_search_result_custom_values():

    document = SearchDocument(
        id="1",
        text="Python",
    )

    result = SearchResult(
        document=document,
        score=0.91,
        rank=2,
        source=SearchType.VECTOR,
    )

    assert result.score == pytest.approx(0.91)
    assert result.rank == 2
    assert result.source == SearchType.VECTOR


# ---------------------------------------------------------
# HybridSearchResult
# ---------------------------------------------------------


def test_hybrid_search_result_defaults():

    result = HybridSearchResult(
        query="python"
    )

    assert result.query == "python"
    assert result.results == []
    assert result.elapsed_ms == 0.0


def test_hybrid_search_result_with_results():

    document = SearchDocument(
        id="1",
        text="Python Guide",
    )

    search_result = SearchResult(
        document=document,
        score=0.95,
        rank=1,
        source=SearchType.BM25,
    )

    result = HybridSearchResult(
        query="python",
        results=[search_result],
        elapsed_ms=15.7,
    )

    assert len(result.results) == 1
    assert result.results[0] == search_result
    assert result.elapsed_ms == pytest.approx(15.7)


# ---------------------------------------------------------
# Serialization
# ---------------------------------------------------------


def test_search_document_model_dump():

    document = SearchDocument(
        id="1",
        text="Hello",
        metadata={
            "source": "docs"
        },
    )

    data = document.model_dump()

    assert data["id"] == "1"
    assert data["text"] == "Hello"
    assert data["metadata"]["source"] == "docs"


def test_search_request_model_dump():

    request = SearchRequest(
        query="AI",
        top_k=3,
    )

    data = request.model_dump()

    assert data["query"] == "AI"
    assert data["top_k"] == 3


def test_search_result_model_dump():

    document = SearchDocument(
        id="5",
        text="Machine Learning",
    )

    result = SearchResult(
        document=document,
        score=0.88,
        source=SearchType.KEYWORD,
    )

    data = result.model_dump()

    assert data["score"] == pytest.approx(0.88)
    assert data["source"] == SearchType.KEYWORD


# ---------------------------------------------------------
# Equality
# ---------------------------------------------------------


def test_document_equality():

    d1 = SearchDocument(
        id="1",
        text="abc",
    )

    d2 = SearchDocument(
        id="1",
        text="abc",
    )

    assert d1 == d2


def test_request_equality():

    r1 = SearchRequest(
        query="python"
    )

    r2 = SearchRequest(
        query="python"
    )

    assert r1 == r2


# ---------------------------------------------------------
# Edge Cases
# ---------------------------------------------------------


def test_empty_embedding():

    document = SearchDocument(
        id="1",
        text="test",
        embedding=[],
    )

    assert document.embedding == []


def test_large_embedding():

    embedding = [0.1] * 1536

    document = SearchDocument(
        id="1",
        text="Embedding",
        embedding=embedding,
    )

    assert len(document.embedding) == 1536


def test_empty_metadata():

    document = SearchDocument(
        id="1",
        text="Example",
        metadata={},
    )

    assert document.metadata == {}


def test_nested_metadata():

    document = SearchDocument(
        id="1",
        text="Example",
        metadata={
            "author": {
                "name": "Alice",
                "team": "AI",
            }
        },
    )

    assert document.metadata["author"]["name"] == "Alice"