"""
Knowledge Loader
"""

from __future__ import annotations

from pathlib import Path


class KnowledgeLoader:
    """
    Loads textual knowledge sources.
    """

    def load(self, path: str | Path) -> str:
        path = Path(path)

        return path.read_text(
            encoding="utf-8",
        )