from __future__ import annotations

from typing import Any
from elosam.core.agent import Agent


class ArbitrationEngine:
    def __init__(self, agents: list[Agent]) -> None:
        self._agents = agents

    def execute(self, payload: dict[str, Any]) -> dict[str, Any]:
        results = []

        for agent in self._agents:
            result = agent.handle(payload)
            result["score"] = agent.score
            results.append(result)

        task = payload.get("task", "")

        best = None
        best_score = -1.0

        for r in results:
            agent_name = r["agent"]

            agent_obj = next(a for a in self._agents if a.name == agent_name)

            score = agent_obj.score

            if agent_obj.capability in task:
                score += 5  # capability boost

            if score > best_score:
                best_score = score
                best = r

        return {
            "selected": best,
            "all_results": results,
            "score": best_score,
        }
