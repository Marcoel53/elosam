"""
ELOSam ARCHITECTURE PREDICTIVE ENGINE v1
Predicts future architectural risk trends
"""

from elosam.core.dependency_graph_engine import DependencyGraphEngine
from elosam.core.impact_analysis_engine import ImpactAnalysisEngine
from elosam.core.impact_propagation_engine import ImpactPropagationEngine


class ArchitecturePredictiveEngine:
    def __init__(self):
        self.graph_engine = DependencyGraphEngine()
        self.impact_engine = ImpactAnalysisEngine(self.graph_engine)
        self.propagation_engine = ImpactPropagationEngine()

    def analyze_trend(self):
        graph_data = self.graph_engine.build()
        impact_data = self.impact_engine.analyze("src")

        graph = graph_data["graph"]
        total_modules = graph_data["total_modules"]
        impact = impact_data["impact_score"]

        # =========================
        # 1. COMPLEXIDADE FUTURA
        # =========================
        avg_dependencies = sum(len(v) for v in graph.values()) / max(len(graph), 1)

        complexity_trend = "STABLE"

        if avg_dependencies > 8:
            complexity_trend = "GROWING_COMPLEXITY"
        elif avg_dependencies > 5:
            complexity_trend = "MODERATE_GROWTH"

        # =========================
        # 2. HOTSPOTS FUTUROS (heurística)
        # =========================
        risk_projection = {}

        for module, imports in graph.items():
            risk_projection[module] = len(imports) * impact

        predicted_hotspots = sorted(
            risk_projection.items(),
            key=lambda x: x[1],
            reverse=True
        )[:5]

        # =========================
        # 3. RISCO GLOBAL FUTURO
        # =========================
        future_risk = avg_dependencies * impact

        if future_risk > 0.15:
            risk_state = "HIGH_FUTURE_RISK"
        elif future_risk > 0.07:
            risk_state = "MEDIUM_FUTURE_RISK"
        else:
            risk_state = "LOW_FUTURE_RISK"

        # =========================
        # OUTPUT
        # =========================
        return {
            "modules": total_modules,
            "impact": impact,
            "avg_dependencies": avg_dependencies,
            "complexity_trend": complexity_trend,
            "future_risk": future_risk,
            "risk_state": risk_state,
            "predicted_hotspots": predicted_hotspots
        }


if __name__ == "__main__":
    engine = ArchitecturePredictiveEngine()
    result = engine.analyze_trend()

    print("\n🧠 PREDICTIVE ARCHITECTURE REPORT\n")

    print("📦 Modules:", result["modules"])
    print("⚖ Impact:", result["impact"])
    print("📊 Avg Dependencies:", result["avg_dependencies"])
    print("📈 Complexity:", result["complexity_trend"])
    print("🚨 Risk State:", result["risk_state"])

    print("\n🔥 Predicted Hotspots:")
    for h in result["predicted_hotspots"]:
        print("-", h)