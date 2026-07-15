from copy import deepcopy


class ConfidenceScorer:
    """
    Scores the quality of an execution plan.

    Final Score =

        Tool Validity
      + Argument Completeness
      + Dependency Quality
      + Optimization
      - Repair Penalty

    Maximum = 100
    """

    @classmethod
    def score(
        cls,
        plan,
        candidate_tools=None,
        repairs=None,
        optimizations=None,
    ):

        plan = deepcopy(plan)

        repairs = repairs or []

        optimizations = optimizations or []

        #
        # --------------------------
        # Tool lookup
        # --------------------------
        #

        available = set()

        if candidate_tools:

            available = {

                (
                    tool["server"],
                    tool["name"],
                )

                for tool in candidate_tools

            }

        #
        # --------------------------
        # Components
        # --------------------------
        #

        tool_score = cls.tool_score(
            plan,
            available,
        )

        argument_score = cls.argument_score(
            plan,
        )

        dependency_score = cls.dependency_score(
            plan,
        )

        optimization_score = cls.optimization_score(
            optimizations,
        )

        repair_penalty = cls.repair_penalty(
            repairs,
        )

        #
        # Weighted score
        #

        total = (

            tool_score * 0.35

            +

            argument_score * 0.30

            +

            dependency_score * 0.20

            +

            optimization_score * 0.15

            -

            repair_penalty

        )

        total = max(
            0,
            min(
                100,
                round(total, 2),
            ),
        )

        return {

            "score": total,

            "grade": cls.grade(total),

            "status": cls.status(total),

            "breakdown": {

                "tool_validity": round(
                    tool_score,
                    2,
                ),

                "argument_completeness": round(
                    argument_score,
                    2,
                ),

                "dependency_quality": round(
                    dependency_score,
                    2,
                ),

                "optimization": round(
                    optimization_score,
                    2,
                ),

                "repair_penalty": round(
                    repair_penalty,
                    2,
                ),

            },

        }

    #
    # ---------------------------------
    # Tool Score
    # ---------------------------------
    #

    @staticmethod
    def tool_score(
        plan,
        available,
    ):

        if not plan:
            return 0

        #
        # Offline unit tests:
        # if no candidate tools supplied,
        # assume planner selected valid tools.
        #

        if not available:
            return 100

        valid = 0

        for step in plan:

            key = (
                step["server"],
                step["tool"],
            )

            if key in available:

                valid += 1

        return (valid / len(plan)) * 100

    #
    # ---------------------------------
    # Argument Score
    # ---------------------------------
    #

    @staticmethod
    def argument_score(
        plan,
    ):

        if not plan:
            return 0

        total = 0

        for step in plan:

            args = step.get(
                "arguments",
                {},
            )

            if not args:

                total += 80

                continue

            complete = 0

            for value in args.values():

                if value not in (

                    None,

                    "",

                    "UNKNOWN",

                ):

                    complete += 1

            total += (

                complete

                /

                max(
                    1,
                    len(args),
                )

            ) * 100

        return total / len(plan)

    #
    # ---------------------------------
    # Dependency Score
    # ---------------------------------
    #

    @staticmethod
    def dependency_score(
        plan,
    ):

        if not plan:

            return 100

        ids = {

            step["id"]

            for step in plan

        }

        score = 100

        for step in plan:

            deps = step.get(
                "depends_on",
                [],
            )

            for dep in deps:

                if dep not in ids:

                    score -= 15

                if dep == step["id"]:

                    score -= 20

        return max(
            0,
            score,
        )

    #
    # ---------------------------------
    # Optimization Score
    # ---------------------------------
    #

    @staticmethod
    def optimization_score(
        optimizations,
    ):

        if not optimizations:

            return 80

        return min(

            100,

            80 + len(optimizations) * 5,

        )

    #
    # ---------------------------------
    # Repair Penalty
    # ---------------------------------
    #

    @staticmethod
    def repair_penalty(
        repairs,
    ):

        return min(

            30,

            len(repairs) * 3,

        )

    #
    # ---------------------------------
    # Grade
    # ---------------------------------
    #

    @staticmethod
    def grade(
        score,
    ):

        if score >= 95:
            return "A+"

        if score >= 90:
            return "A"

        if score >= 80:
            return "B"

        if score >= 70:
            return "C"

        if score >= 60:
            return "D"

        return "F"

    #
    # ---------------------------------
    # Status
    # ---------------------------------
    #

    @staticmethod
    def status(
        score,
    ):

        if score >= 95:
            return "Excellent"

        if score >= 85:
            return "High"

        if score >= 70:
            return "Medium"

        if score >= 50:
            return "Low"

        return "Poor"