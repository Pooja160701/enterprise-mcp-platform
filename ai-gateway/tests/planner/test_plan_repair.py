import json

from app.planner.plan_repair import PlanRepair


#
# Intentionally broken plan
#

plan = [
    {
        "id": 1,
        "server": "github",
        "tool": "list_repositories",
    },
    {
        "id": 1,
        "server": "github",
        "tool": "list_branches",
        "arguments": {
            "repository": "enterprise-mcp-platform",
        },
        "depends_on": 1,
    },
    {
        "id": 3,
        "server": "github",
        "tool": "latest_commit",
        "arguments": {},
        "depends_on": [99],
    },
]

print("\nBroken Plan\n")

print(
    json.dumps(
        plan,
        indent=2,
    )
)

repaired = PlanRepair.repair(plan)

print("\nRepaired Plan\n")

print(
    json.dumps(
        repaired,
        indent=2,
    )
)