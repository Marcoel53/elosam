from elosam.core.engineering_pipeline import (
    EngineeringPipeline,
    PipelineStage,
)
from elosam.core.event_bus import EventBus


def test_pipeline_publishes_all_events() -> None:
    bus = EventBus()
    pipeline = EngineeringPipeline()

    received: list[PipelineStage] = []

    pipeline.bind(bus)

    bus.subscribe(
        "engineering.stage.changed",
        lambda event: received.append(event.payload),
    )

    result = pipeline.run(
        {
            "objective": "engineering pipeline",
        }
    )

    assert result.status == PipelineStage.COMPLETED

    assert received == [
        PipelineStage.CREATED,
        PipelineStage.PLANNING,
        PipelineStage.ARCHITECTURE,
        PipelineStage.DECISION,
        PipelineStage.CAPABILITY,
        PipelineStage.EXECUTION,
        PipelineStage.VALIDATION,
        PipelineStage.COMPLETED,
    ]


def test_pipeline_publishes_failed_event() -> None:
    bus = EventBus()
    pipeline = EngineeringPipeline()

    received: list[PipelineStage] = []

    pipeline.bind(bus)

    bus.subscribe(
        "engineering.stage.changed",
        lambda event: received.append(event.payload),
    )

    result = pipeline.run({})

    assert result.status == PipelineStage.FAILED
    assert received == [PipelineStage.FAILED]