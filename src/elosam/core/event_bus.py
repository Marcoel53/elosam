"""
AEGIS CORE Event Bus.
"""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Callable
from typing import Any

from elosam.core.event import Event


EventHandler = Callable[[Event], None]


class EventBus:
    """
    Synchronous event bus.
    """

    def __init__(self) -> None:
        self._handlers: dict[str, list[EventHandler]] = defaultdict(list)

    def subscribe(
        self,
        event: str,
        handler: EventHandler,
    ) -> None:
        self._handlers[event].append(handler)

    def unsubscribe(
        self,
        event: str,
        handler: EventHandler,
    ) -> None:
        if handler in self._handlers[event]:
            self._handlers[event].remove(handler)

    def publish(
        self,
        event: str | Event,
        payload: Any = None,
    ) -> None:

        if isinstance(event, str):
            event = Event(
                name=event,
                payload=payload,
            )

        for handler in self._handlers[event.name]:
            handler(event)

    def clear(self) -> None:
        self._handlers.clear()
