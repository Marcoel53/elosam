import time
import uuid


approvals = {}


async def activate(resolver, transport, logger):
    logger.info("Approval Engine ativado.")


def approval_request(
    resolver,
    mission_id: str,
    step_id: str,
    context: dict | None = None,
):
    approval_id = str(uuid.uuid4())

    approvals[approval_id] = {
        "id": approval_id,
        "mission_id": mission_id,
        "step_id": step_id,
        "context": context or {},
        "status": "PENDING",
        "created_at": time.time(),
    }

    return approvals[approval_id]
