"""
AEGIS MISSION ORCHESTRATOR.
Connects all EloSam subsystems.
"""

from __future__ import annotations

from typing import Any

from elosam.core.mission_engine import MissionEngine
from elosam.core.knowledge_engine import KnowledgeEngine
from elosam.core.policy_engine import PolicyEngine, PolicyContext
from elosam.core.decision_engine import DecisionEngine, DecisionContext
from elosam.core.audit import AuditLog


class MissionOrchestrator:
    """
    Central brain that coordinates mission execution lifecycle.
    """

    def __init__(
        self,
        missions: MissionEngine,
        knowledge: KnowledgeEngine,
        policies: PolicyEngine,
        decisions: DecisionEngine,
        audit: AuditLog,
    ) -> None:
        self.missions = missions
        self.knowledge = knowledge
        self.policies = policies
        self.decisions = decisions
        self.audit = audit

    def execute_mission(
        self,
        mission_id: str,
        name: str,
        payload: dict[str, Any],
    ) -> dict[str, Any]:

        # -------------------------
        # 1. CREATE MISSION
        # -------------------------
        mission = self.missions.create(mission_id, name, payload)
        self.audit.record("mission.created", mission)

        # -------------------------
        # 2. POLICY CHECK
        # -------------------------
        policy_ok = self.policies.allowed(PolicyContext(payload))

        if not policy_ok:
            mission.status = "blocked"
            self.audit.record("mission.blocked", mission)

            return {
                "status": "blocked",
                "mission": mission,
            }

        # -------------------------
        # 3. DECISION PHASE
        # -------------------------
        decision = self.decisions.evaluate(DecisionContext(payload))

        self.audit.record("mission.decision", decision)

        # -------------------------
        # 4. UPDATE MISSION
        # -------------------------
        mission.status = "running"

        # -------------------------
        # 5. KNOWLEDGE STORAGE
        # -------------------------
        self.knowledge.remember(
            key=f"mission:{mission_id}",
            value={
                "mission": mission,
                "decision": decision,
            },
            tags=["mission", "execution"],
        )

        self.audit.record("mission.stored", mission)

        return {
            "status": "running",
            "mission": mission,
            "decision": decision,
        }
