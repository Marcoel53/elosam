"""
WEIGHT MODEL - ELOSam Structural Importance
"""

WEIGHTS = {
    "core": 5.0,
    "runtime": 5.0,
    "contracts": 4.5,
    "engine": 4.0,
    "services": 3.0,
    "application": 3.0,
    "mission": 3.0,
    "default": 1.0,
}


def get_weight(module: str) -> float:
    for key, value in WEIGHTS.items():
        if key in module:
            return value
    return WEIGHTS["default"]
