"""
AEGIS AUTONOMOUS RUNTIME LOOP.
Continuously executes system intelligence cycle.
"""

from __future__ import annotations

import time
from typing import Any

from elosam.core.agent_registry import AgentRegistry
from elosam.core.agent_arbitration import ArbitrationEngine
from elosam.core.meta_agent_engine import MetaAgentEngine


class AutonomousRuntime:
    """
    Continuous self-running intelligence loop.
    """

    def __init__(
        self,
        registry: AgentRegistry,
        arbitration: ArbitrationEngine,
        meta: MetaAgentEngine,
    ) -> None:
        self.registry = registry
        self.arbitration = arbitration
        self.meta = meta
        self.running = False

    def step(self, task: dict[str, Any]) -> dict[str, Any]:
        return self.arbitration.execute(task)

    def cycle(self, task: dict[str, Any], iterations: int = 3) -> list[dict[str, Any]]:
        results = []

        for _ in range(iterations):

            # 1. run arbitration
            result = self.step(task)
            results.append(result)

            # 2. meta evolution
            self.meta.evolve()

            # 3. optional slow thinking delay (simulated cognition)
            time.sleep(0.01)

        return results

    def run_forever(self, task: dict[str, Any]) -> None:
        self.running = True

        while self.running:
            self.step(task)
            self.meta.evolve()

            # safety throttle
            time.sleep(0.05)

    def stop(self) -> None:
        self.running = False
