from elosam.core.decision_engine import DecisionEngine, DecisionContext


def test_empty_context_rejects() -> None:
    engine = DecisionEngine()

    result = engine.evaluate(DecisionContext(data={}))

    assert result.decision == "reject"
    assert result.confidence == 1.0
    assert result.metadata["reason"] == "empty_context"


def test_non_empty_context_accepts() -> None:
    engine = DecisionEngine()

    result = engine.evaluate(
        DecisionContext(data={"task": "analyze"})
    )

    assert result.decision == "accept"
    assert result.confidence == 0.6
    assert "size" in result.metadata
