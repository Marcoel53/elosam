from .mission import Mission
from .enums import MissionStatus


class MissionController:
    """Executes missions."""

    def execute(self, mission: Mission) -> Mission:
        mission.status = MissionStatus.RUNNING

        mission.result = "SUCCESS"

        mission.status = MissionStatus.COMPLETED

        return mission
