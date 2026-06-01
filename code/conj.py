"""
Core utilities for the conjecture  sigma(n) = 2 sigma*(n)  =>  n = 108 (mod 216).

We work with the multiplicative ratio
        R(n) = sigma(n) / sigma*(n) = prod_{p^a || n} R(p^a),
        R(p^a) = (1 + p + ... + p^a) / (p^a + 1) = (p^{a+1}-1) / ((p-1)(p^a+1)).
R(p) = 1, so only the *powerful core* of n matters.  The equation is R(n) = 2.

Everything here is exact (Fraction / integers); no floating point in the proofs.
"""
from fractions import Fraction
from functools import lru_cache
from math import isqrt


# ----------------------------------------------------------------------
# Arithmetic functions on prime powers (exact)
# ----------------------------------------------------------------------
def sigma_pp(p, a):
    """sigma(p^a) = 1 + p + ... + p^a."""
    return (p ** (a + 1) - 1) // (p - 1)


def sigma_star_pp(p, a):
    """sigma*(p^a) = p^a + 1  (the two unitary divisors 1 and p^a)."""
    return p ** a + 1


def R_pp(p, a):
    """R(p^a) as an exact Fraction."""
    return Fraction(sigma_pp(p, a), sigma_star_pp(p, a))


# ----------------------------------------------------------------------
# Factorisation (trial division; fine for our ranges) and full-n functions
# ----------------------------------------------------------------------
def factorize(n):
    """Return dict {p: a}."""
    f = {}
    d = 2
    while d * d <= n:
        while n % d == 0:
            f[d] = f.get(d, 0) + 1
            n //= d
        d += 1 if d == 2 else 2
    if n > 1:
        f[n] = f.get(n, 0) + 1
    return f


def R_of(n):
    """R(n) for a positive integer n, exact."""
    r = Fraction(1)
    for p, a in factorize(n).items():
        r *= R_pp(p, a)
    return r


def sigma(n):
    s = 1
    for p, a in factorize(n).items():
        s *= sigma_pp(p, a)
    return s


def sigma_star(n):
    s = 1
    for p, a in factorize(n).items():
        s *= sigma_star_pp(p, a)
    return s


def is_powerful(n):
    """n is powerful iff every prime exponent is >= 2."""
    if n == 1:
        return True
    return all(a >= 2 for a in factorize(n).values())


def powerful_core(n):
    """Product of p^a || n with a >= 2 (the part R sees)."""
    m = 1
    for p, a in factorize(n).items():
        if a >= 2:
            m *= p ** a
    return m


# ----------------------------------------------------------------------
# Prime generation
# ----------------------------------------------------------------------
def primes_upto(N):
    if N < 2:
        return []
    sieve = bytearray([1]) * (N + 1)
    sieve[0] = sieve[1] = 0
    for i in range(2, isqrt(N) + 1):
        if sieve[i]:
            sieve[i * i :: i] = bytearray(len(range(i * i, N + 1, i)))
    return [i for i in range(2, N + 1) if sieve[i]]


# ----------------------------------------------------------------------
# Enumerate powerful numbers <= X  (every powerful number is a^2 * b^3)
# ----------------------------------------------------------------------
def powerful_numbers_upto(X):
    """
    Yield every powerful number <= X exactly once.
    Standard representation: powerful = b^3 * c^2 with c squarefree... but the
    classic clean enumeration is m = a^2 * b^3 with b cubefree-ish; we instead
    build directly from prime powers to avoid duplicate bookkeeping.
    Here we use: every powerful number is uniquely a^2 * b^3 with b squarefree.
    """
    res = []
    b = 1
    while b ** 3 <= X:
        if _squarefree(b):
            b3 = b ** 3
            a = 1
            while a * a * b3 <= X:
                res.append(a * a * b3)
                a += 1
        b += 1
    res = sorted(set(res))
    return res


def _squarefree(n):
    d = 2
    while d * d <= n:
        if n % (d * d) == 0:
            return False
        if n % d == 0:
            n //= d
        else:
            d += 1
    return True


if __name__ == "__main__":
    # Sanity: the paper's central identity and the unique known solution.
    print("R(108)      =", R_of(108), " (108 = 2^2 * 3^3)")
    print("R(2^2)      =", R_pp(2, 2))
    print("R(3^3)      =", R_pp(3, 3))
    print("R(2^2)*R(3^3)=", R_pp(2, 2) * R_pp(3, 3))
    print("sigma(108)  =", sigma(108), " 2*sigma*(108) =", 2 * sigma_star(108))
    print("108 mod 216 =", 108 % 216)
