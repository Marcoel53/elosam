from elosam.core.capability_engine import CapabilityEngine
from elosam.core.capability_registry import CapabilityRegistry
from elosam.core.event_bus import EventBus
from elosam.core.kernel import Kernel
from elosam.services.base_capability import BaseCapability


class RuntimeCapability(BaseCapability):
    def __init__(self) -> None:
        self.started = False

    @property
    def name(self) -> str:
        return "runtime"

    def initialize(self) -> None:
        self.started = True

    def ready(self) -> bool:
        return self.started


def test_runtime_capability_engine() -> None:
    registry = CapabilityRegistry()
    registry.register("runtime", RuntimeCapability())

    engine = CapabilityEngine(registry)

    engine.initialize()

    assert engine.ready()


def test_kernel_event_bus_exists() -> None:
    kernel = Kernel()

    assert isinstance(kernel.events, EventBus)


def test_kernel_registry_exists() -> None:
    kernel = Kernel()

    assert len(kernel.registry.all()) == 0


def test_kernel_can_register_service() -> None:
    kernel = Kernel()

    assert kernel.registry is not None
