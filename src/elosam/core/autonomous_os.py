"""
AEGIS AUTONOMOUS OPERATING CORE.
Unifies event-driven + autonomous runtime execution.
"""

from __future__ import annotations

from typing import Any

from elosam.core.event_bus import EventBus
from elosam.core.agent_registry import AgentRegistry
from elosam.core.agent_arbitration import ArbitrationEngine
from elosam.core.meta_agent_engine import MetaAgentEngine
from elosam.core.autonomous_runtime import AutonomousRuntime


class AutonomousOS:
    """
    Final orchestration layer of EloSam.
    """

    def __init__(
        self,
        bus: EventBus,
        registry: AgentRegistry,
        arbitration: ArbitrationEngine,
        meta: MetaAgentEngine,
    ) -> None:
        self.bus = bus
        self.registry = registry
        self.meta = meta

        self.runtime = AutonomousRuntime(
            registry=registry,
            arbitration=arbitration,
            meta=meta,
        )

        self._bind_events()

    def _bind_events(self) -> None:
        """
        Connect external world → internal system.
        """

        self.bus.subscribe("system.task", self._on_task)
        self.bus.subscribe("system.stop", self._on_stop)

    def _on_task(self, event: Any) -> None:
        payload = getattr(event, "payload", event)

        if not isinstance(payload, dict):
            return

        # inject task into autonomous cycle
        self.runtime.step(payload)

    def _on_stop(self, event: Any) -> None:
        self.runtime.stop()

    def run_cycle(self, task: dict[str, Any], iterations: int = 3) -> list[Any]:
        return self.runtime.cycle(task, iterations)
