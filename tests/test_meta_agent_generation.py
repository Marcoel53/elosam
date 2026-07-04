from elosam.core.agent import Agent
from elosam.core.meta_agent_engine import MetaAgentEngine


def test_agent_generation():
    agents = [
        Agent("a1", "analyze", score=0.5),
    ]

    meta = MetaAgentEngine(agents)

    new_agents = meta.generate_agents()

    assert len(new_agents) >= 1
    assert any(a.name == "auto_executor" for a in new_agents)
