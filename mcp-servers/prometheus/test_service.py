from service import PrometheusService

prom = PrometheusService()

print("\nHealth\n")
print(prom.health())

print("\nTargets\n")
print(prom.list_targets())

print("\nAlerts\n")
print(prom.list_alerts())

print("\nRules\n")
print(prom.list_rules())

#
# Example Instant Query
#

print("\nQuery: up\n")
print(
    prom.query(
        "up"
    )
)