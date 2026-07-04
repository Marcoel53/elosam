from __future__ import annotations

from typing import Any

from elosam.memory.memory import Memory


class Knowledge:
    """
    Knowledge repository backed by Memory.
    """

    def __init__(self) -> None:
        self._memory = Memory()

    def add(
        self,
        name: str,
        content: Any,
    ) -> None:
        self._memory.set(name, content)

    def get(
        self,
        name: str,
    ) -> Any | None:
        return self._memory.get(name)

    def exists(
        self,
        name: str,
    ) -> bool:
        return self._memory.exists(name)

    def remove(
        self,
        name: str,
    ) -> None:
        self._memory.delete(name)

    def names(self) -> list[str]:
        return self._memory.keys()

    def size(self) -> int:
        return self._memory.size()

    def clear(self) -> None:
        self._memory.clear()