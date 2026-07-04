"""
LifecycleManager - central authority for lifecycle transitions.
"""

from elosam.core.lifecycle_state import LifecycleState


class LifecycleManager:
    def __init__(self) -> None:
        self._state = LifecycleState.CREATED

    @property
    def state(self) -> LifecycleState:
        return self._state

    def transition(self, new_state: LifecycleState) -> None:
        if self._state == LifecycleState.STOPPED:
            raise RuntimeError("Cannot transition from STOPPED state")

        if self._state == LifecycleState.CREATED and new_state != LifecycleState.BOOTSTRAPPING:
            raise RuntimeError("Invalid transition from CREATED")

        if self._state == LifecycleState.BOOTSTRAPPING and new_state != LifecycleState.INITIALIZING:
            raise RuntimeError("Invalid transition from BOOTSTRAPPING")

        if self._state == LifecycleState.INITIALIZING and new_state != LifecycleState.READY:
            raise RuntimeError("Invalid transition from INITIALIZING")

        self._state = new_state
