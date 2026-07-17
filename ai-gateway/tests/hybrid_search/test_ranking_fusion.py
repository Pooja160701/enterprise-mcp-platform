import pytest

from app.hybrid_search.models import (
    SearchDocument,
    SearchResult,
    SearchType,
)
from app.hybrid_search.ranking_fusion import RankingFusion


# ---------------------------------------------------------
# Fixtures
# ---------------------------------------------------------


@pytest.fixture
def fusion():

    return RankingFusion()


@pytest.fixture
def keyword_results():

    return [

        SearchResult(
            document=SearchDocument(
                id="1",
                text="Python",
            ),
            score=10.0,
            rank=1,
            source=SearchType.KEYWORD,
        ),

        SearchResult(
            document=SearchDocument(
                id="2",
                text="Docker",
            ),
            score=9.0,
            rank=2,
            source=SearchType.KEYWORD,
        ),

        SearchResult(
            document=SearchDocument(
                id="3",
                text="FastAPI",
            ),
            score=8.0,
            rank=3,
            source=SearchType.KEYWORD,
        ),

    ]


@pytest.fixture
def bm25_results():

    return [

        SearchResult(
            document=SearchDocument(
                id="2",
                text="Docker",
            ),
            score=15.0,
            rank=1,
            source=SearchType.BM25,
        ),

        SearchResult(
            document=SearchDocument(
                id="3",
                text="FastAPI",
            ),
            score=14.0,
            rank=2,
            source=SearchType.BM25,
        ),

        SearchResult(
            document=SearchDocument(
                id="4",
                text="Kubernetes",
            ),
            score=13.0,
            rank=3,
            source=SearchType.BM25,
        ),

    ]


@pytest.fixture
def vector_results():

    return [

        SearchResult(
            document=SearchDocument(
                id="3",
                text="FastAPI",
            ),
            score=0.98,
            rank=1,
            source=SearchType.VECTOR,
        ),

        SearchResult(
            document=SearchDocument(
                id="4",
                text="Kubernetes",
            ),
            score=0.95,
            rank=2,
            source=SearchType.VECTOR,
        ),

        SearchResult(
            document=SearchDocument(
                id="5",
                text="TensorFlow",
            ),
            score=0.90,
            rank=3,
            source=SearchType.VECTOR,
        ),

    ]


# ---------------------------------------------------------
# Reciprocal Rank Score
# ---------------------------------------------------------


def test_rrf_score_positive(
    fusion,
):

    score = fusion._rrf_score(1)

    assert score > 0


def test_rrf_score_decreases(
    fusion,
):

    assert fusion._rrf_score(1) > fusion._rrf_score(2)
    assert fusion._rrf_score(2) > fusion._rrf_score(3)


def test_rrf_score_large_rank(
    fusion,
):

    assert fusion._rrf_score(100) > 0


# ---------------------------------------------------------
# Fuse
# ---------------------------------------------------------


def test_fuse_multiple_lists(
    fusion,
    keyword_results,
    bm25_results,
    vector_results,
):

    results = fusion.fuse(
        [
            keyword_results,
            bm25_results,
            vector_results,
        ]
    )

    assert len(results) == 5


def test_fuse_empty_lists(
    fusion,
):

    results = fusion.fuse(
        [
            [],
            [],
        ]
    )

    assert results == []


def test_fuse_duplicate_documents(
    fusion,
    keyword_results,
    bm25_results,
):

    results = fusion.fuse(
        [
            keyword_results,
            bm25_results,
        ]
    )

    ids = [r.document.id for r in results]

    assert ids.count("2") == 1
    assert ids.count("3") == 1


def test_fuse_top_k(
    fusion,
    keyword_results,
    bm25_results,
):

    results = fusion.fuse(
        [
            keyword_results,
            bm25_results,
        ],
        top_k=2,
    )

    assert len(results) == 2


def test_fuse_assigns_rank(
    fusion,
    keyword_results,
):

    results = fusion.fuse(
        [
            keyword_results,
        ]
    )

    assert results[0].rank == 1
    assert results[1].rank == 2


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------


def test_configuration(
    fusion,
):

    config = fusion.configuration()

    assert config["algorithm"] == "rrf"
    assert config["k"] == 60


def test_custom_configuration():

    fusion = RankingFusion(
        k=100,
    )

    config = fusion.configuration()

    assert config["k"] == 100


# ---------------------------------------------------------
# Statistics
# ---------------------------------------------------------


def test_statistics(
    fusion,
    keyword_results,
):

    fusion.fuse(
        [
            keyword_results,
        ]
    )

    stats = fusion.statistics()

    assert stats["requests"] == 1
    assert stats["returned"] == 3


def test_clear_statistics(
    fusion,
    keyword_results,
):

    fusion.fuse(
        [
            keyword_results,
        ]
    )

    fusion.clear_statistics()

    assert fusion.statistics() == {}


# ---------------------------------------------------------
# Reset
# ---------------------------------------------------------


def test_reset(
    fusion,
    keyword_results,
):

    fusion.fuse(
        [
            keyword_results,
        ]
    )

    fusion.reset()

    assert fusion.statistics() == {}

    config = fusion.configuration()

    assert config["k"] == 60


# ---------------------------------------------------------
# Dunder
# ---------------------------------------------------------


def test_len(
    fusion,
):

    assert len(fusion) == 2


def test_iter(
    fusion,
):

    config = dict(iter(fusion))

    assert config["algorithm"] == "rrf"


# ---------------------------------------------------------
# Edge Cases
# ---------------------------------------------------------


def test_empty_input(
    fusion,
):

    assert fusion.fuse([]) == []


def test_single_result_list(
    fusion,
    keyword_results,
):

    results = fusion.fuse(
        [
            keyword_results,
        ]
    )

    assert len(results) == 3


def test_multiple_fuse_calls(
    fusion,
    keyword_results,
):

    for _ in range(5):

        fusion.fuse(
            [
                keyword_results,
            ]
        )

    stats = fusion.statistics()

    assert stats["requests"] == 5
    assert stats["returned"] == 15


def test_duplicate_in_same_list(
    fusion,
):

    doc = SearchDocument(
        id="1",
        text="Python",
    )

    results = fusion.fuse(
        [
            [
                SearchResult(
                    document=doc,
                    score=10,
                    rank=1,
                    source=SearchType.KEYWORD,
                ),
                SearchResult(
                    document=doc,
                    score=9,
                    rank=2,
                    source=SearchType.KEYWORD,
                ),
            ]
        ]
    )

    assert len(results) == 1


def test_large_number_of_lists(
    fusion,
):

    result_lists = []

    for i in range(10):

        result_lists.append(
            [
                SearchResult(
                    document=SearchDocument(
                        id=str(i),
                        text=f"Doc {i}",
                    ),
                    score=1.0,
                    rank=1,
                    source=SearchType.KEYWORD,
                )
            ]
        )

    results = fusion.fuse(result_lists)

    assert len(results) == 10