"""
AEGIS CORE Kernel.
"""

from __future__ import annotations

from elosam.contracts.service import Service
from elosam.core.lifecycle import Lifecycle
from elosam.core.lifecycle_state import LifecycleState
from elosam.core.service_registry import ServiceRegistry


class Kernel:
    """
    Central runtime coordinator.
    """

    def __init__(self) -> None:
        self._registry = ServiceRegistry()
        self._lifecycle = Lifecycle()

    @property
    def registry(self) -> ServiceRegistry:
        return self._registry

    @property
    def state(self) -> LifecycleState:
        return self._lifecycle.state

    def register(self, service: Service) -> None:
        self._registry.register(service)

    def initialize(self) -> None:
        self._lifecycle.initializing()

        for service in self._registry:
            service.initialize()

        self._lifecycle.initialized()

    def start(self) -> None:
        self._lifecycle.starting()

        for service in self._registry:
            service.start()

        self._lifecycle.running()

    def stop(self) -> None:
        self._lifecycle.stopping()

        for service in reversed(self._registry.all()):
            service.stop()

        self._lifecycle.stopped()

    def healthy(self) -> bool:
        return all(service.health() for service in self._registry)
