import re


_runtime = None
_logger = None


def extract_monthly_target(goal):
    text = goal.lower()

    patterns = [
        r"r\$\s*([\d\.\,]+)",
        r"([\d\.\,]+)\s*reais",
    ]

    for pattern in patterns:
        match = re.search(
            pattern,
            text,
        )

        if match:
            raw = match.group(1)

            raw = raw.replace(
                ".",
                "",
            )

            raw = raw.replace(
                ",",
                ".",
            )

            try:
                return float(raw)

            except ValueError:
                pass

    return None


def format_brl(value):
    if value is None:
        return "não identificada"

    formatted = (
        f"{value:,.2f}"
        .replace(",", "X")
        .replace(".", ",")
        .replace("X", ".")
    )

    return f"R$ {formatted}"


def diagnostic_worker(
    goal,
    context,
):
    target = extract_monthly_target(
        goal
    )

    return {
        "objective": goal,
        "monthly_target": target,
        "monthly_target_formatted":
            format_brl(target),
        "diagnosis": [
            (
                "Meta financeira identificada: "
                + format_brl(target)
                + "."
            )
            if target
            else (
                "Nenhum valor mensal explícito "
                "foi identificado."
            )
        ],
    }


def revenue_worker(
    goal,
    context,
):
    target = context.get(
        "monthly_target"
    )

    opportunities = [
        {
            "priority": 1,
            "name":
                "Receita operacional imediata",
            "share": 0.50,
        },
        {
            "priority": 2,
            "name":
                "Serviços digitais especializados",
            "share": 0.30,
        },
        {
            "priority": 3,
            "name":
                "Produto digital recorrente",
            "share": 0.20,
        },
    ]

    for opportunity in opportunities:
        if target:
            opportunity["target"] = (
                format_brl(
                    target
                    * opportunity["share"]
                )
            )

    return {
        "opportunities": opportunities,
    }


def viability_worker(
    goal,
    context,
):
    return {
        "decision":
            "Estratégia híbrida recomendada.",
        "criteria": [
            "Velocidade para gerar caixa",
            "Baixo investimento inicial",
            "Controle de risco",
            "Potencial de recorrência",
        ],
    }


def synthesis_worker(
    goal,
    context,
):
    target = context.get(
        "monthly_target"
    )

    if target:
        immediate = target * 0.50
        services = target * 0.30
        recurring = target * 0.20

        actions = [
            {
                "phase": 1,
                "title":
                    "Gerar caixa imediatamente",
                "target":
                    format_brl(immediate),
                "action":
                    "Ativar a fonte de receita "
                    "mais rápida disponível "
                    "e medir o resultado diário.",
            },
            {
                "phase": 2,
                "title":
                    "Monetizar capacidade técnica",
                "target":
                    format_brl(services),
                "action":
                    "Criar uma oferta simples "
                    "de serviço digital com "
                    "preço e entrega claros.",
            },
            {
                "phase": 3,
                "title":
                    "Construir renda recorrente",
                "target":
                    format_brl(recurring),
                "action":
                    "Desenvolver um ativo digital "
                    "ou automação que gere "
                    "receita repetida.",
            },
        ]

    else:
        actions = [
            {
                "phase": 1,
                "title":
                    "Definir meta financeira",
                "target": None,
                "action":
                    "Estabelecer o valor mensal "
                    "necessário.",
            },
            {
                "phase": 2,
                "title":
                    "Ativar receita imediata",
                "target": None,
                "action":
                    "Selecionar a alternativa "
                    "de menor tempo para caixa.",
            },
            {
                "phase": 3,
                "title":
                    "Criar receita recorrente",
                "target": None,
                "action":
                    "Construir uma fonte "
                    "escalável.",
            },
        ]

    return {
        "summary":
            "Plano financeiro operacional "
            "consolidado.",
        "monthly_target":
            format_brl(target),
        "actions":
            actions,
        "next_action":
            "Executar a Fase 1 e registrar "
            "receita, custo e resultado real.",
    }


async def run_temporary_worker(
    *,
    name,
    role,
    task,
    handler,
    goal,
    context,
):
    if _runtime is None:
        raise RuntimeError(
            "Worker Runtime não foi injetado "
            "no Brother Financeiro."
        )

    worker = _runtime.create(
        name=name,
        role=role,
        task=task,
        metadata={
            "brother":
                "Financeiro",
            "temporary":
                True,
        },
    )

    try:
        result = await _runtime.execute(
            worker,
            handler,
            goal,
            context,
        )

        snapshot = dict(worker)

        snapshot["events"] = [
            dict(event)
            for event in worker["events"]
        ]

        return result, snapshot

    finally:
        _runtime.destroy(
            worker["id"]
        )


async def financeiro_plan(
    resolver,
    goal: str,
):
    workers = []

    context = {
        "goal": goal,
    }

    result, worker = (
        await run_temporary_worker(
            name="Worker Diagnóstico",
            role="diagnostic",
            task=(
                "Interpretar a missão e "
                "identificar a meta financeira."
            ),
            handler=diagnostic_worker,
            goal=goal,
            context=context,
        )
    )

    workers.append(worker)

    diagnostic = result

    context["monthly_target"] = (
        diagnostic.get(
            "monthly_target"
        )
    )

    result, worker = (
        await run_temporary_worker(
            name="Worker Receita",
            role="revenue",
            task=(
                "Criar alternativas de "
                "geração de receita."
            ),
            handler=revenue_worker,
            goal=goal,
            context=context,
        )
    )

    workers.append(worker)

    revenue = result

    context["revenue"] = revenue

    result, worker = (
        await run_temporary_worker(
            name="Worker Viabilidade",
            role="viability",
            task=(
                "Avaliar velocidade, "
                "investimento e risco."
            ),
            handler=viability_worker,
            goal=goal,
            context=context,
        )
    )

    workers.append(worker)

    viability = result

    context["viability"] = viability

    result, worker = (
        await run_temporary_worker(
            name="Worker Síntese",
            role="synthesis",
            task=(
                "Consolidar o trabalho "
                "em um plano operacional."
            ),
            handler=synthesis_worker,
            goal=goal,
            context=context,
        )
    )

    workers.append(worker)

    synthesis = result

    plan = []

    for action in synthesis["actions"]:
        target = action.get(
            "target"
        )

        if target:
            description = (
                f"{action['title']} "
                f"({target}): "
                f"{action['action']}"
            )
        else:
            description = (
                f"{action['title']}: "
                f"{action['action']}"
            )

        plan.append(
            {
                "description":
                    description
            }
        )

    return {
        "type":
            "brother_execution",
        "brother":
            "Financeiro",
        "goal":
            goal,
        "status":
            "COMPLETED",
        "worker_model":
            "kernel-worker-runtime-v1",
        "workers":
            workers,
        "diagnostic":
            diagnostic,
        "revenue":
            revenue,
        "viability":
            viability,
        "synthesis":
            synthesis,
        "plan":
            plan,
    }


async def activate(
    resolver,
    transport,
    logger,
    worker_runtime,
):
    global _runtime
    global _logger

    _runtime = worker_runtime
    _logger = logger

    if _runtime is None:
        raise RuntimeError(
            "Worker Runtime indisponível."
        )

    logger.info(
        "Brother Financeiro 1.5 ativado "
        "com Worker Runtime nativo."
    )