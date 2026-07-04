from elosam.application import EloSam
from elosam.core.engineering_pipeline import PipelineStage


def test_application_execute() -> None:
    app = EloSam()

    result = app.execute(
        mission_id="APP-001",
        name="Application Execute",
        payload={
            "objective": "application execution",
        },
    )

    assert result.status == PipelineStage.COMPLETED