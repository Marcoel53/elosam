_runtime = None
_logger = None


def offer_worker(
    goal,
    context,
):
    return {
        "objective": goal,
        "offer": (
            "Oferta comercial estruturada para comunicar "
            "problema, solução, valor e resultado esperado."
        ),
        "elements": [
            "Problema do cliente",
            "Solução oferecida",
            "Benefício principal",
            "Forma de entrega",
            "Próxima ação",
        ],
    }


def customer_worker(
    goal,
    context,
):
    offer = context.get(
        "offer",
        {},
    )

    return {
        "objective": goal,
        "input_offer": offer,
        "customer": (
            "Perfil de cliente prioritário definido "
            "para orientar a abordagem comercial."
        ),
        "criteria": [
            "Possui o problema que a oferta resolve",
            "Reconhece a necessidade",
            "Pode tomar ou influenciar a decisão",
            "Possui potencial real de contratação",
        ],
    }


def conversion_worker(
    goal,
    context,
):
    customer = context.get(
        "customer",
        {},
    )

    return {
        "objective": goal,
        "input_customer": customer,
        "conversion": (
            "Processo de conversão estruturado para "
            "transformar interesse em oportunidade real."
        ),
        "steps": [
            "Identificar potenciais clientes",
            "Iniciar contato",
            "Entender a necessidade",
            "Apresentar a oferta",
            "Registrar resposta",
        ],
    }


def closing_worker(
    goal,
    context,
):
    conversion = context.get(
        "conversion",
        {},
    )

    return {
        "objective": goal,
        "input_conversion": conversion,
        "closing": (
            "Processo de fechamento preparado para "
            "transformar oportunidade em acordo."
        ),
        "steps": [
            "Confirmar necessidade",
            "Alinhar escopo",
            "Apresentar condições",
            "Resolver objeções",
            "Definir próxima ação concreta",
        ],
    }


def synthesis_worker(
    goal,
    context,
):
    return {
        "summary": (
            "Plano comercial operacional consolidado."
        ),
        "actions": [
            {
                "phase": 1,
                "title": "Estruturar oferta",
                "action": (
                    "Definir claramente o problema, "
                    "a solução e o benefício oferecido."
                ),
            },
            {
                "phase": 2,
                "title": "Identificar clientes",
                "action": (
                    "Selecionar clientes com necessidade "
                    "e potencial real de contratação."
                ),
            },
            {
                "phase": 3,
                "title": "Executar abordagem",
                "action": (
                    "Iniciar contatos, entender necessidades "
                    "e apresentar a oferta."
                ),
            },
            {
                "phase": 4,
                "title": "Buscar fechamento",
                "action": (
                    "Transformar oportunidades qualificadas "
                    "em uma próxima ação comercial concreta."
                ),
            },
        ],
        "next_action": (
            "Executar a primeira abordagem comercial "
            "e registrar respostas e conversões reais."
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
            "no Brother Comercial."
        )

    worker = _runtime.create(
        name=name,
        role=role,
        task=task,
        metadata={
            "brother": "Comercial",
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


async def comercial_plan(
    resolver,
    goal: str,
):
    workers = []

    context = {
        "goal": goal,
    }

    result, worker = await run_temporary_worker(
        name="Worker Oferta",
        role="offer",
        task=(
            "Interpretar a missão e estruturar "
            "a oferta comercial."
        ),
        handler=offer_worker,
        goal=goal,
        context=context,
    )

    workers.append(worker)

    offer = result
    context["offer"] = offer

    result, worker = await run_temporary_worker(
        name="Worker Cliente",
        role="customer",
        task=(
            "Identificar o perfil de cliente "
            "prioritário para a oferta."
        ),
        handler=customer_worker,
        goal=goal,
        context=context,
    )

    workers.append(worker)

    customer = result
    context["customer"] = customer

    result, worker = await run_temporary_worker(
        name="Worker Conversão",
        role="conversion",
        task=(
            "Definir o processo para transformar "
            "interesse em oportunidade comercial."
        ),
        handler=conversion_worker,
        goal=goal,
        context=context,
    )

    workers.append(worker)

    conversion = result
    context["conversion"] = conversion

    result, worker = await run_temporary_worker(
        name="Worker Fechamento",
        role="closing",
        task=(
            "Definir o processo de negociação "
            "e fechamento comercial."
        ),
        handler=closing_worker,
        goal=goal,
        context=context,
    )

    workers.append(worker)

    closing = result
    context["closing"] = closing

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
        "brother": "Comercial",
        "goal": goal,
        "status": "COMPLETED",
        "worker_model": (
            "kernel-worker-runtime-v1"
        ),
        "workers": workers,
        "offer": offer,
        "customer": customer,
        "conversion": conversion,
        "closing": closing,
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
        "Brother Comercial 1.9 ativado "
        "com Worker Runtime nativo."
    )
