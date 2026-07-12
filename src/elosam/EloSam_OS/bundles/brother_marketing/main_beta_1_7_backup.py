async def activate(resolver, transport, logger):
    logger.info("Brother Marketing ativado.")


def marketing_plan(resolver, goal: str):
    return {
        "brother": "Marketing",
        "goal": goal,
        "status": "PLANNED",
        "plan": [
            "Analisar objetivo",
            "Selecionar capabilities",
            "Executar trabalho",
            "Validar resultado",
        ],
    }
