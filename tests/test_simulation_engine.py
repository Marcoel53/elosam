from elosam.core.patch_generator import Patch
from elosam.core.simulation_engine import SimulationEngine


def test_simulation_low_risk():
    engine = SimulationEngine(system_state={})

    patch = Patch(
        target="system",
        change="minor logging improvement",
        reason="test",
    )

    result = engine.simulate(patch)

    assert result.impact in ["low", "medium"]
    assert isinstance(result.safe, bool)


def test_simulation_high_risk():
    engine = SimulationEngine(system_state={})

    patch = Patch(
        target="system",
        change="remove PolicyEngine and MetaAgentEngine",
        reason="test",
    )

    result = engine.simulate(patch)

    assert result.impact == "high"
    assert result.risk_score > 0.5
