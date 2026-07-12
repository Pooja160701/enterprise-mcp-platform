import time
from datetime import datetime, UTC


class TelemetryService:

    def __init__(self):
        self.steps = {}
        self.total_start = None
        self.started_at = None

    def begin(self):
        self.total_start = time.perf_counter()
        self.started_at = datetime.now(UTC)

    def start_step(self, name: str):
        self.steps[name] = {
            "start": time.perf_counter()
        }

    def end_step(self, name: str):
        if name not in self.steps:
            return

        self.steps[name]["duration"] = (
            time.perf_counter()
            - self.steps[name]["start"]
        ) * 1000

    def finish(self):

        completed_at = datetime.now(UTC)

        total = (
            time.perf_counter()
            - self.total_start
        ) * 1000

        return {

            "total": round(total, 2),

            "started_at": self.started_at.isoformat(),

            "completed_at": completed_at.isoformat(),

            "steps": {
                key: round(value["duration"], 2)
                for key, value in self.steps.items()
            }

        }