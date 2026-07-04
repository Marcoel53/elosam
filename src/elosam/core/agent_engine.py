"""
AEGIS AGENT ENGINE.
Autonomous execution layer over missions.
"""

from __future__ import annotations

from typing import Any

from elosam.core.event_bus import EventBus
from elosam.core.mission_engine import MissionEngine


class AgentEngine:
    """
    Turns events into autonomous mission execution.
    """

    def __init__(
        self,
        events: EventBus,
        missions: MissionEngine,
    ) -> None:
        self._events = events
        self._missions = missions

    def bind(self) -> None:
        """
        Attach agent behavior to event system.
        """

        self._events.subscribe(
            "agent.request",
            self._handle_request,
        )

    def _handle_request(self, event: Any) -> None:
        payload = getattr(event, "payload", event)

        if not isinstance(payload, dict):
            return

        mission_id = payload.get("id", "auto-mission")
        name = payload.get("name", "auto-generated")
        data = payload.get("data", {})

        mission = self._missions.create(mission_id, name, data)
        self._missions.start(mission_id)

        # feedback loop into event system
        self._events.publish(
            "agent.executed",
            {
                "mission_id": mission_id,
                "status": mission.status,
            },
        )
