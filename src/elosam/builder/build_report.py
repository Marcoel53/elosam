from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class BuildReport:
    """
    Result of a build execution.
    """

    specification: str

    generated: list[Path]

    @property
    def total_files(self) -> int:
        return len(self.generated)