from elosam.core.agent_registry import AgentRegistry, Agent


def test_agent_routing():
    registry = AgentRegistry()

    analyzer = Agent("analyzer", "analyze")
    executor = Agent("executor", "run")

    registry.register(analyzer)
    registry.register(executor)

    result = registry.route({"task": "analyze data"})

    assert result["agent"] == "analyzer"


def test_fallback_agent():
    registry = AgentRegistry()

    agent = Agent("default", "general")
    registry.register(agent)

    result = registry.route({"task": "unknown task"})

    assert result["agent"] == "default"
