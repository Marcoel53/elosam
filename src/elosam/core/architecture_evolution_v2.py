"""
ELOSam ARCHITECTURE EVOLUTION ENGINE v2
"""

from elosam.core.dependency_graph_engine import DependencyGraphEngine
from elosam.core.impact_analysis_engine import ImpactAnalysisEngine


class ArchitectureEvolutionV2:
    def __init__(self):
        self.graph_engine = DependencyGraphEngine()
        self.impact_engine = ImpactAnalysisEngine(self.graph_engine)

    def analyze(self):
        graph_data = self.graph_engine.build()
        impact_data = self.impact_engine.analyze("src")

        graph = graph_data["graph"]
        total_modules = graph_data["total_modules"]
        impact_score = impact_data["impact_score"]

        dependency_count = {}

        for module, imports in graph.items():
            dependency_count[module] = len(imports)

        hotspots = sorted(
            dependency_count.items(),
            key=lambda x: x[1],
            reverse=True
        )[:10]

        recommendations = []

        if impact_score < 0.01:
            recommendations.append("Sistema está estável")

        if impact_score > 0.02:
            recommendations.append("Revisar acoplamento")

        if total_modules > 80:
            recommendations.append("Sistema grande — modularizar")

        if hotspots and hotspots[0][1] > 15:
            recommendations.append(f"Hotspot: {hotspots[0][0]}")

        return {
            "modules": total_modules,
            "impact": impact_score,
            "hotspots": hotspots,
            "recommendations": recommendations
        }


if __name__ == "__main__":
    engine = ArchitectureEvolutionV2()
    result = engine.analyze()

    print("\n🧠 EVOLUTION V2 REPORT\n")
    print("Modules:", result["modules"])
    print("Impact:", result["impact"])

    print("\nHotspots:")
    for h in result["hotspots"]:
        print("-", h)

    print("\nRecommendations:")
    for r in result["recommendations"]:
        print("-", r)
