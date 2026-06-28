"""
Main application class for EloSam.
"""

from .lifecycle import LifecycleState


class EloSamApplication:
    """Represents the EloSam application."""

    def __init__(self) -> None:
        self._state = LifecycleState.CREATED

    @property
    def state(self) -> LifecycleState:
        return self._state

    def start(self) -> None:
        self._state = LifecycleState.BOOTSTRAPPING
        self._state = LifecycleState.INITIALIZING
        self._state = LifecycleState.READY

    def stop(self) -> None:
        self._state = LifecycleState.STOPPING
        self._state = LifecycleState.STOPPED
