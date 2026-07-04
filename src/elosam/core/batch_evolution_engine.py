"""
ELOSam BATCH EVOLUTION ENGINE v1
Processa múltiplos módulos em lote (alta performance)
"""

from elosam.core.dependency_graph_engine import DependencyGraphEngine
from elosam.core.impact_analysis_engine import ImpactAnalysisEngine


class BatchEvolutionEngine:
    def __init__(self):
        self.graph_engine = DependencyGraphEngine()
        self.impact_engine = ImpactAnalysisEngine(self.graph_engine)

    def run_batch(self, batch_size=3):
        graph_data = self.graph_engine.build()
        graph = graph_data["graph"]

        impact_data = self.impact_engine.analyze("src")

        modules = list(graph.items())

        results = []

        # 🔥 processa em blocos (batch)
        for i in range(0, len(modules), batch_size):
            batch = modules[i:i + batch_size]

            batch_result = {
                "batch_id": i // batch_size,
                "modules": [],
                "avg_score": 0
            }

            score_sum = 0

            for module, imports in batch:
                score = len(imports)

                batch_result["modules"].append({
                    "module": module,
                    "score": score
                })

                score_sum += score

            batch_result["avg_score"] = score_sum / max(len(batch), 1)

            results.append(batch_result)

        # 🔥 ordena batches mais críticos primeiro
        results.sort(key=lambda x: x["avg_score"], reverse=True)

        return {
            "total_modules": len(modules),
            "batches": results
        }


if __name__ == "__main__":
    engine = BatchEvolutionEngine()
    result = engine.run_batch(batch_size=3)

    print("\n⚡ BATCH EVOLUTION REPORT\n")

    print("📦 Total Modules:", result["total_modules"])

    for b in result["batches"]:
        print(f"\n🔹 BATCH {b['batch_id']} (avg={b['avg_score']})")
        for m in b["modules"]:
            print(" -", m)