"""
ELOSam REFACTOR DESIGN ENGINE v1
Gera plano estruturado de refatoração baseado em risco e impacto
"""

from elosam.core.dependency_graph_engine import DependencyGraphEngine
from elosam.core.impact_analysis_engine import ImpactAnalysisEngine
from elosam.core.impact_propagation_engine import ImpactPropagationEngine


class RefactorDesignEngine:
    def __init__(self):
        self.graph_engine = DependencyGraphEngine()
        self.impact_engine = ImpactAnalysisEngine(self.graph_engine)
        self.propagation_engine = ImpactPropagationEngine()

    def analyze(self):
        graph_data = self.graph_engine.build()
        impact_data = self.impact_engine.analyze("src")

        graph = graph_data["graph"]

        # =========================
        # 1. SCORE DE DEPENDÊNCIA
        # =========================
        dependency_score = {
            module: len(imports)
            for module, imports in graph.items()
        }

        sorted_modules = sorted(
            dependency_score.items(),
            key=lambda x: x[1],
            reverse=True
        )

        critical = sorted_modules[:10]

        # =========================
        # 2. PLANO DE REFACTOR
        # =========================
        plan = []

        for module, score in critical:

            propagation = self.propagation_engine.propagate(module)

            # 🔥 FIX DEFINITIVO DO KEY ERROR
            risk = (
                propagation.get("risk_level")
                or propagation.get("risk_score")
                or 0
            )

            step = {
                "module": module,
                "dependency_score": score,
                "risk": risk,
            }

            # 🧠 decisão arquitetural
            if score >= 10 and risk > 0.02:
                step["action"] = "EXTRACT MODULE"
                step["priority"] = 1

            elif score >= 7:
                step["action"] = "REDUCE COUPLING"
                step["priority"] = 2

            else:
                step["action"] = "KEEP"
                step["priority"] = 3

            plan.append(step)

        # =========================
        # 3. ORDENAÇÃO FINAL
        # =========================
        plan = sorted(plan, key=lambda x: x["priority"])

        return {
            "total_modules": len(graph),
            "refactor_plan": plan
        }


if __name__ == "__main__":
    engine = RefactorDesignEngine()
    result = engine.analyze()

    print("\n🧠 REFACTOR DESIGN REPORT\n")

    print("📦 Modules:", result["total_modules"])

    print("\n📌 REFACTOR PLAN:")
    for p in result["refactor_plan"]:
        print("-", p)