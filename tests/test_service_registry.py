from elosam.core.service_registry import ServiceRegistry
from elosam.services.base_service import BaseService


class FakeService(BaseService):
    """Service used only for tests."""

    pass


def test_register_service() -> None:
    registry = ServiceRegistry()

    service = FakeService()

    registry.register(service)

    assert len(registry) == 1
    assert registry.exists(service.name)
    assert registry.get(service.name) is service


def test_unregister_service() -> None:
    registry = ServiceRegistry()

    service = FakeService()

    registry.register(service)
    registry.unregister(service.name)

    assert len(registry) == 0
    assert not registry.exists(service.name)


def test_duplicate_registration() -> None:
    registry = ServiceRegistry()

    service = FakeService()

    registry.register(service)

    try:
        registry.register(service)
    except ValueError:
        return

    assert False, "Expected ValueError"