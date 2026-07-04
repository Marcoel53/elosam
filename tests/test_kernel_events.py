from elosam.core.event import Event
from elosam.core.kernel import Kernel
from elosam.services.base_service import BaseService


class DummyService(BaseService):
    @property
    def name(self) -> str:
        return "dummy"

    def initialize(self) -> None:
        pass

    def start(self) -> None:
        pass

    def stop(self) -> None:
        pass

    def health(self) -> bool:
        return True


def test_kernel_publishes_service_registered_event() -> None:
    kernel = Kernel()

    received = []

    kernel.events.subscribe(
        "service.registered",
        lambda event: received.append(event.payload),
    )

    kernel.register(DummyService())

    assert received == ["dummy"]


def test_kernel_publishes_lifecycle_events() -> None:
    kernel = Kernel()

    events = []

    kernel.events.subscribe(
        "kernel.initializing",
        lambda event: events.append(event.name),
    )

    kernel.events.subscribe(
        "kernel.running",
        lambda event: events.append(event.name),
    )

    kernel.initialize()

    assert events == [
        "kernel.initializing",
        "kernel.running",
    ]
