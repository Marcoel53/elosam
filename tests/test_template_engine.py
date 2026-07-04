from pathlib import Path

from elosam.builder.template_engine import TemplateEngine


def test_render_template() -> None:
    engine = TemplateEngine()

    result = engine.render(
        Path("src/elosam/builder/templates/capability/module.tpl"),
        {
            "module_name": "vision",
            "class_name": "Vision",
        },
    )

    assert "class Vision" in result