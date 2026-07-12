async def activate(resolver, transport, logger):
    logger.info("Brother Financeiro ativado.")


def financeiro_plan(resolver, goal: str):
    return {
        "brother": "Financeiro",
        "goal": goal,
        "status": "PLANNED",
        "plan": [
            "Analisar objetivo",
            "Selecionar capabilities",
            "Executar trabalho",
            "Validar resultado",
        ],
    }
