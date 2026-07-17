import json

from app.observability.grafana_dashboard import GrafanaDashboard


def pretty(data):

    print(
        json.dumps(
            data,
            indent=2,
        )
    )


print("\n=== Grafana Dashboard Test ===\n")

# -------------------------------------------------
# Initialize
# -------------------------------------------------

print("Initializing Grafana Dashboard\n")

dashboard = GrafanaDashboard()

pretty(
    dashboard.statistics()
)

# -------------------------------------------------
# Configure Dashboard
# -------------------------------------------------

print("\nConfiguring Dashboard\n")

dashboard.configure(

    title="Enterprise MCP Platform",

    uid="enterprise-mcp-platform",

    refresh="10s",

)

pretty(
    dashboard.statistics()
)

# -------------------------------------------------
# Add Panels
# -------------------------------------------------

print("\nAdding Panels\n")

print(

    dashboard.add_panel(

        title="CPU Usage",

        panel_type="timeseries",

        targets=[
            {
                "expr": "cpu_usage_percent",
            }
        ],

    )

)

print(

    dashboard.add_panel(

        title="Memory Usage",

        panel_type="timeseries",

        targets=[
            {
                "expr": "memory_usage_percent",
            }
        ],

    )

)

print(

    dashboard.add_panel(

        title="HTTP Requests",

        panel_type="stat",

        targets=[
            {
                "expr": "http_requests_total",
            }
        ],

    )

)

pretty(
    dashboard.statistics()
)

# -------------------------------------------------
# Add Variables
# -------------------------------------------------

print("\nAdding Variables\n")

print(

    dashboard.add_variable(

        "environment",

        "label_values(environment)",

    )

)

print(

    dashboard.add_variable(

        "instance",

        "label_values(instance)",

    )

)

pretty(
    dashboard.statistics()
)

# -------------------------------------------------
# Add Annotations
# -------------------------------------------------

print("\nAdding Annotations\n")

print(
    dashboard.add_annotation(
        "Deployments",
    )
)

print(
    dashboard.add_annotation(
        "Alerts",
    )
)

pretty(
    dashboard.statistics()
)

# -------------------------------------------------
# Set Time Range
# -------------------------------------------------

print("\nSetting Time Range\n")

print(

    dashboard.set_time_range(

        start="now-24h",

        end="now",

    )

)

# -------------------------------------------------
# Dashboard
# -------------------------------------------------

print("\nDashboard\n")

pretty(
    dashboard.dashboard()
)

# -------------------------------------------------
# Export JSON
# -------------------------------------------------

print("\nExport JSON\n")

print(
    dashboard.export_json()
)

# -------------------------------------------------
# Export Dictionary
# -------------------------------------------------

print("\nExport\n")

pretty(
    dashboard.export()
)

# -------------------------------------------------
# Remove Panel
# -------------------------------------------------

print("\nRemoving Panel\n")

print(
    dashboard.remove_panel(2)
)

pretty(
    dashboard.statistics()
)

# -------------------------------------------------
# Cleanup
# -------------------------------------------------

print("\nCleanup\n")

dashboard.clear()

pretty(
    dashboard.statistics()
)

print("\nGrafana Dashboard Test Passed")