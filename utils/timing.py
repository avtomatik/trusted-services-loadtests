import time

SECONDS_TO_MILLISECONDS = 1000


def get_run_time_in_ms(start: float) -> float:
    return (time.perf_counter() - start) * SECONDS_TO_MILLISECONDS
