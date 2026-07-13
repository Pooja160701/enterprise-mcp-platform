import json


class PlanValidator:

    REQUIRED_FIELDS = {
        "id",
        "server",
        "tool",
        "arguments",
    }

    @classmethod
    def validate(cls, response: str):

        try:

            plan = json.loads(response)

        except Exception as e:

            raise ValueError(
                f"Planner returned invalid JSON\n\n{e}"
            )

        if not isinstance(plan, list):

            raise ValueError(
                "Planner must return a JSON list."
            )

        for step in plan:

            missing = cls.REQUIRED_FIELDS - set(step.keys())

            if missing:

                raise ValueError(
                    f"Missing planner fields: {missing}"
                )

        return plan