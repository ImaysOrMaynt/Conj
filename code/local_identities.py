"""
Local (l-adic) valuation identities for R(m) = sigma(m)/sigma*(m).

For a solution R(m) = 2 we must have, for every prime l,
        v_l(sigma(m)) - v_l(sigma*(m)) = v_l(2) = [l == 2].
Expanding each side prime-power by prime-power and using lifting-the-exponent
(LTE) gives an identity in the *exponents* of m.  Two cases are clean:

  l = 2  (paper Theorem 6):   sum_{P odd, e_P odd} v2(e_P + 1) = 1 + k,
          where k = number of distinct odd primes of m.

  l = 3  (NEW here):          for the per-prime contribution
          D3(p,a) := v3(sigma(p^a)) - v3(p^a + 1) we have
              p = 3            : 0
              p = 1 (mod 3)    : v3(a+1)
              p = 2 (mod 3), a even : 0
              p = 2 (mod 3), a odd  : v3(a+1) - v3(a)
          and sum_{p^a || m} D3(p,a) = v3(R(m)), which must be 0 for a solution.

This module verifies the per-prime formulas directly (no LTE shortcut) on a wide
range of prime powers, then checks the global identities.
"""
from conj import sigma_pp, R_pp, factorize
from fractions import Fraction


def v(l, n):
    """l-adic valuation of a nonzero integer n."""
    if n == 0:
        return float("inf")
    c = 0
    while n % l == 0:
        n //= l
        c += 1
    return c


def vQ(l, q: Fraction):
    """l-adic valuation of a rational."""
    return v(l, q.numerator) - v(l, q.denominator)


# ---- predicted per-prime 3-adic contribution D3(p,a) -------------------
def D3_formula(p, a):
    if p == 3:
        return 0
    if p % 3 == 1:
        return v(3, a + 1)
    # p % 3 == 2
    if a % 2 == 0:
        return 0
    return v(3, a + 1) - v(3, a)


def D3_direct(p, a):
    return v(3, sigma_pp(p, a)) - v(3, p ** a + 1)


# ---- predicted per-prime 2-adic contribution (for Theorem 6) -----------
def D2_direct(p, a):
    return v(2, sigma_pp(p, a)) - v(2, p ** a + 1)


if __name__ == "__main__":
    from conj import primes_upto

    primes = primes_upto(2000)

    # (1) Verify the 3-adic per-prime formula D3 on every prime power
    #     p in primes, a = 2..40.
    bad = 0
    for p in primes:
        for a in range(2, 41):
            if D3_formula(p, a) != D3_direct(p, a):
                bad += 1
                if bad <= 5:
                    print("  MISMATCH D3", p, a, D3_formula(p, a), D3_direct(p, a))
    print(f"[3-adic] per-prime formula checked for {len(primes)} primes x a=2..40: "
          f"{'ALL OK' if bad==0 else str(bad)+' MISMATCHES'}")

    # (2) Verify global: sum of D3 over prime powers of m equals v3(R(m)),
    #     for a batch of random powerful numbers m.
    import random
    random.seed(1)
    bad = 0
    checks = 0
    for _ in range(4000):
        # build a random powerful m
        fac = {}
        for _ in range(random.randint(1, 4)):
            p = random.choice(primes[:60])
            fac[p] = fac.get(p, 0) + random.randint(2, 6)
        m = 1
        R = Fraction(1)
        s3 = 0
        for p, a in fac.items():
            m *= p ** a
            R *= R_pp(p, a)
            s3 += D3_formula(p, a)
        if s3 != vQ(3, R):
            bad += 1
        checks += 1
    print(f"[3-adic] global identity  sum D3 == v3(R(m))  on {checks} random m: "
          f"{'ALL OK' if bad==0 else str(bad)+' MISMATCHES'}")

    # (3) Verify Theorem 6 (2-adic) on random m: sum_{P odd, e odd} v2(e+1) == 1+k
    #     should hold *iff* v2(R(m)) == 1, i.e. iff m could be a solution 2-adically.
    #     We instead verify the underlying matching: v2(R(m)) computed two ways.
    bad = 0
    checks = 0
    for _ in range(4000):
        fac = {}
        for _ in range(random.randint(1, 4)):
            p = random.choice(primes[:60])
            fac[p] = fac.get(p, 0) + random.randint(2, 6)
        R = Fraction(1)
        for p, a in fac.items():
            R *= R_pp(p, a)
        # Theorem-6 bookkeeping
        k = sum(1 for p in fac if p % 2 == 1)
        lhs = sum(v(2, e + 1) for p, e in fac.items() if p % 2 == 1 and e % 2 == 1)
        # v2(R) == 1  <=>  lhs == 1 + k   (Theorem 6's matching, valid when 2 may or may not divide m)
        cond_formula = (lhs == 1 + k)
        cond_direct = (vQ(2, R) == 1)
        if cond_formula != cond_direct:
            bad += 1
        checks += 1
    print(f"[2-adic] Theorem 6 matching (v2(R)==1 <=> sum v2(e+1)==1+k) on {checks} random m: "
          f"{'ALL OK' if bad==0 else str(bad)+' MISMATCHES'}")
