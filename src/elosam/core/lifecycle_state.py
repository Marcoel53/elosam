"""
AEGIS CORE lifecycle states.
"""

from enum import Enum


class LifecycleState(str, Enum):
    CREATED = "created"
    INITIALIZING = "initializing"
    INITIALIZED = "initialized"
    STARTING = "starting"
    RUNNING = "running"
    STOPPING = "stopping"
    STOPPED = "stopped"
    FAILED = "failed"
