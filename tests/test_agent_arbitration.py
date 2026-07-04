from elosam.core.agent_registry import Agent
from elosam.core.agent_arbitration import ArbitrationEngine


def test_arbitration_selects_best():
    a1 = Agent("analyzer", "analyze")
    a2 = Agent("executor", "run")

    engine = ArbitrationEngine([a1, a2])

    result = engine.execute({"task": "analyze data"})

    assert result["selected"]["agent"] == "analyzer"


def test_arbitration_returns_all():
    a1 = Agent("a", "x")
    a2 = Agent("b", "y")

    engine = ArbitrationEngine([a1, a2])

    result = engine.execute({"task": "something"})

    assert len(result["all_results"]) == 2
