from __future__ import annotations

from .citation_engine import CitationEngine
from .models import (
    AnswerRequest,
    AnswerResponse,
)
from .retrieval import RetrievalEngine


class AnswerGenerator:
    """
    Production-ready RAG answer generator.

    Responsibilities
    ----------------
    - Retrieve relevant chunks
    - Generate citations
    - Build context
    - Produce an answer

    Current implementation:
        - Mock answer generation

    Future implementations:
        - OpenAI GPT
        - Azure OpenAI
        - Anthropic Claude
        - Google Gemini
        - Local LLMs (Llama, Mistral)
    """

    def __init__(
        self,
        retrieval_engine: RetrievalEngine,
        citation_engine: CitationEngine,
    ):

        self.retrieval_engine = retrieval_engine
        self.citation_engine = citation_engine

        self._statistics: dict[str, int] = {}

    # ---------------------------------------------------------
    # Public API
    # ---------------------------------------------------------

    def generate(
        self,
        request: AnswerRequest,
    ) -> AnswerResponse:

        retrieval_results = self.retrieval_engine.retrieve(
            request=request,
        )

        citation_result = self.citation_engine.generate(
            retrieval_results,
        )

        context = self._build_context(
            retrieval_results,
        )

        answer = self._generate_answer(
            question=request.question,
            context=context,
        )

        self._statistics["requests"] = (
            self._statistics.get("requests", 0) + 1
        )

        self._statistics["answers"] = (
            self._statistics.get("answers", 0) + 1
        )

        self._statistics["retrieved_chunks"] = (
            self._statistics.get("retrieved_chunks", 0)
            + len(retrieval_results)
        )

        return AnswerResponse(
            answer=answer,
            citations=citation_result.citations,
            retrieved_chunks=retrieval_results,
        )

    # ---------------------------------------------------------
    # Context Builder
    # ---------------------------------------------------------

    def _build_context(
        self,
        results,
    ) -> str:

        if not results:
            return ""

        return "\n\n".join(
            result.chunk.text
            for result in results
        )

    # ---------------------------------------------------------
    # Mock LLM
    # ---------------------------------------------------------

    def _generate_answer(
        self,
        question: str,
        context: str,
    ) -> str:

        if not context.strip():

            return (
                "I could not find any relevant information "
                "to answer your question."
            )

        preview = context[:500]

        return (
            f"Question:\n{question}\n\n"
            f"Answer:\n"
            f"The following answer was generated using the "
            f"retrieved context.\n\n"
            f"{preview}"
            f"{'...' if len(context) > 500 else ''}"
        )

    # ---------------------------------------------------------
    # Convenience API
    # ---------------------------------------------------------

    def ask(
        self,
        question: str,
        top_k: int = 5,
        filters: dict | None = None,
    ) -> AnswerResponse:

        return self.generate(
            AnswerRequest(
                question=question,
                top_k=top_k,
                filters=filters or {},
            )
        )

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
            "retrieval_engine": type(
                self.retrieval_engine
            ).__name__,
            "citation_engine": type(
                self.citation_engine
            ).__name__,
            "generator": "mock_llm",
        }

    # ---------------------------------------------------------
    # Dunder
    # ---------------------------------------------------------

    def __len__(self):

        return 3

    def __iter__(self):

        yield from self.configuration().items()