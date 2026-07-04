"""
ELOSam ARCHITECTURE EVOLUTION ENGINE v4
Decision-level architecture intelligence (SIMULATION + RISK)
"""

from elosam.core.dependency_graph_engine import DependencyGraphEngine
from elosam.core.impact_analysis_engine import ImpactAnalysisEngine


class ArchitectureEvolutionV4:
    def __init__(self):
        self.graph_engine = DependencyGraphEngine()
        self.impact_engine = ImpactAnalysisEngine(self.graph_engine)

    def run(self):
        graph_data = self.graph_engine.build()
        impact_data = self.impact_engine.analyze("src")

        graph = graph_data["graph"]
        total_modules = graph_data["total_modules"]
        impact = impact_data["impact_score"]

        # =========================
        # 1. RISK MAP
        # =========================
        risk_map = {}

        for module, imports in graph.items():
            risk_map[module] = len(imports)

        sorted_risk = sorted(
            risk_map.items(),
            key=lambda x: x[1],
            reverse=True
        )

        top = sorted_risk[:10]

        # =========================
        # 2. DECISION ENGINE
        # =========================
        decisions = []

        for module, score in top:
            if score >= 10:
                action = "REFATORAR IMEDIATAMENTE"
            elif score >= 7:
                action = "REVISAR E REDUZIR DEPENDÊNCIAS"
            elif score >= 4:
                action = "MONITORAR"
            else:
                action = "OK"

            decisions.append({
                "module": module,
                "score": score,
                "action": action
            })

        # =========================
        # 3. SIMULAÇÃO SIMPLES
        # =========================
        simulation = []

        if impact < 0.01:
            simulation.append("Sistema estável → mudanças podem ser lentas e seguras")

        if impact >= 0.02:
            simulation.append("Mudanças devem ser feitas com cuidado (acoplamento moderado)")

        if total_modules > 100:
            simulation.append("Sistema grande → risco de complexidade emergente")

        # =========================
        # OUTPUT FINAL
        # =========================
        return {
            "modules": total_modules,
            "impact": impact,
            "top_risk_modules": top,
            "decisions": decisions,
            "simulation": simulation
        }


if __name__ == "__main__":
    engine = ArchitectureEvolutionV4()
    result = engine.run()

    print("\n🧠 EVOLUTION V4 REPORT\n")

    print("📦 Modules:", result["modules"])
    print("⚖ Impact:", result["impact"])

    print("\n🔥 TOP RISK:")
    for m in result["top_risk_modules"]:
        print("-", m)

    print("\n🚨 DECISIONS:")
    for d in result["decisions"]:
        print("-", d)

    print("\n🧭 SIMULATION:")
    for s in result["simulation"]:
        print("-", s)