"""
AEGIS CORE Lifecycle.
"""

from __future__ import annotations

from .lifecycle_state import LifecycleState


class Lifecycle:
    """Controls the kernel lifecycle."""

    def __init__(self) -> None:
        self._state = LifecycleState.CREATED

    @property
    def state(self) -> LifecycleState:
        return self._state

    def initializing(self) -> None:
        self._state = LifecycleState.INITIALIZING

    def initialized(self) -> None:
        self._state = LifecycleState.INITIALIZED

    def starting(self) -> None:
        self._state = LifecycleState.STARTING

    def running(self) -> None:
        self._state = LifecycleState.RUNNING

    def stopping(self) -> None:
        self._state = LifecycleState.STOPPING

    def stopped(self) -> None:
        self._state = LifecycleState.STOPPED

    def failed(self) -> None:
        self._state = LifecycleState.FAILED

    def reset(self) -> None:
        self._state = LifecycleState.CREATED
