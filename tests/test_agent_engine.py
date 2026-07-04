from elosam.core.event_bus import EventBus
from elosam.core.mission_engine import MissionEngine
from elosam.core.agent_engine import AgentEngine


def test_agent_executes_mission():
    bus = EventBus()
    missions = MissionEngine()
    agent = AgentEngine(bus, missions)

    agent.bind()

    results = []

    bus.subscribe(
        "agent.executed",
        lambda e: results.append(e.payload),
    )

    bus.publish(
        "agent.request",
        {
            "id": "m1",
            "name": "test",
            "data": {"task": "analyze"},
        },
    )

    assert len(results) == 1
    assert results[0]["mission_id"] == "m1"
