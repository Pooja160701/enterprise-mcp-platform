from service import PrometheusService

service = PrometheusService()


#
# -------------------------
# Health
# -------------------------
#

def health():
    return service.health()


#
# -------------------------
# Targets
# -------------------------
#

def list_targets():
    return service.list_targets()


#
# -------------------------
# Alerts
# -------------------------
#

def list_alerts():
    return service.list_alerts()


#
# -------------------------
# Rules
# -------------------------
#

def list_rules():
    return service.list_rules()


#
# -------------------------
# Instant Query
# -------------------------
#

def query(expression: str):
    return service.query(expression)


#
# -------------------------
# Range Query
# -------------------------
#

def query_range(
    expression: str,
    start: str,
    end: str,
    step: str = "60s",
):
    return service.query_range(
        expression,
        start,
        end,
        step,
    )