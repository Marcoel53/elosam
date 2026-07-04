"""
AEGIS CORE Boot Manager.
"""

from __future__ import annotations

from elosam.core.lifecycle import Lifecycle
from elosam.core.service_registry import ServiceRegistry


class BootManager:
    """
    Coordinates the Kernel bootstrap process.
    """

    def __init__(
        self,
        lifecycle: Lifecycle,
        registry: ServiceRegistry,
    ) -> None:
        self._lifecycle = lifecycle
        self._registry = registry

    def boot(self) -> None:
        """
        Boot all registered services.
        """

        self._lifecycle.initializing()

        for service in self._registry:
            service.initialize()

        self._lifecycle.initialized()

        self._lifecycle.starting()

        for service in self._registry:
            service.start()

        self._lifecycle.running()

    def shutdown(self) -> None:
        """
        Shutdown all registered services.
        """

        self._lifecycle.stopping()

        for service in reversed(self._registry.all()):
            service.stop()

        self._lifecycle.stopped()
