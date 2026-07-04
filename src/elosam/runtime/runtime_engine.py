"""
AEGIS Runtime Engine.
"""

from __future__ import annotations

from elosam.core.boot_manager import BootManager
from elosam.core.capability_engine import CapabilityEngine
from elosam.core.capability_registry import CapabilityRegistry
from elosam.core.configuration_manager import ConfigurationManager
from elosam.core.event_bus import EventBus
from elosam.core.health_manager import HealthManager
from elosam.core.lifecycle import Lifecycle
from elosam.core.logging_manager import LoggingManager
from elosam.core.service_registry import ServiceRegistry


class RuntimeEngine:
    """
    Central runtime orchestrator.
    """

    def __init__(self) -> None:
        self.lifecycle = Lifecycle()
        self.services = ServiceRegistry()
        self.capabilities = CapabilityRegistry()
        self.events = EventBus()
        self.configuration = ConfigurationManager()
        self.logging = LoggingManager()

        self.health = HealthManager(self.services)

        self.boot = BootManager(self.lifecycle, self.services)

        self.capability_engine = CapabilityEngine(self.capabilities)

    def initialize(self) -> None:
        self.boot.boot()
        self.capability_engine.initialize()

    def shutdown(self) -> None:
        self.capability_engine.shutdown()
        self.boot.shutdown()

    def healthy(self) -> bool:
        return self.health.healthy()
