from __future__ import annotations

from typing import Any


class Memory:
    """
    In-memory key/value storage.
    """

    def __init__(self) -> None:
        self._data: dict[str, Any] = {}

    def set(
        self,
        key: str,
        value: Any,
    ) -> None:
        self._data[key] = value

    def get(
        self,
        key: str,
        default: Any = None,
    ) -> Any:
        return self._data.get(
            key,
            default,
        )

    def exists(
        self,
        key: str,
    ) -> bool:
        return key in self._data

    def clear(self) -> None:
        self._data.clear()

    def size(self) -> int:
        return len(self._data)