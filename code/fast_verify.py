"""
Optimised, still-rigorous verifier: list all powerful m <= X with R(m) = 2.

R is carried as an EXACT reduced fraction (integer numerator/denominator), so the
final test R == 2 is exact.  The pruning upper bound is ALSO exact: the product
prod_{p>=q, p^2 fits} p/(p-1) over the greedily-smallest fitting primes is a
strict over-estimate of any reachable R (since R(p^a) < p/(p-1) and small primes
maximise factor-per-size), and it has only ~13 terms for X <= 10^18.  A branch is
cut only when this exact over-estimate * (R so far) <= 2, which is sound because
the true reachable value is then STRICTLY below 2.  Hence "the only powerful
solution <= X is 108" is rigorous, with no floating point anywhere.
"""
import sys
from math import isqrt, gcd
from conj import primes_upto, sigma_pp


def solutions_upto(X):
    primes = primes_upto(isqrt(X))
    P = len(primes)
    # exact p/(p-1) as (numerator, denominator) = (p, p-1)
    results = []

    def max_reach_num_den(start, budget):
        """EXACT over-estimate prod_{p>=primes[start], p^2 fits} p/(p-1), as (num,den).
        Each included prime consumes >= p^2 of the budget, so the product is short."""
        num = 1
        den = 1
        b = budget
        j = start
        while j < P:
            p = primes[j]
            p2 = p * p
            if p2 > b:
                break
            num *= p
            den *= (p - 1)
            b //= p2
            j += 1
        return num, den

    def rec(start, m, Rn, Rd):
        # invariant: Rn/Rd = R so far, in lowest terms, and < 2
        budget = X // m
        # exact optimistic prune: (Rn/Rd)*(num/den) <= 2  =>  true reachable < 2  => cut
        mn, md = max_reach_num_den(start, budget)
        if Rn * mn <= 2 * Rd * md:
            return
        for i in range(start, P):
            p = primes[i]
            p2 = p * p
            if m * p2 > X:
                break
            a = 2
            pa = p2
            while m * pa <= X:
                sn = sigma_pp(p, a)       # sigma(p^a)
                sd = pa + 1               # p^a + 1
                nn = Rn * sn
                dd = Rd * sd
                g = gcd(nn, dd)
                nn //= g
                dd //= g
                # compare nn/dd to 2
                lhs = nn
                rhs = 2 * dd
                if lhs < rhs:
                    rec(i + 1, m * pa, nn, dd)
                elif lhs == rhs:
                    results.append(m * pa)
                    break
                else:
                    break
                a += 1
                pa *= p

    rec(0, 1, 1, 1)
    return sorted(set(results))


if __name__ == "__main__":
    import time
    X = int(float(sys.argv[1])) if len(sys.argv) > 1 else 10**14
    t0 = time.time()
    s = solutions_upto(X)
    print(f"solutions_upto({X:.1e}) = {s}    [{time.time()-t0:.1f}s]")
