from __future__ import annotations

from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class SearchType(str, Enum):
    KEYWORD = "keyword"
    BM25 = "bm25"
    VECTOR = "vector"
    HYBRID = "hybrid"


class SearchDocument(BaseModel):
    id: str

    text: str

    metadata: Dict[str, Any] = Field(
        default_factory=dict
    )

    embedding: Optional[List[float]] = None


class SearchResult(BaseModel):
    document: SearchDocument

    score: float = 0.0

    rank: int = 0

    source: SearchType


class SearchRequest(BaseModel):
    query: str

    top_k: int = 10

    metadata_filter: Dict[str, Any] = Field(
        default_factory=dict
    )

    search_type: SearchType = SearchType.HYBRID


class HybridSearchResult(BaseModel):
    query: str

    results: List[SearchResult] = Field(
        default_factory=list
    )

    elapsed_ms: float = 0.0