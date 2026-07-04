from elosam.core.engineering_pipeline import (
    EngineeringPipeline,
    PipelineStage,
)
from elosam.core.mission_engine import MissionEngine


def test_mission_starts_pipeline() -> None:
    mission_engine = MissionEngine()
    pipeline = EngineeringPipeline()

    mission = mission_engine.create(
        mission_id="MISSION-001",
        name="Pipeline Test",
        payload={"goal": "integration"},
    )

    result = pipeline.run(mission.payload)

    assert result.status == PipelineStage.COMPLETED

    assert result.history[-1] == PipelineStage.COMPLETED