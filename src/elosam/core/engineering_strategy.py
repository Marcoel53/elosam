"""
Engineering Strategy

Defines the execution sequence used by the
Engineering Pipeline.
"""

from __future__ import annotations

from elosam.core.engineering_pipeline import PipelineStage


class DefaultEngineeringStrategy:
    """
    Default constitutional engineering flow.
    """

    def stages(self) -> list[PipelineStage]:
        return [
            PipelineStage.CREATED,
            PipelineStage.PLANNING,
            PipelineStage.ARCHITECTURE,
            PipelineStage.DECISION,
            PipelineStage.CAPABILITY,
            PipelineStage.EXECUTION,
            PipelineStage.VALIDATION,
            PipelineStage.COMPLETED,
        ]