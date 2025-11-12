import time

SECONDS_TO_MILLISECONDS = 1000


def ms_since(start: float) -> float:
    return (time.perf_counter() - start) * SECONDS_TO_MILLISECONDS
