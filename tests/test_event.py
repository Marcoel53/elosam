from elosam.core.event import Event


def test_event_name() -> None:
    event = Event("kernel.started")

    assert event.name == "kernel.started"


def test_event_payload() -> None:
    event = Event(
        "kernel.started",
        payload={"version": "1.0"},
    )

    assert event.payload["version"] == "1.0"


def test_event_timestamp() -> None:
    event = Event("kernel.started")

    assert event.timestamp is not None


def test_events_are_independent() -> None:
    first = Event("a")
    second = Event("b")

    assert first != second
