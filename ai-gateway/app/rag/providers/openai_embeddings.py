from __future__ import annotations

from openai import OpenAI

from ..models import (
    EmbeddingProvider,
    EmbeddingRequest,
    EmbeddingResponse,
)


class OpenAIEmbeddings:
    """
    OpenAI Embedding Provider.

    Supports:
        - text-embedding-3-small
        - text-embedding-3-large

    Uses the official OpenAI Python SDK.
    """

    def __init__(
        self,
        api_key: str,
        model: str = "text-embedding-3-small",
    ):

        self.client = OpenAI(api_key=api_key)
        self.model = model

        self._statistics: dict[str, int] = {}

    # ---------------------------------------------------------
    # Public API
    # ---------------------------------------------------------

    def embed(
        self,
        request: EmbeddingRequest,
    ) -> EmbeddingResponse:

        response = self.client.embeddings.create(
            model=self.model,
            input=request.texts,
        )

        embeddings = [
            item.embedding
            for item in response.data
        ]

        self._statistics["requests"] = (
            self._statistics.get("requests", 0) + 1
        )

        self._statistics["texts"] = (
            self._statistics.get("texts", 0)
            + len(request.texts)
        )

        return EmbeddingResponse(
            provider=EmbeddingProvider.OPENAI,
            dimensions=len(embeddings[0]) if embeddings else 0,
            embeddings=embeddings,
        )

    def embed_query(
        self,
        query: str,
    ) -> list[float]:

        response = self.client.embeddings.create(
            model=self.model,
            input=query,
        )

        self._statistics["queries"] = (
            self._statistics.get("queries", 0) + 1
        )

        return response.data[0].embedding

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
            "provider": EmbeddingProvider.OPENAI.value,
            "model": self.model,
        }

    # ---------------------------------------------------------
    # Dunder
    # ---------------------------------------------------------

    def __len__(self):

        return len(self.configuration())

    def __iter__(self):

        yield from self.configuration().items()