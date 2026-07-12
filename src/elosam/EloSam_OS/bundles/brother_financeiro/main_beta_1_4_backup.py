from datetime import datetime
import re
import uuid


def now():
    return datetime.now().isoformat(
        timespec="seconds"
    )


def create_worker(
    name,
    role,
    task,
):
    return {
        "id": str(uuid.uuid4()),
        "name": name,
        "role": role,
        "task": task,
        "status": "CREATED",
        "created_at": now(),
        "started_at": None,
        "completed_at": None,
        "result": None,
    }


def run_worker(
    worker,
    goal,
    context,
):
    worker["status"] = "RUNNING"
    worker["started_at"] = now()

    role = worker["role"]

    if role == "diagnostic":
        result = diagnostic_worker(
            goal,
            context,
        )

    elif role == "revenue":
        result = revenue_worker(
            goal,
            context,
        )

    elif role == "viability":
        result = viability_worker(
            goal,
            context,
        )

    elif role == "synthesis":
        result = synthesis_worker(
            goal,
            context,
        )

    else:
        result = {
            "summary":
                "Worker sem função registrada."
        }

    worker["result"] = result
    worker["status"] = "COMPLETED"
    worker["completed_at"] = now()

    return result


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

    result = {
        "objective": goal,
        "monthly_target": target,
        "monthly_target_formatted":
            format_brl(target),
        "diagnosis": [],
    }

    result["diagnosis"].append(
        "A missão exige transformar uma meta "
        "financeira em fontes concretas de receita."
    )

    if target:
        result["diagnosis"].append(
            "Meta mensal identificada: "
            + format_brl(target)
            + "."
        )

        result["diagnosis"].append(
            "A meta deve ser dividida entre "
            "fontes de curto, médio e longo prazo."
        )

    else:
        result["diagnosis"].append(
            "Nenhum valor mensal explícito "
            "foi identificado."
        )

    return result


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
            "objective":
                "Gerar caixa no curto prazo "
                "com trabalho ou serviço "
                "de rápida ativação.",
            "time_horizon":
                "curto prazo",
            "risk":
                "baixo a médio",
        },
        {
            "priority": 2,
            "name":
                "Serviços digitais especializados",
            "objective":
                "Monetizar conhecimento técnico "
                "por projetos, automações "
                "ou serviços digitais.",
            "time_horizon":
                "curto a médio prazo",
            "risk":
                "médio",
        },
        {
            "priority": 3,
            "name":
                "Produto digital recorrente",
            "objective":
                "Construir uma fonte de receita "
                "escalável e recorrente.",
            "time_horizon":
                "médio prazo",
            "risk":
                "médio",
        },
    ]

    if target:
        immediate = target * 0.50
        services = target * 0.30
        recurring = target * 0.20

        opportunities[0][
            "target"
        ] = format_brl(immediate)

        opportunities[1][
            "target"
        ] = format_brl(services)

        opportunities[2][
            "target"
        ] = format_brl(recurring)

    return {
        "opportunities": opportunities,
    }


def viability_worker(
    goal,
    context,
):
    target = context.get(
        "monthly_target"
    )

    checks = [
        {
            "criterion":
                "Velocidade para gerar caixa",
            "recommendation":
                "Priorizar primeiro atividades "
                "que possam gerar receita "
                "em dias ou semanas.",
        },
        {
            "criterion":
                "Investimento inicial",
            "recommendation":
                "Evitar comprometer capital alto "
                "antes de validar demanda.",
        },
        {
            "criterion":
                "Risco",
            "recommendation":
                "Combinar uma fonte previsível "
                "com fontes escaláveis.",
        },
        {
            "criterion":
                "Escalabilidade",
            "recommendation":
                "Transformar parte do trabalho "
                "manual em ativos digitais "
                "e automações.",
        },
    ]

    return {
        "target":
            format_brl(target),
        "checks":
            checks,
        "decision":
            "Estratégia híbrida recomendada.",
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
                    "de serviço digital "
                    "com preço e entrega claros.",
            },
            {
                "phase": 3,
                "title":
                    "Construir renda recorrente",
                "target":
                    format_brl(recurring),
                "action":
                    "Desenvolver um ativo digital "
                    "ou automação que possa "
                    "gerar receita repetida.",
            },
        ]

    else:
        actions = [
            {
                "phase": 1,
                "title":
                    "Definir meta financeira",
                "action":
                    "Estabelecer o valor mensal "
                    "necessário.",
            },
            {
                "phase": 2,
                "title":
                    "Ativar receita imediata",
                "action":
                    "Selecionar a alternativa "
                    "de menor tempo para caixa.",
            },
            {
                "phase": 3,
                "title":
                    "Criar receita recorrente",
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


def financeiro_plan(
    resolver,
    goal: str,
):
    workers = []

    context = {
        "goal": goal,
    }

    worker = create_worker(
        name="Worker Diagnóstico",
        role="diagnostic",
        task=(
            "Interpretar a missão e "
            "identificar a meta financeira."
        ),
    )

    workers.append(worker)

    diagnostic = run_worker(
        worker,
        goal,
        context,
    )

    context[
        "monthly_target"
    ] = diagnostic.get(
        "monthly_target"
    )

    worker = create_worker(
        name="Worker Receita",
        role="revenue",
        task=(
            "Criar alternativas de "
            "geração de receita."
        ),
    )

    workers.append(worker)

    revenue = run_worker(
        worker,
        goal,
        context,
    )

    context[
        "revenue"
    ] = revenue

    worker = create_worker(
        name="Worker Viabilidade",
        role="viability",
        task=(
            "Avaliar velocidade, "
            "investimento e risco."
        ),
    )

    workers.append(worker)

    viability = run_worker(
        worker,
        goal,
        context,
    )

    context[
        "viability"
    ] = viability

    worker = create_worker(
        name="Worker Síntese",
        role="synthesis",
        task=(
            "Consolidar o trabalho "
            "dos Workers em um plano."
        ),
    )

    workers.append(worker)

    synthesis = run_worker(
        worker,
        goal,
        context,
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
            "temporary-workers-v1",
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
        "plan": [
            {
                "description":
                    action["title"]
                    + ": "
                    + action["action"]
            }
            for action
            in synthesis["actions"]
        ],
    }


def register(registry):
    registry.register(
        name="financeiro.plan",
        handler=financeiro_plan,
        metadata={
            "bundle":
                "financeiro",
            "version":
                "1.4.0",
            "brother":
                "Financeiro",
            "worker_model":
                "temporary-workers-v1",
        },
    )


async def activate(
    resolver,
    transport,
    logger,
):
    logger.info(
        "Brother Financeiro 1.4 ativado "
        "com Workers temporários."
    )