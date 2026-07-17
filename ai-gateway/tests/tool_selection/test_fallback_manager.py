import pytest

from app.tool_selection.fallback_manager import FallbackManager
from app.tool_selection.models import ToolCandidate, ToolMetadata


@pytest.fixture
def manager():
    return FallbackManager()


@pytest.fixture
def tool1():
    return ToolCandidate(
        tool=ToolMetadata(
            name="GPT4",
            description="",
            provider="OpenAI",
            capabilities=[],
            reliability=0.95,
            confidence=0.95,
            average_latency_ms=100,
            average_cost=0.01,
            enabled=True,
        ),
        total_score=0.95,
    )


@pytest.fixture
def tool2():
    return ToolCandidate(
        tool=ToolMetadata(
            name="Claude",
            description="",
            provider="Anthropic",
            capabilities=[],
            reliability=0.90,
            confidence=0.90,
            average_latency_ms=200,
            average_cost=0.02,
            enabled=True,
        ),
        total_score=0.90,
    )


# -------------------------------------------------
# Execute One
# -------------------------------------------------


def test_execute_one_success(manager, tool1):
    def executor(candidate):
        return candidate.tool.name

    result = manager.execute_one(tool1, executor)

    assert result == "GPT4"


def test_execute_one_failure(manager, tool1):
    def executor(candidate):
        raise RuntimeError("failed")

    with pytest.raises(RuntimeError):
        manager.execute_one(tool1, executor)


# -------------------------------------------------
# Execute
# -------------------------------------------------


def test_execute_first_success(manager, tool1, tool2):
    def executor(candidate):
        return candidate.tool.name

    result = manager.execute(
        [tool1, tool2],
        executor,
    )

    assert result == "GPT4"


def test_execute_second_after_failure(manager, tool1, tool2):
    calls = []

    def executor(candidate):
        calls.append(candidate.tool.name)

        if candidate.tool.name == "GPT4":
            raise RuntimeError()

        return candidate.tool.name

    result = manager.execute(
        [tool1, tool2],
        executor,
    )

    assert result == "Claude"
    assert len(calls) == 2


def test_execute_all_fail(manager, tool1, tool2):
    def executor(candidate):
        raise RuntimeError()

    with pytest.raises(RuntimeError):
        manager.execute(
            [tool1, tool2],
            executor,
        )


def test_execute_empty(manager):
    with pytest.raises(RuntimeError):
        manager.execute(
            [],
            lambda x: x,
        )


# -------------------------------------------------
# Retry
# -------------------------------------------------


def test_retry_success(manager, tool1):
    counter = {"count": 0}

    def executor(candidate):
        counter["count"] += 1

        if counter["count"] == 1:
            raise RuntimeError()

        return "success"

    result = manager.execute(
        [tool1],
        executor,
    )

    assert result == "success"


def test_retry_limit(manager, tool1):
    manager.max_retries = 1

    def executor(candidate):
        raise RuntimeError()

    with pytest.raises(RuntimeError):
        manager.execute(
            [tool1],
            executor,
        )


# -------------------------------------------------
# Statistics
# -------------------------------------------------


def test_statistics(manager, tool1):
    def executor(candidate):
        return True

    manager.execute(
        [tool1],
        executor,
    )

    stats = manager.statistics()

    assert "requests" in stats


def test_clear_statistics(manager):
    manager.clear_statistics()

    assert manager.statistics() == {}


# -------------------------------------------------
# Reset
# -------------------------------------------------


def test_reset(manager):
    manager.max_retries = 10
    manager.retry_delay = 5

    manager.reset()

    config = manager.configuration()

    assert manager.statistics() == {}

    assert config["max_retries"] >= 0
    assert config["retry_delay"] >= 0


# -------------------------------------------------
# Configuration
# -------------------------------------------------


def test_configuration(manager):
    config = manager.configuration()

    assert "max_retries" in config
    assert "retry_delay" in config


# -------------------------------------------------
# Dunder
# -------------------------------------------------


def test_len(manager):
    assert len(manager) == 2


def test_iter(manager):
    config = dict(iter(manager))

    assert "max_retries" in config
    assert "retry_delay" in config


# -------------------------------------------------
# Edge Cases
# -------------------------------------------------


def test_execute_single_candidate(manager, tool1):
    result = manager.execute(
        [tool1],
        lambda c: c.tool.name,
    )

    assert result == "GPT4"


def test_execute_returns_object(manager, tool1):
    result = manager.execute(
        [tool1],
        lambda c: c,
    )

    assert result.tool.name == "GPT4"


def test_multiple_failures_before_success(manager, tool1, tool2):
    counter = {"count": 0}

    def executor(candidate):
        counter["count"] += 1

        if counter["count"] < 3:
            raise RuntimeError()

        return "done"

    result = manager.execute(
        [tool1, tool2],
        executor,
    )

    assert result == "done"