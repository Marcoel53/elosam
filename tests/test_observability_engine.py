from elosam.core.observability_engine import ObservabilityEngine


def test_trace_logging():
    obs = ObservabilityEngine()

    obs.log("agent", "execute", {"id": 1})
    obs.log("decision", "evaluate", {"ok": True})

    assert len(obs.all()) == 2


def test_filter_by_layer():
    obs = ObservabilityEngine()

    obs.log("agent", "run", {})
    obs.log("meta", "evolve", {})

    assert len(obs.filter_by_layer("agent")) == 1
