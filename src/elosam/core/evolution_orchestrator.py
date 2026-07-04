"""
AEGIS GOVERNED EVOLUTION ORCHESTRATOR.
Central brain for system evolution decisions.
"""

from __future__ import annotations

from typing import Any

from elosam.core.evolution_policy_engine import EvolutionPolicy
from elosam.core.dependency_graph_engine import DependencyGraphEngine
from elosam.core.impact_analysis_engine import ImpactAnalysisEngine
from elosam.core.patch_simulation_engine import PatchSimulationEngine
from elosam.core.evolution_decision_engine import EvolutionDecisionEngine


class EvolutionOrchestrator:
    """
    Final governance layer of EloSam evolution system.
    """

    def __init__(
        self,
        policy: EvolutionPolicy,
        graph_engine: DependencyGraphEngine,
        impact_engine: ImpactAnalysisEngine,
        simulation_engine: PatchSimulationEngine,
        decision_engine: EvolutionDecisionEngine,
    ) -> None:

        self.policy = policy
        self.graph = graph_engine
        self.impact = impact_engine
        self.simulation = simulation_engine
        self.decision = decision_engine

    def evaluate(self, target_module: str) -> dict[str, Any]:
        """
        Full governed evaluation pipeline.
        """

        # 1. structural impact
        impact_report = self.impact.analyze(target_module)

        # 2. policy check
        allowed = self.policy.is_allowed(
            target_module,
            impact_report["impact_score"],
        )

        # 3. simulation step
        simulation = self.simulation.simulate()

        # 4. final decision (meta-layer)
        decision = self.decision.decide()

        # 5. governance result
        return {
            "target": target_module,
            "impact": impact_report,
            "policy_allowed": allowed,
            "simulation": simulation,
            "decision": decision.selected if decision else None,
            "status": (
                "approved"
                if allowed and impact_report["impact_score"] < self.policy.risk_threshold
                else "blocked"
            ),
        }
