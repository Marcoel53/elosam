from elosam.core.decision_engine import DecisionEngine
from elosam.core.event_bus import EventBus


def test_decision_event_execution() -> None:
    bus = EventBus()
    engine = DecisionEngine()

    results = []

    engine.bind(bus)

    bus.subscribe(
        "decision.executed",
        lambda event: results.append(event.payload),
    )

    bus.publish(
        "decision.requested",
        {"task": "analyze"},
    )

    assert len(results) == 1
    assert results[0].decision == "accept"


def test_decision_empty_context_event() -> None:
    bus = EventBus()
    engine = DecisionEngine()

    results = []

    engine.bind(bus)

    bus.subscribe(
        "decision.executed",
        lambda event: results.append(event.payload),
    )

    bus.publish(
        "decision.requested",
        {},
    )

    assert results[0].decision == "reject"
