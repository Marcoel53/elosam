from elosam.core.agent import Agent
from elosam.core.agent_registry import AgentRegistry
from elosam.core.agent_arbitration import ArbitrationEngine
from elosam.core.meta_agent_engine import MetaAgentEngine
from elosam.core.autonomous_runtime import AutonomousRuntime


def test_autonomous_runtime_cycle():
    registry = AgentRegistry()

    registry.register(Agent("a1", "analyze", score=1.0))
    registry.register(Agent("a2", "run", score=1.0))

    arbitration = ArbitrationEngine(registry.all())
    meta = MetaAgentEngine(registry.all())

    runtime = AutonomousRuntime(registry, arbitration, meta)

    results = runtime.cycle({"task": "analyze data"}, iterations=2)

    assert len(results) == 2
