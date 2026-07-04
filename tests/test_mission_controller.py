from elosam.mission import Mission
from elosam.enums import MissionStatus
from elosam.mission_controller import MissionController


def test_controller_executes_mission():
    mission = Mission(name="Test")

    controller = MissionController()

    result = controller.execute(mission)

    assert result.status == MissionStatus.COMPLETED
    assert result.result == "SUCCESS"
