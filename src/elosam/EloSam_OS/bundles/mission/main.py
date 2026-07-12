import time
import uuid


missions = {}


async def activate(resolver, transport, logger):
    logger.info("Mission Engine ativado.")


def mission_define(
    resolver,
    goal: str,
    context: dict | None = None,
):
    mission_id = str(uuid.uuid4())

    missions[mission_id] = {
        "id": mission_id,
        "goal": goal,
        "state": "CREATED",
        "context": context or {},
        "created_at": time.time(),
    }

    return missions[mission_id]


def mission_start(resolver, mission_id: str):
    mission = missions.get(mission_id)

    if mission is None:
        return {
            "success": False,
            "error": "Mission not found",
        }

    mission["state"] = "RUNNING"
    mission["started_at"] = time.time()

    return {
        "success": True,
        "mission": mission,
    }
