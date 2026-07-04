"""
ELOSam EVOLUTION SIMULATION ENGINE v1
Simula mudanças arquiteturais sem modificar o sistema real
"""

from copy import deepcopy
from elosam.core.dependency_graph_engine import DependencyGraphEngine
from elosam.core.impact_analysis_engine import ImpactAnalysisEngine


class EvolutionSimulationEngine:
    def __init__(self):
        self.graph_engine = DependencyGraphEngine()
        self.impact_engine = ImpactAnalysisEngine(self.graph_engine)

    # =========================
    # 1. BASELINE (estado atual)
    # =========================
    def baseline(self):
        graph_data = self.graph_engine.build()
        impact_data = self.impact_engine.analyze("src")

        return {
            "modules": graph_data["total_modules"],
            "graph": graph_data["graph"],
            "impact": impact_data["impact_score"]
        }

    # =========================
    # 2. SIMULAÇÃO DE MUDANÇA
    # =========================
    def simulate_removal(self, target_module: str):
        base = self.baseline()

        graph = deepcopy(base["graph"])

        # simula remoção do módulo
        if target_module in graph:
            del graph[target_module]

        # recalcula impacto simplificado
        total_edges = sum(len(v) for v in graph.values())
        total_nodes = len(graph)

        simulated_impact = total_edges / max(total_nodes, 1)

        return {
            "removed": target_module,
            "before_modules": base["modules"],
            "after_modules": total_nodes,
            "before_impact": base["impact"],
            "after_impact": simulated_impact,
            "delta": simulated_impact - base["impact"]
        }

    # =========================
    # 3. SIMULAÇÃO DE EFEITO EM CADEIA
    # =========================
    def simulate_failure_propagation(self, target_module: str):
        graph_data = self.graph_engine.build()
        graph = graph_data["graph"]

        affected = set()
        queue = [target_module]

        reverse = {}

        for mod, imports in graph.items():
            for imp in imports:
                reverse.setdefault(imp, []).append(mod)

        while queue:
            current = queue.pop(0)

            if current in affected:
                continue

            affected.add(current)

            for dep in reverse.get(current, []):
                queue.append(dep)

        return {
            "target": target_module,
            "affected_count": len(affected),
            "affected_modules": list(affected),
            "risk_level": len(affected) / max(len(graph), 1)
        }

    # =========================
    # 4. PIPELINE FINAL
    # =========================
    def run(self, target="src.elosam.core.runtime_engine"):
        baseline = self.baseline()
        removal = self.simulate_removal(target)
        propagation = self.simulate_failure_propagation(target)

        return {
            "baseline": baseline,
            "removal_simulation": removal,
            "propagation_simulation": propagation
        }


if __name__ == "__main__":
    engine = EvolutionSimulationEngine()
    result = engine.run()

    print("\n🧠 EVOLUTION SIMULATION REPORT\n")

    print("📦 BASELINE:")
    print(result["baseline"])

    print("\n🧪 REMOVAL SIMULATION:")
    print(result["removal_simulation"])

    print("\n💥 PROPAGATION:")
    print(result["propagation_simulation"])