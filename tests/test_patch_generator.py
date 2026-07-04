from elosam.core.architecture_analyzer import ArchitectureAnalyzer
from elosam.core.patch_generator import PatchGenerator


def test_patch_generator_creates_fixes():
    analyzer = ArchitectureAnalyzer(
        components=["Kernel", "EventBus"]
    )

    report = analyzer.analyze()

    generator = PatchGenerator(report)

    patches = generator.generate()

    assert len(patches) >= 1
    assert any("MetaAgentEngine" in p.change or "meta" in p.change.lower() for p in patches)


def test_patch_generator_empty_system():
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
    generator = PatchGenerator(report)

    patches = generator.generate()

    assert patches == []
