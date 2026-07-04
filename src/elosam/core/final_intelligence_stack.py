"""
ELOSam FINAL INTELLIGENCE STACK
Levels 11–13: Cleaning + Centrality + Autonomous Refactor Agent
"""

from elosam.core.dependency_graph_engine import DependencyGraphEngine
from elosam.core.impact_analysis_engine import ImpactAnalysisEngine
from elosam.core.impact_propagation_engine import ImpactPropagationEngine


# =========================
# NÍVEL 11 — GRAPH CLEANER
# =========================
class GraphCleaner:
    def __init__(self):
        self.blacklist = {
            "typing",
            "dataclasses",
            "pathlib",
            "datetime",
            "time",
            "__future__",
        }

    def clean(self, graph: dict):
        cleaned = {}

        for module, imports in graph.items():
            if any(b in module for b in self.blacklist):
                continue

            filtered = [
                imp for imp in imports
                if not any(b in imp for b in self.blacklist)
            ]

            cleaned[module] = filtered

        return cleaned


# =========================
# NÍVEL 12 — TRUE CENTRALITY
# =========================
class TrueCentralityEngine:
    def compute(self, graph: dict):
        score = {}

        for node in graph:
            incoming = sum(node in deps for deps in graph.values())
            outgoing = len(graph[node])

            # pseudo PageRank simples
            score[node] = (incoming * 2) + outgoing

        return sorted(score.items(), key=lambda x: x[1], reverse=True)


# =========================
# NÍVEL 13 — AUTONOMOUS REFACTOR AGENT
# =========================
class AutonomousRefactorAgent:
    def __init__(self):
        self.graph_engine = DependencyGraphEngine()
        self.impact_engine = ImpactAnalysisEngine(self.graph_engine)
        self.propagation_engine = ImpactPropagationEngine()

        self.cleaner = GraphCleaner()
        self.centrality = TrueCentralityEngine()

    def run(self):
        raw = self.graph_engine.build()
        graph = raw["graph"]

        # 🔥 CLEAN GRAPH (NÍVEL 11)
        clean_graph = self.cleaner.clean(graph)

        # 🧠 CENTRALITY REAL (NÍVEL 12)
        centrality = self.centrality.compute(clean_graph)

        # 🤖 REFACTOR PLAN (NÍVEL 13)
        plan = []

        for module, score in centrality[:10]:
            propagation = self.propagation_engine.propagate(module)

            risk = propagation.get("risk_level") or propagation.get("risk_score") or 0

            if score > 15 and risk > 0.02:
                action = "CRITICAL REFACTOR"
            elif score > 8:
                action = "OPTIMIZE"
            else:
                action = "KEEP"

            plan.append({
                "module": module,
                "centrality": score,
                "risk": risk,
                "action": action
            })

        return {
            "clean_modules": len(clean_graph),
            "top_nodes": centrality[:10],
            "refactor_plan": plan
        }


# =========================
# EXECUÇÃO
# =========================
if __name__ == "__main__":
    engine = AutonomousRefactorAgent()
    result = engine.run()

    print("\n🧠 ELOSam FINAL INTELLIGENCE STACK\n")

    print("📦 Clean Modules:", result["clean_modules"])

    print("\n🔥 TOP CENTRAL NODES:")
    for n in result["top_nodes"]:
        print("-", n)

    print("\n🤖 REFACTOR PLAN:")
    for p in result["refactor_plan"]:
        print("-", p)