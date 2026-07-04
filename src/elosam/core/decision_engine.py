from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from elosam.core.event import Event
from elosam.core.event_bus import EventBus
from elosam.core.rule_engine import RuleEngine, RuleContext


@dataclass(slots=True)
class DecisionContext:
    data: dict[str, Any]


@dataclass(slots=True)
class DecisionResult:
    decision: str
    confidence: float
    metadata: dict[str, Any]


class DecisionEngine:
    def __init__(
        self,
        events: EventBus | None = None,
        rules: RuleEngine | None = None,
    ) -> None:
        self._events = events
        self._rules = rules

    def bind(self, events: EventBus) -> None:
        self._events = events

        def handler(event: Event) -> None:
            payload = event.payload
            if isinstance(payload, dict):
                self.evaluate(DecisionContext(payload))

        events.subscribe("decision.requested", handler)

    def evaluate(self, context: DecisionContext) -> DecisionResult:

        if not self._rules:
            if not context.data:
                result = DecisionResult(
                    decision="reject",
                    confidence=1.0,
                    metadata={"reason": "empty_context"},
                )
            else:
                result = DecisionResult(
                    decision="accept",
                    confidence=0.6,
                    metadata={"size": len(context.data)},
                )
        else:
            result = self._from_rules(context)

        if self._events:
            self._events.publish(
                Event(
                    name="decision.executed",
                    payload=result,
                )
            )

        return result

    def _from_rules(self, context: DecisionContext) -> DecisionResult:
        result = self._rules.evaluate(RuleContext(context.data))

        normalized = result["normalized"]

        decision = "accept" if normalized >= 0.5 else "reject"

        return DecisionResult(
            decision=decision,
            confidence=normalized,
            metadata={
                "total_score": result["total_score"],
                "max_score": result["max_score"],
                "size": len(context.data),
            },
        )
