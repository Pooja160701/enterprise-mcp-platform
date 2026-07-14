from service import GrafanaService

service = GrafanaService()


def health():
    return service.health()


def list_dashboards():
    return service.list_dashboards()


def list_datasources():
    return service.list_datasources()


def dashboard_info(uid: str):
    return service.dashboard_info(uid)


def list_alerts():
    return service.list_alerts()