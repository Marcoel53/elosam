"""
ELOSam ARCHITECTURE EVOLUTION V3
Priority-based refactor intelligence
"""

from elosam.core.dependency_graph_engine import DependencyGraphEngine
from elosam.core.impact_analysis_engine import ImpactAnalysisEngine


class ArchitectureEvolutionV3:
    def __init__(self):
        self.graph_engine = DependencyGraphEngine()
        self.impact_engine = ImpactAnalysisEngine(self.graph_engine)

    def analyze(self):
        graph_data = self.graph_engine.build()
        impact_data = self.impact_engine.analyze("src")

        graph = graph_data["graph"]
        total_modules = graph_data["total_modules"]
        impact_score = impact_data["impact_score"]

        # 📊 build dependency weights
        dependency_score = {}

        for module, imports in graph.items():
            dependency_score[module] = len(imports)

        # 🔥 rank modules by criticality
        ranked = sorted(
            dependency_score.items(),
            key=lambda x: x[1],
            reverse=True
        )

        top_critical = ranked[:5]

        # 🧠 PRIORITY ENGINE
        priorities = []

        for module, score in top_critical:
            priority = "LOW"

            if score >= 10:
                priority = "CRITICAL"
            elif score >= 7:
                priority = "HIGH"
            elif score >= 4:
                priority = "MEDIUM"

            priorities.append({
                "module": module,
                "dependencies": score,
                "priority": priority
            })

        # 🧠 STRATEGY LAYER
        strategy = []

        if impact_score < 0.01:
            strategy.append("Sistema saudável — otimizar estrutura, não refatorar agressivamente")

        if impact_score >= 0.02:
            strategy.append("Revisar acoplamento entre módulos críticos")

        if total_modules > 80:
            strategy.append("Introduzir separação por domínios (core/runtime/orchestrator)")

        return {
            "modules": total_modules,
            "impact": impact_score,
            "priorities": priorities,
            "strategy": strategy
        }


if __name__ == "__main__":
    engine = ArchitectureEvolutionV3()
    result = engine.analyze()

    print("\n🧠 EVOLUTION V3 REPORT\n")

    print("📦 Modules:", result["modules"])
    print("⚖ Impact:", result["impact"])

    print("\n🔥 PRIORITIES:")
    for p in result["priorities"]:
        print("-", p)

    print("\n🧭 STRATEGY:")
    for s in result["strategy"]:
        print("-", s)
