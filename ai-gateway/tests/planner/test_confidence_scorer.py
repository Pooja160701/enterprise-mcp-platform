import json

from app.planner.confidence_scorer import ConfidenceScorer


plan = [
    {
        "id": 1,
        "server": "github",
        "tool": "list_branches",
        "arguments": {
            "repository": "enterprise-mcp-platform",
        },
        "depends_on": [],
    },
    {
        "id": 2,
        "server": "github",
        "tool": "latest_commit",
        "arguments": {
            "repository": "enterprise-mcp-platform",
        },
        "depends_on": [1],
    },
]


print("\nExecution Plan\n")

print(
    json.dumps(
        plan,
        indent=2,
    )
)

result = ConfidenceScorer.score(plan)

print("\nConfidence Result\n")

print(
    json.dumps(
        result,
        indent=2,
    )
)

print("\nSummary\n")

print(f"Score  : {result['score']}")
print(f"Grade  : {result['grade']}")
print(f"Status : {result['status']}")