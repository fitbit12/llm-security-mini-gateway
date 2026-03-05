# latency.py

import time
from typing import Callable, Any, Tuple

def measure_ms(fn: Callable[..., Any], *args, **kwargs) -> Tuple[Any, float]:
    start = time.perf_counter()
    out = fn(*args, **kwargs)
    end = time.perf_counter()
    return out, (end - start) * 1000.0