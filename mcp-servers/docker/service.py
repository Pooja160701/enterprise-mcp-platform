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

        return {
            "id": container.short_id,
            "name": container.name,
            "status": container.status,
            "image": container.image.tags,
        }


    def container_logs(self, name: str, tail: int = 50):

        container = self.client.containers.get(name)

        return container.logs(tail=tail).decode()


    def start_container(self, name: str):

        container = self.client.containers.get(name)

        container.start()

        return {
            "status": "started",
            "container": name,
        }


    def stop_container(self, name: str):

        try:

            container = self.client.containers.get(name)

            container.stop()

            return {
                "success": True,
                "container": name,
                "status": "stopped",
            }

        except docker.errors.NotFound:

            return {
                "success": False,
                "error": f"Container '{name}' not found."
            }

        except Exception as e:

            return {
                "success": False,
                "error": str(e)
            }