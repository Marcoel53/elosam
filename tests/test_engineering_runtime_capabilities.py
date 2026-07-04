from elosam.capabilities.logging_capability import LoggingCapability
from elosam.core.capability_engine import CapabilityEngine
from elosam.core.capability_registry import CapabilityRegistry


def test_runtime_capability_stack() -> None:
    registry = CapabilityRegistry()

    registry.register(
        "logging",
        LoggingCapability(),
    )

    engine = CapabilityEngine(registry)

    engine.initialize()

    assert registry.exists("logging")

    assert engine.ready()