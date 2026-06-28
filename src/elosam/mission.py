from dataclasses import dataclass, field
from uuid import UUID, uuid4

from .enums import MissionStatus


@dataclass(slots=True)
class Mission:
    id: UUID = field(default_factory=uuid4)
    name: str = ""
    objective: str = ""
    status: MissionStatus = MissionStatus.CREATED
    result: object | None = None
