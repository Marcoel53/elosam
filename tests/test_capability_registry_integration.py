from elosam.capabilities.logging_capability import LoggingCapability
from elosam.core.capability_registry import CapabilityRegistry


def test_logging_capability_registration() -> None:
    registry = CapabilityRegistry()

    capability = LoggingCapability()

    registry.register(
        capability.name,
        capability,
    )

    assert registry.exists("logging")

    loaded = registry.get("logging")

    assert loaded is capability