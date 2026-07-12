from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class ApprovalLevel(str, Enum):
    NONE = "none"
    REQUIRED = "required"
    AUTOMATIC = "automatic"


@dataclass
class CapabilityDescriptor:
    id: str
    version: str = "1.0"
    timeout: int = 60
    retries: int = 3
    approval: ApprovalLevel = ApprovalLevel.NONE
    owner: str = "system"
    priority: int = 0
    metadata: dict[str, Any] = field(default_factory=dict)
