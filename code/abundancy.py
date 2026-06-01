"""
Proposition 8 (abundancy lower bounds) and the two-sided window.

Since 1 < R(p^a) < p/(p-1) for a >= 2 (Lemma 1), a solution R(m) = 2 satisfies
        prod_{p | m} p/(p-1)  >  2            (lower abundancy bound)
        prod_{p | m} R(p^2)   <= 2            (upper window; does NOT cap omega).

If every prime of m is >= q, then prod_{p|m} p/(p-1) <= prod over the omega
smallest primes >= q, so omega must be large enough to push that product past 2.
This yields a lower bound on omega depending only on the least prime of m.
"""
from fractions import Fraction
from conj import primes_upto, R_pp

PRIMES = primes_upto(10000)


def min_omega_given_least_prime(q):
    """Smallest t such that the product of the t smallest primes >= q exceeds 2."""
    prod = Fraction(1)
    t = 0
    for p in PRIMES:
        if p < q:
            continue
        prod *= Fraction(p, p - 1)
        t += 1
        if prod > 2:
            return t, prod
    raise RuntimeError("increase PRIMES")


if __name__ == "__main__":
    print("Proposition 8 table  (least prime q  ->  forced omega(m) >= N):")
    print(f"  {'least prime q':>14} | {'omega >=':>9} | product just exceeding 2")
    for q in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]:
        t, prod = min_omega_given_least_prime(q)
        print(f"  {q:>14} | {t:>9} | {float(prod):.5f}")

    print()
    print("Paper's stated row (least prime 5,7,11,13,17,19,23 -> 7,15,27,41,62,85,115):")
    row = [(q, min_omega_given_least_prime(q)[0]) for q in (5, 7, 11, 13, 17, 19, 23)]
    print("  computed:", row)
    expected = [(5,7),(7,15),(11,27),(13,41),(17,62),(19,85),(23,115)]
    print("  expected:", expected)
    print("  MATCH" if row == expected else "  MISMATCH")

    print()
    # Demonstrate the upper window does NOT cap omega: product of R(p^2) over
    # many large primes stays below 2 forever (each factor -> 1).
    prod = Fraction(1)
    cnt = 0
    for p in PRIMES:
        if p < 101:
            continue
        prod *= R_pp(p, 2)
        cnt += 1
        if cnt in (10, 100, 500, 1000):
            print(f"  prod_{{first {cnt} primes >=101}} R(p^2) = {float(prod):.6f}  (<2, and grows only ~log)")
