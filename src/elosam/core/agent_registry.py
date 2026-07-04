from __future__ import annotations

from typing import Any
from elosam.core.agent import Agent


class AgentRegistry:
    def __init__(self) -> None:
        self._agents: list[Agent] = []

    def register(self, agent: Agent) -> None:
        self._agents.append(agent)

    def all(self) -> list[Agent]:
        return self._agents

    # ----------------------------
    # COMPATIBILITY LAYER (FIX)
    # ----------------------------
    def route(self, payload: dict[str, Any]) -> dict[str, Any]:
        if not self._agents:
            return {"error": "no agents"}

        task = payload.get("task", "")

        # 1. match por capability
        for agent in self._agents:
            if agent.capability in task:
                return agent.handle(payload)

        # 2. fallback: primeiro agente
        return self._agents[0].handle(payload)
