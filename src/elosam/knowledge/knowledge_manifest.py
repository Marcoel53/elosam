"""
Knowledge Manifest

Defines the official knowledge sources
recognized by EloSam.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class KnowledgeSource:
    name: str
    description: str


KNOWLEDGE_SOURCES = (
    KnowledgeSource(
        "constitution",
        "Architectural constitution",
    ),
    KnowledgeSource(
        "adr",
        "Architecture Decision Records",
    ),
    KnowledgeSource(
        "rfc",
        "Requests For Comments",
    ),
    KnowledgeSource(
        "code",
        "Python source code",
    ),
    KnowledgeSource(
        "tests",
        "Test suite",
    ),
)