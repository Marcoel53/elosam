"""
AEGIS EVOLUTION POLICY ENGINE.
Defines rules for safe system evolution.
"""

from dataclasses import dataclass
from typing import Any


@dataclass
class EvolutionPolicy:
    allow_auto_apply: bool = False
    risk_threshold: float = 0.6
    forbidden_targets: list[str] = None
    allowed_targets: list[str] = None

    def is_allowed(self, target: str, risk: float) -> bool:
        forbidden = self.forbidden_targets or []
        allowed = self.allowed_targets or []

        if target in forbidden:
            return False

        if allowed and target not in allowed:
            return False

        return risk <= self.risk_threshold
