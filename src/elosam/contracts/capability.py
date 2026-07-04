"""
Capability contract for the AEGIS CORE.
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class Capability(ABC):
    """
    Base contract for every runtime capability.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """
        Unique capability name.
        """

    @abstractmethod
    def initialize(self) -> None:
        """
        Prepare the capability.
        """

    @abstractmethod
    def shutdown(self) -> None:
        """
        Shutdown the capability.
        """

    @abstractmethod
    def ready(self) -> bool:
        """
        Returns True when the capability is ready.
        """
