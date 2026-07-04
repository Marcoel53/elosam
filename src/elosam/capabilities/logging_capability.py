"""
Logging Capability
"""

from __future__ import annotations


class LoggingCapability:
    """
    First official EloSam Capability.
    """

    name = "logging"

    def initialize(self) -> None:
        pass

    def shutdown(self) -> None:
        pass

    def ready(self) -> bool:
        return True