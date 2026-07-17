import pytest

from app.hybrid_search.models import (
    SearchDocument,
    SearchRequest,
    SearchResult,
    SearchType,
)
from app.hybrid_search.reranker import ReRanker


# ---------------------------------------------------------
# Fixtures
# ---------------------------------------------------------


@pytest.fixture
def reranker():

    return ReRanker()


@pytest.fixture
def results():

    return [

        SearchResult(
            document=SearchDocument(
                id="1",
                text="Python FastAPI Docker",
            ),
            score=0.80,
            rank=1,
            source=SearchType.KEYWORD,
        ),

        SearchResult(
            document=SearchDocument(
                id="2",
                text="Python Machine Learning",
            ),
            score=0.75,
            rank=2,
            source=SearchType.BM25,
        ),

        SearchResult(
            document=SearchDocument(
                id="3",
                text="Java Spring Boot",
            ),
            score=0.70,
            rank=3,
            source=SearchType.VECTOR,
        ),

    ]


# ---------------------------------------------------------
# Score
# ---------------------------------------------------------


def test_score_positive(
    reranker,
):

    request = SearchRequest(
        query="python"
    )

    result = SearchResult(
        document=SearchDocument(
            id="1",
            text="Python FastAPI",
        ),
        score=1.0,
        source=SearchType.KEYWORD,
    )

    score = reranker.score(
        request,
        result,
    )

    assert score > 0


def test_score_no_match(
    reranker,
):

    request = SearchRequest(
        query="golang"
    )

    result = SearchResult(
        document=SearchDocument(
            id="1",
            text="Python FastAPI",
        ),
        score=1.0,
        source=SearchType.KEYWORD,
    )

    assert reranker.score(
        request,
        result,
    ) == 0.0


def test_score_multiple_matches(
    reranker,
):

    request = SearchRequest(
        query="python fastapi"
    )

    result = SearchResult(
        document=SearchDocument(
            id="1",
            text="Python FastAPI Docker",
        ),
        score=1.0,
        source=SearchType.KEYWORD,
    )

    score = reranker.score(
        request,
        result,
    )

    assert score == 2.0


# ---------------------------------------------------------
# Tokenization
# ---------------------------------------------------------


def test_tokenize(
    reranker,
):

    tokens = reranker._tokenize(
        "Python FastAPI Docker"
    )

    assert tokens == [
        "python",
        "fastapi",
        "docker",
    ]


def test_tokenize_empty(
    reranker,
):

    assert reranker._tokenize("") == []


# ---------------------------------------------------------
# Re-rank
# ---------------------------------------------------------


def test_rerank(
    reranker,
    results,
):

    request = SearchRequest(
        query="python"
    )

    ranked = reranker.rerank(
        request,
        results,
    )

    assert len(ranked) == 3


def test_rerank_top_k(
    results,
):

    reranker = ReRanker(
        top_k=2,
    )

    request = SearchRequest(
        query="python"
    )

    ranked = reranker.rerank(
        request,
        results,
    )

    assert len(ranked) == 2


def test_rerank_assigns_rank(
    reranker,
    results,
):

    request = SearchRequest(
        query="python"
    )

    ranked = reranker.rerank(
        request,
        results,
    )

    assert ranked[0].rank == 1
    assert ranked[1].rank == 2


def test_rerank_empty(
    reranker,
):

    request = SearchRequest(
        query="python"
    )

    assert reranker.rerank(
        request,
        [],
    ) == []


# ---------------------------------------------------------
# Best
# ---------------------------------------------------------


def test_best(
    reranker,
    results,
):

    request = SearchRequest(
        query="python"
    )

    best = reranker.best(
        request,
        results,
    )

    assert best is not None


def test_best_empty(
    reranker,
):

    request = SearchRequest(
        query="python"
    )

    assert reranker.best(
        request,
        [],
    ) is None


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------


def test_configuration(
    reranker,
):

    config = reranker.configuration()

    assert config["algorithm"] == "reranker"
    assert config["top_k"] == 10


def test_custom_configuration():

    reranker = ReRanker(
        top_k=5,
    )

    config = reranker.configuration()

    assert config["top_k"] == 5


# ---------------------------------------------------------
# Statistics
# ---------------------------------------------------------


def test_statistics(
    reranker,
    results,
):

    request = SearchRequest(
        query="python"
    )

    reranker.rerank(
        request,
        results,
    )

    stats = reranker.statistics()

    assert stats["requests"] == 1
    assert stats["returned"] == 3


def test_clear_statistics(
    reranker,
    results,
):

    request = SearchRequest(
        query="python"
    )

    reranker.rerank(
        request,
        results,
    )

    reranker.clear_statistics()

    assert reranker.statistics() == {}


# ---------------------------------------------------------
# Reset
# ---------------------------------------------------------


def test_reset(
    reranker,
    results,
):

    request = SearchRequest(
        query="python"
    )

    reranker.rerank(
        request,
        results,
    )

    reranker.reset()

    assert reranker.statistics() == {}

    config = reranker.configuration()

    assert config["top_k"] == 10


# ---------------------------------------------------------
# Dunder
# ---------------------------------------------------------


def test_len(
    reranker,
):

    assert len(reranker) == 2


def test_iter(
    reranker,
):

    config = dict(iter(reranker))

    assert config["algorithm"] == "reranker"


# ---------------------------------------------------------
# Edge Cases
# ---------------------------------------------------------


def test_case_insensitive(
    reranker,
):

    request = SearchRequest(
        query="PYTHON"
    )

    result = SearchResult(
        document=SearchDocument(
            id="1",
            text="python",
        ),
        score=1.0,
        source=SearchType.KEYWORD,
    )

    assert reranker.score(
        request,
        result,
    ) == 1.0


def test_unicode(
    reranker,
):

    request = SearchRequest(
        query="café"
    )

    result = SearchResult(
        document=SearchDocument(
            id="1",
            text="Python Café",
        ),
        score=1.0,
        source=SearchType.KEYWORD,
    )

    assert reranker.score(
        request,
        result,
    ) == 1.0


def test_multiple_calls(
    reranker,
    results,
):

    request = SearchRequest(
        query="python"
    )

    for _ in range(5):

        reranker.rerank(
            request,
            results,
        )

    stats = reranker.statistics()

    assert stats["requests"] == 5
    assert stats["returned"] == 15


def test_document_empty_text(
    reranker,
):

    request = SearchRequest(
        query="python"
    )

    result = SearchResult(
        document=SearchDocument(
            id="1",
            text="",
        ),
        score=1.0,
        source=SearchType.KEYWORD,
    )

    assert reranker.score(
        request,
        result,
    ) == 0.0


def test_duplicate_query_terms(
    reranker,
):

    request = SearchRequest(
        query="python python"
    )

    result = SearchResult(
        document=SearchDocument(
            id="1",
            text="python",
        ),
        score=1.0,
        source=SearchType.KEYWORD,
    )

    assert reranker.score(
        request,
        result,
    ) == 2.0