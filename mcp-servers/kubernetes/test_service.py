from service import KubernetesService

service = KubernetesService()

print("\nNodes\n")
print(service.list_nodes())

print("\nNamespaces\n")
print(service.list_namespaces())

print("\nPods\n")
print(service.list_pods())

print("\nDeployments\n")
print(service.list_deployments())

print("\nServices\n")
print(service.list_services())