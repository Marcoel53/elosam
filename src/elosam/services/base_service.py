"""
Base implementation for EloSam services.
"""

from __future__ import annotations

from elosam.contracts.service import Service


class BaseService(Service):
    """
    Default implementation for EloSam services.
    """

    @property
    def name(self) -> str:
        return self.__class__.__name__

    def initialize(self) -> None:
        pass

    def start(self) -> None:
        pass

    def stop(self) -> None:
        pass

    def health(self) -> bool:
        return True
