from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
import time


# ---------------------------------------------------------
# Reasoning Step
# ---------------------------------------------------------

@dataclass
class ReasoningStep:

    name: str

    data: Any = None

    timestamp: float = field(
        default_factory=time.time
    )


# ---------------------------------------------------------
# Decision
# ---------------------------------------------------------

@dataclass
class Decision:

    decision: str

    reason: str = ""

    confidence: float = 1.0

    tools: List[Dict[str, Any]] = field(
        default_factory=list
    )

    timestamp: float = field(
        default_factory=time.time
    )


# ---------------------------------------------------------
# Tool Plan
# ---------------------------------------------------------

@dataclass
class ToolPlan:

    tool: str

    arguments: Dict[str, Any] = field(
        default_factory=dict
    )

    priority: int = 50

    parallel: bool = False

    depends_on: Optional[str] = None


# ---------------------------------------------------------
# Goal
# ---------------------------------------------------------

@dataclass
class Goal:

    id: int

    goal: str

    priority: int = 50

    status: str = "pending"

    progress: int = 0

    depends_on: Optional[int] = None

    created_at: float = field(
        default_factory=time.time
    )

    completed_at: Optional[float] = None


# ---------------------------------------------------------
# Reflection
# ---------------------------------------------------------

@dataclass
class ReflectionResult:

    summary: str

    confidence: float

    improvements: List[str] = field(
        default_factory=list
    )


# ---------------------------------------------------------
# Self Critique
# ---------------------------------------------------------

@dataclass
class CritiqueResult:

    passed: bool

    score: float

    issues: List[str] = field(
        default_factory=list
    )

    suggestions: List[str] = field(
        default_factory=list
    )


# ---------------------------------------------------------
# Reasoning Trace
# ---------------------------------------------------------

@dataclass
class Trace:

    query: str

    steps: List[ReasoningStep] = field(
        default_factory=list
    )

    decision: Optional[Decision] = None

    reflection: Optional[ReflectionResult] = None

    critique: Optional[CritiqueResult] = None

    response: Optional[Any] = None

    duration: float = 0.0


# ---------------------------------------------------------
# Complete Reasoning Result
# ---------------------------------------------------------

@dataclass
class ReasoningResult:

    reasoning: Dict[str, Any]

    decision: Dict[str, Any]

    tool_plan: List[Dict[str, Any]]

    reflection: Dict[str, Any]

    critique: Dict[str, Any]

    trace: Dict[str, Any]


# ---------------------------------------------------------
# Statistics
# ---------------------------------------------------------

@dataclass
class ReasoningStatistics:

    reasoning_steps: int = 0

    tool_calls: int = 0

    goals: int = 0

    completed_goals: int = 0

    duration: float = 0.0