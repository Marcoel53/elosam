"""
AEGIS META AGENT ENGINE.
Now capable of generating new agents automatically.
"""

from __future__ import annotations

from typing import Any
from elosam.core.agent import Agent


class MetaAgentEngine:
    def __init__(self, agents: list[Agent]) -> None:
        self._agents = agents

    def analyze(self) -> dict[str, Any]:
        total = len(self._agents)

        avg_score = sum(a.score for a in self._agents) / total if total else 0

        weak = [a for a in self._agents if a.score < 1.0]
        strong = [a for a in self._agents if a.score >= 2.0]

        return {
            "total_agents": total,
            "average_score": avg_score,
            "weak_agents": len(weak),
            "strong_agents": len(strong),
        }

    def evolve(self) -> None:
        for agent in self._agents:
            if agent.score < 1.0:
                agent.score = max(0.1, agent.score - 0.1)
            elif agent.score >= 2.0:
                agent.score += 0.05

    def generate_agents(self) -> list[Agent]:
        """
        Create new agents when system is unbalanced.
        """

        new_agents: list[Agent] = []

        # If too many weak agents ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ create analyzer agent
        weak_count = sum(1 for a in self._agents if a.score < 1.0)

        if weak_count > 1:
            new_agents.append(Agent("auto_analyzer", "analyze", score=1.0))

        # If no executor agents ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ create one
        if not any(a.capability == "run" for a in self._agents):
            new_agents.append(Agent("auto_executor", "run", score=1.0))

        # If system too small ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ bootstrap general agent
        if len(self._agents) < 2:
            new_agents.append(Agent("auto_generalist", "general", score=1.0))

        self._agents.extend(new_agents)

        return new_agents
