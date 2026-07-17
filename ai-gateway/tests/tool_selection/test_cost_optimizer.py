import pytest

from app.tool_selection.cost_optimizer import CostOptimizer
from app.tool_selection.models import ToolCandidate, ToolMetadata


@pytest.fixture
def optimizer():
    return CostOptimizer()


@pytest.fixture
def candidate1():
    tool = ToolMetadata(
        name="GPT-4",
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
        total_score=0.95,
    )


@pytest.fixture
def candidate2():
    tool = ToolMetadata(
        name="Claude",
        description="",
        provider="Anthropic",
        capabilities=[],
        reliability=0.90,
        confidence=0.85,
        average_latency_ms=300,
        average_cost=0.05,
        enabled=True,
    )

    return ToolCandidate(
        tool=tool,
        total_score=0.90,
    )


# -------------------------------------------------
# Configuration
# -------------------------------------------------


def test_default_configuration(optimizer):
    config = optimizer.configuration()

    assert config["maximum_cost"] == float("inf")
    assert config["preferred_provider"] is None
    assert config["maximum_latency_ms"] is None


def test_set_maximum_cost(optimizer):
    optimizer.maximum_cost = 0.05
    assert optimizer.maximum_cost == 0.05


def test_negative_cost_becomes_zero(optimizer):
    optimizer.maximum_cost = -10
    assert optimizer.maximum_cost == 0.0


def test_set_provider(optimizer):
    optimizer.preferred_provider = "OpenAI"
    assert optimizer.preferred_provider == "OpenAI"


def test_set_latency(optimizer):
    optimizer.maximum_latency = 200
    assert optimizer.maximum_latency == 200


# -------------------------------------------------
# Cost Filter
# -------------------------------------------------


def test_filter_by_cost(
    optimizer,
    candidate1,
    candidate2,
):
    optimizer.maximum_cost = 0.02

    filtered = optimizer.filter_by_cost(
        [candidate1, candidate2]
    )

    assert len(filtered) == 1
    assert filtered[0].tool.name == "GPT-4"


def test_filter_by_cost_empty(
    optimizer,
):
    assert optimizer.filter_by_cost([]) == []


def test_filter_by_cost_statistics(
    optimizer,
    candidate1,
    candidate2,
):
    optimizer.maximum_cost = 0.02

    optimizer.filter_by_cost(
        [candidate1, candidate2]
    )

    assert (
        optimizer.statistics()["cost_filtered"]
        == 1
    )


# -------------------------------------------------
# Latency Filter
# -------------------------------------------------


def test_filter_by_latency(
    optimizer,
    candidate1,
    candidate2,
):
    optimizer.maximum_latency = 200

    filtered = optimizer.filter_by_latency(
        [candidate1, candidate2]
    )

    assert len(filtered) == 1
    assert filtered[0].tool.name == "GPT-4"


def test_filter_by_latency_none(
    optimizer,
    candidate1,
):
    filtered = optimizer.filter_by_latency(
        [candidate1]
    )

    assert len(filtered) == 1


def test_filter_by_latency_statistics(
    optimizer,
    candidate1,
    candidate2,
):
    optimizer.maximum_latency = 150

    optimizer.filter_by_latency(
        [candidate1, candidate2]
    )

    assert (
        optimizer.statistics()["latency_filtered"]
        == 1
    )


# -------------------------------------------------
# Provider Preference
# -------------------------------------------------


def test_prioritize_provider(
    optimizer,
    candidate1,
    candidate2,
):
    optimizer.preferred_provider = "OpenAI"

    ranked = optimizer.prioritize_provider(
        [candidate2, candidate1]
    )

    assert ranked[0].tool.provider == "OpenAI"


def test_prioritize_case_insensitive(
    optimizer,
    candidate1,
):
    optimizer.preferred_provider = "openai"

    ranked = optimizer.prioritize_provider(
        [candidate1]
    )

    assert ranked[0].tool.provider == "OpenAI"


def test_prioritize_none(
    optimizer,
    candidate1,
):
    ranked = optimizer.prioritize_provider(
        [candidate1]
    )

    assert ranked[0] == candidate1


# -------------------------------------------------
# Optimize
# -------------------------------------------------


def test_optimize(
    optimizer,
    candidate1,
    candidate2,
):
    ranked = optimizer.optimize(
        [candidate1, candidate2]
    )

    assert len(ranked) == 2


def test_optimize_empty(
    optimizer,
):
    assert optimizer.optimize([]) == []


def test_optimize_statistics(
    optimizer,
    candidate1,
):
    optimizer.optimize([candidate1])

    stats = optimizer.statistics()

    assert stats["requests"] == 1
    assert stats["successful"] == 1


# -------------------------------------------------
# Selection
# -------------------------------------------------


def test_cheapest(
    optimizer,
    candidate1,
    candidate2,
):
    result = optimizer.cheapest(
        [candidate1, candidate2]
    )

    assert result.tool.average_cost == 0.01


def test_fastest(
    optimizer,
    candidate1,
    candidate2,
):
    result = optimizer.fastest(
        [candidate1, candidate2]
    )

    assert result.tool.average_latency_ms == 100


def test_best_value(
    optimizer,
    candidate1,
    candidate2,
):
    result = optimizer.best_value(
        [candidate1, candidate2]
    )

    assert result.total_score >= candidate2.total_score


def test_best_value_empty(
    optimizer,
):
    assert optimizer.best_value([]) is None


# -------------------------------------------------
# Statistics
# -------------------------------------------------


def test_clear_statistics(
    optimizer,
    candidate1,
):
    optimizer.optimize([candidate1])

    optimizer.clear_statistics()

    assert optimizer.statistics() == {}


# -------------------------------------------------
# Reset
# -------------------------------------------------


def test_reset(
    optimizer,
    candidate1,
):
    optimizer.maximum_cost = 0.05
    optimizer.maximum_latency = 100
    optimizer.preferred_provider = "OpenAI"

    optimizer.optimize([candidate1])

    optimizer.reset()

    config = optimizer.configuration()

    assert config["maximum_cost"] == float("inf")
    assert config["preferred_provider"] is None
    assert config["maximum_latency_ms"] is None
    assert optimizer.statistics() == {}


# -------------------------------------------------
# Dunder
# -------------------------------------------------


def test_len(
    optimizer,
):
    assert len(optimizer) == 3


def test_iter(
    optimizer,
):
    items = dict(iter(optimizer))

    assert "maximum_cost" in items
    assert "preferred_provider" in items
    assert "maximum_latency_ms" in items