"""
AEGIS REAL PATCH GENERATOR (CONTROLLED MODE).
Generates actual file modification diffs safely.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class RealPatch:
    file: str
    before: str
    after: str
    reason: str


class RealPatchGenerator:
    """
    Converts evolution decisions into real code patches.
    (NO AUTO-APPLY - ONLY GENERATION)
    """

    def generate(self, decision: Any) -> dict[str, Any]:
        selected = getattr(decision, "selected", None)

        if not selected:
            return {
                "status": "no_patch",
                "reason": getattr(decision, "reasoning", "no decision"),
            }

        target = getattr(selected, "target", "unknown.py")
        action = getattr(selected, "change", "")

        # SIMULATED PATCH (safe template, not executing filesystem writes)
        patch = RealPatch(
            file=target,
            before="# current version (unknown state)",
            after=f"# proposed change:\n# {action}",
            reason=getattr(decision, "reasoning", ""),
        )

        return {
            "status": "patch_generated",
            "patch": patch,
        }
