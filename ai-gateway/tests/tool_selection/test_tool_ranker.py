import pytest

from app.tool_selection.models import (
    RankingWeights,
    ToolCandidate,
    ToolMetadata,
)
from app.tool_selection.tool_ranker import ToolRanker


@pytest.fixture
def ranker():
    return ToolRanker()


@pytest.fixture
def candidate1():
    tool = ToolMetadata(
        name="Tool1",
        description="",
        provider="OpenAI",
        capabilities=[],
        reliability=0.95,
        confidence=0.90,
        average_latency_ms=100,
        average_cost=0.01,
        enabled=True,
    )

    return ToolCandidate(
        tool=tool,
        capability_score=1.0,
    )


@pytest.fixture
def candidate2():
    tool = ToolMetadata(
        name="Tool2",
        description="",
        provider="Anthropic",
        capabilities=[],
        reliability=0.80,
        confidence=0.75,
        average_latency_ms=300,
        average_cost=0.05,
        enabled=True,
    )

    return ToolCandidate(
        tool=tool,
        capability_score=0.60,
    )


# -------------------------------------------------
# Normalization
# -------------------------------------------------


def test_normalize_same_values():
    assert (
        ToolRanker._normalize_inverse(
            5,
            5,
            5,
        )
        == 1.0
    )


def test_normalize_minimum():
    assert (
        ToolRanker._normalize_inverse(
            1,
            1,
            5,
        )
        == 1.0
    )


def test_normalize_maximum():
    assert (
        ToolRanker._normalize_inverse(
            5,
            1,
            5,
        )
        == 0.0
    )


def test_normalize_middle():
    value = ToolRanker._normalize_inverse(
        3,
        1,
        5,
    )

    assert 0 < value < 1


# -------------------------------------------------
# Score
# -------------------------------------------------


def test_score(
    ranker,
    candidate1,
):
    result = ranker.score(
        candidate1,
        100,
        300,
        0.01,
        0.05,
    )

    assert result.total_score > 0
    assert result.latency_score == 1.0
    assert result.cost_score == 1.0


def test_score_updates_statistics(
    ranker,
    candidate1,
):
    ranker.score(
        candidate1,
        100,
        300,
        0.01,
        0.05,
    )

    assert (
        ranker.statistics()["scored"]
        == 1
    )


def test_score_contains_scores(
    ranker,
    candidate1,
):
    result = ranker.score(
        candidate1,
        100,
        300,
        0.01,
        0.05,
    )

    assert result.reliability_score > 0
    assert result.confidence_score > 0


# -------------------------------------------------
# Rank
# -------------------------------------------------


def test_rank(
    ranker,
    candidate1,
    candidate2,
):
    ranked = ranker.rank(
        [
            candidate2,
            candidate1,
        ]
    )

    assert ranked[0].tool.name == "Tool1"


def test_rank_empty(
    ranker,
):
    assert ranker.rank([]) == []


def test_rank_statistics(
    ranker,
    candidate1,
):
    ranker.rank([candidate1])

    assert (
        ranker.statistics()["requests"]
        == 1
    )


def test_rank_returns_all(
    ranker,
    candidate1,
    candidate2,
):
    ranked = ranker.rank(
        [
            candidate1,
            candidate2,
        ]
    )

    assert len(ranked) == 2


# -------------------------------------------------
# Best
# -------------------------------------------------


def test_best(
    ranker,
    candidate1,
    candidate2,
):
    best = ranker.best(
        [
            candidate1,
            candidate2,
        ]
    )

    assert best.tool.name == "Tool1"


def test_best_empty(
    ranker,
):
    assert ranker.best([]) is None


# -------------------------------------------------
# Top
# -------------------------------------------------


def test_top(
    ranker,
    candidate1,
    candidate2,
):
    result = ranker.top(
        [
            candidate1,
            candidate2,
        ],
        limit=1,
    )

    assert len(result) == 1


def test_top_default_limit(
    ranker,
    candidate1,
):
    result = ranker.top(
        [candidate1]
    )

    assert len(result) == 1


# -------------------------------------------------
# Weights
# -------------------------------------------------


def test_default_weights(
    ranker,
):
    assert isinstance(
        ranker.weights,
        RankingWeights,
    )


def test_set_weights():
    weights = RankingWeights(
        capability=0.5,
        confidence=0.2,
        reliability=0.2,
        latency=0.05,
        cost=0.05,
    )

    ranker = ToolRanker()

    ranker.set_weights(
        weights
    )

    assert (
        ranker.weights
        == weights
    )


# -------------------------------------------------
# Statistics
# -------------------------------------------------


def test_statistics(
    ranker,
    candidate1,
):
    ranker.rank(
        [candidate1]
    )

    stats = ranker.statistics()

    assert "requests" in stats


def test_clear_statistics(
    ranker,
    candidate1,
):
    ranker.rank(
        [candidate1]
    )

    ranker.clear_statistics()

    assert (
        ranker.statistics()
        == {}
    )


# -------------------------------------------------
# Reset
# -------------------------------------------------


def test_reset(
    candidate1,
):
    ranker = ToolRanker()

    custom = RankingWeights(
        capability=0.9
    )

    ranker.set_weights(
        custom
    )

    ranker.rank(
        [candidate1]
    )

    ranker.reset()

    assert isinstance(
        ranker.weights,
        RankingWeights,
    )

    assert (
        ranker.statistics()
        == {}
    )


# -------------------------------------------------
# Dunder
# -------------------------------------------------


def test_len(
    ranker,
):
    assert len(ranker) == 5


def test_iter(
    ranker,
):
    items = list(ranker)

    assert len(items) == 5

    assert items[0][0] == "capability"

    assert isinstance(
        items[0][1],
        float,
    )


# -------------------------------------------------
# Edge Cases
# -------------------------------------------------


def test_rank_single_candidate(
    ranker,
    candidate1,
):
    ranked = ranker.rank(
        [candidate1]
    )

    assert len(ranked) == 1


def test_score_rounding(
    ranker,
    candidate1,
):
    scored = ranker.score(
        candidate1,
        100,
        300,
        0.01,
        0.05,
    )

    assert round(
        scored.total_score,
        3,
    ) == scored.total_score