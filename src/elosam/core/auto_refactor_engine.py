"""
ELOSam AUTO REFACTOR ENGINE v1
Sugere refatorações seguras com base em impacto e dependência
"""

from elosam.core.dependency_graph_engine import DependencyGraphEngine
from elosam.core.impact_analysis_engine import ImpactAnalysisEngine
from elosam.core.impact_propagation_engine import ImpactPropagationEngine


class AutoRefactorEngine:
    def __init__(self):
        self.graph_engine = DependencyGraphEngine()
        self.impact_engine = ImpactAnalysisEngine(self.graph_engine)
        self.propagation_engine = ImpactPropagationEngine()

    def analyze(self):
        graph_data = self.graph_engine.build()
        impact_data = self.impact_engine.analyze("src")

        graph = graph_data["graph"]

        # 🔥 identificar módulos mais críticos
        dependency_score = {
            m: len(i) for m, i in graph.items()
        }

        sorted_modules = sorted(
            dependency_score.items(),
            key=lambda x: x[1],
            reverse=True
        )

        critical = sorted_modules[:5]

        suggestions = []

        for module, score in critical:
            impact = self.propagation_engine.propagate(module)

            risk = impact["risk_score"]

            # 🧠 lógica de refatoração segura
            if score >= 10 and risk > 0.02:
                suggestions.append({
                    "module": module,
                    "action": "REFACTOR PRIORITY",
                    "reason": "alto acoplamento + propagação de risco",
                    "risk": risk
                })

            elif score >= 7:
                suggestions.append({
                    "module": module,
                    "action": "REVIEW",
                    "reason": "dependência alta",
                    "risk": risk
                })

            else:
                suggestions.append({
                    "module": module,
                    "action": "KEEP",
                    "reason": "baixo impacto estrutural",
                    "risk": risk
                })

        return {
            "modules": len(graph),
            "suggestions": suggestions
        }


if __name__ == "__main__":
    engine = AutoRefactorEngine()
    result = engine.analyze()

    print("\n🧠 AUTO REFACTOR REPORT\n")

    print("📦 Modules:", result["modules"])

    print("\n💡 SUGGESTIONS:")
    for s in result["suggestions"]:
        print("-", s)