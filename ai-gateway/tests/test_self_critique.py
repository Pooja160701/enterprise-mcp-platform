import json

from app.reasoning.self_critique import SelfCritique


print("\n=== Self Critique Test ===\n")

critique = SelfCritique()

# -------------------------------------------------
# Initial State
# -------------------------------------------------

print("Initializing Self Critique\n")

print(
    json.dumps(
        critique.statistics(),
        indent=2,
    )
)

# -------------------------------------------------
# Run Critique
# -------------------------------------------------

print("\nRunning Self Critique\n")

critique.critique(
    query="List all GitHub repositories.",
    response="Found 12 GitHub repositories successfully.",
)

# -------------------------------------------------
# Approved
# -------------------------------------------------

print("Approved\n")

print(
    critique.approved()
)

# -------------------------------------------------
# Confidence
# -------------------------------------------------

print("\nConfidence\n")

print(
    critique.confidence()
)

# -------------------------------------------------
# Issues
# -------------------------------------------------

print("\nIssues\n")

print(
    json.dumps(
        critique.issues(),
        indent=2,
    )
)

# -------------------------------------------------
# Recommendations
# -------------------------------------------------

print("\nRecommendations\n")

print(
    json.dumps(
        critique.recommendations(),
        indent=2,
    )
)

# -------------------------------------------------
# Statistics
# -------------------------------------------------

print("\nStatistics\n")

print(
    json.dumps(
        critique.statistics(),
        indent=2,
    )
)

# -------------------------------------------------
# Export
# -------------------------------------------------

print("\nExport\n")

print(
    json.dumps(
        critique.export(),
        indent=2,
    )
)

# -------------------------------------------------
# Cleanup
# -------------------------------------------------

print("\nCleanup\n")

critique.clear()

print(
    json.dumps(
        critique.statistics(),
        indent=2,
    )
)

print("\nSelf Critique Test Passed ✓")