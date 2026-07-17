from copy import deepcopy
from collections import defaultdict
import time


class PrometheusMetrics:
    """
    Enterprise Prometheus Metrics

    Lightweight Prometheus-compatible metrics collector.

    Features

    ✓ Counter
    ✓ Gauge
    ✓ Histogram
    ✓ Summary
    ✓ Labels
    ✓ Prometheus Text Export
    ✓ Statistics

    Used by

    - Observability Manager
    - Prometheus
    - Grafana
    - API Gateway
    - Tool Executor
    """

    COUNTER = "counter"
    GAUGE = "gauge"
    HISTOGRAM = "histogram"
    SUMMARY = "summary"

    def __init__(self):

        self.clear()

    # -------------------------------------------------
    # Counter
    # -------------------------------------------------

    def counter(
        self,
        name,
        value=1,
        labels=None,
    ):

        metric = self._metrics[name]

        metric["type"] = self.COUNTER

        metric["value"] += value

        metric["labels"] = deepcopy(labels or {})

        metric["updated_at"] = time.time()

        return metric["value"]

    # -------------------------------------------------
    # Gauge
    # -------------------------------------------------

    def gauge(
        self,
        name,
        value,
        labels=None,
    ):

        metric = self._metrics[name]

        metric["type"] = self.GAUGE

        metric["value"] = value

        metric["labels"] = deepcopy(labels or {})

        metric["updated_at"] = time.time()

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

        metric = self._metrics[name]

        metric["type"] = self.HISTOGRAM

        metric["values"].append(value)

        metric["labels"] = deepcopy(labels or {})

        metric["updated_at"] = time.time()

        return value

    # -------------------------------------------------
    # Summary
    # -------------------------------------------------

    def summary(
        self,
        name,
        value,
        labels=None,
    ):

        metric = self._metrics[name]

        metric["type"] = self.SUMMARY

        metric["values"].append(value)

        metric["labels"] = deepcopy(labels or {})

        metric["updated_at"] = time.time()

        return value

    # -------------------------------------------------
    # Exists
    # -------------------------------------------------

    def exists(
        self,
        name,
    ):

        return name in self._metrics

    # -------------------------------------------------
    # Metric
    # -------------------------------------------------

    def metric(
        self,
        name,
    ):

        if name not in self._metrics:

            return None

        return deepcopy(self._metrics[name])

    # -------------------------------------------------
    # Label Formatter
    # -------------------------------------------------

    @staticmethod
    def _labels(labels):

        if not labels:

            return ""

        parts = [

            f'{k}="{v}"'

            for k, v in labels.items()

        ]

        return "{" + ",".join(parts) + "}"

    # -------------------------------------------------
    # Prometheus Export
    # -------------------------------------------------

    def scrape(
        self,
    ):

        lines = []

        for name, metric in self._metrics.items():

            labels = self._labels(

                metric["labels"]

            )

            lines.append(

                f"# TYPE {name} {metric['type']}"

            )

            if metric["type"] in (

                self.COUNTER,

                self.GAUGE,

            ):

                lines.append(

                    f"{name}{labels} {metric['value']}"

                )

            else:

                values = metric["values"]

                count = len(values)

                total = sum(values)

                avg = (

                    total / count

                    if count

                    else 0

                )

                lines.append(

                    f"{name}_count{labels} {count}"

                )

                lines.append(

                    f"{name}_sum{labels} {total}"

                )

                lines.append(

                    f"{name}_avg{labels} {round(avg,6)}"

                )

        return "\n".join(lines)

    # -------------------------------------------------
    # Statistics
    # -------------------------------------------------

    def statistics(
        self,
    ):

        counters = 0

        gauges = 0

        histograms = 0

        summaries = 0

        for metric in self._metrics.values():

            if metric["type"] == self.COUNTER:

                counters += 1

            elif metric["type"] == self.GAUGE:

                gauges += 1

            elif metric["type"] == self.HISTOGRAM:

                histograms += 1

            elif metric["type"] == self.SUMMARY:

                summaries += 1

        return {

            "metrics": len(self._metrics),

            "counters": counters,

            "gauges": gauges,

            "histograms": histograms,

            "summaries": summaries,

        }

    # -------------------------------------------------
    # Export
    # -------------------------------------------------

    def export(
        self,
    ):

        return {

            "metrics": deepcopy(

                dict(self._metrics)

            ),

            "scrape": self.scrape(),

        }

    # -------------------------------------------------
    # Clear
    # -------------------------------------------------

    def clear(
        self,
    ):

        self._metrics = defaultdict(

            lambda: {

                "type": None,

                "value": 0,

                "values": [],

                "labels": {},

                "updated_at": None,

            }

        )

    # -------------------------------------------------
    # Empty
    # -------------------------------------------------

    @staticmethod
    def empty():

        return PrometheusMetrics()