from pathlib import Path

from elosam.builder.renderer import Renderer


def test_renderer_renders_template() -> None:
    renderer = Renderer()

    text = renderer.render(
        Path("src/elosam/builder/templates/capability/module.tpl"),
        {
            "module_name": "vision",
            "class_name": "Vision",
        },
    )

    assert "class Vision" in text