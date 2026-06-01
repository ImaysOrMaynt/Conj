"""
Recursive rational search for powerful solutions of  R(m) = sigma(m)/sigma*(m) = 2.

Two rigorous, terminating modes:

  solutions_upto(X)            : ALL powerful m <= X with R(m) = 2.
  solutions_omega(k, ...)      : ALL powerful m with omega(m) <= k and R(m) = 2,
                                 subject to an explicit exponent cap A (stated).

Both walk primes in increasing order, choosing a subset to include (each with
exponent >= 2).  Pruning uses two exact facts:
  * R is strictly increasing in the exponent, with sup R(p^a) = p/(p-1);
  * including only primes >= q, each at exponent >= 2, the product of factors
    is < prod_{p>=q, p^2 fits} p/(p-1)  (a size-bounded upper estimate).
A branch is killed as soon as the partial product exceeds 2, or the optimistic
upper estimate cannot reach 2.
"""
from fractions import Fraction
from conj import R_pp, primes_upto
from math import isqrt

TWO = Fraction(2)


def solutions_upto(X, verbose=False):
    """Return sorted list of all powerful m <= X with R(m) = 2."""
    primes = primes_upto(isqrt(X))
    P = len(primes)
    # Precompute p/(p-1) as Fractions for the optimistic bound.
    ratio = [Fraction(p, p - 1) for p in primes]

    results = []
    # Optimistic upper bound on the product of p/(p-1) over primes[i:] whose
    # square still fits in 'budget'.  Used to prune.
    def max_reach(i, budget):
        prod = Fraction(1)
        j = i
        b = budget
        while j < P:
            p = primes[j]
            if p * p > b:
                break
            prod *= ratio[j]
            b //= (p * p)          # this prime consumes at least p^2 of the budget
            j += 1
        return prod

    def rec(start, m, R):
        if R == TWO:
            results.append(m)
            return
        # R < 2 strictly here (we never recurse with R > 2)
        budget = X // m
        if R * max_reach(start, budget) < TWO:
            return  # cannot possibly reach 2 from here
        for i in range(start, P):
            p = primes[i]
            p2 = p * p
            if m * p2 > X:
                break  # p^2 too big; larger primes also too big
            # try exponents a = 2, 3, ... while size fits and R stays <= 2
            a = 2
            pa = p2
            while m * pa <= X:
                Rp = R_pp(p, a)
                newR = R * Rp
                if newR < TWO:
                    rec(i + 1, m * pa, newR)
                elif newR == TWO:
                    results.append(m * pa)
                    break  # larger exponent only increases R further
                else:
                    break  # newR > 2; larger exponent worse
                a += 1
                pa *= p

    rec(0, 1, Fraction(1))
    return sorted(set(results))


def solutions_omega(k, exp_cap=400, prime_cap=None, verbose=False):
    """
    Return all powerful m with omega(m) <= k, R(m) = 2, every exponent <= exp_cap,
    and (optionally) every prime <= prime_cap.  RIGOROUS modulo the exponent cap:
    the smallest prime at each level is bounded by abundancy, so the prime range
    is finite; only the exponent of a prime whose p/(p-1) <= current target is
    a priori unbounded, and that is what exp_cap controls.  Reports any branch
    that hits the cap so we know whether the bound bit.
    """
    cap_hits = []

    def rec(primes_used, m, R, min_prime, remaining):
        # remaining = how many more primes we may still add
        if R == TWO:
            cap_hits.append(("SOLUTION", m, primes_used))
            return
        if remaining == 0:
            return
        # smallest next prime p must satisfy (p/(p-1))^remaining > target=2/R
        # i.e. it is bounded above.
        target = TWO / R
        # find max prime p with (p/(p-1))^remaining > target
        # (p/(p-1))^remaining > target  <=>  p/(p-1) > target^(1/remaining)
        # solve for p:  p < 1/(1 - target^(-1/remaining)); use float then verify.
        thr = float(target) ** (1.0 / remaining)
        if thr <= 1.0:
            pmax = 10**9
        else:
            pmax = int(1.0 / (1.0 - 1.0 / thr)) + 2
        if prime_cap:
            pmax = min(pmax, prime_cap)
        p = _next_prime(min_prime)
        while p <= pmax:
            # verify the bound exactly: need (p/(p-1))^remaining > target
            if Fraction(p, p - 1) ** remaining <= target:
                p = _next_prime(p)
                continue
            for a in range(2, exp_cap + 1):
                Rp = R_pp(p, a)
                newR = R * Rp
                if newR > TWO:
                    break  # exponent too large; R increasing -> stop
                if a == exp_cap:
                    cap_hits.append(("CAPHIT", p, a, m))
                rec(primes_used + [(p, a)], m * p**a, newR, p, remaining - 1)
            p = _next_prime(p)

    rec([], 1, Fraction(1), 1, k)
    return cap_hits


_small_primes = primes_upto(10**6)
_sp_set = set(_small_primes)


def _next_prime(n):
    m = n + 1
    while True:
        if _is_prime(m):
            return m
        m += 1


def _is_prime(n):
    if n < 2:
        return False
    if n < 10**6:
        return n in _sp_set
    d = 2
    while d * d <= n:
        if n % d == 0:
            return False
        d += 1
    return True


if __name__ == "__main__":
    import time, sys
    X = int(float(sys.argv[1])) if len(sys.argv) > 1 else 10**12
    t0 = time.time()
    sols = solutions_upto(X)
    print(f"solutions_upto({X:.0e}) = {sols}    [{time.time()-t0:.2f}s]")
