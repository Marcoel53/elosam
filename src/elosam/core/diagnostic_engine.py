"""
AEGIS SELF DEBUGGING ENGINE.
Analyzes system traces and detects anomalies.
"""

from __future__ import annotations

from typing import Any
from collections import Counter

from elosam.core.observability_engine import ObservabilityEngine


class DiagnosticEngine:
    """
    Self-analysis engine for system behavior.
    """

    def __init__(self, observability: ObservabilityEngine) -> None:
        self.obs = observability

    def analyze(self) -> dict[str, Any]:
        traces = self.obs.all()

        if not traces:
            return {
                "status": "empty",
                "issues": ["no_activity_detected"],
            }

        layer_count = Counter(t.layer for t in traces)
        event_count = Counter(t.event for t in traces)

        issues = []

        # detect imbalance
        if layer_count.get("agent", 0) == 0:
            issues.append("no_agent_activity")

        # detect missing evolution signals
        if "evolve" not in event_count:
            issues.append("no_evolution_detected")

        # detect decision absence
        if "decision" not in layer_count:
            issues.append("no_decision_flow")

        status = "healthy" if not issues else "degraded"

        return {
            "status": status,
            "issues": issues,
            "layers": dict(layer_count),
            "events": dict(event_count),
        }
