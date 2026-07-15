import asyncio
from datetime import datetime, timezone


class StreamingExecutor:
    """
    Enterprise Streaming Executor

    Features

    ✓ Live execution events
    ✓ Step started
    ✓ Step completed
    ✓ Step failed
    ✓ Level completed
    ✓ Final completed

    Ready for

    ✓ WebSocket
    ✓ Server Sent Events
    ✓ React Live Timeline
    ✓ Progress Bar
    """

    def __init__(self):

        self.events = []

    async def execute(
        self,
        plan,
        executor,
    ):

        from app.planner.dependency_executor import (
            DependencyExecutor,
        )

        levels = DependencyExecutor.execution_levels(
            plan
        )

        results = []

        result_map = {}

        total_steps = len(plan)

        completed = 0

        #
        # Execute each dependency level
        #

        for level_index, level in enumerate(levels):

            self.emit(

                "level_started",

                {

                    "level": level_index + 1,

                    "steps": len(level),

                },

            )

            tasks = []

            for step in level:

                tasks.append(

                    self.execute_step(

                        step,

                        executor,

                        result_map,

                    )

                )

            level_results = await asyncio.gather(
                *tasks
            )

            for result in level_results:

                completed += 1

                results.append(result)

                result_map[
                    result["id"]
                ] = result

            self.emit(

                "level_completed",

                {

                    "level": level_index + 1,

                    "completed": completed,

                    "total": total_steps,

                    "progress": round(
                        completed * 100 / total_steps,
                        1,
                    ),

                },

            )

        self.emit(

            "execution_completed",

            {

                "completed": completed,

                "total": total_steps,

            },

        )

        return results

    async def execute_step(
        self,
        step,
        executor,
        result_map,
    ):

        self.emit(

            "step_started",

            {

                "id": step["id"],

                "server": step["server"],

                "tool": step["tool"],

            },

        )

        try:

            result = await executor.execute_step(

                step,

                result_map,

            )

            self.emit(

                "step_completed",

                {

                    "id": step["id"],

                    "server": step["server"],

                    "tool": step["tool"],

                },

            )

            return result

        except Exception as exc:

            self.emit(

                "step_failed",

                {

                    "id": step["id"],

                    "server": step["server"],

                    "tool": step["tool"],

                    "error": str(exc),

                },

            )

            raise

    def emit(
        self,
        event,
        payload,
    ):

        message = {

            "time": datetime.now(timezone.utc).isoformat(),

            "event": event,

            "payload": payload,

        }

        self.events.append(message)

        print(
            f"[STREAM] {event} -> {payload}"
        )

    def history(
        self,
    ):

        return list(self.events)

    def clear(
        self,
    ):

        self.events.clear()