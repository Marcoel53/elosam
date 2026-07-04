"""
AEGIS KNOWLEDGE ENGINE.
Persistent memory for decisions and patterns.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class KnowledgeEntry:
    key: str
    value: Any
    tags: list[str]


class KnowledgeEngine:
    """
    Simple in-memory knowledge store.
    """

    def __init__(self) -> None:
        self._store: dict[str, KnowledgeEntry] = {}

    def remember(self, key: str, value: Any, tags: list[str] | None = None) -> None:
        self._store[key] = KnowledgeEntry(
            key=key,
            value=value,
            tags=tags or [],
        )

    def recall(self, key: str) -> Any | None:
        entry = self._store.get(key)
        return entry.value if entry else None

    def search_by_tag(self, tag: str) -> list[KnowledgeEntry]:
        return [
            e for e in self._store.values()
            if tag in e.tags
        ]

    def all(self) -> list[KnowledgeEntry]:
        return list(self._store.values())
