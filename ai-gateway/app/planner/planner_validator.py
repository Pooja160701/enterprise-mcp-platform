from copy import deepcopy


class PlannerValidator:
    """
    Validates execution plans before they reach the executor.

    Checks:

    ✓ Valid server
    ✓ Valid tool
    ✓ Duplicate ids
    ✓ Missing ids
    ✓ Dependency existence
    ✓ Circular dependencies
    ✓ Missing arguments object

    Returns

    {
        "valid": bool,
        "errors": [...],
        "warnings": [...],
        "plan": validated_plan
    }
    """

    REQUIRED_FIELDS = (
        "id",
        "server",
        "tool",
        "arguments",
    )

    @classmethod
    def validate(
        cls,
        plan,
        candidate_tools=None,
    ):

        validated = deepcopy(plan)

        errors = []

        warnings = []

        #
        # ----------------------------
        # Empty
        # ----------------------------
        #

        if not validated:

            errors.append(
                "Execution plan is empty."
            )

            return {
                "valid": False,
                "errors": errors,
                "warnings": warnings,
                "plan": [],
            }

        #
        # ----------------------------
        # Build tool lookup
        # ----------------------------
        #

        available = {}

        if candidate_tools:

            for tool in candidate_tools:

                available[
                    (
                        tool["server"],
                        tool["name"],
                    )
                ] = True

        #
        # ----------------------------
        # Validate steps
        # ----------------------------
        #

        ids = []

        for index, step in enumerate(validated):

            #
            # Must be dict
            #

            if not isinstance(step, dict):

                errors.append(
                    f"Step {index + 1} is not an object."
                )

                continue

            #
            # Required fields
            #

            for field in cls.REQUIRED_FIELDS:

                if field not in step:

                    errors.append(
                        f"Step {step.get('id', index + 1)} missing '{field}'."
                    )

            #
            # Arguments
            #

            if not isinstance(
                step.get(
                    "arguments",
                    {},
                ),
                dict,
            ):

                errors.append(
                    f"Step {step.get('id')} arguments must be an object."
                )

            #
            # depends_on
            #

            depends = step.get(
                "depends_on",
                [],
            )

            if depends is None:

                step["depends_on"] = []

            elif not isinstance(
                depends,
                list,
            ):

                errors.append(
                    f"Step {step.get('id')} depends_on must be a list."
                )

            #
            # Duplicate ids
            #

            if step.get("id") in ids:

                errors.append(
                    f"Duplicate step id {step['id']}."
                )

            ids.append(step.get("id"))

            #
            # Validate tool only if candidate tools were supplied
            #

            if available:

                key = (
                    step.get("server"),
                    step.get("tool"),
                )

                if key not in available:

                    errors.append(
                        f"Unknown tool {step.get('server')} -> {step.get('tool')}."
                    )

        #
        # ----------------------------
        # Dependency existence
        # ----------------------------
        #

        valid_ids = set(ids)

        for step in validated:

            for dep in step.get(
                "depends_on",
                [],
            ):

                if dep not in valid_ids:

                    errors.append(
                        f"Step {step['id']} depends on missing step {dep}."
                    )

        #
        # ----------------------------
        # Circular dependency
        # ----------------------------
        #

        graph = {}

        for step in validated:

            graph[
                step["id"]
            ] = step.get(
                "depends_on",
                [],
            )

        visited = set()

        stack = set()

        def dfs(node):

            if node in stack:

                return True

            if node in visited:

                return False

            visited.add(node)

            stack.add(node)

            for child in graph.get(
                node,
                [],
            ):

                if dfs(child):

                    return True

            stack.remove(node)

            return False

        for node in graph:

            if dfs(node):

                errors.append(
                    "Circular dependency detected."
                )

                break

        #
        # ----------------------------
        # Dependency ordering
        # ----------------------------
        #

        ordering = {}

        for i, step in enumerate(validated):

            ordering[
                step["id"]
            ] = i

        for step in validated:

            current = ordering[
                step["id"]
            ]

            for dep in step.get(
                "depends_on",
                [],
            ):

                if ordering[dep] > current:

                    warnings.append(
                        f"Step {step['id']} appears before dependency {dep}."
                    )

        #
        # ----------------------------
        # Ensure arguments exist
        # ----------------------------
        #

        for step in validated:

            if "arguments" not in step:

                step["arguments"] = {}

        #
        # ----------------------------
        # Result
        # ----------------------------
        #

        return {

            "valid": len(errors) == 0,

            "errors": errors,

            "warnings": warnings,

            "plan": validated,

        }