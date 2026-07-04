from __future__ import annotations

from typing import Any

from elosam.core.knowledge_engine import KnowledgeEngine
from elosam.core.audit import AuditLog


class KnowledgeMixin:
    def __init__(
        self,
        knowledge: KnowledgeEngine | None = None,
        audit: AuditLog | None = None,
    ) -> None:
        self._knowledge = knowledge
        self._audit = audit

    def store_decision(self, key: str, data: Any) -> None:
        if self._knowledge:
            self._knowledge.remember(
                key=key,
                value=data,
                tags=["decision"]
            )

        if self._audit:
            self._audit.record("knowledge.stored", {"key": key})
