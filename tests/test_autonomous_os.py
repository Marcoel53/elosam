from elosam.core.event_bus import EventBus
from elosam.core.agent import Agent
from elosam.core.agent_registry import AgentRegistry
from elosam.core.agent_arbitration import ArbitrationEngine
from elosam.core.meta_agent_engine import MetaAgentEngine
from elosam.core.autonomous_os import AutonomousOS


def test_autonomous_os_event_flow():
    bus = EventBus()

    registry = AgentRegistry()
    registry.register(Agent("a1", "analyze", score=1.0))

    arbitration = ArbitrationEngine(registry.all())
    meta = MetaAgentEngine(registry.all())

    os = AutonomousOS(bus, registry, arbitration, meta)

    results = os.run_cycle({"task": "analyze data"}, iterations=2)

    assert len(results) == 2


def test_autonomous_os_event_binding():
    bus = EventBus()

    registry = AgentRegistry()
    registry.register(Agent("a1", "run", score=1.0))

    arbitration = ArbitrationEngine(registry.all())
    meta = MetaAgentEngine(registry.all())

    os = AutonomousOS(bus, registry, arbitration, meta)

    bus.publish("system.task", {"task": "run job"})
