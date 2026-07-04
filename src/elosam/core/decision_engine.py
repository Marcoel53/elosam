"""
EloSam Decision Engine
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from elosam.core.event_bus import EventBus


@dataclass(slots=True)
class DecisionContext:
    data: dict[str, Any]


@dataclass(slots=True)
class DecisionResult:
    decision: str
    confidence: float
    metadata: dict[str, Any] = field(default_factory=dict)


class DecisionEngine:
    def __init__(self) -> None:
        self._bus: EventBus | None = None

    def bind(self, bus: EventBus) -> None:
        self._bus = bus
        bus.subscribe(
            "decision.requested",
            self._on_decision_requested,
        )

    def evaluate(
        self,
        context: DecisionContext,
    ) -> DecisionResult:

        if not context.data:
            return DecisionResult(
                decision="reject",
                confidence=1.0,
                metadata={
                    "reason": "empty_context",
                },
            )

        return DecisionResult(
            decision="accept",
            confidence=0.6,
            metadata={
                "size": len(context.data),
            },
        )

    def _on_decision_requested(self, event) -> None:
        result = self.evaluate(
            DecisionContext(
                data=event.payload,
            )
        )

        if self._bus is not None:
            self._bus.publish(
                "decision.executed",
                result,
            )