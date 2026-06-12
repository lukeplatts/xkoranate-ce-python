"""Mersenne-twister RNG mimicking std::tr1::mt19937 as used by the C++ code.

The C++ code calls `(*r)()` for a raw 32-bit value and uses r->min()/r->max()
to scale to [0, 1]. We back it with Python's random.Random (also MT19937).
"""

import random
import time


class Mt19937:
    MIN = 0
    MAX = 0xFFFFFFFF

    def __init__(self, seed=None):
        if seed is None:
            seed = int(time.time())
        self._r = random.Random(seed)

    def __call__(self):
        return self.next32()

    def next32(self):
        return self._r.getrandbits(32)

    def seed(self, s):
        self._r.seed(s)

    def min(self):
        return self.MIN

    def max(self):
        return self.MAX

    def shuffle(self, seq):
        """std::random_shuffle equivalent using this generator."""
        for i in range(len(seq) - 1, 0, -1):
            j = self.next32() % (i + 1)
            seq[i], seq[j] = seq[j], seq[i]
