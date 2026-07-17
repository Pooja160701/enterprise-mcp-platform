from copy import deepcopy
import json
import time


class GrafanaDashboard:
    """
    Enterprise Grafana Dashboard

    Manages Grafana dashboards for Enterprise MCP Platform.

    Features

    ✓ Dashboard Metadata
    ✓ Panels
    ✓ Variables
    ✓ Annotations
    ✓ Time Range
    ✓ JSON Export
    ✓ Statistics

    Used by

    - Observability Manager
    - Prometheus
    - OpenTelemetry
    - Monitoring
    """

    def __init__(self):

        self.clear()

    # -------------------------------------------------
    # Configure Dashboard
    # -------------------------------------------------

    def configure(
        self,
        *,
        title="Enterprise MCP Dashboard",
        uid="enterprise-mcp",
        timezone="browser",
        refresh="30s",
    ):

        self._title = title

        self._uid = uid

        self._timezone = timezone

        self._refresh = refresh

        return self

    # -------------------------------------------------
    # Add Panel
    # -------------------------------------------------

    def add_panel(
        self,
        *,
        title,
        panel_type="timeseries",
        datasource="Prometheus",
        targets=None,
        grid_pos=None,
    ):

        panel = {

            "id": len(self._panels) + 1,

            "title": title,

            "type": panel_type,

            "datasource": datasource,

            "targets": deepcopy(targets or []),

            "gridPos": deepcopy(

                grid_pos or {

                    "h": 8,

                    "w": 12,

                    "x": 0,

                    "y": len(self._panels) * 8,

                }

            ),

        }

        self._panels.append(panel)

        return panel["id"]

    # -------------------------------------------------
    # Remove Panel
    # -------------------------------------------------

    def remove_panel(
        self,
        panel_id,
    ):

        before = len(self._panels)

        self._panels = [

            panel

            for panel in self._panels

            if panel["id"] != panel_id

        ]

        return len(self._panels) != before

    # -------------------------------------------------
    # Add Variable
    # -------------------------------------------------

    def add_variable(
        self,
        name,
        query,
    ):

        self._variables.append({

            "name": name,

            "query": query,

        })

        return True

    # -------------------------------------------------
    # Add Annotation
    # -------------------------------------------------

    def add_annotation(
        self,
        name,
        datasource="Prometheus",
    ):

        self._annotations.append({

            "name": name,

            "datasource": datasource,

            "enabled": True,

        })

        return True

    # -------------------------------------------------
    # Time Range
    # -------------------------------------------------

    def set_time_range(
        self,
        *,
        start="now-1h",
        end="now",
    ):

        self._time = {

            "from": start,

            "to": end,

        }

        return True

    # -------------------------------------------------
    # Dashboard JSON
    # -------------------------------------------------

    def dashboard(
        self,
    ):

        return {

            "title": self._title,

            "uid": self._uid,

            "timezone": self._timezone,

            "refresh": self._refresh,

            "schemaVersion": 39,

            "version": 1,

            "time": deepcopy(self._time),

            "templating": {

                "list": deepcopy(

                    self._variables

                )

            },

            "annotations": {

                "list": deepcopy(

                    self._annotations

                )

            },

            "panels": deepcopy(

                self._panels

            ),

        }

    # -------------------------------------------------
    # Export JSON
    # -------------------------------------------------

    def export(
        self,
    ):

        return deepcopy(

            self.dashboard()

        )

    # -------------------------------------------------
    # Export String
    # -------------------------------------------------

    def export_json(
        self,
    ):

        return json.dumps(

            self.dashboard(),

            indent=2,

        )

    # -------------------------------------------------
    # Statistics
    # -------------------------------------------------

    def statistics(
        self,
    ):

        return {

            "title": self._title,

            "uid": self._uid,

            "panels": len(

                self._panels

            ),

            "variables": len(

                self._variables

            ),

            "annotations": len(

                self._annotations

            ),

            "refresh": self._refresh,

            "created_at": self._created_at,

        }

    # -------------------------------------------------
    # Clear
    # -------------------------------------------------

    def clear(
        self,
    ):

        self._title = "Enterprise MCP Dashboard"

        self._uid = "enterprise-mcp"

        self._timezone = "browser"

        self._refresh = "30s"

        self._panels = []

        self._variables = []

        self._annotations = []

        self._time = {

            "from": "now-1h",

            "to": "now",

        }

        self._created_at = time.time()

    # -------------------------------------------------
    # Empty
    # -------------------------------------------------

    @staticmethod
    def empty():

        return GrafanaDashboard()