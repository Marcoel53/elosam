"""
ELOSam CORE ENGINE FINAL (UNIFIED)
Observa → Avalia → Decide → Propõe evolução arquitetural
"""

from dataclasses import dataclass
from elosam.core.dependency_graph_engine import DependencyGraphEngine
from elosam.core.impact_analysis_engine import ImpactAnalysisEngine


@dataclass
class EvolutionProposal:
    recommendation: str
    risk: float
    confidence: float


class EloSamCoreEngine:
    def __init__(self):
        self.graph = DependencyGraphEngine()
        self.impact = ImpactAnalysisEngine(self.graph)

    def observe(self):
        return self.graph.build()

    def evaluate(self):
        return self.impact.analyze("src")

    def decide(self, impact_score: float):
        if impact_score < 0.01:
            return "STABLE"
        elif impact_score < 0.05:
            return "OPTIMIZABLE"
        return "CRITICAL"

    def propose(self, state, impact_score):
        modules = state["total_modules"]

        if impact_score < 0.01:
            return EvolutionProposal(
                "Sistema estável. Recomenda-se apenas monitoramento.",
                0.1,
                0.9
            )

        if modules > 80:
            return EvolutionProposal(
                "Sugestão: modularizar áreas altamente conectadas para reduzir acoplamento.",
                0.4,
                0.8
            )

        return EvolutionProposal(
            "Revisar dependências críticas e simplificar grafo.",
            0.6,
            0.7
        )

    def run(self):
        state = self.observe()
        impact = self.evaluate()

        decision = self.decide(impact["impact_score"])
        proposal = self.propose(state, impact["impact_score"])

        return {
            "state": decision,
            "impact": impact["impact_score"],
            "modules": state["total_modules"],
            "proposal": proposal.__dict__
        }


if __name__ == "__main__":
    engine = EloSamCoreEngine()
    print(engine.run())
