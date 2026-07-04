"""
AEGIS AUTONOMOUS EVOLUTION LOOP ENGINE.
Full self-modifying system with Git integration.
"""

from __future__ import annotations

import subprocess
from typing import Any

from elosam.core.evolution_decision_engine import EvolutionDecisionEngine
from elosam.core.real_patch_generator import RealPatchGenerator
from elosam.core.safe_apply_engine import SafeApplyEngine


class AutonomousEvolutionLoop:
    """
    Full autonomous evolution cycle with version control.
    """

    def __init__(
        self,
        decision_engine: EvolutionDecisionEngine,
        patch_generator: RealPatchGenerator,
        apply_engine: SafeApplyEngine,
    ) -> None:
        self.decision_engine = decision_engine
        self.patch_generator = patch_generator
        self.apply_engine = apply_engine

        self.history: list[Any] = []

    def run(self) -> dict[str, Any]:
        # 1. decide evolution
        decision = self.decision_engine.decide()

        # 2. generate patch
        patch = self.patch_generator.generate(decision)

        # 3. apply safely
        result = self.apply_engine.apply(patch)

        # 4. git commit (safe automated versioning)
        commit_msg = f"auto-evolution: {result.status}"

        try:
            subprocess.run(["git", "add", "."], check=False)
            subprocess.run(["git", "commit", "-m", commit_msg], check=False)
        except Exception:
            pass  # safe mode fallback

        # 5. store history
        record = {
            "decision": decision,
            "patch": patch,
            "apply_result": result,
        }

        self.history.append(record)

        return record
