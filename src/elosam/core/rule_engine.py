from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

from elosam.core.evidence import Evidence, EvidenceBundle


@dataclass(slots=True)
class RuleContext:
    data: dict[str, Any]


@dataclass(slots=True)
class RuleResult:
    name: str
    passed: bool
    score: float
    evidence: Evidence


class Rule:
    def __init__(
        self,
        name: str,
        condition: Callable[[RuleContext], bool],
        weight: float = 1.0,
    ) -> None:
        self.name = name
        self.condition = condition
        self.weight = weight

    def evaluate(self, context: RuleContext) -> RuleResult:
        passed = self.condition(context)

        return RuleResult(
            name=self.name,
            passed=passed,
            score=self.weight if passed else 0.0,
            evidence=Evidence(
                source=self.name,
                weight=self.weight,
                passed=passed,
            ),
        )


class RuleEngine:
    def __init__(self) -> None:
        self._rules: list[Rule] = []

    def add_rule(self, rule: Rule) -> None:
        self._rules.append(rule)

    def evaluate(self, context: RuleContext) -> dict[str, Any]:
        results = [r.evaluate(context) for r in self._rules]

        bundle = EvidenceBundle([r.evidence for r in results])

        total_score = sum(r.score for r in results)
        max_score = sum(r.weight for r in self._rules)

        return {
            "total_score": total_score,
            "max_score": max_score,
            "normalized": (total_score / max_score) if max_score else 0.0,
            "evidence": bundle,
        }
