from elosam.core.agent import Agent
from elosam.core.meta_agent_engine import MetaAgentEngine


def test_meta_analysis():
    agents = [
        Agent("a1", "x", score=0.5),
        Agent("a2", "y", score=2.5),
    ]

    meta = MetaAgentEngine(agents)

    report = meta.analyze()

    assert report["total_agents"] == 2
    assert report["weak_agents"] == 1
    assert report["strong_agents"] == 1


def test_meta_evolution():
    agents = [
        Agent("a1", "x", score=0.5),
        Agent("a2", "y", score=2.5),
    ]

    meta = MetaAgentEngine(agents)

    meta.evolve()

    assert agents[0].score <= 0.5
    assert agents[1].score > 2.5
