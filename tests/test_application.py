from elosam.application import EloSamApplication
from elosam.lifecycle import LifecycleState


def test_application_starts_ready():
    app = EloSamApplication()

    assert app.state == LifecycleState.CREATED

    app.start()

    assert app.state == LifecycleState.READY
