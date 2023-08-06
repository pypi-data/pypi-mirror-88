from contextlib import contextmanager
from time import time


@contextmanager
def timeit(description: str, enabled:bool=False) -> None:
    """
    Generic Context manager  simple Timeit

    :param description:
    :param enabled:
    :return:
    """
    t0 = time()
    yield
    ellapsed_time = time() - t0

    if enabled:
        print(f"{description} done in {ellapsed_time:.3f} s.")
