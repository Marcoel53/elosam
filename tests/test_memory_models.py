from elosam.memory.models import MemoryEntry


def test_memory_entry() -> None:
    entry = MemoryEntry(
        key="mission",
        value="ENG-001",
    )

    assert entry.key == "mission"
    assert entry.value == "ENG-001"