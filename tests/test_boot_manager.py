from elosam.core.boot_manager import BootManager
from elosam.core.lifecycle import Lifecycle
from elosam.core.lifecycle_state import LifecycleState
from elosam.core.service_registry import ServiceRegistry
from elosam.services.base_service import BaseService


class DummyService(BaseService):
    def __init__(self) -> None:
        self.initialized = False
        self.started = False
        self.stopped = False

    def initialize(self) -> None:
        self.initialized = True

    def start(self) -> None:
        self.started = True

    def stop(self) -> None:
        self.stopped = True


def test_boot_manager_boot() -> None:
    lifecycle = Lifecycle()
    registry = ServiceRegistry()

    service = DummyService()
    registry.register(service)

    boot = BootManager(lifecycle, registry)
    boot.boot()

    assert service.initialized
    assert service.started
    assert lifecycle.state is LifecycleState.RUNNING


def test_boot_manager_shutdown() -> None:
    lifecycle = Lifecycle()
    registry = ServiceRegistry()

    service = DummyService()
    registry.register(service)

    boot = BootManager(lifecycle, registry)

    boot.boot()
    boot.shutdown()

    assert service.stopped
    assert lifecycle.state is LifecycleState.STOPPED
