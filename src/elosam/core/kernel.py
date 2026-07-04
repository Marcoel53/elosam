"""
AEGIS CORE Kernel.
"""

from __future__ import annotations

from elosam.contracts.service import Service
from elosam.core.boot_manager import BootManager
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
        self._boot = BootManager(
            self._lifecycle,
            self._registry,
        )

    @property
    def registry(self) -> ServiceRegistry:
        return self._registry

    @property
    def state(self) -> LifecycleState:
        return self._lifecycle.state

    def register(self, service: Service) -> None:
        self._registry.register(service)

    def initialize(self) -> None:
        """
        Maintained for backward compatibility.
        """
        self._boot.boot()

    def start(self) -> None:
        """
        Maintained for backward compatibility.
        """

    def stop(self) -> None:
        self._boot.shutdown()

    def healthy(self) -> bool:
        return all(service.health() for service in self._registry)
