from copy import deepcopy


class ToolPlanner:
    """
    Enterprise Tool Planner

    Converts a reasoning decision into an executable
    tool execution plan.

    Features

    ✓ Tool Selection
    ✓ Dependency Planning
    ✓ Parallel Grouping
    ✓ Sequential Execution
    ✓ Priority Ordering
    ✓ Execution Statistics

    Used by

    - Reasoning Engine
    - Decision Engine
    - Parallel Executor
    - Agent Service
    """

    def __init__(self):

        self.clear()

    # -------------------------------------------------
    # Add Tool
    # -------------------------------------------------

    def add(
        self,
        tool,
        arguments=None,
        priority=50,
        parallel=False,
        depends_on=None,
    ):

        self._plan.append(

            {

                "tool": tool,

                "arguments": deepcopy(arguments or {}),

                "priority": priority,

                "parallel": parallel,

                "depends_on": depends_on,

            }

        )

        return self

    # -------------------------------------------------
    # Build Execution Plan
    # -------------------------------------------------

    def build(
        self,
    ):

        self._plan.sort(

            key=lambda x: x["priority"],

            reverse=True,

        )

        return deepcopy(

            self._plan,

        )

    # -------------------------------------------------
    # Parallel Tasks
    # -------------------------------------------------

    def parallel_groups(
        self,
    ):

        return [

            deepcopy(task)

            for task in self._plan

            if task["parallel"]

        ]

    # -------------------------------------------------
    # Sequential Tasks
    # -------------------------------------------------

    def sequential_tasks(
        self,
    ):

        return [

            deepcopy(task)

            for task in self._plan

            if not task["parallel"]

        ]

    # -------------------------------------------------
    # Has Parallel
    # -------------------------------------------------

    def has_parallel(
        self,
    ):

        return any(

            task["parallel"]

            for task in self._plan

        )

    # -------------------------------------------------
    # Has Dependencies
    # -------------------------------------------------

    def has_dependencies(
        self,
    ):

        return any(

            task["depends_on"] is not None

            for task in self._plan

        )

    # -------------------------------------------------
    # Statistics
    # -------------------------------------------------

    def statistics(
        self,
    ):

        parallel = sum(

            task["parallel"]

            for task in self._plan

        )

        sequential = len(self._plan) - parallel

        dependencies = sum(

            task["depends_on"] is not None

            for task in self._plan

        )

        return {

            "tools": len(self._plan),

            "parallel": parallel,

            "sequential": sequential,

            "dependencies": dependencies,

        }

    # -------------------------------------------------
    # Export
    # -------------------------------------------------

    def export(
        self,
    ):

        return deepcopy(

            self._plan,

        )

    # -------------------------------------------------
    # Clear
    # -------------------------------------------------

    def clear(
        self,
    ):

        self._plan = []

    # -------------------------------------------------
    # Empty Planner
    # -------------------------------------------------

    @staticmethod
    def empty():

        return ToolPlanner()