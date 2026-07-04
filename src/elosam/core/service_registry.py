"""
Service registry for the AEGIS CORE.
"""

from __future__ import annotations

from collections.abc import Iterator

from elosam.contracts.service import Service


class ServiceRegistry:
    """
    Registry responsible for storing and retrieving services.
    """

    def __init__(self) -> None:
        self._services: dict[str, Service] = {}

    def register(self, service: Service) -> None:
        if service.name in self._services:
            raise ValueError(
                f"Service '{service.name}' is already registered."
            )

        self._services[service.name] = service

    def unregister(self, name: str) -> None:
        self._services.pop(name, None)

    def get(self, name: str) -> Service:
        return self._services[name]

    def exists(self, name: str) -> bool:
        return name in self._services

    def all(self) -> list[Service]:
        return list(self._services.values())

    def clear(self) -> None:
        self._services.clear()

    def __contains__(self, name: str) -> bool:
        return name in self._services

    def __len__(self) -> int:
        return len(self._services)

    def __iter__(self) -> Iterator[Service]:
        return iter(self._services.values())
