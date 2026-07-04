"""
ELOSam Engineering Pipeline
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from elosam.core.engineering_strategy import DefaultEngineeringStrategy
from elosam.core.event_bus import EventBus


class PipelineStage(str, Enum):
    CREATED = "created"
    PLANNING = "planning"
    ARCHITECTURE = "architecture"
    DECISION = "decision"
    CAPABILITY = "capability"
    EXECUTION = "execution"
    VALIDATION = "validation"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass(slots=True)
class PipelineResult:
    status: PipelineStage
    history: list[PipelineStage] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


class EngineeringPipeline:

    def __init__(
        self,
        strategy: DefaultEngineeringStrategy | None = None,
    ) -> None:
        self._history: list[PipelineStage] = []
        self._bus: EventBus | None = None
        self._strategy = strategy or DefaultEngineeringStrategy()

    @property
    def history(self) -> list[PipelineStage]:
        return list(self._history)

    def bind(self, bus: EventBus) -> None:
        self._bus = bus

    def _publish(self, stage: PipelineStage) -> None:
        if self._bus is not None:
            self._bus.publish(
                "engineering.stage.changed",
                stage,
            )

    def run(
        self,
        mission: dict[str, Any],
    ) -> PipelineResult:

        if not mission:
            self._publish(PipelineStage.FAILED)

            return PipelineResult(
                status=PipelineStage.FAILED,
                history=[PipelineStage.FAILED],
                metadata={
                    "reason": "empty_mission",
                },
            )

        self._history.clear()

        for stage in self._strategy.stages():
            self._history.append(stage)
            self._publish(stage)

        return PipelineResult(
            status=PipelineStage.COMPLETED,
            history=self.history,
            metadata={
                "mission": mission,
            },
        )