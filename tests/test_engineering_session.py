from elosam.core.engineering_session import EngineeringSession


def test_session_creation() -> None:
    session = EngineeringSession(
        mission_id="ENG-001",
        name="Session",
        payload={
            "goal": "test",
        },
    )

    assert session.completed is False

    assert session.events == []

    assert session.result is None