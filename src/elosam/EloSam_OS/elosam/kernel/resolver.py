import inspect


class CapabilityResolver:
    def __init__(self, registry):
        self.registry = registry

    def resolve(self, name: str):
        return self.registry.get_implementation(name)

    async def execute(self, name: str, **parameters):
        implementation = self.resolve(name)

        if implementation is None:
            raise KeyError(f"Capability não encontrada: {name}")

        result = implementation(self, **parameters)

        if inspect.isawaitable(result):
            result = await result

        return result


