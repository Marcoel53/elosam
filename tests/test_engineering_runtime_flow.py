from elosam.core.engineering_runtime import EngineeringRuntime
from elosam.core.engineering_pipeline import PipelineStage


def test_engineering_runtime_flow() -> None:
    runtime = EngineeringRuntime()

    mission = runtime.missions.create(
        mission_id="ENG-001",
        name="Engineering Runtime",
        payload={
            "objective": "Validate Runtime",
        },
    )

    result = runtime.pipeline.run(
        mission.payload,
    )

    assert result.status == PipelineStage.COMPLETED

    assert result.history[-1] == PipelineStage.COMPLETED