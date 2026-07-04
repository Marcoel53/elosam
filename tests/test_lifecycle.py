from elosam.core.lifecycle import Lifecycle
from elosam.core.lifecycle_state import LifecycleState


def test_initial_state() -> None:
    lifecycle = Lifecycle()

    assert lifecycle.state is LifecycleState.CREATED


def test_running_state() -> None:
    lifecycle = Lifecycle()

    lifecycle.initializing()
    lifecycle.initialized()
    lifecycle.starting()
    lifecycle.running()

    assert lifecycle.state is LifecycleState.RUNNING


def test_stopped_state() -> None:
    lifecycle = Lifecycle()

    lifecycle.stopping()
    lifecycle.stopped()

    assert lifecycle.state is LifecycleState.STOPPED


def test_failed_state() -> None:
    lifecycle = Lifecycle()

    lifecycle.failed()

    assert lifecycle.state is LifecycleState.FAILED


def test_reset() -> None:
    lifecycle = Lifecycle()

    lifecycle.failed()
    lifecycle.reset()

    assert lifecycle.state is LifecycleState.CREATED
