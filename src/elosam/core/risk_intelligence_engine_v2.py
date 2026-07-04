"""
ELOSam RISK INTELLIGENCE ENGINE v2
Calcula risco REAL baseado em estrutura do grafo (não heurística fixa)
"""

from elosam.core.dependency_graph_engine import DependencyGraphEngine


class RiskIntelligenceEngineV2:
    def __init__(self):
        self.graph_engine = DependencyGraphEngine()

    # =========================
    # 1. FAN IN / FAN OUT
    # =========================
    def compute_links(self, graph):
        fan_in = {}
        fan_out = {}

        for module, imports in graph.items():
            fan_out[module] = len(imports)

            for imp in imports:
                fan_in[imp] = fan_in.get(imp, 0) + 1

        for m in graph:
            fan_in.setdefault(m, 0)

        return fan_in, fan_out

    # =========================
    # 2. CORE DISTANCE (IMPORTÂNCIA ARQUITETURAL)
    # =========================
    def compute_core_distance(self, graph):
        core_modules = [
            "runtime_engine",
            "offline_evolution_runner",
            "evolution_orchestrator",
            "impact_analysis_engine"
        ]

        distance = {}

        for module in graph:
            dist = 0

            for core in core_modules:
                if core in module:
                    dist += 3  # muito crítico

            distance[module] = dist

        return distance

    # =========================
    # 3. RISK SCORE REAL
    # =========================
    def compute_risk(self, fan_in, fan_out, core_distance):
        risk = {}

        for node in fan_in:
            incoming = fan_in[node]
            outgoing = fan_out.get(node, 0)
            core = core_distance.get(node, 0)

            # 🧠 fórmula nova REAL de risco estrutural
            risk[node] = (
                incoming * 2 +
                outgoing * 1.5 +
                core * 3
            )

        return risk

    # =========================
    # 4. PIPELINE FINAL
    # =========================
    def analyze(self):
        graph_data = self.graph_engine.build()
        graph = graph_data["graph"]

        fan_in, fan_out = self.compute_links(graph)
        core_distance = self.compute_core_distance(graph)
        risk = self.compute_risk(fan_in, fan_out, core_distance)

        sorted_risk = sorted(
            risk.items(),
            key=lambda x: x[1],
            reverse=True
        )

        return {
            "total_modules": len(graph),
            "top_risk": sorted_risk[:10],
            "risk_map": risk
        }


if __name__ == "__main__":
    engine = RiskIntelligenceEngineV2()
    result = engine.analyze()

    print("\n🧠 RISK INTELLIGENCE ENGINE v2\n")

    print("📦 Modules:", result["total_modules"])

    print("\n🔥 TOP RISK NODES:")
    for r in result["top_risk"]:
        print("-", r)