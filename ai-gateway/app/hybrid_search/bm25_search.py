from __future__ import annotations

import math
from collections import Counter
from typing import Dict, List

from app.hybrid_search.models import (
    SearchDocument,
    SearchRequest,
    SearchResult,
    SearchType,
)


class BM25Search:
    """
    Enterprise BM25 Search

    Responsibilities
    ----------------
    • BM25 lexical ranking
    • IDF computation
    • Document length normalization
    • Top-K retrieval
    • Statistics collection
    """

    def __init__(
        self,
        k1: float = 1.5,
        b: float = 0.75,
    ):
        self._k1 = k1
        self._b = b

        self._statistics = Counter()

    # -------------------------------------------------
    # Search
    # -------------------------------------------------

    def search(
        self,
        request: SearchRequest,
        documents: List[SearchDocument],
    ) -> List[SearchResult]:

        self._statistics["requests"] += 1

        if not documents:
            return []

        corpus = [
            self._tokenize(doc.text)
            for doc in documents
        ]

        avg_doc_length = (
            sum(len(doc) for doc in corpus)
            / len(corpus)
        )

        idf = self._compute_idf(corpus)

        query_terms = self._tokenize(
            request.query
        )

        results = []

        for document, tokens in zip(
            documents,
            corpus,
        ):

            score = self._bm25_score(
                query_terms=query_terms,
                document=tokens,
                idf=idf,
                avg_doc_length=avg_doc_length,
            )

            if score <= 0:
                continue

            results.append(

                SearchResult(
                    document=document,
                    score=score,
                    source=SearchType.BM25,
                )

            )

        results.sort(
            key=lambda r: r.score,
            reverse=True,
        )

        for rank, result in enumerate(
            results,
            start=1,
        ):
            result.rank = rank

        self._statistics["matched"] += len(
            results
        )

        return results[: request.top_k]

    # -------------------------------------------------
    # BM25 Score
    # -------------------------------------------------

    def _bm25_score(
        self,
        query_terms: List[str],
        document: List[str],
        idf: Dict[str, float],
        avg_doc_length: float,
    ) -> float:

        tf = Counter(document)

        score = 0.0

        doc_length = len(document)

        for term in query_terms:

            if term not in tf:
                continue

            frequency = tf[term]

            numerator = frequency * (
                self._k1 + 1
            )

            denominator = (
                frequency
                + self._k1
                * (
                    1
                    - self._b
                    + self._b
                    * doc_length
                    / avg_doc_length
                )
            )

            score += idf.get(term, 0.0) * (
                numerator / denominator
            )

        return score

    # -------------------------------------------------
    # IDF
    # -------------------------------------------------

    def _compute_idf(
        self,
        corpus: List[List[str]],
    ) -> Dict[str, float]:

        document_count = len(corpus)

        frequencies = Counter()

        for document in corpus:

            frequencies.update(
                set(document)
            )

        idf = {}

        for term, freq in frequencies.items():

            idf[term] = math.log(
                (
                    document_count
                    - freq
                    + 0.5
                )
                /
                (
                    freq
                    + 0.5
                )
                + 1
            )

        return idf

    # -------------------------------------------------
    # Tokenizer
    # -------------------------------------------------

    def _tokenize(
        self,
        text: str,
    ) -> List[str]:

        return [

            token

            for token

            in text.lower().split()

            if token

        ]

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
    # Reset
    # -------------------------------------------------

    def reset(
        self,
    ):

        self.clear_statistics()

    # -------------------------------------------------
    # Configuration
    # -------------------------------------------------

    def configuration(
        self,
    ) -> dict:

        return {

            "algorithm": "bm25",

            "k1": self._k1,

            "b": self._b,

        }

    # -------------------------------------------------
    # Dunder
    # -------------------------------------------------

    def __len__(
        self,
    ):

        return 3

    def __iter__(
        self,
    ):

        return iter(
            self.configuration().items()
        )