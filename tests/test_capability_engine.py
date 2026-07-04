from elosam.core.capability_engine import CapabilityEngine
from elosam.core.capability_registry import CapabilityRegistry
from elosam.services.base_capability import BaseCapability


class DummyCapability(BaseCapability):
    def __init__(self) -> None:
        self.initialized = False
        self.stopped = False

    @property
    def name(self) -> str:
        return "dummy"

    def initialize(self) -> None:
        self.initialized = True

    def shutdown(self) -> None:
        self.stopped = True

    def ready(self) -> bool:
        return self.initialized and not self.stopped


def test_initialize() -> None:
    registry = CapabilityRegistry()
    capability = DummyCapability()

    registry.register(capability.name, capability)

    engine = CapabilityEngine(registry)
    engine.initialize()

    assert capability.initialized


def test_ready() -> None:
    registry = CapabilityRegistry()
    capability = DummyCapability()

    registry.register(capability.name, capability)

    engine = CapabilityEngine(registry)

    engine.initialize()

    assert engine.ready()


def test_shutdown() -> None:
    registry = CapabilityRegistry()
    capability = DummyCapability()

    registry.register(capability.name, capability)

    engine = CapabilityEngine(registry)

    engine.initialize()
    engine.shutdown()

    assert capability.stopped


def test_empty_registry() -> None:
    registry = CapabilityRegistry()

    engine = CapabilityEngine(registry)

    assert engine.ready()
