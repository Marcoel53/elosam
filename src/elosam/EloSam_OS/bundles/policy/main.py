async def activate(resolver, transport, logger):
    logger.info("Policy Engine ativado.")


def policy_evaluate(resolver, request: dict):
    return {
        "decision": "ALLOW",
        "reason": "Política padrão Beta 1.9",
        "request": request,
    }


