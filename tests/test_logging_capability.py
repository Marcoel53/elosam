from elosam.capabilities.logging_capability import LoggingCapability


def test_logging_capability_ready() -> None:
    capability = LoggingCapability()

    capability.initialize()

    assert capability.ready()

    capability.shutdown()