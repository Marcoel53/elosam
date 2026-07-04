"""
AEGIS CORE Evidence System.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class Evidence:
    """
    Represents why a rule or decision was made.
    """

    source: str
    weight: float
    passed: bool
    detail: str = ""


@dataclass(slots=True)
class EvidenceBundle:
    """
    Collection of evidences used to explain a decision.
    """

    items: list[Evidence]

    def total_score(self) -> float:
        return sum(e.weight for e in self.items if e.passed)

    def explanation(self) -> str:
        passed = [e for e in self.items if e.passed]
        failed = [e for e in self.items if not e.passed]

        return (
            f"passed={len(passed)}, "
            f"failed={len(failed)}, "
            f"score={self.total_score():.2f}"
        )
