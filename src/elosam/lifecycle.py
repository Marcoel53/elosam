"""
Lifecycle states of the EloSam application.
"""

from enum import Enum, auto


class LifecycleState(Enum):
    """Represents the lifecycle of the application."""

    CREATED = auto()
    BOOTSTRAPPING = auto()
    INITIALIZING = auto()
    READY = auto()
    STOPPING = auto()
    STOPPED = auto()
    ERROR = auto()
