from ast import arguments
from copy import deepcopy
from operator import index


class VariableResolver:
    """
    Resolves variables like:

    $step1.first_match
    $step2.repository
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
                # $step1.first_match
                #

                variable = value[1:]

                parts = variable.split(".")

                left = parts[0]

                fields = parts[1:]

                index = int(
                    left.replace("step", "")
                ) - 1

                value = previous_results[index]

                for field in fields:

                    if isinstance(value, dict):

                        value = value.get(field)

                    elif isinstance(value, list):

                        value = value[int(field)]

                arguments[key] = value

                if isinstance(result, dict):

                    for field in fields:

                        result = result.get(field)

                    arguments[key] = result

        return resolved