from elosam.core.engineering_pipeline import (
    EngineeringPipeline,
    PipelineStage,
)


def test_empty_mission_fails() -> None:
    pipeline = EngineeringPipeline()

    result = pipeline.run({})

    assert result.status == PipelineStage.FAILED
    assert result.metadata["reason"] == "empty_mission"


def test_pipeline_runs_to_completion() -> None:
    pipeline = EngineeringPipeline()

    result = pipeline.run(
        {
            "objective": "Build Engineering Pipeline",
        }
    )

    assert result.status == PipelineStage.COMPLETED

    assert result.history == [
        PipelineStage.CREATED,
        PipelineStage.PLANNING,
        PipelineStage.ARCHITECTURE,
        PipelineStage.DECISION,
        PipelineStage.CAPABILITY,
        PipelineStage.EXECUTION,
        PipelineStage.VALIDATION,
        PipelineStage.COMPLETED,
    ]


def test_history_property() -> None:
    pipeline = EngineeringPipeline()

    pipeline.run({"mission": "demo"})

    assert pipeline.history[-1] == PipelineStage.COMPLETED
    assert len(pipeline.history) == 8