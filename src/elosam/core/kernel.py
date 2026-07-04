"""
AEGIS CORE Kernel.
"""

from __future__ import annotations

from elosam.contracts.service import Service
from elosam.core.lifecycle_state import LifecycleState
from elosam.core.event_bus import EventBus
from elosam.runtime.runtime_engine import RuntimeEngine


class Kernel:
    """
    Central runtime coordinator.
    """

    def __init__(self) -> None:
        self._runtime = RuntimeEngine()

        # unify event bus (single source of truth)
        self._events = self._runtime.events

    @property
    def runtime(self) -> RuntimeEngine:
        return self._runtime

    @property
    def registry(self):
        return self._runtime.services

    @property
    def events(self) -> EventBus:
        return self._events

    @property
    def state(self) -> LifecycleState:
        return self._runtime.lifecycle.state

    def register(self, service: Service) -> None:
        self._runtime.services.register(service)
        self._events.publish("service.registered", service.name)

    def initialize(self) -> None:
        self._events.publish("kernel.initializing")
        self._runtime.initialize()
        self._events.publish("kernel.running")

    def start(self) -> None:
        self.initialize()

    def stop(self) -> None:
        self._events.publish("kernel.stopping")
        self._runtime.shutdown()
        self._events.publish("kernel.stopped")

    def healthy(self) -> bool:
        return self._runtime.healthy()
