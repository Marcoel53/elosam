from elosam.core.event import Event
from elosam.core.event_bus import EventBus


def test_subscribe_and_publish() -> None:
    bus = EventBus()
    received = []

    def handler(event: Event) -> None:
        received.append(event.payload)

    bus.subscribe("message", handler)
    bus.publish("message", "hello")

    assert received == ["hello"]


def test_unsubscribe() -> None:
    bus = EventBus()
    received = []

    def handler(event: Event) -> None:
        received.append(event.payload)

    bus.subscribe("message", handler)
    bus.unsubscribe("message", handler)
    bus.publish("message", "hello")

    assert received == []


def test_multiple_handlers() -> None:
    bus = EventBus()
    received = []

    def first(event: Event) -> None:
        received.append(("first", event.payload))

    def second(event: Event) -> None:
        received.append(("second", event.payload))

    bus.subscribe("message", first)
    bus.subscribe("message", second)

    bus.publish("message", 123)

    assert received == [
        ("first", 123),
        ("second", 123),
    ]


def test_clear() -> None:
    bus = EventBus()
    received = []

    def handler(event: Event) -> None:
        received.append(event.payload)

    bus.subscribe("message", handler)
    bus.clear()
    bus.publish("message", "hello")

    assert received == []
