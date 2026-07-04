"""
AEGIS CORE Capability Registry.
"""

from __future__ import annotations

from collections.abc import Iterator


class CapabilityRegistry:
    """
    Registry responsible for storing runtime capabilities.
    """

    def __init__(self) -> None:
        self._capabilities: dict[str, object] = {}

    def register(self, name: str, capability: object) -> None:
        if name in self._capabilities:
            raise ValueError(
                f"Capability '{name}' is already registered."
            )

        self._capabilities[name] = capability

    def unregister(self, name: str) -> None:
        self._capabilities.pop(name, None)

    def get(self, name: str) -> object:
        return self._capabilities[name]

    def exists(self, name: str) -> bool:
        return name in self._capabilities

    def all(self) -> list[object]:
        return list(self._capabilities.values())

    def clear(self) -> None:
        self._capabilities.clear()

    def __contains__(self, name: str) -> bool:
        return name in self._capabilities

    def __len__(self) -> int:
        return len(self._capabilities)

    def __iter__(self) -> Iterator[object]:
        return iter(self._capabilities.values())
