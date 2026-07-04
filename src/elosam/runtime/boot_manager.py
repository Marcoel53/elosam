"""
BootManager - responsible for bootstrapping the AEGIS Runtime.
"""

from elosam.core.lifecycle_state import LifecycleState


class BootManager:
    def __init__(self, runtime) -> None:
        self._runtime = runtime

    def boot(self) -> None:
        self._runtime.lifecycle.transition(LifecycleState.BOOTSTRAPPING)

        self._runtime.initialize()

        self._runtime.lifecycle.transition(LifecycleState.INITIALIZING)

        self._runtime.start()

        self._runtime.lifecycle.transition(LifecycleState.READY)

        self._runtime.events.publish("runtime.ready")
