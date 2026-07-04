"""
AEGIS CORE Configuration Manager.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import json


class ConfigurationManager:
    """
    Simple JSON configuration manager.
    """

    def __init__(self) -> None:
        self._data: dict[str, Any] = {}

    def load(self, path: str | Path) -> None:
        file = Path(path)

        with file.open("r", encoding="utf-8") as fp:
            self._data = json.load(fp)

    def get(self, key: str, default: Any = None) -> Any:
        return self._data.get(key, default)

    def set(self, key: str, value: Any) -> None:
        self._data[key] = value

    def has(self, key: str) -> bool:
        return key in self._data

    def clear(self) -> None:
        self._data.clear()

    @property
    def data(self) -> dict[str, Any]:
        return dict(self._data)
