from elosam.memory.contracts import MemoryContract
from elosam.memory.memory import Memory


def test_memory_implements_contract() -> None:
    memory: MemoryContract = Memory()

    memory.set(
        "mission",
        "ENG-001",
    )

    assert memory.get("mission") == "ENG-001"