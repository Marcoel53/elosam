"""
AEGIS PATCH SIMULATION ENGINE.
Simulates code modifications safely before application.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from elosam.core.change_proposal_engine import ChangeProposalEngine


@dataclass(slots=True)
class PatchDiff:
    target: str
    change: str
    risk: str
    impact_score: float


class PatchSimulationEngine:
    """
    Simulates the effect of proposed code changes.
    """

    def __init__(self, proposal_engine: ChangeProposalEngine) -> None:
        self.proposal_engine = proposal_engine

    def simulate(self) -> dict[str, Any]:
        result = self.proposal_engine.propose()

        proposals = result.get("proposals", [])

        diffs: list[PatchDiff] = []

        for p in proposals:

            # heuristic impact model (safe simulation only)
            base_risk = {
                "low": 0.2,
                "medium": 0.5,
                "high": 0.8,
            }.get(getattr(p, "risk", "medium"), 0.5)

            impact_score = base_risk

            # structural amplification rules
            if "kernel" in p.target.lower():
                impact_score += 0.2

            if "autonomous" in p.target.lower():
                impact_score += 0.1

            diffs.append(
                PatchDiff(
                    target=p.target,
                    change=p.action,
                    risk=p.risk,
                    impact_score=round(impact_score, 2),
                )
            )

        return {
            "total_proposals": len(proposals),
            "diffs": diffs,
        }
