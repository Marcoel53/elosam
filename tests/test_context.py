from elosam.context.context import Context


def test_context_memory() -> None:
    context = Context()

    context.remember(
        "mission",
        "ENG-001",
    )

    assert context.recall("mission") == "ENG-001"


def test_context_knowledge() -> None:
    context = Context()

    context.learn(
        "constitution",
        "AEGIS",
    )

    assert context.know("constitution") == "AEGIS"