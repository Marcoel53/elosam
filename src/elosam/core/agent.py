from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class Agent:
    name: str
    capability: str
    score: float = 1.0
    success_count: int = 0
    failure_count: int = 0

    def handle(self, payload: dict[str, Any]) -> dict[str, Any]:
        return {
            "agent": self.name,
            "status": "handled",
            "payload": payload,
        }

    def reward(self, success: bool) -> None:
        if success:
            self.success_count += 1
            self.score += 0.1
        else:
            self.failure_count += 1
            self.score = max(0.1, self.score - 0.2)
