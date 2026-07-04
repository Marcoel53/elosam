"""
AEGIS CORE Capability Engine.
"""

from __future__ import annotations

from elosam.core.capability_registry import CapabilityRegistry


class CapabilityEngine:
    """
    Responsible for managing runtime capabilities.
    """

    def __init__(self, registry: CapabilityRegistry) -> None:
        self._registry = registry

    def initialize(self) -> None:
        for capability in self._registry:
            capability.initialize()

    def shutdown(self) -> None:
        for capability in reversed(self._registry.all()):
            capability.shutdown()

    def ready(self) -> bool:
        return all(
            capability.ready()
            for capability in self._registry
        )
