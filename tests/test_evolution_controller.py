from elosam.core.agent import Agent
from elosam.core.agent_registry import AgentRegistry
from elosam.core.agent_arbitration import ArbitrationEngine
from elosam.core.meta_agent_engine import MetaAgentEngine
from elosam.core.autonomous_runtime import AutonomousRuntime
from elosam.core.evolution_controller import EvolutionController


def test_evolution_controller_cycle():
    registry = AgentRegistry()
    registry.register(Agent("a1", "analyze", score=1.0))

    arbitration = ArbitrationEngine(registry.all())
    meta = MetaAgentEngine(registry.all())

    runtime = AutonomousRuntime(registry, arbitration, meta)

    controller = EvolutionController(runtime, arbitration, meta)
    controller.start()

    results = controller.cycle({"task": "analyze data"}, max_cycles=3)

    assert len(results) == 3


def test_evolution_controller_stop():
    registry = AgentRegistry()
    registry.register(Agent("a1", "run", score=1.0))

    arbitration = ArbitrationEngine(registry.all())
    meta = MetaAgentEngine(registry.all())

    runtime = AutonomousRuntime(registry, arbitration, meta)

    controller = EvolutionController(runtime, arbitration, meta)
    controller.start()
    controller.stop()

    results = controller.cycle({"task": "run job"}, max_cycles=5)

    assert len(results) <= 5
