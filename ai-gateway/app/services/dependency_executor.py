from copy import deepcopy


class DependencyExecutor:
    """
    Resolves dependencies between execution steps.

    Example:

    Step 2:
        "$step1.repository"

    becomes

    "enterprise-mcp-platform"
    """

    @staticmethod
    def resolve(plan, previous_results):

        resolved = deepcopy(plan)

        for step in resolved:

            arguments = step.get("arguments", {})

            for key, value in arguments.items():

                if not isinstance(value, str):
                    continue

                if not value.startswith("$step"):
                    continue

                #
                # Example:
                #
                # $step1.repository
                #

                left, field = value[1:].split(".")

                index = int(
                    left.replace("step", "")
                ) - 1

                result = previous_results[index]

                if isinstance(result, dict):

                    arguments[key] = result.get(field)

        return resolved