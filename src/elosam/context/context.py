from __future__ import annotations

from typing import Any

from elosam.knowledge.knowledge import Knowledge
from elosam.memory.memory import Memory


class Context:
    """
    Combines Memory and Knowledge into a single context.
    """

    def __init__(
        self,
        memory: Memory | None = None,
        knowledge: Knowledge | None = None,
    ) -> None:
        self.memory = memory or Memory()
        self.knowledge = knowledge or Knowledge()

    def remember(
        self,
        key: str,
        value: Any,
    ) -> None:
        self.memory.set(key, value)

    def recall(
        self,
        key: str,
        default: Any = None,
    ) -> Any:
        return self.memory.get(key, default)

    def learn(
        self,
        name: str,
        content: Any,
    ) -> None:
        self.knowledge.add(name, content)

    def know(
        self,
        name: str,
    ) -> Any:
        return self.knowledge.get(name)