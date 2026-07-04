"""
AEGIS CORE Event.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any


@dataclass(slots=True, frozen=True)
class Event:
    """
    Base event for the AEGIS runtime.
    """

    name: str
    payload: Any = None
    timestamp: datetime = field(
        default_factory=lambda: datetime.now(UTC)
    )
