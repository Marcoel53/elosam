"""
ELOSam ARCHITECTURE EVOLUTION ENGINE v1
Transforma análise estrutural em recomendações de arquitetura
"""

from elosam.core.dependency_graph_engine import DependencyGraphEngine
from elosam.core.impact_analysis_engine import ImpactAnalysisEngine


class ArchitectureEvolutionEngine:
    def __init__(self):
        self.graph = DependencyGraphEngine()
        self.impact = ImpactAnalysisEngine(self.graph)

    def analyze(self):
        graph = self.graph.build()
        impact = self.impact.analyze("src")

        score = impact["impact_score"]
        modules = graph["total_modules"]

        recommendations = []

        # 🧠 interpretação arquitetural
        if score < 0.01:
            recommendations.append(
                "Arquitetura saudável. Manter estrutura atual e monitorar crescimento."
            )

        if modules > 80:
            recommendations.append(
                "Sistema grande: considerar modularização por domínio funcional."
            )

        if score > 0.03:
            recommendations.append(
                "Acoplamento detectado: revisar dependências críticas entre módulos."
            )

        if modules > 100:
            recommendations.append(
                "Sugestão: introduzir camadas (core / services / runtime)."
            )

        return {
            "modules": modules,
            "impact": score,
            "recommendations": recommendations
        }


if __name__ == "__main__":
    engine = ArchitectureEvolutionEngine()
    result = engine.analyze()

    print("\n🧠 ELOSam ARCHITECTURE REPORT\n")
    print(f"📦 Modules: {result['modules']}")
    print(f"⚖ Impact: {result['impact']}")
    print("\n💡 Recommendations:")
    for r in result["recommendations"]:
        print("-", r)
