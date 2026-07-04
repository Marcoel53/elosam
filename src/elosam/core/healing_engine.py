"""
AEGIS SELF HEALING ENGINE.
Transforms diagnostics into repair suggestions.
"""

from __future__ import annotations

from typing import Any

from elosam.core.diagnostic_engine import DiagnosticEngine
from elosam.core.patch_generator import Patch


class HealingEngine:
    """
    Suggests system repairs based on diagnostics.
    """

    def __init__(self, diagnostic: DiagnosticEngine) -> None:
        self.diagnostic = diagnostic

    def heal(self) -> dict[str, Any]:
        report = self.diagnostic.analyze()

        issues = report.get("issues", [])

        patches: list[Patch] = []

        for issue in issues:

            if issue == "no_agent_activity":
                patches.append(
                    Patch(
                        target="system",
                        change="ensure AgentEngine is bound to runtime cycle",
                        reason="restore agent execution flow",
                    )
                )

            if issue == "no_evolution_detected":
                patches.append(
                    Patch(
                        target="system",
                        change="trigger MetaAgentEngine evolve loop periodically",
                        reason="restore system evolution",
                    )
                )

            if issue == "no_decision_flow":
                patches.append(
                    Patch(
                        target="system",
                        change="bind DecisionEngine into runtime pipeline",
                        reason="restore reasoning layer",
                    )
                )

        return {
            "status": report.get("status"),
            "issues": issues,
            "patches": patches,
        }
