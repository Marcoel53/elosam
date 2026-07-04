from elosam.capabilities.logging_capability import LoggingCapability
from elosam.core.capability_engine import CapabilityEngine
from elosam.core.capability_registry import CapabilityRegistry


def test_capability_engine_initializes_logging() -> None:
    registry = CapabilityRegistry()

    capability = LoggingCapability()

    registry.register(
        capability.name,
        capability,
    )

    engine = CapabilityEngine(registry)

    engine.initialize()

    assert engine.ready()

    engine.shutdown()