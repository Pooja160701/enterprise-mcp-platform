from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


# ---------------------------------------------------------
# Enums
# ---------------------------------------------------------


class DocumentType(str, Enum):
    TEXT = "text"
    MARKDOWN = "markdown"
    PDF = "pdf"
    HTML = "html"
    DOCX = "docx"
    UNKNOWN = "unknown"


class EmbeddingProvider(str, Enum):
    MOCK = "mock"
    OPENAI = "openai"
    AZURE = "azure"
    SENTENCE_TRANSFORMERS = "sentence_transformers"


class VectorStoreType(str, Enum):
    MEMORY = "memory"
    CHROMA = "chroma"
    FAISS = "faiss"
    QDRANT = "qdrant"
    PINECONE = "pinecone"


# ---------------------------------------------------------
# Metadata
# ---------------------------------------------------------


class ChunkMetadata(BaseModel):
    document_id: str
    filename: str
    document_type: DocumentType = DocumentType.TEXT
    chunk_index: int = 0
    page: int | None = None
    start_char: int = 0
    end_char: int = 0
    source: str | None = None
    extra: dict[str, Any] = Field(default_factory=dict)


# ---------------------------------------------------------
# Documents
# ---------------------------------------------------------


class Document(BaseModel):
    id: str
    filename: str
    content: str
    document_type: DocumentType = DocumentType.TEXT
    metadata: dict[str, Any] = Field(default_factory=dict)


class DocumentChunk(BaseModel):
    id: str
    document_id: str
    text: str
    metadata: ChunkMetadata
    embedding: list[float] = Field(default_factory=list)


# ---------------------------------------------------------
# Embeddings
# ---------------------------------------------------------


class EmbeddingRequest(BaseModel):
    texts: list[str]
    provider: EmbeddingProvider = EmbeddingProvider.MOCK


class EmbeddingResponse(BaseModel):
    provider: EmbeddingProvider
    dimensions: int
    embeddings: list[list[float]]


# ---------------------------------------------------------
# Retrieval
# ---------------------------------------------------------


class RetrievalRequest(BaseModel):
    query: str
    top_k: int = 5
    filters: dict[str, Any] = Field(default_factory=dict)


class RetrievalResult(BaseModel):
    chunk: DocumentChunk
    score: float


# ---------------------------------------------------------
# Citations
# ---------------------------------------------------------


class Citation(BaseModel):
    index: int
    document_id: str
    filename: str
    chunk_id: str
    page: int | None = None
    source: str | None = None
    score: float


class CitationResult(BaseModel):
    citations: list[Citation] = Field(default_factory=list)


# ---------------------------------------------------------
# Answer Generation
# ---------------------------------------------------------


class AnswerRequest(BaseModel):
    question: str
    top_k: int = 5
    filters: dict[str, Any] = Field(default_factory=dict)


class AnswerResponse(BaseModel):
    answer: str
    citations: list[Citation] = Field(default_factory=list)
    retrieved_chunks: list[RetrievalResult] = Field(default_factory=list)


# ---------------------------------------------------------
# Vector Store
# ---------------------------------------------------------


class VectorStoreStats(BaseModel):
    documents: int = 0
    chunks: int = 0
    dimensions: int = 0
    provider: EmbeddingProvider = EmbeddingProvider.MOCK
    store: VectorStoreType = VectorStoreType.MEMORY