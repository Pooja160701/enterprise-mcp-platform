from service import GrafanaService

g = GrafanaService()

print("\nHealth\n")
print(g.health())

print("\nDashboards\n")
print(g.list_dashboards())

print("\nDatasources\n")
print(g.list_datasources())