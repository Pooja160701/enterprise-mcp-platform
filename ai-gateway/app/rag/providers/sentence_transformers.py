from __future__ import annotations

from sentence_transformers import SentenceTransformer

from ..models import (
    EmbeddingProvider,
    EmbeddingRequest,
    EmbeddingResponse,
)


class SentenceTransformerEmbeddings:
    """
    Sentence Transformers embedding provider.

    Popular models:
        - all-MiniLM-L6-v2
        - all-mpnet-base-v2
        - multi-qa-mpnet-base-dot-v1
        - bge-small-en-v1.5
        - bge-base-en-v1.5
        - bge-large-en-v1.5

    Works completely offline after the model
    has been downloaded.
    """

    def __init__(
        self,
        model_name: str = "all-MiniLM-L6-v2",
        device: str | None = None,
    ):

        self.model = SentenceTransformer(
            model_name,
            device=device,
        )

        self.model_name = model_name

        self._statistics: dict[str, int] = {}

    # ---------------------------------------------------------
    # Public API
    # ---------------------------------------------------------

    def embed(
        self,
        request: EmbeddingRequest,
    ) -> EmbeddingResponse:

        embeddings = self.model.encode(
            request.texts,
            convert_to_numpy=True,
            normalize_embeddings=True,
        )

        embeddings = embeddings.tolist()

        self._statistics["requests"] = (
            self._statistics.get("requests", 0) + 1
        )

        self._statistics["texts"] = (
            self._statistics.get("texts", 0)
            + len(request.texts)
        )

        return EmbeddingResponse(
            provider=EmbeddingProvider.SENTENCE_TRANSFORMERS,
            dimensions=len(embeddings[0]) if embeddings else 0,
            embeddings=embeddings,
        )

    def embed_query(
        self,
        query: str,
    ) -> list[float]:

        embedding = self.model.encode(
            query,
            convert_to_numpy=True,
            normalize_embeddings=True,
        )

        self._statistics["queries"] = (
            self._statistics.get("queries", 0) + 1
        )

        return embedding.tolist()

    # ---------------------------------------------------------
    # Similarity
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

        denominator1 = sum(
            a * a
            for a in embedding1
        ) ** 0.5

        denominator2 = sum(
            b * b
            for b in embedding2
        ) ** 0.5

        if denominator1 == 0 or denominator2 == 0:
            return 0.0

        return numerator / (denominator1 * denominator2)

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
            "provider": EmbeddingProvider.SENTENCE_TRANSFORMERS.value,
            "model": self.model_name,
            "dimensions": self.model.get_sentence_embedding_dimension(),
        }

    # ---------------------------------------------------------
    # Dunder
    # ---------------------------------------------------------

    def __len__(self):

        return self.model.get_sentence_embedding_dimension()

    def __iter__(self):

        yield from self.configuration().items()