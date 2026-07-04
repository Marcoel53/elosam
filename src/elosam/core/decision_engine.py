"""
ELOSam DECISION LAYER v1 (ACTIVE EVOLUTION)
"""

class DecisionEngine:
    def decide(self, result: dict) -> dict:
        impact = result.get("impact", {}).get("impact_score", 0)

        if impact < 0.02:
            action = "ignore"
        elif impact < 0.05:
            action = "record"
        else:
            action = "simulate_evolution"

        return {
            "impact": impact,
            "action": action
        }

# force evolution signal
