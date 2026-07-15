import json

from app.planner.planner_validator import PlannerValidator


candidate_tools = [
    {
        "server": "github",
        "name": "list_repositories",
    },
    {
        "server": "github",
        "name": "list_branches",
    },
]

plan = [
    {
        "id": 1,
        "server": "github",
        "tool": "list_repositories",
        "arguments": {},
    },
    {
        "id": 2,
        "server": "github",
        "tool": "list_branches",
        "arguments": {
            "repository": "enterprise-mcp-platform",
        },
        "depends_on": [1],
    },
]

print("\nOriginal Plan\n")
print(json.dumps(plan, indent=2))

result = PlannerValidator.validate(
    plan,
    candidate_tools,
)

print("\nValidation Result\n")
print(json.dumps(result, indent=2))

print("\nSummary\n")
print(f"Valid     : {result['valid']}")
print(f"Errors    : {len(result['errors'])}")
print(f"Warnings  : {len(result['warnings'])}")