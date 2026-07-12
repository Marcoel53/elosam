_runtime = None
_logger = None


def investigation_worker(
    goal,
    context,
):
    return {
        "objective": goal,
        "research_question": (
            "Investigar informações relevantes "
            "para apoiar a missão."
        ),
        "research_scope": [
            "Contexto do objetivo",
            "Alternativas disponíveis",
            "Restrições relevantes",
            "Riscos e oportunidades",
        ],
    }


def evidence_worker(
    goal,
    context,
):
    return {
        "objective": goal,
        "evidence_status": (
            "Estrutura de evidências preparada."
        ),
        "evidence_requirements": [
            "Identificar fatos verificáveis",
            "Separar fatos de hipóteses",
            "Registrar limitações",
            "Priorizar fontes confiáveis",
        ],
    }


def comparison_worker(
    goal,
    context,
):
    return {
        "objective": goal,
        "comparison_status": (
            "Critérios de comparação definidos."
        ),
        "criteria": [
            "Benefício esperado",
            "Custo",
            "Tempo",
            "Risco",
            "Reversibilidade",
        ],
    }


def synthesis_worker(
    goal,
    context,
):
    return {
        "summary": (
            "Plano de pesquisa operacional "
            "consolidado."
        ),
        "actions": [
            {
                "phase": 1,
                "title": (
                    "Definir a pergunta de pesquisa"
                ),
                "action": (
                    "Transformar o objetivo em "
                    "perguntas verificáveis."
                ),
            },
            {
                "phase": 2,
                "title": (
                    "Coletar evidências"
                ),
                "action": (
                    "Reunir informações relevantes "
                    "e separar fatos de hipóteses."
                ),
            },
            {
                "phase": 3,
                "title": (
                    "Comparar alternativas"
                ),
                "action": (
                    "Avaliar opções por benefício, "
                    "custo, tempo e risco."
                ),
            },
            {
                "phase": 4,
                "title": (
                    "Consolidar conclusão"
                ),
                "action": (
                    "Produzir uma síntese útil "
                    "para tomada de decisão."
                ),
            },
        ],
        "next_action": (
            "Executar a pesquisa com fontes reais "
            "quando uma capability de coleta externa "
            "estiver disponível."
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
            "no Brother Pesquisa."
        )

    worker = _runtime.create(
        name=name,
        role=role,
        task=task,
        metadata={
            "brother": "Pesquisa",
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


async def pesquisa_plan(
    resolver,
    goal: str,
):
    workers = []

    context = {
        "goal": goal,
    }

    result, worker = await run_temporary_worker(
        name="Worker Investigação",
        role="investigation",
        task=(
            "Interpretar a missão e definir "
            "o escopo da pesquisa."
        ),
        handler=investigation_worker,
        goal=goal,
        context=context,
    )

    workers.append(worker)

    investigation = result

    context["investigation"] = investigation

    result, worker = await run_temporary_worker(
        name="Worker Evidências",
        role="evidence",
        task=(
            "Definir quais evidências são "
            "necessárias para apoiar a decisão."
        ),
        handler=evidence_worker,
        goal=goal,
        context=context,
    )

    workers.append(worker)

    evidence = result

    context["evidence"] = evidence

    result, worker = await run_temporary_worker(
        name="Worker Comparação",
        role="comparison",
        task=(
            "Estruturar a comparação entre "
            "as alternativas identificadas."
        ),
        handler=comparison_worker,
        goal=goal,
        context=context,
    )

    workers.append(worker)

    comparison = result

    context["comparison"] = comparison

    result, worker = await run_temporary_worker(
        name="Worker Síntese",
        role="synthesis",
        task=(
            "Consolidar o trabalho em "
            "um plano de pesquisa operacional."
        ),
        handler=synthesis_worker,
        goal=goal,
        context=context,
    )

    workers.append(worker)

    synthesis = result

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
        "brother": "Pesquisa",
        "goal": goal,
        "status": "COMPLETED",
        "worker_model": (
            "kernel-worker-runtime-v1"
        ),
        "workers": workers,
        "investigation": investigation,
        "evidence": evidence,
        "comparison": comparison,
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
        "Brother Pesquisa 1.7 ativado "
        "com Worker Runtime nativo."
    )