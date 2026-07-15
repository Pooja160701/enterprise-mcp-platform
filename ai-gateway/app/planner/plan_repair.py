from copy import deepcopy


class PlanRepair:
    """
    Automatically repairs common planner mistakes.

    Repairs

    ✓ Missing ids
    ✓ Duplicate ids
    ✓ Missing arguments
    ✓ Missing depends_on
    ✓ Invalid tools (when candidate_tools supplied)
    ✓ Invalid servers (when candidate_tools supplied)
    ✓ Broken dependencies
    ✓ Invalid step objects

    Returns

    {
        "plan": repaired_plan,
        "repairs": [...]
    }
    """

    @classmethod
    def repair(
        cls,
        plan,
        candidate_tools=None,
    ):

        repaired = deepcopy(plan)

        repairs = []

        #
        # Empty
        #

        if not repaired:

            return {

                "plan": [],

                "repairs": [
                    "Planner produced an empty execution plan."
                ],

            }

        #
        # Build tool lookup
        #

        available = {}

        if candidate_tools:

            for tool in candidate_tools:

                available[
                    (
                        tool["server"],
                        tool["name"],
                    )
                ] = tool

        #
        # Remove invalid objects
        #

        cleaned = []

        for step in repaired:

            if not isinstance(step, dict):

                repairs.append(
                    "Removed invalid planner step."
                )

                continue

            cleaned.append(step)

        repaired = cleaned

        #
        # Repair IDs
        #

        used = set()

        next_id = 1

        for step in repaired:

            sid = step.get("id")

            if sid is None or sid in used:

                while next_id in used:

                    next_id += 1

                step["id"] = next_id

                repairs.append(
                    f"Assigned step id {next_id}."
                )

            used.add(step["id"])

        #
        # arguments
        #

        for step in repaired:

            if not isinstance(
                step.get("arguments"),
                dict,
            ):

                step["arguments"] = {}

                repairs.append(
                    f"Step {step['id']} arguments repaired."
                )

        #
        # depends_on
        #

        for step in repaired:

            deps = step.get("depends_on")

            if deps is None:

                step["depends_on"] = []

                repairs.append(
                    f"Step {step['id']} added depends_on."
                )

            elif isinstance(
                deps,
                int,
            ):

                step["depends_on"] = [deps]

                repairs.append(
                    f"Step {step['id']} normalized depends_on."
                )

            elif not isinstance(
                deps,
                list,
            ):

                step["depends_on"] = []

                repairs.append(
                    f"Step {step['id']} repaired depends_on."
                )

        #
        # Remove broken dependencies
        #

        valid_ids = {

            s["id"]

            for s in repaired

        }

        for step in repaired:

            step["depends_on"] = [

                dep

                for dep in step["depends_on"]

                if dep in valid_ids

            ]

        #
        # Remove unknown tools
        # (only in production)
        #

        if available:

            final = []

            for step in repaired:

                key = (

                    step.get("server"),

                    step.get("tool"),

                )

                if key not in available:

                    repairs.append(

                        f"Removed unknown tool {step['server']} -> {step['tool']}."

                    )

                    continue

                final.append(step)

            repaired = final

        #
        # Normalize strings
        #

        for step in repaired:

            step["server"] = str(
                step["server"]
            ).strip()

            step["tool"] = str(
                step["tool"]
            ).strip()

        #
        # Remove duplicate identical steps
        #

        seen = set()

        dedup = []

        for step in repaired:

            key = (

                step["server"],

                step["tool"],

                tuple(
                    sorted(
                        step["arguments"].items()
                    )
                ),

            )

            if key in seen:

                repairs.append(
                    f"Removed duplicate step {step['id']}."
                )

                continue

            seen.add(key)

            dedup.append(step)

        repaired = dedup

        #
        # Sort
        #

        repaired.sort(
            key=lambda x: x["id"]
        )

        #
        # Renumber
        #

        mapping = {}

        for new_id, step in enumerate(

            repaired,

            start=1,

        ):

            mapping[
                step["id"]
            ] = new_id

            step["id"] = new_id

        #
        # Rewrite dependencies
        #

        for step in repaired:

            step["depends_on"] = [

                mapping[d]

                for d in step["depends_on"]

                if d in mapping

            ]

        #
        # Final defaults
        #

        for step in repaired:

            step.setdefault(
                "arguments",
                {},
            )

            step.setdefault(
                "depends_on",
                [],
            )

        return {

            "plan": repaired,

            "repairs": repairs,

        }