"""
AEGIS CHANGE PROPOSAL ENGINE.
Generates structured code modification proposals (SAFE MODE).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from elosam.core.code_introspector import CodeIntrospector
from elosam.core.diagnostic_engine import DiagnosticEngine


@dataclass(slots=True)
class ChangeProposal:
    target: str
    action: str
    reason: str
    risk: str


class ChangeProposalEngine:
    """
    Converts system diagnostics into code-level change proposals.
    """

    def __init__(
        self,
        introspector: CodeIntrospector,
        diagnostic: DiagnosticEngine,
    ) -> None:
        self.introspector = introspector
        self.diagnostic = diagnostic

    def propose(self) -> dict[str, Any]:
        structure = self.introspector.scan()
        report = self.diagnostic.analyze()

        proposals: list[ChangeProposal] = []

        issues = report.get("issues", [])

        # RULE: missing evolution loop
        if "no_evolution_detected" in issues:
            proposals.append(
                ChangeProposal(
                    target="meta_agent_engine.py",
                    action="ensure evolve() is triggered in runtime loop",
                    reason="system is not self-evolving consistently",
                    risk="low",
                )
            )

        # RULE: missing agent activity
        if "no_agent_activity" in issues:
            proposals.append(
                ChangeProposal(
                    target="autonomous_os.py",
                    action="bind AgentEngine into execution pipeline",
                    reason="agents are not being executed in runtime",
                    risk="medium",
                )
            )

        # RULE: no decision flow
        if "no_decision_flow" in issues:
            proposals.append(
                ChangeProposal(
                    target="kernel.py",
                    action="inject DecisionEngine into execution path",
                    reason="system lacks reasoning layer in runtime",
                    risk="high",
                )
            )

        return {
            "total_modules": structure["total_modules"],
            "proposals": proposals,
        }
