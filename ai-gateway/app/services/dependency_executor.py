from collections import defaultdict


class DependencyExecutor:
    """
    Groups execution steps by dependency level.

    Example

    Step 1
      ↓
    Step 2   Step 3
      ↓         ↓
         Step 4

    becomes

    [
        [step1],
        [step2, step3],
        [step4]
    ]
    """

    @staticmethod
    def build(plan):

        step_map = {
            step["id"]: step
            for step in plan
        }

        indegree = {}
        graph = defaultdict(list)

        for step in plan:

            deps = step.get("depends_on", [])

            indegree[step["id"]] = len(deps)

            for dep in deps:
                graph[dep].append(step["id"])

        queue = []

        for step in plan:

            if indegree[step["id"]] == 0:
                queue.append(step["id"])

        levels = []

        while queue:

            current_level = []

            next_queue = []

            for node in queue:

                current_level.append(
                    step_map[node]
                )

                for child in graph[node]:

                    indegree[child] -= 1

                    if indegree[child] == 0:
                        next_queue.append(child)

            levels.append(current_level)

            queue = next_queue

        return levels

    @staticmethod
    def resolve(level, previous_results):
        """
        Placeholder.

        Later we'll replace references such as

        $1.name

        with the actual output from step 1.
        """

        return level