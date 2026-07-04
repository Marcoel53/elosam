"""
Engineering Runtime

Constitutional Runtime Composer.
"""

from __future__ import annotations

from typing import Any

from elosam.core.decision_engine import DecisionEngine
from elosam.core.engineering_pipeline import EngineeringPipeline
from elosam.core.event_bus import EventBus
from elosam.core.mission_engine import MissionEngine


class EngineeringRuntime:
    """
    Composes the engineering pipeline components.
    """

    def __init__(self) -> None:
        self.events = EventBus()
        self.missions = MissionEngine()
        self.decisions = DecisionEngine()
        self.pipeline = EngineeringPipeline()

        self.pipeline.bind(self.events)

    def healthy(self) -> bool:
        return True

    def execute(
        self,
        mission_id: str,
        name: str,
        payload: dict[str, Any],
    ):
        mission = self.missions.create(
            mission_id=mission_id,
            name=name,
            payload=payload,
        )

        return self.pipeline.run(
            mission.payload,
        )