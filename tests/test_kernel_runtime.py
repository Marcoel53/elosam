from elosam.core.event_bus import EventBus
from elosam.core.kernel import Kernel
from elosam.core.service_registry import ServiceRegistry


def test_kernel_exposes_registry() -> None:
    kernel = Kernel()

    assert isinstance(kernel.registry, ServiceRegistry)


def test_kernel_exposes_event_bus() -> None:
    kernel = Kernel()

    assert isinstance(kernel.events, EventBus)


def test_kernel_initial_state() -> None:
    kernel = Kernel()

    assert kernel.healthy()


def test_kernel_stop_without_services() -> None:
    kernel = Kernel()

    kernel.stop()

    assert kernel.healthy()
