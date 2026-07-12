async def activate(resolver, transport, logger):
    logger.info("Brother Engenharia ativado.")


def engenharia_plan(resolver, goal: str):
    return {
        "brother": "Engenharia",
        "goal": goal,
        "status": "PLANNED",
        "plan": [
            "Analisar objetivo",
            "Selecionar capabilities",
            "Executar trabalho",
            "Validar resultado",
        ],
    }
