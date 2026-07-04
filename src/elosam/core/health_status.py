"""
AEGIS CORE Health Status.
"""

from __future__ import annotations

from enum import Enum


class HealthStatus(str, Enum):
    """Represents the runtime health status."""

    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
