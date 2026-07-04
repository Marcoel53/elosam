from __future__ import annotations

from dataclasses import dataclass

from .models import BuildSpecification


@dataclass(slots=True, frozen=True)
class BuildPlan:
    """
    Internal execution plan produced from a build specification.
    """

    specification: BuildSpecification


class Planner:
    """
    Converts a build specification into an execution plan.
    """

    def create_plan(
        self,
        specification: BuildSpecification,
    ) -> BuildPlan:
        return BuildPlan(
            specification=specification,
        )