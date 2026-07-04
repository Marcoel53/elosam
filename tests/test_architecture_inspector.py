from elosam.inspector.architecture_inspector import (
    ArchitectureInspector,
)


def test_architecture_rule_passes() -> None:
    inspector = ArchitectureInspector()

    result = inspector.validate(
        True,
        "core_isolated",
    )

    assert result.passed
    assert result.rule == "core_isolated"


def test_architecture_rule_fails() -> None:
    inspector = ArchitectureInspector()

    result = inspector.validate(
        False,
        "core_isolated",
    )

    assert result.passed is False