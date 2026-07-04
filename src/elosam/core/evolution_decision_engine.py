"""
AEGIS EVOLUTION DECISION ENGINE.
Final selector of system evolution paths.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from elosam.core.patch_simulation_engine import PatchSimulationEngine


@dataclass(slots=True)
class EvolutionPlan:
    selected: Any
    alternatives: list[Any]
    reasoning: str


class EvolutionDecisionEngine:
    """
    Selects safest and most valuable evolution path.
    """

    def __init__(self, simulator: PatchSimulationEngine) -> None:
        self.simulator = simulator

    def decide(self) -> EvolutionPlan:
        simulation = self.simulator.simulate()

        diffs = simulation.get("diffs", [])

        if not diffs:
            return EvolutionPlan(
                selected=None,
                alternatives=[],
                reasoning="no evolution needed",
            )

        # select best candidate (lowest risk, highest stability)
        best = min(diffs, key=lambda d: d.impact_score)

        alternatives = [d for d in diffs if d != best]

        reasoning = (
            "selected lowest-risk evolution path "
            "based on simulated architectural impact"
        )

        return EvolutionPlan(
            selected=best,
            alternatives=alternatives,
            reasoning=reasoning,
        )
