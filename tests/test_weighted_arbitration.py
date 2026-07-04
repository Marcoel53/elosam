from elosam.core.agent import Agent
from elosam.core.agent_arbitration import ArbitrationEngine


def test_weighted_arbitration():
    a1 = Agent("analyzer", "analyze", score=1.0)
    a2 = Agent("executor", "run", score=5.0)

    engine = ArbitrationEngine([a1, a2])

    result = engine.execute({"task": "analyze data"})

    assert result["selected"]["agent"] == "analyzer"
