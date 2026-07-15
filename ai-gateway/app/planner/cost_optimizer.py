from copy import deepcopy


class CostOptimizer:
    """
    Optimizes execution plans.

    Optimizations

    ✓ Remove duplicate steps
    ✓ Merge identical tool calls
    ✓ Remove unused dependencies
    ✓ Reorder by dependency level
    ✓ Sort by estimated execution cost

    Returns

    {
        "plan": optimized_plan,
        "optimizations":[...],
        "estimated_cost": float
    }
    """

    #
    # Relative execution cost
    #

    TOOL_COST = {

        "filesystem": 1,

        "postgres": 2,

        "docker": 2,

        "github": 3,

        "kubernetes": 4,

        "prometheus": 4,

        "grafana": 4,

        "aws": 5,

    }

    @classmethod
    def optimize(
        cls,
        plan,
    ):

        optimized = deepcopy(plan)

        optimizations = []

        #
        # -----------------------------------------
        # Remove duplicate tool calls
        # -----------------------------------------
        #

        unique = {}

        id_mapping = {}

        dedup = []

        for step in optimized:

            key = (
                step["server"],
                step["tool"],
                tuple(
                    sorted(
                        step.get(
                            "arguments",
                            {},
                        ).items()
                    )
                ),
            )

            if key in unique:

                id_mapping[
                    step["id"]
                ] = unique[key]["id"]

                optimizations.append(
                    f"Merged duplicate step {step['id']} into {unique[key]['id']}."
                )

                continue

            unique[key] = step

            dedup.append(step)

        optimized = dedup

        #
        # -----------------------------------------
        # Rewrite dependencies
        # -----------------------------------------
        #

        for step in optimized:

            deps = []

            for dep in step.get(
                "depends_on",
                [],
            ):

                deps.append(
                    id_mapping.get(
                        dep,
                        dep,
                    )
                )

            #
            # Remove duplicates
            #

            step["depends_on"] = sorted(
                list(set(deps))
            )

        #
        # -----------------------------------------
        # Remove self dependencies
        # -----------------------------------------
        #

        for step in optimized:

            step["depends_on"] = [

                dep

                for dep in step["depends_on"]

                if dep != step["id"]

            ]

        #
        # -----------------------------------------
        # Estimate execution cost
        # -----------------------------------------
        #

        total_cost = 0

        for step in optimized:

            total_cost += cls.TOOL_COST.get(
                step["server"],
                5,
            )

        #
        # -----------------------------------------
        # Dependency level
        # -----------------------------------------
        #

        levels = {}

        def level(step):

            sid = step["id"]

            if sid in levels:

                return levels[sid]

            deps = step.get(
                "depends_on",
                [],
            )

            if not deps:

                levels[sid] = 0

                return 0

            value = 1 + max(

                level(
                    next(
                        s

                        for s in optimized

                        if s["id"] == dep
                    )
                )

                for dep in deps

            )

            levels[sid] = value

            return value

        for step in optimized:

            level(step)

        #
        # -----------------------------------------
        # Sort
        # -----------------------------------------
        #

        optimized.sort(

            key=lambda s: (

                levels[s["id"]],

                cls.TOOL_COST.get(
                    s["server"],
                    5,
                ),

                s["id"],

            )

        )

        #
        # -----------------------------------------
        # Sequential IDs
        # -----------------------------------------
        #

        mapping = {}

        for new_id, step in enumerate(

            optimized,

            start=1,

        ):

            mapping[
                step["id"]
            ] = new_id

            step["id"] = new_id

        #
        # Rewrite dependency ids
        # -----------------------------------------
        #

        for step in optimized:

            step["depends_on"] = [

                mapping[d]

                for d in step["depends_on"]

                if d in mapping

            ]

        #
        # -----------------------------------------
        # Final report
        # -----------------------------------------
        #

        return {

            "plan": optimized,

            "optimizations": optimizations,

            "estimated_cost": total_cost,

        }