from collections import defaultdict


class DependencyGraph:
    """
    Builds an execution graph from a plan.

    Example

    [
        {"id":1},
        {"id":2,"depends_on":[1]},
        {"id":3,"depends_on":[1]},
        {"id":4,"depends_on":[2,3]}
    ]
    """

    @staticmethod
    def build(plan):

        graph = defaultdict(list)
        indegree = defaultdict(int)

        ids = {
            step["id"]
            for step in plan
        }

        for step in plan:

            indegree.setdefault(
                step["id"],
                0,
            )

            for dependency in step.get(
                "depends_on",
                [],
            ):

                if dependency not in ids:
                    raise ValueError(
                        f"Unknown dependency {dependency}"
                    )

                graph[dependency].append(
                    step["id"]
                )

                indegree[step["id"]] += 1

        return graph, indegree

    @staticmethod
    def execution_levels(plan):
        """
        Returns execution batches.

        Example

        [[1],[2,3],[4]]
        """

        graph, indegree = DependencyGraph.build(plan)

        queue = []

        for step in plan:

            if indegree[step["id"]] == 0:
                queue.append(step["id"])

        levels = []

        while queue:

            current = queue.copy()
            queue.clear()

            levels.append(current)

            for node in current:

                for child in graph[node]:

                    indegree[child] -= 1

                    if indegree[child] == 0:
                        queue.append(child)

        return levels