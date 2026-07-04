"""
ELOSam IMPACT PROPAGATION ENGINE
Simula impacto real de mudanças no sistema inteiro
"""

from elosam.core.dependency_graph_engine import DependencyGraphEngine


class ImpactPropagationEngine:
    def __init__(self):
        self.graph_engine = DependencyGraphEngine()

    def build_reverse_graph(self, graph):
        reverse = {}

        for module, imports in graph.items():
            for imp in imports:
                if imp not in reverse:
                    reverse[imp] = []
                reverse[imp].append(module)

        return reverse

    def propagate(self, target_module: str):
        graph_data = self.graph_engine.build()
        graph = graph_data["graph"]

        reverse_graph = self.build_reverse_graph(graph)

        affected = set()
        queue = [target_module]

        while queue:
            current = queue.pop(0)

            if current in affected:
                continue

            affected.add(current)

            if current in reverse_graph:
                queue.extend(reverse_graph[current])

        return {
            "target": target_module,
            "affected_system": list(affected),
            "risk_score": len(affected) / max(len(graph), 1)
        }


if __name__ == "__main__":
    engine = ImpactPropagationEngine()

    # 🔥 TESTE: simular mudança no núcleo
    result = engine.propagate("src.elosam.core.runtime_engine")

    print("\n🧠 IMPACT PROPAGATION REPORT\n")
    print("Target:", result["target"])
    print("Risk Score:", result["risk_score"])
    print("\nAffected System:")
    for m in result["affected_system"]:
        print("-", m)