"""
AEGIS CORE Health Manager.
"""

from __future__ import annotations

from elosam.core.health_status import HealthStatus
from elosam.core.service_registry import ServiceRegistry


class HealthManager:
    """
    Evaluates the health of the runtime.
    """

    def __init__(self, registry: ServiceRegistry) -> None:
        self._registry = registry

    def status(self) -> HealthStatus:
        """
        Returns the current runtime health status.
        """
        if all(service.health() for service in self._registry):
            return HealthStatus.HEALTHY

        return HealthStatus.UNHEALTHY

    def healthy(self) -> bool:
        """
        Returns True when the runtime is healthy.
        """
        return self.status() is HealthStatus.HEALTHY
