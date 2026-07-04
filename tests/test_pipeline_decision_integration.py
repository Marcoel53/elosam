from elosam.core.decision_engine import (
    DecisionContext,
    DecisionEngine,
)
from elosam.core.engineering_pipeline import EngineeringPipeline


def test_pipeline_uses_decision_engine() -> None:
    pipeline = EngineeringPipeline()
    decision = DecisionEngine()

    result = decision.evaluate(
        DecisionContext(
            data={
                "mission": "engineering",
            }
        )
    )

    assert result.decision == "accept"

    pipeline_result = pipeline.run(
        {
            "mission": "engineering",
        }
    )

    assert pipeline_result.status.value == "completed"