"""
ELOSam ARCHITECTURE AI ENGINE (FULL PIPELINE)
One-shot system analysis: graph → impact → risk → priorities → evolution plan
"""

from elosam.core.dependency_graph_engine import DependencyGraphEngine
from elosam.core.impact_analysis_engine import ImpactAnalysisEngine


class ArchitectureAIEngine:
    def __init__(self):
        self.graph_engine = DependencyGraphEngine()
        self.impact_engine = ImpactAnalysisEngine(self.graph_engine)

    # =========================
    # 1. OBSERVAÇÃO
    # =========================
    def observe(self):
        graph_data = self.graph_engine.build()
        return graph_data

    # =========================
    # 2. IMPACTO
    # =========================
    def analyze_impact(self):
        return self.impact_engine.analyze("src")

    # =========================
    # 3. HOTSPOTS
    # =========================
    def detect_hotspots(self, graph):
        scores = {
            module: len(imports)
            for module, imports in graph.items()
        }

        return sorted(
            scores.items(),
            key=lambda x: x[1],
            reverse=True
        )

    # =========================
    # 4. PRIORIZAÇÃO
    # =========================
    def prioritize(self, hotspots):
        result = []

        for module, score in hotspots[:10]:
            if score >= 10:
                priority = "CRITICAL"
            elif score >= 7:
                priority = "HIGH"
            elif score >= 4:
                priority = "MEDIUM"
            else:
                priority = "LOW"

            result.append({
                "module": module,
                "score": score,
                "priority": priority
            })

        return result

    # =========================
    # 5. PLANO DE EVOLUÇÃO
    # =========================
    def evolution_plan(self, impact, hotspots, total_modules):
        plan = []

        if impact < 0.01:
            plan.append("Sistema estável — não refatorar agora")

        if impact >= 0.02:
            plan.append("Revisar acoplamento estrutural")

        if total_modules > 80:
            plan.append("Separar arquitetura em camadas (core/runtime/orchestrator)")

        if hotspots and hotspots[0][1] > 12:
            plan.append(f"Hotspot crítico: {hotspots[0][0]}")

        return plan

    # =========================
    # 6. PIPELINE FINAL
    # =========================
    def run(self):
        graph_data = self.observe()
        impact_data = self.analyze_impact()

        graph = graph_data["graph"]
        total_modules = graph_data["total_modules"]
        impact = impact_data["impact_score"]

        hotspots = self.detect_hotspots(graph)
        priorities = self.prioritize(hotspots)
        plan = self.evolution_plan(impact, hotspots, total_modules)

        return {
            "modules": total_modules,
            "impact": impact,
            "hotspots": hotspots[:10],
            "priorities": priorities,
            "plan": plan
        }


# =========================
# EXECUÇÃO DIRETA
# =========================
if __name__ == "__main__":
    engine = ArchitectureAIEngine()
    result = engine.run()

    print("\n🧠 ELOSam FULL ARCHITECTURE AI REPORT\n")

    print("📦 Modules:", result["modules"])
    print("⚖ Impact:", result["impact"])

    print("\n🔥 HOTSPOTS:")
    for h in result["hotspots"]:
        print("-", h)

    print("\n🚨 PRIORITIES:")
    for p in result["priorities"]:
        print("-", p)

    print("\n🧭 EVOLUTION PLAN:")
    for p in result["plan"]:
        print("-", p)