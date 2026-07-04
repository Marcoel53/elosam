from elosam.core.healing_loop_engine import HealingLoopEngine


def test_healing_loop_runs():
    engine = HealingLoopEngine()

    trace = [
        {"layer": "agent", "event": "execute", "data": {}},
        {"layer": "meta", "event": "evolve", "data": {}},
        {"layer": "decision", "event": "evaluate", "data": {}},
    ]

    result = engine.run_cycle(trace)

    assert "diagnostic" in result
    assert "generated_patches" in result


def test_healing_loop_empty_trace():
    engine = HealingLoopEngine()

    result = engine.run_cycle([])

    assert isinstance(result, dict)
