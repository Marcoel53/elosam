"""
AEGIS CORE Audit System.
Tracks decisions and system behavior.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from datetime import datetime, timezone


@dataclass(slots=True)
class AuditRecord:
    event: str
    payload: Any
    timestamp: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


class AuditLog:
    """
    Stores full decision history.
    """

    def __init__(self) -> None:
        self._records: list[AuditRecord] = []

    def record(self, event: str, payload: Any) -> None:
        self._records.append(
            AuditRecord(
                event=event,
                payload=payload,
            )
        )

    def all(self) -> list[AuditRecord]:
        return list(self._records)

    def clear(self) -> None:
        self._records.clear()
