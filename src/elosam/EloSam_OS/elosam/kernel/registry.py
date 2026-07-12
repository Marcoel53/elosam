from collections.abc import Callable
from typing import Any

from .descriptors import CapabilityDescriptor


class CapabilityRegistry:
    def __init__(self):
        self._descriptors: dict[str, CapabilityDescriptor] = {}
        self._implementations: dict[str, Callable[..., Any]] = {}

    def register(
        self,
        descriptor: CapabilityDescriptor,
        implementation: Callable[..., Any],
    ):
        self._descriptors[descriptor.id] = descriptor
        self._implementations[descriptor.id] = implementation

    def get_descriptor(self, name: str):
        return self._descriptors.get(name)

    def get_implementation(self, name: str):
        return self._implementations.get(name)

    def list_capabilities(self):
        return sorted(self._descriptors.keys())

    def count(self):
        return len(self._descriptors)
