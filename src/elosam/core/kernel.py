"""
AEGIS CORE Kernel.
"""

from __future__ import annotations

from elosam.contracts.service import Service
from elosam.core.service_registry import ServiceRegistry


class Kernel:
    """
    Central runtime coordinator.

    The Kernel is intentionally small.
    Its only responsibility is orchestrating services.
    """

    def __init__(self) -> None:
        self._registry = ServiceRegistry()

    @property
    def registry(self) -> ServiceRegistry:
        return self._registry

    def register(self, service: Service) -> None:
        self._registry.register(service)

    def initialize(self) -> None:
        for service in self._registry:
            service.initialize()

    def start(self) -> None:
        for service in self._registry:
            service.start()

    def stop(self) -> None:
        for service in reversed(self._registry.all()):
            service.stop()

    def healthy(self) -> bool:
        return all(service.health() for service in self._registry)