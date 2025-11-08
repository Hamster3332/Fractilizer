import math

def lerp_pos(pos1: tuple[float, float], pos2: tuple[float, float], lerp_val: float) -> tuple[float, float]:
    return (pos1[0] + lerp_val * (pos2[0] - pos1[0]), pos1[1] + lerp_val * (pos2[1] - pos1[1]))

def lerp(current: float, goal: float, lerp_val: float) -> float:
    return current + (goal - current) * lerp_val

def easeInOutSine(x: float) -> float:
    if x <= 0:
        return 0
    return -(math.cos(math.pi * x) - 1) / 2

def f(x : float) -> float:
    return math.pow(x, 2) * (3 - 2 * x)

def easeInCubic(x: float) -> float:
    return x * x * x

def easeOutCubic(x: float) -> float:
    return 1 - math.pow(1 - x, 3)