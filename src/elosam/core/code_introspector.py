"""
AEGIS CODE INTROSPECTOR.
Analyzes system structure for self-modification planning.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class ModuleInfo:
    path: str
    size: int


class CodeIntrospector:
    """
    Scans source code to build system map.
    """

    def __init__(self, root: str = "src") -> None:
        self.root = root

    def scan(self) -> dict[str, Any]:
        modules: list[ModuleInfo] = []

        for base, _, files in os.walk(self.root):
            for f in files:
                if f.endswith(".py"):
                    path = os.path.join(base, f)
                    modules.append(
                        ModuleInfo(
                            path=path,
                            size=os.path.getsize(path),
                        )
                    )

        return {
            "total_modules": len(modules),
            "modules": modules,
        }
