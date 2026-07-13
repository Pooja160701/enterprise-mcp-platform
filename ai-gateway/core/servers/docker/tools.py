from .service import DockerService

service = DockerService()


TOOLS = {

    "list_running_containers":
        service.list_running_containers,

    "list_all_containers":
        service.list_all_containers,

    "list_images":
        service.list_images,

    "inspect_container":
        service.inspect_container,

}