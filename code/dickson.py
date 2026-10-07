"""
Free-prime Dickson prover:  all powerful M with exactly k distinct primes, drawn
from an allowed set, such that R(M) = target.

This extends three_primes.solve_fixed (exponents free, primes fixed) to the case
where the PRIMES are free too.  Primes are chosen in increasing order.  A node is

    chosen : tuple of (p, e, open)    -- e pinned, or open meaning e, e+1, ...
    j      : number of primes still to choose
    P      : every remaining prime is an allowed prime >= P

For j >= 1 the unchosen primes contribute a factor in (1, prod_{i<j} q_i/(q_i-1)),
q_0 < q_1 < ... the j smallest allowed primes >= P (both ends excluded: R(q^e) > 1
and R(q^e) < q/(q-1)).  So the node's values lie in an exact interval [lo, hi] with
known strictness, and a node whose interval misses the target is discarded.

Splitting (widest factor ratio first, which makes every infinite chain converge):
  * an open exponent  e  ->  {e} | {e+1, ...}
  * the free block          ->  take P (as an open coordinate (P, 2, open)) | skip P
A node with j = 1 and nothing open is solved in closed form: R(q^e) - 1 lies in
(1/(q+1), 1/(q-1)) for every e >= 2, so q is one of at most two integers near
1/(X-1), and then e is found by monotonicity.

All arithmetic is exact.  `is_prime` is Miller-Rabin; it never rejects a prime, so
a composite mistaken for prime could only ADD branches -- the search never skips a
real prime and "no solution" verdicts stay sound (any reported solution is
re-verified with exact arithmetic anyway).

Termination: by the compactness argument of three_primes.py, an infinite chain
must converge to a limit configuration (some exponents -> oo, giving p/(p-1), some
primes -> oo, giving 1) whose value equals the target with the interval open on
BOTH sides -- a "two-sided" limit.  If no such limit exists the search terminates
and its verdict is a proof.  Where one exists (e.g. R(2^oo) * 1 * ... = 2) the node
cap trips and the verdict is reported as NOT proved.
"""
from fractions import Fraction
from math import prod

from conj import R_pp

_SMALL = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41]


def is_prime(n):
    if n < 2:
        return False
    for p in _SMALL:
        if n % p == 0:
            return n == p
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for a in _SMALL:
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


class Primes:
    """Allowed primes: primes >= lo, not in `exclude`."""

    def __init__(self, lo=2, exclude=()):
        self.lo, self.exclude = lo, frozenset(exclude)
        self._next = {}

    def ok(self, n):
        return n >= self.lo and n not in self.exclude and is_prime(n)

    def first_at_least(self, n):
        n = max(n, self.lo)
        while not self.ok(n):
            n += 1
        return n

    def after(self, p):
        if p not in self._next:
            self._next[p] = self.first_at_least(p + 1)
        return self._next[p]

    def run(self, P, j):
        out, q = [], self.first_at_least(P)
        for _ in range(j):
            out.append(q)
            q = self.after(q)
        return out


def _last_slot(X, P, primes):
    """All (q, e), q allowed prime >= P, e >= 2, with R(q^e) == X exactly."""
    if X <= 1:
        return []
    c = 1 / (X - 1)                      # q in (c - 1, c + 1)
    out = []
    for q in range(max(P, int(c) - 1), int(c) + 3):
        if not (c - 1 < q < c + 1) or not primes.ok(q):
            continue
        if X >= Fraction(q, q - 1):
            continue
        e = 2
        while True:
            r = R_pp(q, e)
            if r == X:
                out.append((q, e))
            if r >= X:
                break
            e += 1
    return out


def solve_free(target, k, primes, max_nodes=10**6, start=None):
    """All powerful M with omega(M) = k, primes from `primes`, R(M) = target.

    Returns (solutions, nodes, complete); solutions are tuples of (p, e)."""
    target = Fraction(target)
    sols, nodes = [], 0
    stack = [start if start is not None else ((), k, primes.first_at_least(primes.lo))]
    while stack:
        if nodes >= max_nodes:
            return sorted(sols), nodes, False
        nodes += 1
        chosen, j, P = stack.pop()
        lows = [R_pp(p, e) for p, e, _ in chosen]
        highs = [Fraction(p, p - 1) if o else r for (p, _, o), r in zip(chosen, lows)]
        free_run = primes.run(P, j)
        free_hi = prod(Fraction(q, q - 1) for q in free_run)
        lo = prod(lows)
        hi = prod(highs) * free_hi
        any_open = any(o for _, _, o in chosen)
        lo_strict = j >= 1
        hi_strict = j >= 1 or any_open
        if target < lo or (lo_strict and target == lo):
            continue
        if target > hi or (hi_strict and target == hi):
            continue
        if j == 0 and not any_open:
            sols.append(tuple((p, e) for p, e, _ in chosen))
            continue
        if j == 1 and not any_open:
            for q, e in _last_slot(target / lo, P, primes):
                sols.append(tuple((p, x) for p, x, _ in chosen) + ((q, e),))
            continue
        if j == 1:
            # the last prime q needs R(q^e) = X with X in [target/fixed_hi, target/lo],
            # and R(q^e) - 1 lies in (1/(q+1), 1/(q-1)): jump P to the first q that
            # could possibly fit, and prune if even that is past the last one.
            fixed_hi = prod(highs)
            x_max, x_min = target / lo, target / fixed_hi
            q_lo = 1 / (x_max - 1) - 1                      # need q > q_lo
            if x_min > 1 and P > 1 / (x_min - 1) + 1:       # need q < this
                continue
            if P <= q_lo:
                stack.append((chosen, j, primes.first_at_least(int(q_lo) + 1)))
                continue
        # widest ratio: open exponents vs the free block
        best, best_ratio = None, Fraction(1)
        for i, ((p, e, o), r, h) in enumerate(zip(chosen, lows, highs)):
            if o and h / r > best_ratio:
                best, best_ratio = i, h / r
        if j >= 1 and free_hi > best_ratio:
            best = "free"
        if best == "free":
            nxt = primes.after(free_run[0])
            stack.append((chosen, j, nxt))                                  # skip P
            stack.append((chosen + ((free_run[0], 2, True),), j - 1, nxt))  # take P
        else:
            p, e, _ = chosen[best]
            stack.append((chosen[:best] + ((p, e + 1, True),) + chosen[best + 1:], j, P))
            stack.append((chosen[:best] + ((p, e, False),) + chosen[best + 1:], j, P))
    return sorted(sols), nodes, True


def verify(sol, target):
    return prod(R_pp(p, e) for p, e in sol) == Fraction(target)
