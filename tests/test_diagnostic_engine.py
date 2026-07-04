from elosam.core.observability_engine import ObservabilityEngine
from elosam.core.diagnostic_engine import DiagnosticEngine


def test_diagnostic_detects_empty_system():
    obs = ObservabilityEngine()
    diag = DiagnosticEngine(obs)

    report = diag.analyze()

    assert report["status"] == "empty"
    assert "no_activity_detected" in report["issues"]


def test_diagnostic_detects_healthy_flow():
    obs = ObservabilityEngine()

    obs.log("agent", "execute", {})
    obs.log("meta", "evolve", {})
    obs.log("decision", "evaluate", {})

    diag = DiagnosticEngine(obs)

    report = diag.analyze()

    assert "layers" in report
