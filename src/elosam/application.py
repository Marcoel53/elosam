"""
EloSam Application
"""

from __future__ import annotations

from typing import Any

from elosam.core.engineering_runtime import EngineeringRuntime
from elosam.lifecycle import LifecycleState


class EloSamApplication:
    """
    Public entry point for the EloSam platform.
    """

    def __init__(self) -> None:
        self._runtime = EngineeringRuntime()
        self.state = LifecycleState.CREATED

    @property
    def runtime(self) -> EngineeringRuntime:
        return self._runtime

    def start(self) -> None:
        """
        Starts the application.
        """
        self.state = LifecycleState.READY

    def execute(
        self,
        mission_id: str,
        name: str,
        payload: dict[str, Any],
    ):
        return self._runtime.execute(
            mission_id=mission_id,
            name=name,
            payload=payload,
        )


# Backward compatibility
EloSam = EloSamApplication