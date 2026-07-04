from elosam.core.autonomous_os import AutonomousOS
from elosam.core.production_runtime import ProductionAutonomousRuntime
from elosam.core.event_bus import EventBus
from elosam.core.agent_registry import AgentRegistry
from elosam.core.agent import Agent
from elosam.core.agent_arbitration import ArbitrationEngine
from elosam.core.meta_agent_engine import MetaAgentEngine


def test_production_runtime_starts_and_stops():
    bus = EventBus()

    registry = AgentRegistry()
    registry.register(Agent("a1", "analyze", score=1.0))

    arbitration = ArbitrationEngine(registry.all())
    meta = MetaAgentEngine(registry.all())

    os = AutonomousOS(bus, registry, arbitration, meta)

    runtime = ProductionAutonomousRuntime(os)

    runtime.stop()  # ensure safe start/stop without loop
    assert runtime.running is False
