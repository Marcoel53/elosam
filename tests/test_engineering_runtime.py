from elosam.core.engineering_runtime import EngineeringRuntime


def test_runtime_creation() -> None:
    runtime = EngineeringRuntime()

    assert runtime.healthy()

    assert runtime.events is not None
    assert runtime.pipeline is not None
    assert runtime.decisions is not None
    assert runtime.missions is not None