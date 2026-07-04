"""
AEGIS OFFLINE EVOLUTION RUNNER - STABLE VERSION
"""

from elosam.core.code_introspector import CodeIntrospector
from elosam.core.dependency_graph_engine import DependencyGraphEngine
from elosam.core.impact_analysis_engine import ImpactAnalysisEngine
from elosam.core.observability_engine import ObservabilityEngine
from elosam.core.diagnostic_engine import DiagnosticEngine
from elosam.core.change_proposal_engine import ChangeProposalEngine
from elosam.core.patch_simulation_engine import PatchSimulationEngine
from elosam.core.evolution_decision_engine import EvolutionDecisionEngine
from elosam.core.evolution_orchestrator import EvolutionOrchestrator
from elosam.core.evolution_policy_engine import EvolutionPolicy


class OfflineEvolutionRunner:
    def __init__(self) -> None:

        policy = EvolutionPolicy()

        graph_engine = DependencyGraphEngine()
        impact_engine = ImpactAnalysisEngine(graph_engine)

        observability = ObservabilityEngine()
        diagnostic = DiagnosticEngine(observability)

        introspector = CodeIntrospector()

        proposal_engine = ChangeProposalEngine(
            introspector=introspector,
            diagnostic=diagnostic,
        )

        simulation_engine = PatchSimulationEngine(
            proposal_engine=proposal_engine
        )

        decision_engine = EvolutionDecisionEngine(simulation_engine)

        self.orchestrator = EvolutionOrchestrator(
            policy=policy,
            graph_engine=graph_engine,
            impact_engine=impact_engine,
            simulation_engine=simulation_engine,
            decision_engine=decision_engine,
        )

    def run_once(self, target: str = "src"):
        return self.orchestrator.evaluate(target)


if __name__ == "__main__":
    runner = OfflineEvolutionRunner()
    print(runner.run_once())

# evolution trigger noise 355184049
