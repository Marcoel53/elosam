from elosam.core.engineering_pipeline import PipelineStage
from elosam.core.engineering_runtime import EngineeringRuntime


def test_full_engineering_execution() -> None:
    runtime = EngineeringRuntime()

    result = runtime.execute(
        mission_id="ENG-100",
        name="Full Engineering Execution",
        payload={
            "objective": "validate complete engineering flow",
        },
    )

    assert result.status == PipelineStage.COMPLETED
    assert result.history[-1] == PipelineStage.COMPLETED
    assert len(result.history) >= 8