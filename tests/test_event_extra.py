from elosam.core.event import Event


def test_event_payload_none() -> None:
    event = Event("empty")

    assert event.payload is None


def test_event_name_preserved() -> None:
    event = Event("runtime.started")

    assert event.name == "runtime.started"
