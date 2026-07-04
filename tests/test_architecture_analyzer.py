from elosam.core.architecture_analyzer import ArchitectureAnalyzer


def test_architecture_analyzer_detects_missing_layers():
    analyzer = ArchitectureAnalyzer(
        components=[
            "Kernel",
            "EventBus",
            "DecisionEngine",
        ]
    )

    report = analyzer.analyze()

    assert "missing_meta_layer" in report.weak_points
    assert len(report.suggestions) >= 1


def test_architecture_analyzer_complete_system():
    analyzer = ArchitectureAnalyzer(
        components=[
            "Kernel",
            "EventBus",
            "DecisionEngine",
            "PolicyEngine",
            "MetaAgentEngine",
            "AuditLog",
        ]
    )

    report = analyzer.analyze()

    assert "missing_meta_layer" not in report.weak_points
