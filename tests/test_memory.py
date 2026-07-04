from elosam.memory.memory import Memory


def test_memory_store_and_read() -> None:
    memory = Memory()

    memory.set("mission", "ENG-001")

    assert memory.get("mission") == "ENG-001"


def test_memory_exists() -> None:
    memory = Memory()

    memory.set("a", 10)

    assert memory.exists("a")


def test_memory_delete() -> None:
    memory = Memory()

    memory.set("a", 10)

    memory.delete("a")

    assert not memory.exists("a")


def test_memory_keys() -> None:
    memory = Memory()

    memory.set("b", 2)
    memory.set("a", 1)

    assert memory.keys() == ["a", "b"]


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