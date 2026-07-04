from elosam.core.health_manager import HealthManager
from elosam.core.health_status import HealthStatus
from elosam.core.service_registry import ServiceRegistry
from elosam.services.base_service import BaseService


class HealthyService(BaseService):
    @property
    def name(self) -> str:
        return "healthy"

    def initialize(self) -> None:
        pass

    def start(self) -> None:
        pass

    def stop(self) -> None:
        pass

    def health(self) -> bool:
        return True


class UnhealthyService(BaseService):
    @property
    def name(self) -> str:
        return "unhealthy"

    def initialize(self) -> None:
        pass

    def start(self) -> None:
        pass

    def stop(self) -> None:
        pass

    def health(self) -> bool:
        return False


def test_health_manager_healthy() -> None:
    registry = ServiceRegistry()
    registry.register(HealthyService())

    manager = HealthManager(registry)

    assert manager.healthy()
    assert manager.status() is HealthStatus.HEALTHY


def test_health_manager_unhealthy() -> None:
    registry = ServiceRegistry()
    registry.register(UnhealthyService())

    manager = HealthManager(registry)

    assert not manager.healthy()
    assert manager.status() is HealthStatus.UNHEALTHY
