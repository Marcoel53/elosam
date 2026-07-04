from elosam.services.base_capability import BaseCapability


class ReadyCapability(BaseCapability):
    pass


class NotReadyCapability(BaseCapability):
    def ready(self) -> bool:
        return False


def test_base_capability_name() -> None:
    capability = ReadyCapability()

    assert capability.name == "ReadyCapability"


def test_capability_ready_override() -> None:
    capability = NotReadyCapability()

    assert capability.ready() is False
