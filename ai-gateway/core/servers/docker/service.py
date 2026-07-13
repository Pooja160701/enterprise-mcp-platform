import docker


class DockerService:

    def __init__(self):
        self.client = docker.from_env()

    def list_running_containers(self):

        result = []

        for container in self.client.containers.list():

            result.append({
                "id": container.short_id,
                "name": container.name,
                "image": (
                    container.image.tags[0]
                    if container.image.tags
                    else "<none>"
                ),
                "status": container.status,
            })

        return result

    def list_all_containers(self):

        result = []

        for container in self.client.containers.list(all=True):

            result.append({
                "id": container.short_id,
                "name": container.name,
                "image": (
                    container.image.tags[0]
                    if container.image.tags
                    else "<none>"
                ),
                "status": container.status,
            })

        return result

    def list_images(self):

        images = []

        for image in self.client.images.list():

            images.append({

                "id": image.short_id,

                "tags": image.tags,

            })

        return images

    def inspect_container(self, name: str):

        container = self.client.containers.get(name)

        return container.attrs