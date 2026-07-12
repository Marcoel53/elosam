async def activate(resolver, transport, logger):
    logger.info("Brother Comercial ativado.")


def comercial_plan(resolver, goal: str):
    return {
        "brother": "Comercial",
        "goal": goal,
        "status": "PLANNED",
        "plan": [
            "Analisar objetivo",
            "Selecionar capabilities",
            "Executar trabalho",
            "Validar resultado",
        ],
    }
