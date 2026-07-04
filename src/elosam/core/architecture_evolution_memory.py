"""
ELOSam ARCHITECTURE EVOLUTION MEMORY v1
Tracks architecture evolution over time
"""

from datetime import datetime
from elosam.core.dependency_graph_engine import DependencyGraphEngine
from elosam.core.impact_analysis_engine import ImpactAnalysisEngine


class ArchitectureEvolutionMemory:
    def __init__(self):
        self.graph_engine = DependencyGraphEngine()
        self.impact_engine = ImpactAnalysisEngine(self.graph_engine)
        self.history = []

    def snapshot(self):
        graph_data = self.graph_engine.build()
        impact_data = self.impact_engine.analyze("src")

        snapshot = {
            "time": datetime.now().isoformat(),
            "modules": graph_data["total_modules"],
            "impact": impact_data["impact_score"]
        }

        self.history.append(snapshot)
        return snapshot

    def trend(self):
        if len(self.history) < 2:
            return "INSUFFICIENT_DATA"

        last = self.history[-1]
        prev = self.history[-2]

        module_trend = last["modules"] - prev["modules"]
        impact_trend = last["impact"] - prev["impact"]

        return {
            "module_trend": module_trend,
            "impact_trend": impact_trend,
            "status": self._interpret(module_trend, impact_trend)
        }

    def _interpret(self, m, i):
        if m > 0 and i > 0:
            return "ARCHITECTURE_GROWING_COMPLEXITY"
        elif m > 0 and i <= 0:
            return "SCALING_STABLE"
        elif m == 0:
            return "NO_CHANGE"
        else:
            return "SIMPLIFYING"

    def run(self):
        self.snapshot()
        trend = self.trend()

        return {
            "latest": self.history[-1],
            "trend": trend
        }


if __name__ == "__main__":
    mem = ArchitectureEvolutionMemory()

    print("\n🧠 SNAPSHOT 1")
    print(mem.run())

    print("\n🧠 SNAPSHOT 2")
    print(mem.run())