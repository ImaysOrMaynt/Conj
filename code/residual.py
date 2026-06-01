"""
Theorem 4 (case 6 | m) bookkeeping and the residual equation.

If 6 | m is a powerful solution then v2(m) = 2 (else R(2^3)R(3^2) = 5/3*... > 2)
and v3(m) in {2,3}.  v3 = 3 gives m = 108.  v3 = 2 gives m = 36*M with M powerful,
coprime to 6, and
        R(2^2) R(3^2) R(M) = 2   =>   R(M) = 2 / (7/5 * 13/10) = 2 / (91/50) = 100/91.
The paper shows every such M has omega(M) >= 3 and all prime factors >= 11.
Here we verify those reductions exactly and search the residual up to a height.
"""
from fractions import Fraction
from math import isqrt, gcd
from conj import R_pp, primes_upto, sigma_pp


def search_target(target: Fraction, X, min_prime=2, exclude=()):
    """
    All powerful m <= X with R(m) = target, smallest prime >= min_prime,
    using only primes not in `exclude`.  Same rigorous prune as fast_verify.
    """
    primes = [p for p in primes_upto(isqrt(X)) if p >= min_prime and p not in exclude]
    P = len(primes)
    ratio_f = [p / (p - 1) for p in primes]
    tnum, tden = target.numerator, target.denominator
    tf = float(target)
    results = []

    def max_reach_f(start, budget):
        prod = 1.0
        b = budget
        j = start
        while j < P:
            p = primes[j]
            p2 = p * p
            if p2 > b:
                break
            prod *= ratio_f[j]
            b //= p2
            j += 1
        return prod

    def rec(start, m, Rn, Rd):
        budget = X // m
        if (Rn / Rd) * max_reach_f(start, budget) < tf * (1 - 1e-9):
            return
        for i in range(start, P):
            p = primes[i]
            p2 = p * p
            if m * p2 > X:
                break
            a = 2
            pa = p2
            while m * pa <= X:
                sn = sigma_pp(p, a)
                sd = pa + 1
                nn = Rn * sn
                dd = Rd * sd
                g = gcd(nn, dd)
                nn //= g
                dd //= g
                # compare nn/dd to target tnum/tden
                lhs = nn * tden
                rhs = tnum * dd
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
    # Exact reductions
    print("R(2^2)*R(3^2)      =", R_pp(2, 2) * R_pp(3, 2), " (expect 91/50)")
    print("2 / (91/50)        =", Fraction(2) / (R_pp(2, 2) * R_pp(3, 2)), " (expect 100/91 = residual)")
    print("R(11^2)            =", R_pp(11, 2), " ~", float(R_pp(11, 2)))
    print("R(11^3)            =", R_pp(11, 3), " ~", float(R_pp(11, 3)))
    print("100/91             ~", 100 / 91, " (between R(11^2) and R(11^3))")

    # Verify primes <= 7 cannot divide a residual M: R(p^2) > 100/91 for p in {5,7}
    for p in (5, 7):
        print(f"R({p}^2) = {R_pp(p,2)} ~ {float(R_pp(p,2)):.5f}  (> 100/91 ~ {100/91:.5f}? "
              f"{R_pp(p,2) > Fraction(100,91)})")

    # Search the residual R(M)=100/91 over M coprime to 6 up to a height bound.
    for X in [10**10, 10**12, 10**14]:
        t0 = time.time()
        sols = search_target(Fraction(100, 91), X, min_prime=5, exclude=(2, 3))
        print(f"residual R(M)=100/91, M coprime to 6, <= {X:.0e}: {sols}   [{time.time()-t0:.1f}s]")
