import json

from app.planner.cost_optimizer import CostOptimizer


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
        "tool": "list_repositories",
        "arguments": {},
    },
    {
        "id": 3,
        "server": "github",
        "tool": "list_branches",
        "arguments": {
            "repository": "enterprise-mcp-platform",
        },
    },
    {
        "id": 4,
        "server": "github",
        "tool": "list_branches",
        "arguments": {
            "repository": "enterprise-mcp-platform",
        },
    },
]

print("\nOriginal Plan\n")

print(
    json.dumps(
        plan,
        indent=2,
    )
)

optimized = CostOptimizer.optimize(plan)

print("\nOptimized Plan\n")

print(
    json.dumps(
        optimized,
        indent=2,
    )
)

print("\nStatistics\n")

print(f"Original Steps : {len(plan)}")
print(f"Optimized Steps: {len(optimized['plan'])}")

print(f"\nEstimated Cost : {optimized['estimated_cost']}")

print("\nOptimizations")

for item in optimized["optimizations"]:
    print(f"- {item}")