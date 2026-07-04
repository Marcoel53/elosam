from elosam.services.base_capability import BaseCapability


class DummyCapability(BaseCapability):
    pass


def test_default_name() -> None:
    capability = DummyCapability()

    assert capability.name == "DummyCapability"


def test_default_ready() -> None:
    capability = DummyCapability()

    assert capability.ready()


def test_initialize_shutdown() -> None:
    capability = DummyCapability()

    capability.initialize()
    capability.shutdown()

    assert capability.ready()
