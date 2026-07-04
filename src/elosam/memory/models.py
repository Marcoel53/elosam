from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class MemoryEntry:
    """
    Represents a value stored in memory.
    """

    key: str

    value: Any