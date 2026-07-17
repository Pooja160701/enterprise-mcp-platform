from __future__ import annotations

import hashlib
import math

from ..models import (
    EmbeddingProvider,
    EmbeddingRequest,
    EmbeddingResponse,
)


class MockEmbeddings:
    """
    Deterministic mock embedding provider.

    Designed for:
        - Unit tests
        - Local development
        - CI/CD pipelines
        - Offline execution

    Produces identical embeddings for identical input,
    making test results completely reproducible.
    """

    DEFAULT_DIMENSIONS = 384

    def __init__(
        self,
        dimensions: int = DEFAULT_DIMENSIONS,
    ):

        if dimensions <= 0:
            raise ValueError(
                "dimensions must be greater than zero."
            )

        self.dimensions = dimensions

        self._statistics: dict[str, int] = {}

    # ---------------------------------------------------------
    # Public API
    # ---------------------------------------------------------

    def embed(
        self,
        request: EmbeddingRequest,
    ) -> EmbeddingResponse:

        embeddings = [
            self.embed_query(text)
            for text in request.texts
        ]

        self._statistics["requests"] = (
            self._statistics.get("requests", 0) + 1
        )

        self._statistics["texts"] = (
            self._statistics.get("texts", 0)
            + len(request.texts)
        )

        return EmbeddingResponse(
            provider=EmbeddingProvider.MOCK,
            dimensions=self.dimensions,
            embeddings=embeddings,
        )

    def embed_query(
        self,
        text: str,
    ) -> list[float]:

        self._statistics["queries"] = (
            self._statistics.get("queries", 0) + 1
        )

        if not text:
            return [0.0] * self.dimensions

        digest = hashlib.sha256(
            text.encode("utf-8")
        ).digest()

        vector: list[float] = []

        while len(vector) < self.dimensions:

            for byte in digest:

                value = (byte / 255.0) * 2.0 - 1.0

                vector.append(value)

                if len(vector) == self.dimensions:
                    break

        return self._normalize(vector)

    # ---------------------------------------------------------
    # Utilities
    # ---------------------------------------------------------

    @staticmethod
    def cosine_similarity(
        embedding1: list[float],
        embedding2: list[float],
    ) -> float:

        if len(embedding1) != len(embedding2):
            raise ValueError(
                "Embedding dimensions do not match."
            )

        numerator = sum(
            a * b
            for a, b in zip(
                embedding1,
                embedding2,
            )
        )

        denominator1 = math.sqrt(
            sum(a * a for a in embedding1)
        )

        denominator2 = math.sqrt(
            sum(b * b for b in embedding2)
        )

        if denominator1 == 0 or denominator2 == 0:
            return 0.0

        return numerator / (
            denominator1 * denominator2
        )

    @staticmethod
    def _normalize(
        vector: list[float],
    ) -> list[float]:

        norm = math.sqrt(
            sum(v * v for v in vector)
        )

        if norm == 0:
            return vector

        return [
            value / norm
            for value in vector
        ]

    # ---------------------------------------------------------
    # Statistics
    # ---------------------------------------------------------

    def statistics(self) -> dict:

        return dict(self._statistics)

    def clear_statistics(self):

        self._statistics.clear()

    def reset(self):

        self.clear_statistics()

    # ---------------------------------------------------------
    # Configuration
    # ---------------------------------------------------------

    def configuration(self) -> dict:

        return {
            "provider": EmbeddingProvider.MOCK.value,
            "dimensions": self.dimensions,
            "deterministic": True,
        }

    # ---------------------------------------------------------
    # Dunder
    # ---------------------------------------------------------

    def __len__(self):

        return self.dimensions

    def __iter__(self):

        yield from self.configuration().items()