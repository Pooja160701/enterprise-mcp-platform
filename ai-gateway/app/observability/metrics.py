from copy import deepcopy
from collections import defaultdict
import statistics
import time


class Metrics:
    """
    Enterprise Metrics Collector

    Collects runtime metrics for the Enterprise
    MCP Platform.

    Features

    ✓ Counters
    ✓ Gauges
    ✓ Histograms
    ✓ Timers
    ✓ Labels
    ✓ Runtime Statistics
    ✓ Export

    Used by

    - Observability Manager
    - Agent Service
    - Workflow Engine
    - Tool Executor
    - API Gateway
    - Prometheus Exporter
    """

    COUNTER = "counter"
    GAUGE = "gauge"
    HISTOGRAM = "histogram"
    TIMER = "timer"

    def __init__(self):

        self.clear()

    # -------------------------------------------------
    # Counter
    # -------------------------------------------------

    def increment(
        self,
        name,
        value=1,
        labels=None,
    ):

        self._counters[name]["value"] += value

        if labels:
            self._counters[name]["labels"].update(
                deepcopy(labels)
            )

        self._updated = time.time()

        return self._counters[name]["value"]

    # -------------------------------------------------
    # Counter Alias
    # -------------------------------------------------

    def counter(
        self,
        name,
        value=1,
        labels=None,
    ):

        return self.increment(
            name,
            value=value,
            labels=labels,
        )

    # -------------------------------------------------
    # Gauge
    # -------------------------------------------------

    def gauge(
        self,
        name,
        value,
        labels=None,
    ):

        self._gauges[name]["value"] = value

        if labels:
            self._gauges[name]["labels"].update(
                deepcopy(labels)
            )

        self._updated = time.time()

        return value

    # -------------------------------------------------
    # Histogram
    # -------------------------------------------------

    def histogram(
        self,
        name,
        value,
        labels=None,
    ):

        self._histograms[name]["values"].append(
            value
        )

        if labels:
            self._histograms[name]["labels"].update(
                deepcopy(labels)
            )

        self._updated = time.time()

        return value

    # -------------------------------------------------
    # Timer
    # -------------------------------------------------

    def timer(
        self,
        name,
        duration,
        labels=None,
    ):

        self._timers[name]["values"].append(
            duration
        )

        if labels:
            self._timers[name]["labels"].update(
                deepcopy(labels)
            )

        self._updated = time.time()

        return duration

    # -------------------------------------------------
    # Start Timer
    # -------------------------------------------------

    def start_timer(
        self,
        name,
    ):

        self._running[name] = time.time()

        return self._running[name]

    # -------------------------------------------------
    # Stop Timer
    # -------------------------------------------------

    def stop_timer(
        self,
        name,
        labels=None,
    ):

        if name not in self._running:

            return None

        duration = round(

            time.time() -

            self._running.pop(name),

            6,

        )

        self.timer(

            name,

            duration,

            labels,

        )

        return duration

    # -------------------------------------------------
    # Counter Value
    # -------------------------------------------------

    def counter_value(
        self,
        name,
    ):

        return self._counters[name]["value"]

    # -------------------------------------------------
    # Gauge Value
    # -------------------------------------------------

    def gauge_value(
        self,
        name,
    ):

        return self._gauges[name]["value"]

    # -------------------------------------------------
    # Histogram Statistics
    # -------------------------------------------------

    def histogram_statistics(
        self,
        name,
    ):

        values = self._histograms[name]["values"]

        if not values:

            return {}

        return {

            "count": len(values),

            "min": min(values),

            "max": max(values),

            "mean": round(

                statistics.mean(values),

                6,

            ),

        }

    # -------------------------------------------------
    # Timer Statistics
    # -------------------------------------------------

    def timer_statistics(
        self,
        name,
    ):

        values = self._timers[name]["values"]

        if not values:

            return {}

        return {

            "count": len(values),

            "min": min(values),

            "max": max(values),

            "mean": round(

                statistics.mean(values),

                6,

            ),

        }

    # -------------------------------------------------
    # Statistics
    # -------------------------------------------------

    def statistics(
        self,
    ):

        return {

            "counters": len(
                self._counters
            ),

            "gauges": len(
                self._gauges
            ),

            "histograms": len(
                self._histograms
            ),

            "timers": len(
                self._timers
            ),

            "running_timers": len(
                self._running
            ),

            "last_updated": self._updated,

        }

    # -------------------------------------------------
    # Export
    # -------------------------------------------------

    def export(
        self,
    ):

        return {

            "counters": deepcopy(
                dict(self._counters)
            ),

            "gauges": deepcopy(
                dict(self._gauges)
            ),

            "histograms": deepcopy(
                dict(self._histograms)
            ),

            "timers": deepcopy(
                dict(self._timers)
            ),

            "running_timers": deepcopy(
                self._running
            ),

            "last_updated": self._updated,

        }

    # -------------------------------------------------
    # Clear
    # -------------------------------------------------

    def clear(
        self,
    ):

        self._counters = defaultdict(

            lambda: {

                "value": 0,

                "labels": {},

            }

        )

        self._gauges = defaultdict(

            lambda: {

                "value": 0,

                "labels": {},

            }

        )

        self._histograms = defaultdict(

            lambda: {

                "values": [],

                "labels": {},

            }

        )

        self._timers = defaultdict(

            lambda: {

                "values": [],

                "labels": {},

            }

        )

        self._running = {}

        self._updated = None

    # -------------------------------------------------
    # Empty
    # -------------------------------------------------

    @staticmethod
    def empty():

        return Metrics()