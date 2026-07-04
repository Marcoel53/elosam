from elosam.core.engineering_pipeline import PipelineStage
from elosam.core.engineering_runtime import EngineeringRuntime


def test_runtime_execute() -> None:
    runtime = EngineeringRuntime()

    result = runtime.execute(
        mission_id="ENG-001",
        name="Runtime Execute",
        payload={
            "objective": "run",
        },
    )

    assert result.status == PipelineStage.COMPLETED