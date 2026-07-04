"""
AEGIS POLICY ENGINE.
Governance layer over decisions.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class PolicyContext:
    data: dict[str, Any]


@dataclass(slots=True)
class PolicyResult:
    allowed: bool
    reason: str
    severity: str  # info | warning | critical


class Policy:
    """
    Single governance rule.
    """

    def __init__(self, name: str, condition, severity: str = "warning") -> None:
        self.name = name
        self.condition = condition
        self.severity = severity

    def evaluate(self, context: PolicyContext) -> PolicyResult:
        violated = self.condition(context)

        if violated:
            return PolicyResult(
                allowed=False,
                reason=self.name,
                severity=self.severity,
            )

        return PolicyResult(
            allowed=True,
            reason="ok",
            severity="info",
        )


class PolicyEngine:
    """
    Evaluates system-level constraints before decisions execute.
    """

    def __init__(self) -> None:
        self._policies: list[Policy] = []

    def add_policy(self, policy: Policy) -> None:
        self._policies.append(policy)

    def evaluate(self, context: PolicyContext) -> list[PolicyResult]:
        return [p.evaluate(context) for p in self._policies]

    def allowed(self, context: PolicyContext) -> bool:
        results = self.evaluate(context)
        return all(r.allowed for r in results)
