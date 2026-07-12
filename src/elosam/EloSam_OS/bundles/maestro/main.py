
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
