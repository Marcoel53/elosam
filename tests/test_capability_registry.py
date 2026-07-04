from elosam.core.capability_registry import CapabilityRegistry
from elosam.services.base_capability import BaseCapability


class DummyCapability(BaseCapability):
    @property
    def name(self) -> str:
        return "dummy"


def test_register() -> None:
    registry = CapabilityRegistry()
    capability = DummyCapability()

    registry.register(capability.name, capability)

    assert registry.exists("dummy")
    assert registry.get("dummy") is capability


def test_unregister() -> None:
    registry = CapabilityRegistry()
    capability = DummyCapability()

    registry.register(capability.name, capability)
    registry.unregister("dummy")

    assert not registry.exists("dummy")


def test_duplicate_registration() -> None:
    registry = CapabilityRegistry()

    registry.register("dummy", DummyCapability())

    try:
        registry.register("dummy", DummyCapability())
        assert False
    except ValueError:
        assert True


def test_iteration() -> None:
    registry = CapabilityRegistry()

    registry.register("dummy", DummyCapability())

    assert len(list(registry)) == 1
