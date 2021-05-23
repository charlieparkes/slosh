import time
from decimal import Decimal
from math import floor, log10


def rnd(x, n):
    """Round x to n decimal places. If less than zero, round to 1 significant figure."""
    if x < 0.01:
        return float(round(x, -int(floor(log10(abs(Decimal(n)))))))
    return float(round(Decimal(x), n))


class Timer:
    def __init__(self):
        self.start = time.time()

    def stop(self):
        self.duration = time.time() - self.start
        return f"{self}"

    def __repr__(self):
        return f"{rnd(self.duration, 2)}s"
