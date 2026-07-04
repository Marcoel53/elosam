from elosam.core.diagnostic_engine import DiagnosticEngine
from elosam.core.observability_engine import ObservabilityEngine
from elosam.core.healing_engine import HealingEngine


def test_healing_detects_missing_agent_flow():
    obs = ObservabilityEngine()
    diag = DiagnosticEngine(obs)

    healer = HealingEngine(diag)

    result = healer.heal()

    assert "patches" in result
    assert isinstance(result["patches"], list)


def test_healing_with_activity():
    obs = ObservabilityEngine()

    obs.log("agent", "execute", {})
    obs.log("meta", "evolve", {})
    obs.log("decision", "evaluate", {})

    diag = DiagnosticEngine(obs)
    healer = HealingEngine(diag)

    result = healer.heal()

    assert isinstance(result, dict)
