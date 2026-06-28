from elosam.mission import Mission
from elosam.enums import MissionStatus


def test_mission_is_created():
    mission = Mission(
        name="First Mission",
        objective="Validation"
    )

    assert mission.status == MissionStatus.CREATED
    assert mission.result is None
