import re
import json


class ArgumentResolver:
    """
    Resolves placeholders inside execution plans.

    Example:

    "$1.name"
        ↓
    "enterprise-mcp-platform"

    "$2.id"
        ↓
    "i-123456"

    "$3.namespace"
        ↓
    "default"
    """

    PLACEHOLDER = re.compile(
        r"^\$(\d+)\.(.+)$"
    )

    @classmethod
    def resolve(
        cls,
        arguments,
        previous_results=None,
    ):

        if previous_results is None:
            previous_results = []

        resolved = {}

        for key, value in arguments.items():

            resolved[key] = cls.resolve_value(
                value,
                previous_results,
            )

        return resolved

    @classmethod
    def resolve_value(
        cls,
        value,
        previous_results,
    ):

        if not isinstance(value, str):
            return value

        match = cls.PLACEHOLDER.match(value)

        if not match:
            return value

        step_id = int(match.group(1))
        field = match.group(2)

        #
        # Find referenced step
        #

        for result in previous_results:

            if result["id"] != step_id:
                continue

            data = result["result"]

            #
            # JSON string
            #

            if isinstance(data, str):

                try:
                    data = json.loads(data)
                except Exception:
                    return value

            #
            # List
            #

            if isinstance(data, list):

                if not data:
                    return None

                data = data[0]

                if isinstance(data, str):

                    try:
                        data = json.loads(data)
                    except Exception:
                        return value

            #
            # Dictionary
            #

            if isinstance(data, dict):

                return data.get(field)

        #
        # Placeholder couldn't be resolved
        #

        return value