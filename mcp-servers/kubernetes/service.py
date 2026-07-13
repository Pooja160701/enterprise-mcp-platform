from kubernetes import client, config


class KubernetesService:

    def __init__(self):
        """
        Load kubeconfig.

        Works with:
        - Docker Desktop Kubernetes
        - Minikube
        - Kind
        - AKS
        - EKS
        """

        try:
            config.load_kube_config()
        except Exception:
            config.load_incluster_config()

        self.core = client.CoreV1Api()
        self.apps = client.AppsV1Api()

    #
    # Nodes
    #

    def list_nodes(self):

        nodes = self.core.list_node().items

        result = []

        for node in nodes:

            result.append(
                {
                    "name": node.metadata.name,
                    "status": node.status.conditions[-1].type,
                    "kubelet_version": node.status.node_info.kubelet_version,
                }
            )

        return result

    #
    # Namespaces
    #

    def list_namespaces(self):

        namespaces = self.core.list_namespace().items

        result = []

        for ns in namespaces:

            result.append(
                {
                    "name": ns.metadata.name,
                    "status": ns.status.phase,
                }
            )

        return result

    #
    # Pods
    #

    def list_pods(
        self,
        namespace: str = "default",
    ):

        pods = self.core.list_namespaced_pod(
            namespace=namespace
        ).items

        result = []

        for pod in pods:

            result.append(
                {
                    "name": pod.metadata.name,
                    "status": pod.status.phase,
                    "node": pod.spec.node_name,
                }
            )

        return result

    #
    # Deployments
    #

    def list_deployments(
        self,
        namespace: str = "default",
    ):

        deployments = self.apps.list_namespaced_deployment(
            namespace=namespace
        ).items

        result = []

        for deployment in deployments:

            result.append(
                {
                    "name": deployment.metadata.name,
                    "replicas": deployment.status.ready_replicas or 0,
                }
            )

        return result

    #
    # Services
    #

    def list_services(
        self,
        namespace: str = "default",
    ):

        services = self.core.list_namespaced_service(
            namespace=namespace
        ).items

        result = []

        for svc in services:

            result.append(
                {
                    "name": svc.metadata.name,
                    "type": svc.spec.type,
                    "cluster_ip": svc.spec.cluster_ip,
                }
            )

        return result