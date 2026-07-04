"""
Architecture Manifest

Defines the constitutional layers of EloSam.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ArchitectureLayer:
    name: str
    description: str


ARCHITECTURE_LAYERS = (
    ArchitectureLayer(
        "application",
        "Public API",
    ),
    ArchitectureLayer(
        "core",
        "Runtime infrastructure",
    ),
    ArchitectureLayer(
        "capabilities",
        "Business capabilities",
    ),
    ArchitectureLayer(
        "inspector",
        "Architecture governance",
    ),
)