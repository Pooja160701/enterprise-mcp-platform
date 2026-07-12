import time


class TelemetryService:

    def __init__(self):

        self.start = None

    def begin(self):

        self.start = time.perf_counter()

    def end(self):

        elapsed = (time.perf_counter() - self.start) * 1000

        return round(elapsed, 2)