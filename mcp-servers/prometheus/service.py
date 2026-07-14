import os

import requests


class PrometheusService:
    """
    Prometheus helper service.
    """

    def __init__(self):

        self.base_url = os.getenv(
            "PROMETHEUS_URL",
            "http://host.docker.internal:9090",
        )

    #
    # -------------------------
    # Helpers
    # -------------------------
    #

    def _get(
        self,
        endpoint: str,
        params: dict | None = None,
    ):

        response = requests.get(
            f"{self.base_url}{endpoint}",
            params=params,
            timeout=20,
        )

        response.raise_for_status()

        return response.json()["data"]

    #
    # -------------------------
    # Health
    # -------------------------
    #

    def health(self):

        try:

            requests.get(
                self.base_url,
                timeout=5,
            ).raise_for_status()

            return {
                "status": "healthy",
            }

        except Exception as e:

            return {
                "status": "offline",
                "error": str(e),
            }

    #
    # -------------------------
    # Targets
    # -------------------------
    #

    def list_targets(self):

        data = self._get(
            "/api/v1/targets"
        )

        results = []

        for target in data["activeTargets"]:

            results.append(
                {
                    "job": target["labels"].get("job"),
                    "instance": target["labels"].get("instance"),
                    "health": target["health"],
                    "scrape_url": target["scrapeUrl"],
                }
            )

        return results

    #
    # -------------------------
    # Alerts
    # -------------------------
    #

    def list_alerts(self):

        return self._get(
            "/api/v1/alerts"
        )["alerts"]

    #
    # -------------------------
    # Rules
    # -------------------------
    #

    def list_rules(self):

        groups = self._get(
            "/api/v1/rules"
        )["groups"]

        rules = []

        for group in groups:

            rules.extend(
                group["rules"]
            )

        return rules

    #
    # -------------------------
    # Instant Query
    # -------------------------
    #

    def query(
        self,
        expression: str,
    ):

        data = self._get(
            "/api/v1/query",
            {
                "query": expression,
            },
        )

        return data["result"]

    #
    # -------------------------
    # Range Query
    # -------------------------
    #

    def query_range(
        self,
        expression: str,
        start: str,
        end: str,
        step: str = "60s",
    ):

        data = self._get(
            "/api/v1/query_range",
            {
                "query": expression,
                "start": start,
                "end": end,
                "step": step,
            },
        )

        return data["result"]