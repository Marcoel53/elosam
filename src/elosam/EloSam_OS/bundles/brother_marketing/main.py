_runtime = None
_logger = None


def audience_worker(
    goal,
    context,
):
    return {
        "objective": goal,
        "audience": (
            "Público prioritário identificado "
            "para orientar a estratégia de marketing."
        ),
        "questions": [
            "Quem possui o problema que a missão resolve?",
            "Qual necessidade é mais urgente?",
            "Onde esse público pode ser alcançado?",
            "Qual resultado esse público valoriza?",
        ],
    }


def positioning_worker(
    goal,
    context,
):
    audience = context.get(
        "audience",
        {},
    )

    return {
        "objective": goal,
        "input_audience": audience,
        "positioning": (
            "Posicionamento preparado para comunicar "
            "valor de forma simples e objetiva."
        ),
        "principles": [
            "Mensagem clara",
            "Problema específico",
            "Benefício compreensível",
            "Diferencial verificável",
            "Promessa realista",
        ],
    }


def strategy_worker(
    goal,
    context,
):
    positioning = context.get(
        "positioning",
        {},
    )

    return {
        "objective": goal,
        "input_positioning": positioning,
        "strategy": (
            "Estratégia de aquisição e comunicação "
            "estruturada para execução."
        ),
        "channels": [
            "Conteúdo",
            "Relacionamento direto",
            "Comunidades",
            "Parcerias",
        ],
    }


def campaign_worker(
    goal,
    context,
):
    strategy = context.get(
        "strategy",
        {},
    )

    return {
        "objective": goal,
        "input_strategy": strategy,
        "campaign": (
            "Campanha inicial preparada para testar "
            "mensagem, canal e resposta do público."
        ),
        "steps": [
            "Criar mensagem principal",
            "Selecionar canal inicial",
            "Publicar ou distribuir a oferta",
            "Medir respostas",
            "Ajustar a comunicação",
        ],
    }


def synthesis_worker(
    goal,
    context,
):
    return {
        "summary": (
            "Plano operacional de marketing "
            "consolidado."
        ),
        "actions": [
            {
                "phase": 1,
                "title": "Definir público",
                "action": (
                    "Identificar o público com maior "
                    "necessidade relacionada à missão."
                ),
            },
            {
                "phase": 2,
                "title": "Definir posicionamento",
                "action": (
                    "Criar uma mensagem clara baseada "
                    "no problema e no benefício."
                ),
            },
            {
                "phase": 3,
                "title": "Selecionar canais",
                "action": (
                    "Escolher os canais com menor custo "
                    "e maior acesso ao público."
                ),
            },
            {
                "phase": 4,
                "title": "Executar campanha",
                "action": (
                    "Testar a mensagem, medir respostas "
                    "e melhorar a estratégia."
                ),
            },
        ],
        "next_action": (
            "Executar o primeiro teste de comunicação "
            "e registrar os resultados reais."
        ),
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
            "no Brother Marketing."
        )

    worker = _runtime.create(
        name=name,
        role=role,
        task=task,
        metadata={
            "brother": "Marketing",
            "temporary": True,
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


async def marketing_plan(
    resolver,
    goal: str,
):
    workers = []

    context = {
        "goal": goal,
    }

    result, worker = await run_temporary_worker(
        name="Worker Público",
        role="audience",
        task=(
            "Interpretar a missão e identificar "
            "o público prioritário."
        ),
        handler=audience_worker,
        goal=goal,
        context=context,
    )

    workers.append(worker)

    audience = result
    context["audience"] = audience

    result, worker = await run_temporary_worker(
        name="Worker Posicionamento",
        role="positioning",
        task=(
            "Definir como a proposta deve ser "
            "comunicada ao público."
        ),
        handler=positioning_worker,
        goal=goal,
        context=context,
    )

    workers.append(worker)

    positioning = result
    context["positioning"] = positioning

    result, worker = await run_temporary_worker(
        name="Worker Estratégia",
        role="strategy",
        task=(
            "Selecionar a estratégia e os canais "
            "para alcançar o público."
        ),
        handler=strategy_worker,
        goal=goal,
        context=context,
    )

    workers.append(worker)

    strategy = result
    context["strategy"] = strategy

    result, worker = await run_temporary_worker(
        name="Worker Campanha",
        role="campaign",
        task=(
            "Criar o plano inicial de campanha "
            "e definir como medir resultados."
        ),
        handler=campaign_worker,
        goal=goal,
        context=context,
    )

    workers.append(worker)

    campaign = result
    context["campaign"] = campaign

    synthesis = synthesis_worker(
        goal,
        context,
    )

    plan = []

    for action in synthesis["actions"]:
        description = (
            f"{action['title']}: "
            f"{action['action']}"
        )

        plan.append(
            {
                "description": description,
            }
        )

    return {
        "type": "brother_execution",
        "brother": "Marketing",
        "goal": goal,
        "status": "COMPLETED",
        "worker_model": (
            "kernel-worker-runtime-v1"
        ),
        "workers": workers,
        "audience": audience,
        "positioning": positioning,
        "strategy": strategy,
        "campaign": campaign,
        "synthesis": synthesis,
        "plan": plan,
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
        "Brother Marketing 1.8 ativado "
        "com Worker Runtime nativo."
    )
