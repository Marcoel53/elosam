from pathlib import Path

ROOT = Path.cwd()
APP = ROOT / "elosam" / "app.py"

if not APP.exists():
    raise FileNotFoundError(
        "Arquivo elosam/app.py não encontrado."
    )

# Backup integral da Beta 1.2
backup_dir = ROOT / "backup_beta_1_2"
backup_dir.mkdir(exist_ok=True)

backup_file = backup_dir / "app.py"

backup_file.write_text(
    APP.read_text(encoding="utf-8"),
    encoding="utf-8",
)

text = APP.read_text(encoding="utf-8")


OLD = r'''                    card.appendChild(name);
                    card.appendChild(meta);

                    resultsElement.appendChild(
                        card
                    );'''


NEW = r'''                    card.appendChild(name);
                    card.appendChild(meta);

                    if (
                        item.success
                        && item.result
                    ) {
                        const output =
                            document.createElement(
                                "div"
                            );

                        output.className =
                            "brother-output";

                        const title =
                            document.createElement(
                                "div"
                            );

                        title.className =
                            "brother-output-title";

                        title.textContent =
                            "Resultado do trabalho";

                        output.appendChild(title);

                        if (
                            item.result.plan
                            && Array.isArray(
                                item.result.plan
                            )
                        ) {
                            const list =
                                document.createElement(
                                    "ol"
                                );

                            item.result.plan.forEach(
                                step => {
                                    const li =
                                        document.createElement(
                                            "li"
                                        );

                                    if (
                                        typeof step
                                        === "string"
                                    ) {
                                        li.textContent =
                                            step;
                                    } else {
                                        li.textContent =
                                            step.description
                                            || JSON.stringify(
                                                step
                                            );
                                    }

                                    list.appendChild(li);
                                }
                            );

                            output.appendChild(list);

                        } else {
                            const pre =
                                document.createElement(
                                    "pre"
                                );

                            pre.textContent =
                                JSON.stringify(
                                    item.result,
                                    null,
                                    2
                                );

                            output.appendChild(pre);
                        }

                        card.appendChild(output);
                    }

                    resultsElement.appendChild(
                        card
                    );'''


if OLD not in text:
    raise RuntimeError(
        "Bloco de resultados da Beta 1.2 "
        "não foi encontrado. "
        "Nenhuma alteração foi aplicada."
    )


text = text.replace(
    OLD,
    NEW,
    1,
)


CSS_MARKER = r'''        .success {
            color: var(--green);
            font-weight: 800;
        }'''


CSS_NEW = r'''        .brother-output {
            margin-top: 16px;
            padding: 16px;
            border-radius: 12px;
            background: var(--surface-3);
            border: 1px solid var(--border);
        }

        .brother-output-title {
            margin-bottom: 10px;
            color: var(--blue-light);
            font-size: 13px;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        .brother-output ol {
            margin:
                10px
                0
                0
                22px;
            padding: 0;
        }

        .brother-output li {
            margin: 8px 0;
            line-height: 1.5;
        }

        .brother-output pre {
            margin: 10px 0 0;
            white-space: pre-wrap;
            overflow-wrap: anywhere;
            color: #cbd8eb;
            font-family:
                Consolas,
                "Courier New",
                monospace;
            font-size: 13px;
            line-height: 1.5;
        }

        .success {
            color: var(--green);
            font-weight: 800;
        }'''


if CSS_MARKER not in text:
    raise RuntimeError(
        "Ponto de inserção do CSS não encontrado."
    )


text = text.replace(
    CSS_MARKER,
    CSS_NEW,
    1,
)


text = text.replace(
    "Mission Control — Beta 1.2",
    "Mission Control — Beta 1.3",
    1,
)

text = text.replace(
    'version="1.2.0-beta"',
    'version="1.3.0-beta"',
    1,
)


APP.write_text(
    text,
    encoding="utf-8",
)


print("=" * 60)
print("ELOSAM OS BETA 1.3 INSTALADO")
print("=" * 60)
print()
print("Resultado dos Brothers agora aparece na interface.")
print()
print("Backup da Beta 1.2:")
print(backup_file)