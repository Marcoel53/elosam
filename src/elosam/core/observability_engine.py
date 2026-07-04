"""
AEGIS OBSERVABILITY ENGINE.
Full system tracing and execution visibility.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from datetime import datetime, timezone


@dataclass(slots=True)
class TraceEvent:
    layer: str
    event: str
    data: Any
    timestamp: datetime


class ObservabilityEngine:
    """
    Captures full system execution trace.
    """

    def __init__(self) -> None:
        self._trace: list[TraceEvent] = []

    def log(self, layer: str, event: str, data: Any) -> None:
        self._trace.append(
            TraceEvent(
                layer=layer,
                event=event,
                data=data,
                timestamp=datetime.now(timezone.utc),
            )
        )

    def all(self) -> list[TraceEvent]:
        return self._trace

    def filter_by_layer(self, layer: str) -> list[TraceEvent]:
        return [t for t in self._trace if t.layer == layer]

    def clear(self) -> None:
        self._trace.clear()
