"""
ELOSam COGNITIVE EVOLUTION CORE v1
Transforma análise em decisão de evolução real
"""

from dataclasses import dataclass
from elosam.core.dependency_graph_engine import DependencyGraphEngine
from elosam.core.impact_analysis_engine import ImpactAnalysisEngine


@dataclass
class EvolutionDecision:
    should_evolve: bool
    risk: float
    reason: str


class CognitiveEvolutionCore:
    def __init__(self):
        self.graph = DependencyGraphEngine()
        self.impact = ImpactAnalysisEngine(self.graph)

    def analyze_state(self):
        result = self.impact.analyze("src")
        score = result["impact_score"]

        return result, score

    def decide(self, score: float):
        if score < 0.01:
            return EvolutionDecision(False, score, "Sistema está estável demais para mudança")
        elif score < 0.05:
            return EvolutionDecision(True, score, "Evolução segura possível")
        else:
            return EvolutionDecision(True, score, "Alta atividade estrutural detectada")

    def run(self):
        data, score = self.analyze_state()
        decision = self.decide(score)

        return {
            "analysis": data,
            "decision": decision.__dict__
        }


if __name__ == "__main__":
    core = CognitiveEvolutionCore()
    print(core.run())
