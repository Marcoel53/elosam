async def activate(resolver, transport, logger):
    logger.info("Brother Pesquisa ativado.")


def pesquisa_plan(resolver, goal: str):
    return {
        "brother": "Pesquisa",
        "goal": goal,
        "status": "PLANNED",
        "plan": [
            "Analisar objetivo",
            "Selecionar capabilities",
            "Executar trabalho",
            "Validar resultado",
        ],
    }
