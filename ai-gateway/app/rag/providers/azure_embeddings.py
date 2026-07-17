from __future__ import annotations

from openai import AzureOpenAI

from ..models import (
    EmbeddingProvider,
    EmbeddingRequest,
    EmbeddingResponse,
)


class AzureOpenAIEmbeddings:
    """
    Azure OpenAI Embedding Provider.

    Supports:
        - text-embedding-3-small
        - text-embedding-3-large
        - Custom Azure deployments

    Uses the official OpenAI Python SDK with Azure support.
    """

    def __init__(
        self,
        api_key: str,
        azure_endpoint: str,
        api_version: str,
        deployment: str,
    ):

        self.client = AzureOpenAI(
            api_key=api_key,
            azure_endpoint=azure_endpoint,
            api_version=api_version,
        )

        # Azure uses deployment names instead of model names
        self.deployment = deployment

        self._statistics: dict[str, int] = {}

    # ---------------------------------------------------------
    # Public API
    # ---------------------------------------------------------

    def embed(
        self,
        request: EmbeddingRequest,
    ) -> EmbeddingResponse:

        response = self.client.embeddings.create(
            model=self.deployment,
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
            provider=EmbeddingProvider.AZURE,
            dimensions=len(embeddings[0]) if embeddings else 0,
            embeddings=embeddings,
        )

    def embed_query(
        self,
        query: str,
    ) -> list[float]:

        response = self.client.embeddings.create(
            model=self.deployment,
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
            "provider": EmbeddingProvider.AZURE.value,
            "deployment": self.deployment,
        }

    # ---------------------------------------------------------
    # Dunder
    # ---------------------------------------------------------

    def __len__(self):

        return len(self.configuration())

    def __iter__(self):

        yield from self.configuration().items()