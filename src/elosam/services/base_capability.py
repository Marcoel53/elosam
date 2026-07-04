"""
Base implementation for AEGIS capabilities.
"""

from __future__ import annotations

from elosam.contracts.capability import Capability


class BaseCapability(Capability):
    """
    Base implementation shared by all capabilities.
    """

    @property
    def name(self) -> str:
        return self.__class__.__name__

    def initialize(self) -> None:
        pass

    def shutdown(self) -> None:
        pass

    def ready(self) -> bool:
        return True
