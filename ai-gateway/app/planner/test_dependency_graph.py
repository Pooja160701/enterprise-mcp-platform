from dependency_graph import DependencyGraph


plan = [
    {
        "id": 1,
        "tool": "list_repositories"
    },
    {
        "id": 2,
        "tool": "list_branches",
        "depends_on": [1]
    },
    {
        "id": 3,
        "tool": "latest_commit",
        "depends_on": [1]
    },
    {
        "id": 4,
        "tool": "list_pull_requests",
        "depends_on": [2, 3]
    },
]

print(
    DependencyGraph.execution_levels(plan)
)