import pytest

from app.tool_selection.selection_manager import SelectionManager
from app.tool_selection.models import (
    IntentType,
    ToolMetadata,
)


@pytest.fixture
def manager():
    return SelectionManager()


@pytest.fixture
def search_tool():
    return ToolMetadata(
        name="Search",
        description="Search Tool",
        provider="OpenAI",
        capabilities=["SEARCH", "WEB"],
        reliability=0.95,
        confidence=0.95,
        average_latency_ms=100,
        average_cost=0.01,
        enabled=True,
    )


@pytest.fixture
def python_tool():
    return ToolMetadata(
        name="Python",
        description="Python Tool",
        provider="OpenAI",
        capabilities=["PYTHON"],
        reliability=0.90,
        confidence=0.90,
        average_latency_ms=200,
        average_cost=0.02,
        enabled=True,
    )


# -------------------------------------------------
# Intent Classification
# -------------------------------------------------


def test_classify(manager):
    result = manager.classify(
        "search the internet"
    )

    assert result.intent == IntentType.SEARCH


# -------------------------------------------------
# Capability Matching
# -------------------------------------------------


def test_match(manager, search_tool):
    intent = manager.classify(
        "search for weather"
    )

    candidates = manager.match(
        intent,
        [search_tool],
    )

    assert len(candidates) == 1


def test_match_empty(manager):
    intent = manager.classify(
        "search"
    )

    candidates = manager.match(
        intent,
        [],
    )

    assert candidates == []


# -------------------------------------------------
# Ranking
# -------------------------------------------------


def test_rank(manager, search_tool):
    intent = manager.classify(
        "search"
    )

    candidates = manager.match(
        intent,
        [search_tool],
    )

    ranked = manager.rank(
        candidates
    )

    assert len(ranked) == 1


# -------------------------------------------------
# Optimization
# -------------------------------------------------


def test_optimize(manager, search_tool):
    intent = manager.classify(
        "search"
    )

    candidates = manager.match(
        intent,
        [search_tool],
    )

    ranked = manager.rank(
        candidates
    )

    optimized = manager.optimize(
        ranked
    )

    assert len(optimized) == 1


# -------------------------------------------------
# Selection
# -------------------------------------------------


def test_select(manager, search_tool):
    intent = manager.classify(
        "search"
    )

    candidates = manager.match(
        intent,
        [search_tool],
    )

    ranked = manager.rank(
        candidates
    )

    optimized = manager.optimize(
        ranked
    )

    result = manager.select(
        optimized
    )

    assert result.selected.name == "Search"


# -------------------------------------------------
# Pipeline
# -------------------------------------------------


def test_pipeline(manager, search_tool):
    result = manager.pipeline(
        "search weather",
        [search_tool],
    )

    assert result.selected.name == "Search"


def test_pipeline_no_tools(manager):
    result = manager.pipeline(
        "search",
        [],
    )

    assert result.selected is None
    assert result.candidates == []


# -------------------------------------------------
# Execute
# -------------------------------------------------


def test_execute(manager, search_tool):
    result = manager.execute(
        "search",
        [search_tool],
        lambda c: c.tool.name,
    )

    assert result == "Search"


def test_execute_no_candidates(manager):
    with pytest.raises(RuntimeError):
        manager.execute(
            "search",
            [],
            lambda c: c,
        )


# -------------------------------------------------
# Best Tool
# -------------------------------------------------


def test_best_tool(manager, search_tool):
    tool = manager.best_tool(
        "search",
        [search_tool],
    )

    assert tool.name == "Search"


def test_best_tool_none(manager):
    assert (
        manager.best_tool(
            "search",
            [],
        )
        is None
    )


# -------------------------------------------------
# Top Tools
# -------------------------------------------------


def test_top_tools(
    manager,
    search_tool,
    python_tool,
):
    tools = manager.top_tools(
        "search",
        [
            search_tool,
            python_tool,
        ],
        limit=1,
    )

    assert len(tools) == 1
    assert tools[0].name == "Search"


def test_top_tools_empty(manager):
    assert (
        manager.top_tools(
            "search",
            [],
        )
        == []
    )


# -------------------------------------------------
# Statistics
# -------------------------------------------------


def test_statistics(
    manager,
    search_tool,
):
    manager.pipeline(
        "search",
        [search_tool],
    )

    stats = manager.statistics()

    assert "intent_classifier" in stats
    assert "tool_ranker" in stats
    assert "cost_optimizer" in stats
    assert "fallback_manager" in stats


# -------------------------------------------------
# Reset
# -------------------------------------------------


def test_reset(
    manager,
    search_tool,
):
    manager.pipeline(
        "search",
        [search_tool],
    )

    manager.reset()

    stats = manager.statistics()

    for value in stats.values():
        assert value == {}


# -------------------------------------------------
# Configuration
# -------------------------------------------------


def test_configuration(manager):
    config = manager.configuration()

    assert "minimum_confidence" in config
    assert "maximum_cost" in config
    assert "preferred_provider" in config
    assert "maximum_latency" in config
    assert "max_retries" in config
    assert "retry_delay" in config


# -------------------------------------------------
# Dunder
# -------------------------------------------------


def test_len(manager):
    assert len(manager) == 6


def test_iter(manager):
    items = dict(iter(manager))

    assert len(items) == 6

    assert "intent_classifier" in items
    assert "capability_matcher" in items
    assert "tool_ranker" in items
    assert "cost_optimizer" in items
    assert "confidence_selector" in items
    assert "fallback_manager" in items


# -------------------------------------------------
# Edge Cases
# -------------------------------------------------


def test_pipeline_unknown_prompt(
    manager,
    search_tool,
):
    result = manager.pipeline(
        "",
        [search_tool],
    )

    assert result is not None


def test_execute_returns_candidate(
    manager,
    search_tool,
):
    result = manager.execute(
        "search",
        [search_tool],
        lambda c: c,
    )

    assert result.tool.name == "Search"