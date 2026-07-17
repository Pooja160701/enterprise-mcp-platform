import math

import pytest

from app.hybrid_search.models import (
    SearchDocument,
    SearchRequest,
    SearchType,
)
from app.hybrid_search.vector_search import VectorSearch


# ---------------------------------------------------------
# Fixtures
# ---------------------------------------------------------


@pytest.fixture
def search():

    return VectorSearch()


@pytest.fixture
def documents():

    return [

        SearchDocument(
            id="1",
            text="Python",
            embedding=[1.0, 0.0, 0.0],
        ),

        SearchDocument(
            id="2",
            text="FastAPI",
            embedding=[0.9, 0.1, 0.0],
        ),

        SearchDocument(
            id="3",
            text="Docker",
            embedding=[0.0, 1.0, 0.0],
        ),

        SearchDocument(
            id="4",
            text="Empty",
            embedding=None,
        ),

    ]


@pytest.fixture
def query_embedding():

    return [1.0, 0.0, 0.0]


# ---------------------------------------------------------
# Search
# ---------------------------------------------------------


def test_search_returns_results(
    search,
    documents,
    query_embedding,
):

    request = SearchRequest(query="python")

    results = search.search(
        request,
        query_embedding,
        documents,
    )

    assert len(results) == 2


def test_search_empty_documents(
    search,
    query_embedding,
):

    request = SearchRequest(query="python")

    assert search.search(
        request,
        query_embedding,
        [],
    ) == []


def test_search_no_embeddings(
    search,
):

    docs = [

        SearchDocument(
            id="1",
            text="Python",
            embedding=None,
        )

    ]

    request = SearchRequest(query="python")

    assert search.search(
        request,
        [1.0, 0.0],
        docs,
    ) == []


def test_search_top_k(
    search,
    documents,
    query_embedding,
):

    request = SearchRequest(
        query="python",
        top_k=1,
    )

    results = search.search(
        request,
        query_embedding,
        documents,
    )

    assert len(results) == 1


def test_search_assigns_rank(
    search,
    documents,
    query_embedding,
):

    request = SearchRequest(query="python")

    results = search.search(
        request,
        query_embedding,
        documents,
    )

    assert results[0].rank == 1


def test_search_source(
    search,
    documents,
    query_embedding,
):

    request = SearchRequest(query="python")

    results = search.search(
        request,
        query_embedding,
        documents,
    )

    for result in results:

        assert result.source == SearchType.VECTOR


# ---------------------------------------------------------
# Cosine Similarity
# ---------------------------------------------------------


def test_cosine_similarity_identical(
    search,
):

    similarity = search._cosine_similarity(
        [1.0, 0.0],
        [1.0, 0.0],
    )

    assert similarity == pytest.approx(1.0)


def test_cosine_similarity_orthogonal(
    search,
):

    similarity = search._cosine_similarity(
        [1.0, 0.0],
        [0.0, 1.0],
    )

    assert similarity == pytest.approx(0.0)


def test_cosine_similarity_opposite(
    search,
):

    similarity = search._cosine_similarity(
        [1.0],
        [-1.0],
    )

    assert similarity == pytest.approx(-1.0)


def test_cosine_similarity_zero_vector(
    search,
):

    similarity = search._cosine_similarity(
        [0.0, 0.0],
        [1.0, 0.0],
    )

    assert similarity == 0.0


# ---------------------------------------------------------
# Best
# ---------------------------------------------------------


def test_best(
    search,
    documents,
    query_embedding,
):

    request = SearchRequest(query="python")

    best = search.best(
        request,
        query_embedding,
        documents,
    )

    assert best is not None
    assert best.document.id == "1"


def test_best_empty(
    search,
):

    request = SearchRequest(query="python")

    assert search.best(
        request,
        [1.0],
        [],
    ) is None


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------


def test_configuration(
    search,
):

    config = search.configuration()

    assert config["algorithm"] == "vector"
    assert config["minimum_similarity"] == 0.0


def test_custom_configuration():

    search = VectorSearch(
        minimum_similarity=0.5,
    )

    config = search.configuration()

    assert config["minimum_similarity"] == 0.5


# ---------------------------------------------------------
# Statistics
# ---------------------------------------------------------


def test_statistics(
    search,
    documents,
    query_embedding,
):

    request = SearchRequest(query="python")

    search.search(
        request,
        query_embedding,
        documents,
    )

    stats = search.statistics()

    assert stats["requests"] == 1
    assert stats["matched"] == 2


def test_clear_statistics(
    search,
    documents,
    query_embedding,
):

    request = SearchRequest(query="python")

    search.search(
        request,
        query_embedding,
        documents,
    )

    search.clear_statistics()

    assert search.statistics() == {}


# ---------------------------------------------------------
# Reset
# ---------------------------------------------------------


def test_reset(
    search,
    documents,
    query_embedding,
):

    request = SearchRequest(query="python")

    search.search(
        request,
        query_embedding,
        documents,
    )

    search.reset()

    assert search.statistics() == {}

    config = search.configuration()

    assert config["algorithm"] == "vector"


# ---------------------------------------------------------
# Dunder
# ---------------------------------------------------------


def test_len(
    search,
):

    assert len(search) == 2


def test_iter(
    search,
):

    config = dict(iter(search))

    assert config["algorithm"] == "vector"


# ---------------------------------------------------------
# Edge Cases
# ---------------------------------------------------------


def test_dimension_mismatch(
    search,
):

    with pytest.raises(ValueError):

        search._cosine_similarity(
            [1.0, 0.0],
            [1.0],
        )


def test_empty_vectors(
    search,
):

    similarity = search._cosine_similarity(
        [],
        [],
    )

    assert similarity == 0.0


def test_high_dimension_vector(
    search,
):

    v1 = [1.0] * 1536
    v2 = [1.0] * 1536

    similarity = search._cosine_similarity(
        v1,
        v2,
    )

    assert similarity == pytest.approx(1.0)


def test_minimum_similarity_filter():

    search = VectorSearch(
        minimum_similarity=0.95,
    )

    docs = [

        SearchDocument(
            id="1",
            text="Python",
            embedding=[0.8, 0.2],
        )

    ]

    request = SearchRequest(query="python")

    results = search.search(
        request,
        [1.0, 0.0],
        docs,
    )

    assert results == []


def test_multiple_search_calls(
    search,
    documents,
    query_embedding,
):

    request = SearchRequest(query="python")

    for _ in range(5):

        search.search(
            request,
            query_embedding,
            documents,
        )

    stats = search.statistics()

    assert stats["requests"] == 5
    assert stats["matched"] == 10


def test_math_stability(
    search,
):

    similarity = search._cosine_similarity(
        [1e-12, 1e-12],
        [1e-12, 1e-12],
    )

    assert math.isfinite(similarity)