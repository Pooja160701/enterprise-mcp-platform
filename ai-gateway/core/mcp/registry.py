class MCPRegistry:
    def __init__(self):
        self._servers = {}

    def register(self, name, session):
        self._servers[name] = session

    def get(self, name):
        return self._servers.get(name)

    def list_servers(self):
        return list(self._servers.keys())