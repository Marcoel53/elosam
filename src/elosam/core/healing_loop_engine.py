"""
AEGIS SELF HEALING LOOP ENGINE.
Closed-cycle safe auto-repair system.
"""

from __future__ import annotations

from typing import Any

from elosam.core.observability_engine import ObservabilityEngine
from elosam.core.diagnostic_engine import DiagnosticEngine
from elosam.core.healing_engine import HealingEngine
from elosam.core.simulation_engine import SimulationEngine


class HealingLoopEngine:
    """
    Full closed-loop self-healing system.
    """

    def __init__(self) -> None:
        self.observability = ObservabilityEngine()
        self.diagnostic = DiagnosticEngine(self.observability)
        self.healing = HealingEngine(self.diagnostic)
        self.simulation = SimulationEngine(system_state={})

        self.applied_patches: list[Any] = []

    def run_cycle(self, fake_runtime_trace: list[dict], iterations: int = 1) -> dict[str, Any]:
        """
        Full healing cycle:
        trace ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ diagnose ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ heal ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ simulate ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ decide
        """

        # 1. feed observability
        for entry in fake_runtime_trace:
            self.observability.log(
                entry.get("layer", "unknown"),
                entry.get("event", "unknown"),
                entry.get("data", {}),
            )

        # 2. diagnose system
        report = self.diagnostic.analyze()

        # 3. generate healing plan
        healing_plan = self.healing.heal()

        patches = healing_plan.get("patches", [])

        safe_to_apply = []
        rejected = []

        # 4. simulate each patch
        for patch in patches:
            result = self.simulation.simulate(patch)

            if result.safe:
                safe_to_apply.append(patch)
            else:
                rejected.append(patch)

        # 5. "apply" safe patches (logical application only)
        for patch in safe_to_apply:
            self.applied_patches.append(patch)

        return {
            "diagnostic": report,
            "generated_patches": len(patches),
            "applied": len(safe_to_apply),
            "rejected": len(rejected),
        }
