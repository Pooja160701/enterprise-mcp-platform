import asyncio
from collections import defaultdict


class DependencyExecutor:
    """
    Executes an execution plan as a Directed Acyclic Graph (DAG).

    Features

    ✓ Dependency-aware scheduling
    ✓ Parallel execution
    ✓ Topological execution
    ✓ Result collection
    ✓ Ready for retries/cache/streaming

    Execution Example

        1

      /   \

     2     3

      \   /

        4

    Levels

    [[1], [2,3], [4]]
    """

    @classmethod
    def execution_levels(
        cls,
        plan,
    ):
        """
        Convert a dependency graph into execution levels.
        """

        if not plan:
            return []

        steps = {
            step["id"]: step
            for step in plan
        }

        indegree = {}

        children = defaultdict(list)

        #
        # Build graph
        #

        for step in plan:

            deps = step.get(
                "depends_on",
                [],
            )

            indegree[step["id"]] = len(deps)

            for dep in deps:

                children[dep].append(
                    step["id"]
                )

        #
        # Initial ready queue
        #

        current = [

            sid

            for sid, degree in indegree.items()

            if degree == 0

        ]

        levels = []

        while current:

            level = []

            next_level = []

            for sid in current:

                level.append(
                    steps[sid]
                )

                for child in children[sid]:

                    indegree[child] -= 1

                    if indegree[child] == 0:

                        next_level.append(
                            child
                        )

            levels.append(level)

            current = next_level

        #
        # Detect cycle
        #

        visited = sum(
            len(level)
            for level in levels
        )

        if visited != len(plan):

            raise ValueError(
                "Circular dependency detected."
            )

        return levels

    @classmethod
    async def execute(
        cls,
        plan,
        executor,
    ):
        """
        Execute dependency levels in order.

        Each level executes in parallel.
        """

        levels = cls.execution_levels(
            plan
        )

        print("\nExecution Levels\n")
        print(levels)

        all_results = []

        result_map = {}

        for level in levels:

            print("\nExecuting Level\n")
            print(level)

            tasks = []

            for step in level:

                tasks.append(

                    executor.execute_step(
                        step,
                        result_map,
                    )

                )

            results = await asyncio.gather(
                *tasks
            )

            for result in results:

                result_map[
                    result["id"]
                ] = result

                all_results.append(
                    result
                )

        return all_results

    @staticmethod
    def resolve_reference(
        reference,
        results,
    ):
        """
        Resolve placeholders.

        Examples

        $1.name

        $2.namespace
        """

        if (
            not isinstance(
                reference,
                str,
            )
            or
            not reference.startswith("$")
        ):

            return reference

        try:

            token = reference[1:]

            step_id, field = token.split(
                ".",
                1,
            )

            step = results.get(
                int(step_id)
            )

            if step is None:

                return reference

            result = step.get(
                "result",
                {},
            )

            if isinstance(
                result,
                dict,
            ):

                return result.get(
                    field,
                    reference,
                )

            return reference

        except Exception:

            return reference

    @classmethod
    def resolve_arguments(
        cls,
        arguments,
        results,
    ):
        """
        Resolve all placeholders inside arguments.
        """

        resolved = {}

        for key, value in arguments.items():

            resolved[key] = cls.resolve_reference(
                value,
                results,
            )

        return resolved