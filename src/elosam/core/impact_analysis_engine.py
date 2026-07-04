"""
IMPACT ANALYSIS ENGINE v4 - STRUCTURAL SIGNIFICANCE
"""

from collections import defaultdict
from elosam.core.dependency_graph_engine import DependencyGraphEngine
from elosam.core.structural_significance import StructuralSignificance


class ImpactAnalysisEngine:
    def __init__(self, graph_engine: DependencyGraphEngine):
        self.graph_engine = graph_engine

    def analyze(self, target_module: str):
        data = self.graph_engine.build()
        graph = data["graph"]

        reverse = defaultdict(list)

        for mod, imports in graph.items():
            for imp in imports:
                reverse[imp].append(mod)

        affected = set()
        queue = [target_module]

        while queue:
            current = queue.pop(0)
            if current in affected:
                continue
            affected.add(current)
            queue.extend(reverse.get(current, []))

        # 🧠 NOVA INTELIGÊNCIA REAL
        significance = StructuralSignificance(graph)
        score = significance.importance(affected)

        return {
            "target": target_module,
            "affected_modules": list(affected),
            "impact_score": round(score, 3),
        }
