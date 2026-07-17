import json

from app.reasoning.decision_engine import DecisionEngine


print("\n=== Decision Engine Test ===\n")

engine = DecisionEngine()

# -------------------------------------------------
# Initial State
# -------------------------------------------------

print("Initializing Decision Engine\n")

print(
    json.dumps(
        engine.statistics(),
        indent=2,
    )
)

# -------------------------------------------------
# Tool Decision
# -------------------------------------------------

print("\nTool Decision\n")

engine.decide(
    query="List all GitHub repositories.",
)

print(
    json.dumps(
        engine.export(),
        indent=2,
    )
)

print("\nRequires Tool\n")

print(
    engine.requires_tool()
)

# -------------------------------------------------
# Parallel Decision
# -------------------------------------------------

print("\nParallel Decision\n")

engine.decide(
    query="List GitHub repositories and search filesystem together.",
)

print(
    json.dumps(
        engine.export(),
        indent=2,
    )
)

print("\nRequires Tool\n")

print(
    engine.requires_tool()
)

# -------------------------------------------------
# Clarification Decision
# -------------------------------------------------

print("\nClarification Decision\n")

engine.decide(
    query="Help me",
)

print(
    json.dumps(
        engine.export(),
        indent=2,
    )
)

# -------------------------------------------------
# Direct Answer Decision
# -------------------------------------------------

print("\nDirect Answer Decision\n")

engine.decide(
    query="What is artificial intelligence?",
)

print(
    json.dumps(
        engine.export(),
        indent=2,
    )
)

# -------------------------------------------------
# Statistics
# -------------------------------------------------

print("\nStatistics\n")

print(
    json.dumps(
        engine.statistics(),
        indent=2,
    )
)

# -------------------------------------------------
# Cleanup
# -------------------------------------------------

print("\nCleanup\n")

engine.clear()

print(
    json.dumps(
        engine.statistics(),
        indent=2,
    )
)

print("\nDecision Engine Test Passed")