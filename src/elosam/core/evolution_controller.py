"""
AEGIS SELF EVOLUTION CONTROLLER.
Controls safe continuous evolution cycles.
"""

from __future__ import annotations

from typing import Any

from elosam.core.meta_agent_engine import MetaAgentEngine
from elosam.core.agent_arbitration import ArbitrationEngine
from elosam.core.autonomous_runtime import AutonomousRuntime


class EvolutionController:
    """
    Safe evolution loop coordinator.
    """

    def __init__(
        self,
        runtime: AutonomousRuntime,
        arbitration: ArbitrationEngine,
        meta: MetaAgentEngine,
    ) -> None:
        self.runtime = runtime
        self.arbitration = arbitration
        self.meta = meta

        self._enabled = False

    def start(self) -> None:
        self._enabled = True

    def stop(self) -> None:
        self._enabled = False

    def cycle(self, task: dict[str, Any], max_cycles: int = 5) -> list[Any]:
        """
        Controlled evolution loop.
        """

        results = []

        for _ in range(max_cycles):

            if not self._enabled:
                break

            # 1. execute
            result = self.runtime.step(task)
            results.append(result)

            # 2. evolve agents
            self.meta.evolve()

        return results
