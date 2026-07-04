from __future__ import annotations

from typing import Any
from typing import Protocol


class MemoryContract(Protocol):
    """
    Memory interface.
    """

    def set(
        self,
        key: str,
        value: Any,
    ) -> None: ...

    def get(
        self,
        key: str,
        default: Any = None,
    ) -> Any: ...

    def exists(
        self,
        key: str,
    ) -> bool: ...