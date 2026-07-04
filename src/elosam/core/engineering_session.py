"""
Engineering Session

Represents a complete engineering execution.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class EngineeringSession:
    mission_id: str
    name: str
    payload: dict[str, Any]

    events: list[Any] = field(default_factory=list)

    result: Any | None = None

    completed: bool = False