import json

from app.reasoning.reflection import Reflection


print("\n=== Reflection Test ===\n")

reflection = Reflection()

# -------------------------------------------------
# Initial State
# -------------------------------------------------

print("Initializing Reflection\n")

print(
    json.dumps(
        reflection.statistics(),
        indent=2,
    )
)

# -------------------------------------------------
# Run Reflection
# -------------------------------------------------

print("\nRunning Reflection\n")

reflection.reflect(
    query="List all GitHub repositories.",
    response="Found 12 repositories.",
)

# -------------------------------------------------
# Query
# -------------------------------------------------

print("Query\n")

print(
    reflection.query()
)

# -------------------------------------------------
# Response
# -------------------------------------------------

print("\nResponse\n")

print(
    reflection.response()
)

# -------------------------------------------------
# Observations
# -------------------------------------------------

print("\nObservations\n")

print(
    json.dumps(
        reflection.observations(),
        indent=2,
    )
)

# -------------------------------------------------
# Suggestions
# -------------------------------------------------

print("\nSuggestions\n")

print(
    json.dumps(
        reflection.suggestions(),
        indent=2,
    )
)

# -------------------------------------------------
# Successful
# -------------------------------------------------

print("\nSuccessful\n")

print(
    reflection.successful()
)

# -------------------------------------------------
# Statistics
# -------------------------------------------------

print("\nStatistics\n")

print(
    json.dumps(
        reflection.statistics(),
        indent=2,
    )
)

# -------------------------------------------------
# Export
# -------------------------------------------------

print("\nExport\n")

print(
    json.dumps(
        reflection.export(),
        indent=2,
    )
)

# -------------------------------------------------
# Cleanup
# -------------------------------------------------

print("\nCleanup\n")

reflection.clear()

print(
    json.dumps(
        reflection.statistics(),
        indent=2,
    )
)

print("\nReflection Test Passed ✓")