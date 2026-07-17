from __future__ import annotations

import hashlib
import math

from .models import (
    EmbeddingProvider,
    EmbeddingRequest,
    EmbeddingResponse,
)


class Embeddings:
    """
    Production-ready embedding interface.

    Current provider:
        - Deterministic Mock Embeddings

    Future providers:
        - OpenAI
        - Azure OpenAI
        - Bedrock
        - SentenceTransformers
        - HuggingFace

    Public API remains unchanged.
    """

    DEFAULT_DIMENSIONS = 384

    def __init__(
        self,
        provider: EmbeddingProvider = EmbeddingProvider.MOCK,
        dimensions: int = DEFAULT_DIMENSIONS,
    ):

        if dimensions <= 0:
            raise ValueError("dimensions must be > 0")

        self.provider = provider
        self.dimensions = dimensions

        self._statistics: dict[str, int] = {}

    # ---------------------------------------------------------
    # Public API
    # ---------------------------------------------------------

    def embed(
        self,
        request: EmbeddingRequest,
    ) -> EmbeddingResponse:

        embeddings = []

        for text in request.texts:

            embeddings.append(
                self._embed_text(text)
            )

        self._statistics["requests"] = (
            self._statistics.get("requests", 0) + 1
        )

        self._statistics["texts"] = (
            self._statistics.get("texts", 0)
            + len(request.texts)
        )

        return EmbeddingResponse(
            provider=self.provider,
            dimensions=self.dimensions,
            embeddings=embeddings,
        )

    def embed_query(
        self,
        query: str,
    ) -> list[float]:

        self._statistics["queries"] = (
            self._statistics.get("queries", 0) + 1
        )

        return self._embed_text(query)

    # ---------------------------------------------------------
    # Mock Embedding Generator
    # ---------------------------------------------------------

    def _embed_text(
        self,
        text: str,
    ) -> list[float]:

        if not text:
            return [0.0] * self.dimensions

        digest = hashlib.sha256(
            text.encode("utf-8")
        ).digest()

        vector = []

        while len(vector) < self.dimensions:

            for byte in digest:

                value = (byte / 255.0) * 2.0 - 1.0

                vector.append(value)

                if len(vector) == self.dimensions:
                    break

        return self._normalize(vector)

    def _normalize(
        self,
        vector: list[float],
    ) -> list[float]:

        norm = math.sqrt(
            sum(v * v for v in vector)
        )

        if norm == 0:
            return vector

        return [
            v / norm
            for v in vector
        ]

    # ---------------------------------------------------------
    # Similarity
    # ---------------------------------------------------------

    def cosine_similarity(
        self,
        a: list[float],
        b: list[float],
    ) -> float:

        if len(a) != len(b):
            raise ValueError(
                "Embedding dimensions do not match."
            )

        denominator = (
            math.sqrt(sum(x * x for x in a))
            * math.sqrt(sum(y * y for y in b))
        )

        if denominator == 0:
            return 0.0

        numerator = sum(
            x * y
            for x, y in zip(a, b)
        )

        return numerator / denominator

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
            "provider": self.provider.value,
            "dimensions": self.dimensions,
            "algorithm": "deterministic_hash_embedding",
        }

    # ---------------------------------------------------------
    # Dunder
    # ---------------------------------------------------------

    def __len__(self):

        return self.dimensions

    def __iter__(self):

        yield from self.configuration().items()