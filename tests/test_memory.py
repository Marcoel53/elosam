from elosam.memory.memory import Memory


def test_memory_store_and_read() -> None:
    memory = Memory()

    memory.set(
        "mission",
        "ENG-001",
    )

    assert memory.get("mission") == "ENG-001"


def test_memory_exists() -> None:
    memory = Memory()

    memory.set(
        "a",
        10,
    )

    assert memory.exists("a")


def test_memory_size() -> None:
    memory = Memory()

    memory.set("a", 1)
    memory.set("b", 2)

    assert memory.size() == 2


def test_memory_clear() -> None:
    memory = Memory()

    memory.set("a", 1)

    memory.clear()

    assert memory.size() == 0