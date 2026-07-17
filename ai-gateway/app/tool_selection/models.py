from __future__ import annotations

from enum import Enum
from typing import Dict, List, Optional

from pydantic import BaseModel, Field


# ---------------------------------------------------------
# Intent
# ---------------------------------------------------------


class IntentType(str, Enum):
    SEARCH = "search"
    CALCULATE = "calculate"
    CODE = "code"
    DATABASE = "database"
    FILESYSTEM = "filesystem"
    WEB = "web"
    EMAIL = "email"
    CALENDAR = "calendar"
    CHAT = "chat"
    ANALYTICS = "analytics"
    UNKNOWN = "unknown"


# ---------------------------------------------------------
# Capability
# ---------------------------------------------------------


class Capability(str, Enum):
    SEARCH = "search"
    REASONING = "reasoning"
    PYTHON = "python"
    SQL = "sql"
    FILESYSTEM = "filesystem"
    WEB = "web"
    IMAGE = "image"
    EMAIL = "email"
    CALENDAR = "calendar"
    VECTOR_DB = "vector_db"
    API = "api"
    MEMORY = "memory"


# ---------------------------------------------------------
# Tool Metadata
# ---------------------------------------------------------


class ToolMetadata(BaseModel):
    name: str

    description: str

    version: str = "1.0.0"

    provider: str = "internal"

    capabilities: List[Capability] = Field(
        default_factory=list
    )

    enabled: bool = True

    average_latency_ms: float = 0

    average_cost: float = 0

    reliability: float = 1.0

    confidence: float = 1.0


# ---------------------------------------------------------
# Intent Result
# ---------------------------------------------------------


class IntentResult(BaseModel):
    intent: IntentType

    confidence: float

    entities: List[str] = Field(
        default_factory=list
    )


# ---------------------------------------------------------
# Tool Candidate
# ---------------------------------------------------------


class ToolCandidate(BaseModel):
    tool: ToolMetadata

    capability_score: float = 0

    confidence_score: float = 0

    latency_score: float = 0

    cost_score: float = 0

    reliability_score: float = 0

    total_score: float = 0


# ---------------------------------------------------------
# Selection Result
# ---------------------------------------------------------


class SelectionResult(BaseModel):
    selected: Optional[ToolMetadata] = None

    candidates: List[ToolCandidate] = Field(
        default_factory=list
    )

    fallback_tools: List[ToolMetadata] = Field(
        default_factory=list
    )

    reason: str = ""


# ---------------------------------------------------------
# Ranking Configuration
# ---------------------------------------------------------


class RankingWeights(BaseModel):
    capability: float = 0.40

    confidence: float = 0.25

    reliability: float = 0.15

    latency: float = 0.10

    cost: float = 0.10


# ---------------------------------------------------------
# Statistics
# ---------------------------------------------------------


class SelectionStatistics(BaseModel):
    requests: int = 0

    successful: int = 0

    fallback_used: int = 0

    average_latency_ms: float = 0

    average_cost: float = 0

    tool_usage: Dict[str, int] = Field(
        default_factory=dict
    )