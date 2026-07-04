"""
Service contract for the AEGIS CORE.
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class Service(ABC):
    """
    Base contract for every EloSam service.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Unique service name."""

    @abstractmethod
    def initialize(self) -> None:
        """Initialize the service."""

    @abstractmethod
    def start(self) -> None:
        """Start the service."""

    @abstractmethod
    def stop(self) -> None:
        """Stop the service."""

    @abstractmethod
    def health(self) -> bool:
        """Return True if the service is healthy."""
