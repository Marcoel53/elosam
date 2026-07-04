from elosam.core.kernel import Kernel
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


def test_kernel_lifecycle() -> None:
    kernel = Kernel()
    service = DummyService()

    kernel.register(service)

    kernel.initialize()
    kernel.start()

    assert service.initialized
    assert service.started

    kernel.stop()

    assert service.stopped


def test_kernel_health() -> None:
    kernel = Kernel()

    kernel.register(DummyService())

    assert kernel.healthy()