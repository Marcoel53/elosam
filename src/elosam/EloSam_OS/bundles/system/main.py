import platform
import socket
import time


async def activate(resolver, transport, logger):
    logger.info("System Bundle ativado.")


def system_info(resolver):
    return {
        "hostname": socket.gethostname(),
        "platform": platform.system(),
        "platform_version": platform.version(),
        "machine": platform.machine(),
    }


def system_time(resolver):
    return {
        "timestamp": time.time(),
    }
