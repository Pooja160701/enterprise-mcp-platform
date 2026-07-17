from __future__ import annotations

import time
from collections import Counter
from typing import Any, Callable, Dict, List, Optional

from app.tool_selection.models import (
    ToolCandidate,
)


class FallbackManager:
    """
    Enterprise Fallback Manager

    Responsibilities
    ----------------
    • Execute tools with automatic fallback
    • Retry failed tools
    • Handle exceptions
    • Maintain execution statistics
    • Track failure history
    """

    def __init__(
        self,
        max_retries: int = 1,
        retry_delay: float = 0.5,
    ):

        self._max_retries = max(0, max_retries)
        self._retry_delay = max(0.0, retry_delay)

        self._statistics = Counter()

        self._failures: Dict[str, int] = {}

    # -------------------------------------------------
    # Execute
    # -------------------------------------------------

    def execute(
        self,
        candidates: List[ToolCandidate],
        executor: Callable[[ToolCandidate], Any],
    ) -> Any:

        if not candidates:

            raise RuntimeError(
                "No candidate tools available."
            )

        self._statistics["requests"] += 1

        last_exception = None

        for candidate in candidates:

            tool = candidate.tool

            retries = 0

            while retries <= self._max_retries:

                try:

                    result = executor(candidate)

                    self._statistics["success"] += 1

                    self._statistics[
                        tool.name
                    ] += 1

                    return result

                except Exception as exc:

                    last_exception = exc

                    retries += 1

                    self._statistics["errors"] += 1

                    self._failures[
                        tool.name
                    ] = (
                        self._failures.get(
                            tool.name,
                            0,
                        )
                        + 1
                    )

                    if retries <= self._max_retries:

                        time.sleep(
                            self._retry_delay
                        )

            self._statistics[
                "fallbacks"
            ] += 1

        raise RuntimeError(
            "All candidate tools failed."
        ) from last_exception

    # -------------------------------------------------
    # Single Tool
    # -------------------------------------------------

    def execute_one(
        self,
        candidate: ToolCandidate,
        executor: Callable[[ToolCandidate], Any],
    ) -> Any:

        return self.execute(
            [candidate],
            executor,
        )

    # -------------------------------------------------
    # Failure History
    # -------------------------------------------------

    def failures(
        self,
    ) -> Dict[str, int]:

        return dict(
            self._failures
        )

    def failure_count(
        self,
        tool_name: str,
    ) -> int:

        return self._failures.get(
            tool_name,
            0,
        )

    def clear_failures(
        self,
    ):

        self._failures.clear()

    # -------------------------------------------------
    # Statistics
    # -------------------------------------------------

    def statistics(
        self,
    ) -> dict:

        return dict(
            self._statistics
        )

    def clear_statistics(
        self,
    ):

        self._statistics.clear()

    # -------------------------------------------------
    # Configuration
    # -------------------------------------------------

    @property
    def max_retries(
        self,
    ) -> int:

        return self._max_retries

    @max_retries.setter
    def max_retries(
        self,
        value: int,
    ):

        self._max_retries = max(
            0,
            value,
        )

    @property
    def retry_delay(
        self,
    ) -> float:

        return self._retry_delay

    @retry_delay.setter
    def retry_delay(
        self,
        value: float,
    ):

        self._retry_delay = max(
            0.0,
            value,
        )

    def configuration(
        self,
    ) -> dict:

        return {
            "max_retries": self._max_retries,
            "retry_delay": self._retry_delay,
        }

    # -------------------------------------------------
    # Reset
    # -------------------------------------------------

    def reset(
        self,
    ):

        self._max_retries = 1
        self._retry_delay = 0.5

        self.clear_statistics()
        self.clear_failures()

    # -------------------------------------------------
    # Dunder
    # -------------------------------------------------

    def __len__(
        self,
    ):

        return len(
            self._failures
        )

    def __contains__(
        self,
        tool_name: str,
    ):

        return tool_name in self._failures

    def __iter__(
        self,
    ):

        return iter(
            self._failures.items()
        )