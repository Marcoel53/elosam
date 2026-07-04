"""
ELOSam EVOLUTION LOOP v1 (SAFE MODE)
Gera propostas de evolução sem modificar o sistema
"""

from elosam.core.dependency_graph_engine import DependencyGraphEngine
from elosam.core.impact_analysis_engine import ImpactAnalysisEngine


class EvolutionLoop:
    def __init__(self):
        self.graph = DependencyGraphEngine()
        self.impact = ImpactAnalysisEngine(self.graph)

    def propose(self):
        graph = self.graph.build()
        impact = self.impact.analyze("src")

        score = impact["impact_score"]

        proposals = []

        # 🧠 regra simples mas poderosa
        if score < 0.01:
            proposals.append("Sistema estável: nenhuma ação necessária")

        if graph["total_modules"] > 80:
            proposals.append("Sugestão: revisar modularização (alto acoplamento potencial)")

        if score > 0.03:
            proposals.append("Sugestão: investigar dependências críticas")

        return {
            "impact": score,
            "modules": graph["total_modules"],
            "proposals": proposals
        }


if __name__ == "__main__":
    loop = EvolutionLoop()
    result = loop.propose()

    print("\n🧬 ELOSam EVOLUTION REPORT\n")
    print("📦 Modules:", result["modules"])
    print("⚖ Impact:", result["impact"])
    print("\n💡 Proposals:")
    for p in result["proposals"]:
        print("-", p)
