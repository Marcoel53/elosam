from pathlib import Path

ROOT = Path.cwd()

APP = ROOT / "elosam" / "app.py"
MAESTRO = ROOT / "bundles" / "maestro" / "main.py"

# Backup
backup = ROOT / "backup_beta_1_1"
backup.mkdir(exist_ok=True)

(backup / "app.py").write_text(
    APP.read_text(encoding="utf-8"),
    encoding="utf-8",
)

(backup / "maestro_main.py").write_text(
    MAESTRO.read_text(encoding="utf-8"),
    encoding="utf-8",
)


MAESTRO_CODE = r'''
async def activate(resolver, transport, logger):
    logger.info("Maestro 1.2 ativado.")


ROUTING_RULES = [
    {
        "brother": "Financeiro",
        "capability": "financeiro.plan",
        "keywords": [
            "renda",
            "dinheiro",
            "financeiro",
            "receita",
            "custo",
            "lucro",
            "economia",
            "dívida",
            "dívidas",
            "orçamento",
            "investimento",
        ],
    },
    {
        "brother": "Pesquisa",
        "capability": "pesquisa.plan",
        "keywords": [
            "pesquisa",
            "pesquisar",
            "descobrir",
            "comparar",
            "mercado",
            "oportunidade",
            "oportunidades",
            "tecnologia",
            "tendência",
        ],
    },
    {
        "brother": "Comercial",
        "capability": "comercial.plan",
        "keywords": [
            "vender",
            "venda",
            "vendas",
            "cliente",
            "clientes",
            "comercial",
            "monetizar",
            "monetização",
            "negócio",
            "negócios",
        ],
    },
    {
        "brother": "Marketing",
        "capability": "marketing.plan",
        "keywords": [
            "marketing",
            "divulgar",
            "divulgação",
            "público",
            "audiência",
            "marca",
            "campanha",
            "conteúdo",
        ],
    },
    {
        "brother": "Engenharia",
        "capability": "engenharia.plan",
        "keywords": [
            "código",
            "programar",
            "software",
            "sistema",
            "aplicativo",
            "app",
            "api",
            "automação",
            "automatizar",
            "desenvolver",
            "construir",
        ],
    },
]


def select_brothers(goal):
    normalized = goal.lower()

    selected = []

    for rule in ROUTING_RULES:
        matches = [
            keyword
            for keyword in rule["keywords"]
            if keyword in normalized
        ]

        if matches:
            selected.append(
                {
                    "brother": rule["brother"],
                    "capability": rule["capability"],
                    "matches": matches,
                    "score": len(matches),
                }
            )

    selected.sort(
        key=lambda item: item["score"],
        reverse=True,
    )

    if not selected:
        selected = [
            {
                "brother": "Pesquisa",
                "capability": "pesquisa.plan",
                "matches": ["fallback"],
                "score": 1,
            }
        ]

    return selected


def maestro_plan(resolver, goal: str):
    selected = select_brothers(goal)

    return {
        "goal": goal,
        "status": "ROUTED",
        "strategy": "deterministic-routing-v1",
        "brothers": selected,
        "plan": [
            {
                "id": "analyze",
                "description": "Analisar objetivo",
                "depends": [],
            },
            {
                "id": "route",
                "description": (
                    "Selecionar Brothers responsáveis"
                ),
                "depends": ["analyze"],
            },
            {
                "id": "execute",
                "description": (
                    "Executar capabilities selecionadas"
                ),
                "depends": ["route"],
            },
            {
                "id": "validate",
                "description": "Validar resultados",
                "depends": ["execute"],
            },
        ],
    }
'''

MAESTRO.write_text(
    MAESTRO_CODE,
    encoding="utf-8",
)


app_text = APP.read_text(encoding="utf-8")

