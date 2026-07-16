from copy import deepcopy
import time


class GoalTracker:
    """
    Enterprise Goal Tracker

    Tracks agent goals throughout execution.

    Features

    ✓ Goal Management
    ✓ Goal Status
    ✓ Progress Tracking
    ✓ Dependencies
    ✓ Completion Metrics
    ✓ Statistics

    Used by

    - Agent Service
    - Reasoning Engine
    - Workflow Engine
    - Planner
    """

    def __init__(self):

        self.clear()

    # -------------------------------------------------
    # Add Goal
    # -------------------------------------------------

    def add(
        self,
        goal,
        priority=50,
        depends_on=None,
    ):

        goal_id = len(self._goals) + 1

        self._goals.append(

            {

                "id": goal_id,

                "goal": goal,

                "priority": priority,

                "depends_on": depends_on,

                "status": "pending",

                "progress": 0,

                "created_at": time.time(),

                "completed_at": None,

            }

        )

        return goal_id

    # -------------------------------------------------
    # Start Goal
    # -------------------------------------------------

    def start(
        self,
        goal_id,
    ):

        goal = self._find(goal_id)

        if goal:

            goal["status"] = "running"

            goal["progress"] = max(goal["progress"], 1)

            return True

        return False

    # -------------------------------------------------
    # Update Progress
    # -------------------------------------------------

    def update(
        self,
        goal_id,
        progress,
    ):

        goal = self._find(goal_id)

        if goal:

            goal["progress"] = max(
                0,
                min(100, progress),
            )

            if goal["progress"] > 0:

                goal["status"] = "running"

            return True

        return False

    # -------------------------------------------------
    # Complete Goal
    # -------------------------------------------------

    def complete(
        self,
        goal_id,
    ):

        goal = self._find(goal_id)

        if goal:

            goal["status"] = "completed"

            goal["progress"] = 100

            goal["completed_at"] = time.time()

            return True

        return False

    # -------------------------------------------------
    # Fail Goal
    # -------------------------------------------------

    def fail(
        self,
        goal_id,
    ):

        goal = self._find(goal_id)

        if goal:

            goal["status"] = "failed"

            return True

        return False

    # -------------------------------------------------
    # Get Goal
    # -------------------------------------------------

    def get(
        self,
        goal_id,
    ):

        goal = self._find(goal_id)

        if goal:

            return deepcopy(goal)

        return None

    # -------------------------------------------------
    # Pending Goals
    # -------------------------------------------------

    def pending(
        self,
    ):

        return [

            deepcopy(goal)

            for goal in self._goals

            if goal["status"] == "pending"

        ]

    # -------------------------------------------------
    # Running Goals
    # -------------------------------------------------

    def running(
        self,
    ):

        return [

            deepcopy(goal)

            for goal in self._goals

            if goal["status"] == "running"

        ]

    # -------------------------------------------------
    # Completed Goals
    # -------------------------------------------------

    def completed(
        self,
    ):

        return [

            deepcopy(goal)

            for goal in self._goals

            if goal["status"] == "completed"

        ]

    # -------------------------------------------------
    # Failed Goals
    # -------------------------------------------------

    def failed(
        self,
    ):

        return [

            deepcopy(goal)

            for goal in self._goals

            if goal["status"] == "failed"

        ]

    # -------------------------------------------------
    # Overall Progress
    # -------------------------------------------------

    def progress(
        self,
    ):

        if not self._goals:

            return 0

        total = sum(

            goal["progress"]

            for goal in self._goals

        )

        return round(

            total / len(self._goals),

            2,

        )

    # -------------------------------------------------
    # Statistics
    # -------------------------------------------------

    def statistics(
        self,
    ):

        return {

            "total": len(self._goals),

            "pending": len(self.pending()),

            "running": len(self.running()),

            "completed": len(self.completed()),

            "failed": len(self.failed()),

            "progress": self.progress(),

        }

    # -------------------------------------------------
    # Export
    # -------------------------------------------------

    def export(
        self,
    ):

        return deepcopy(

            self._goals,

        )

    # -------------------------------------------------
    # Internal Lookup
    # -------------------------------------------------

    def _find(
        self,
        goal_id,
    ):

        for goal in self._goals:

            if goal["id"] == goal_id:

                return goal

        return None

    # -------------------------------------------------
    # Clear
    # -------------------------------------------------

    def clear(
        self,
    ):

        self._goals = []

    # -------------------------------------------------
    # Empty Tracker
    # -------------------------------------------------

    @staticmethod
    def empty():

        return GoalTracker()