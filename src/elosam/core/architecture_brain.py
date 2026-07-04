"""
ELOSam ARCHITECTURE BRAIN v1
Sistema de análise estrutural inteligente de software
"""

from elosam.core.dependency_graph_engine import DependencyGraphEngine
from elosam.core.impact_analysis_engine import ImpactAnalysisEngine


class ArchitectureBrain:
    def __init__(self):
        self.graph_engine = DependencyGraphEngine()
        self.impact_engine = ImpactAnalysisEngine(self.graph_engine)

    def analyze(self):
        graph = self.graph_engine.build()
        impact = self.impact_engine.analyze("src")

        total = graph["total_modules"]
        score = impact["impact_score"]

        # 🧠 diagnóstico simples mas poderoso
        if score < 0.01 and total > 80:
            state = "ARCHITECTURE STABLE 🟢"
            advice = "Sistema saudável, sem necessidade de mudanças"
        elif score < 0.05:
            state = "ARCHITECTURE MODERATE 🟡"
            advice = "Possível otimização estrutural"
        else:
            state = "ARCHITECTURE CRITICAL 🔴"
            advice = "Reestruturação recomendada"

        return {
            "state": state,
            "advice": advice,
            "modules": total,
            "impact": score
        }


if __name__ == "__main__":
    brain = ArchitectureBrain()
    result = brain.analyze()

    print("\n🧠 ELOSam ARCHITECTURE REPORT\n")
    print("📦 Modules:", result["modules"])
    print("⚖ Impact:", result["impact"])
    print("🧭 State:", result["state"])
    print("💡 Advice:", result["advice"])
