from elosam.knowledge.knowledge import Knowledge


def test_add_document() -> None:
    knowledge = Knowledge()

    knowledge.add(
        "constitution",
        "AEGIS",
    )

    assert knowledge.get("constitution") == "AEGIS"


def test_exists() -> None:
    knowledge = Knowledge()

    knowledge.add(
        "doc",
        "text",
    )

    assert knowledge.exists("doc")


def test_remove() -> None:
    knowledge = Knowledge()

    knowledge.add(
        "doc",
        "text",
    )

    knowledge.remove("doc")

    assert not knowledge.exists("doc")


def test_names() -> None:
    knowledge = Knowledge()

    knowledge.add("b", 2)
    knowledge.add("a", 1)

    assert knowledge.names() == [
        "a",
        "b",
    ]


def test_size() -> None:
    knowledge = Knowledge()

    knowledge.add("a", 1)
    knowledge.add("b", 2)

    assert knowledge.size() == 2


def test_clear() -> None:
    knowledge = Knowledge()

    knowledge.add("a", 1)

    knowledge.clear()

    assert knowledge.size() == 0