old_block = '''    mission["plan"] = plan

    add_event(
        mission,
        "maestro.completed",
        "Plano criado pelo Maestro.",
    )

    mission["status"] = "PLANNED"

    add_event(
        mission,
        "mission.planned",
        "Missão planejada com sucesso.",
    )

    return mission
'''

new_block = '''    mission["plan"] = plan
    mission["brothers"] = plan.get(
        "brothers",
        [],
    )
    mission["results"] = []

    add_event(
        mission,
        "maestro.completed",
        "Plano e roteamento criados pelo Maestro.",
    )

    mission["status"] = "ROUTING"

    for brother in mission["brothers"]:
        brother_name = brother["brother"]
        capability = brother["capability"]

        add_event(
            mission,
            "brother.selected",
            f"Brother {brother_name} selecionado.",
        )

        mission["status"] = "EXECUTING"

        add_event(
            mission,
            "brother.started",
            (
                f"Brother {brother_name} "
                "iniciou o trabalho."
            ),
        )

        try:
            result = await kernel.resolver.execute(
                capability,
                goal=goal,
            )

            mission["results"].append(
                {
                    "brother": brother_name,
                    "capability": capability,
                    "success": True,
                    "result": result,
                }
            )

            add_event(
                mission,
                "brother.completed",
                (
                    f"Brother {brother_name} "
                    "concluiu o trabalho."
                ),
            )

        except Exception as error:
            mission["results"].append(
                {
                    "brother": brother_name,
                    "capability": capability,
                    "success": False,
                    "error": str(error),
                }
            )

            add_event(
                mission,
                "brother.failed",
                (
                    f"Brother {brother_name} "
                    f"falhou: {error}"
                ),
            )

    mission["status"] = "COMPLETED"

    add_event(
        mission,
        "mission.completed",
        "Missão executada pelos Brothers.",
    )

    return mission
'''

if old_block not in app_text:
    raise RuntimeError(
        "Bloco Beta 1.1 não encontrado em elosam/app.py. "
        "Nenhuma alteração foi aplicada ao app.py."
    )

app_text = app_text.replace(
    old_block,
    new_block,
    1,
)

# Adiciona área visual de resultados.
old_html = '''            <h3>Linha do Tempo</h3>

            <div id="events"></div>
'''

new_html = '''            <h3>Brothers Executados</h3>

            <div id="results"></div>

            <h3>Linha do Tempo</h3>

            <div id="events"></div>
'''

if old_html not in app_text:
    raise RuntimeError(
        "Área da Timeline não encontrada."
    )

app_text = app_text.replace(
    old_html,
    new_html,
    1,
)


old_js = '''            const events =
                document.getElementById(
                    "events"
                );

            events.innerHTML = "";
'''

new_js = '''            const results =
                document.getElementById(
                    "results"
                );

            results.innerHTML = "";

            if (mission.results) {
                mission.results.forEach(
                    item => {
                        const div =
                            document.createElement(
                                "div"
                            );

                        div.className =
                            "plan-step";

                        const status =
                            item.success
                            ? "CONCLUÍDO"
                            : "FALHOU";

                        div.innerHTML =
                            "<strong>Brother "
                            + item.brother
                            + "</strong><br>"
                            + item.capability
                            + " — "
                            + status;

                        results.appendChild(
                            div
                        );
                    }
                );
            }

            const events =
                document.getElementById(
                    "events"
                );

            events.innerHTML = "";
'''

if old_js not in app_text:
    raise RuntimeError(
        "Bloco JavaScript não encontrado."
    )

app_text = app_text.replace(
    old_js,
    new_js,
    1,
)

APP.write_text(
    app_text,
    encoding="utf-8",
)

print("=" * 60)
print("ELOSAM OS BETA 1.2 INSTALADO")
print("=" * 60)
print()
print("Maestro: roteamento deterministico ativo")
print("Brothers: execucao de capabilities ativa")
print("Mission Control: resultados adicionados")
print()
print("Backup da Beta 1.1:")
print(backup)