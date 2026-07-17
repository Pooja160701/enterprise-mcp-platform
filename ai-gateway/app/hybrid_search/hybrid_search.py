from __future__ import annotations

import time
from collections import Counter
from typing import List

from app.hybrid_search.bm25_search import BM25Search
from app.hybrid_search.keyword_search import KeywordSearch
from app.hybrid_search.metadata_filter import MetadataFilter
from app.hybrid_search.models import (
    HybridSearchResult,
    SearchDocument,
    SearchRequest,
)
from app.hybrid_search.ranking_fusion import RankingFusion
from app.hybrid_search.reranker import ReRanker
from app.hybrid_search.vector_search import VectorSearch


class HybridSearch:
    """
    Enterprise Hybrid Search

    Pipeline

    Metadata Filter
            │
            ▼
    Keyword Search
            │
            ▼
        BM25 Search
            │
            ▼
      Vector Search
            │
            ▼
      Reciprocal Rank Fusion
            │
            ▼
          ReRanker
            │
            ▼
        Final Results
    """

    def __init__(
        self,
        keyword_search: KeywordSearch | None = None,
        bm25_search: BM25Search | None = None,
        vector_search: VectorSearch | None = None,
        metadata_filter: MetadataFilter | None = None,
        ranking_fusion: RankingFusion | None = None,
        reranker: ReRanker | None = None,
    ):

        self.keyword_search = (
            keyword_search
            or KeywordSearch()
        )

        self.bm25_search = (
            bm25_search
            or BM25Search()
        )

        self.vector_search = (
            vector_search
            or VectorSearch()
        )

        self.metadata_filter = (
            metadata_filter
            or MetadataFilter()
        )

        self.ranking_fusion = (
            ranking_fusion
            or RankingFusion()
        )

        self.reranker = (
            reranker
            or ReRanker()
        )

        self._statistics = Counter()

    # -------------------------------------------------
    # Search
    # -------------------------------------------------

    def search(
        self,
        request: SearchRequest,
        documents: List[SearchDocument],
        query_embedding: List[float] | None = None,
    ) -> HybridSearchResult:

        start = time.perf_counter()

        self._statistics["requests"] += 1

        filtered_documents = self.metadata_filter.filter(
            documents,
            request.metadata_filter,
        )

        keyword_results = self.keyword_search.search(
            request,
            filtered_documents,
        )

        bm25_results = self.bm25_search.search(
            request,
            filtered_documents,
        )

        vector_results = []

        if query_embedding is not None:

            vector_results = self.vector_search.search(
                request,
                query_embedding,
                filtered_documents,
            )

        fused_results = self.ranking_fusion.fuse(
            [
                keyword_results,
                bm25_results,
                vector_results,
            ],
            top_k=request.top_k,
        )

        reranked_results = self.reranker.rerank(
            request,
            fused_results,
        )

        elapsed_ms = (
            time.perf_counter() - start
        ) * 1000

        self._statistics["returned"] += len(
            reranked_results
        )

        return HybridSearchResult(

            query=request.query,

            results=reranked_results,

            elapsed_ms=elapsed_ms,

        )

    # -------------------------------------------------
    # Convenience
    # -------------------------------------------------

    def best(
        self,
        request: SearchRequest,
        documents: List[SearchDocument],
        query_embedding: List[float] | None = None,
    ):

        result = self.search(
            request,
            documents,
            query_embedding,
        )

        if not result.results:

            return None

        return result.results[0]

    # -------------------------------------------------
    # Statistics
    # -------------------------------------------------

    def statistics(
        self,
    ):

        return {

            "hybrid_search":
                dict(self._statistics),

            "keyword":
                self.keyword_search.statistics(),

            "bm25":
                self.bm25_search.statistics(),

            "vector":
                self.vector_search.statistics(),

            "metadata":
                self.metadata_filter.statistics(),

            "fusion":
                self.ranking_fusion.statistics(),

            "reranker":
                self.reranker.statistics(),

        }

    def clear_statistics(
        self,
    ):

        self._statistics.clear()

        self.keyword_search.clear_statistics()

        self.bm25_search.clear_statistics()

        self.vector_search.clear_statistics()

        self.metadata_filter.clear_statistics()

        self.ranking_fusion.clear_statistics()

        self.reranker.clear_statistics()

    # -------------------------------------------------
    # Reset
    # -------------------------------------------------

    def reset(
        self,
    ):

        self.clear_statistics()

        self.keyword_search.reset()

        self.bm25_search.reset()

        self.vector_search.reset()

        self.metadata_filter.reset()

        self.ranking_fusion.reset()

        self.reranker.reset()

    # -------------------------------------------------
    # Configuration
    # -------------------------------------------------

    def configuration(
        self,
    ):

        return {

            "pipeline": [

                "metadata_filter",

                "keyword_search",

                "bm25_search",

                "vector_search",

                "ranking_fusion",

                "reranker",

            ],

            "algorithm": "hybrid",

        }

    # -------------------------------------------------
    # Dunder
    # -------------------------------------------------

    def __len__(
        self,
    ):

        return 6

    def __iter__(
        self,
    ):

        return iter(
            self.configuration().items()
        )