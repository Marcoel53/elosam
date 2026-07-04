class ServiceRegistry:
    def __init__(self):
        self._services = {}

    def register(self, service):
        if service.name in self._services:
            raise ValueError("Service already registered")
        self._services[service.name] = service

    def unregister(self, name):
        self._services.pop(name, None)

    def get(self, name):
        return self._services[name]

    def exists(self, name):
        return name in self._services

    def all(self):
        return list(self._services.values())

    def __len__(self):
        return len(self._services)

    def __iter__(self):
        return iter(self._services.values())
