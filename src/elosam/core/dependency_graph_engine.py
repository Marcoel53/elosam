"""
AEGIS DEPENDENCY GRAPH ENGINE.
Builds structural map of system architecture.
"""

from __future__ import annotations

import ast
import os
from dataclasses import dataclass
from typing import Any


@dataclass
class ModuleNode:
    name: str
    imports: list[str]


class DependencyGraphEngine:
    """
    Builds dependency graph from Python source code.
    """

    def __init__(self, root: str = "src") -> None:
        self.root = root

    def _parse_file(self, path: str) -> ModuleNode:
        with open(path, "r", encoding="utf-8") as f:
            tree = ast.parse(f.read(), filename=path)

        imports: list[str] = []

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for n in node.names:
                    imports.append(n.name)

            if isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.append(node.module)

        return ModuleNode(
            name=path.replace(os.sep, "."),
            imports=imports,
        )

    def build(self) -> dict[str, Any]:
        modules: list[ModuleNode] = []

        for base, _, files in os.walk(self.root):
            for f in files:
                if f.endswith(".py"):
                    path = os.path.join(base, f)
                    modules.append(self._parse_file(path))

        graph = {
            m.name: m.imports
            for m in modules
        }

        return {
            "total_modules": len(modules),
            "graph": graph,
        }
