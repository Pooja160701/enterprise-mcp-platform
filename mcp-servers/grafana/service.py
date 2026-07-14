import os
import requests


class GrafanaService:

    def __init__(self):

        self.host = os.getenv(
            "GRAFANA_HOST",
            "http://localhost:3001",
        )

        self.user = os.getenv(
            "GRAFANA_USER",
            "admin",
        )

        self.password = os.getenv(
            "GRAFANA_PASSWORD",
            "admin",
        )

    def _get(self, endpoint):

        response = requests.get(
            f"{self.host}{endpoint}",
            auth=(self.user, self.password),
            timeout=10,
        )

        response.raise_for_status()

        return response.json()

    def health(self):

        try:

            requests.get(
                self.host,
                auth=(self.user, self.password),
                timeout=5,
            )

            return {
                "status": "healthy",
            }

        except Exception as e:

            return {
                "status": "offline",
                "error": str(e),
            }

    def list_dashboards(self):

        data = self._get(
            "/api/search"
        )

        dashboards = []

        for item in data:

            dashboards.append(
                {
                    "title": item.get("title"),
                    "uid": item.get("uid"),
                    "type": item.get("type"),
                }
            )

        return dashboards

    def list_datasources(self):

        data = self._get(
            "/api/datasources"
        )

        return [
            {
                "name": d["name"],
                "type": d["type"],
                "default": d["isDefault"],
            }
            for d in data
        ]