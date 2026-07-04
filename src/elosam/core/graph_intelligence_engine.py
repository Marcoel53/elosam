"""
ELOSam GRAPH INTELLIGENCE ENGINE v1
Analisa estrutura real do grafo: hubs, centralidade e dependência crítica
"""

from elosam.core.dependency_graph_engine import DependencyGraphEngine


class GraphIntelligenceEngine:
    def __init__(self):
        self.graph_engine = DependencyGraphEngine()

    # =========================
    # 1. CENTRALIDADE SIMPLES (FAN-IN / FAN-OUT)
    # =========================
    def compute_centrality(self, graph):
        fan_in = {}
        fan_out = {}

        for module, imports in graph.items():
            fan_out[module] = len(imports)

            for imp in imports:
                fan_in[imp] = fan_in.get(imp, 0) + 1

        # garante todos os nós
        for module in graph:
            fan_in.setdefault(module, 0)

        return fan_in, fan_out

    # =========================
    # 2. SCORE DE IMPORTÂNCIA
    # =========================
    def compute_importance(self, fan_in, fan_out):
        importance = {}

        for node in fan_in:
            importance[node] = fan_in[node] * 2 + fan_out.get(node, 0)

        return importance

    # =========================
    # 3. DETECTAR HUBS CRÍTICOS
    # =========================
    def detect_hubs(self, importance):
        sorted_nodes = sorted(
            importance.items(),
            key=lambda x: x[1],
            reverse=True
        )

        return sorted_nodes[:10]

    # =========================
    # 4. PIPELINE COMPLETO
    # =========================
    def analyze(self):
        graph_data = self.graph_engine.build()
        graph = graph_data["graph"]

        fan_in, fan_out = self.compute_centrality(graph)
        importance = self.compute_importance(fan_in, fan_out)
        hubs = self.detect_hubs(importance)

        return {
            "total_modules": len(graph),
            "top_hubs": hubs,
            "fan_in": fan_in,
            "fan_out": fan_out
        }


if __name__ == "__main__":
    engine = GraphIntelligenceEngine()
    result = engine.analyze()

    print("\n🧠 GRAPH INTELLIGENCE REPORT\n")

    print("📦 Modules:", result["total_modules"])

    print("\n🔥 TOP HUBS:")
    for h in result["top_hubs"]:
        print("-", h)