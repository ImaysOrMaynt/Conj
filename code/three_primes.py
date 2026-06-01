"""
Rigorous solver for  R(p1^a) R(p2^b) R(p3^c) = 2  with p1 < p2 < p3 FIXED primes.

Each factor satisfies  R(p^2) <= R(p^e) < p/(p-1)  and is strictly increasing in e.
So at each level the relevant exponent lies in an interval determined by exact
rational feasibility bounds:

  level 1 (p1):  need target2 := 2/R(p1^a) to be reachable by {p2,p3}, i.e.
                 R(p2^2)R(p3^2) <= target2 < (p2/(p2-1))(p3/(p3-1)).
                 -> 2/(sup2 sup3) < R(p1^a) <= 2/(R(p2^2)R(p3^2)).
  level 2 (p2):  R(p3^2) <= target3 := target2/R(p2^b) < p3/(p3-1).
                 -> target2/sup3 < R(p2^b) <= target2/R(p3^2).
  level 3 (p3):  check whether target3 equals R(p3^c) for some c.

An exponent is *provably bounded* when its upper feasibility value is < the
prime's sup p/(p-1) (because R(p^e) -> p/(p-1) strictly from below).  When that
holds at every reached level, the search is finite and the verdict is RIGOROUS.
If some level has a vacuous upper bound, we fall back to an explicit cap and the
verdict is 'searched to cap'.
"""
from fractions import Fraction
from conj import R_pp


def _exp_range(p, lo_strict, hi_incl, cap):
    """Exponents e>=2 with  lo_strict < R(p^e) <= hi_incl.  Returns (list, bounded?).
    'bounded' is True when hi_incl < p/(p-1) (so the upper end is provably finite)."""
    sup = Fraction(p, p - 1)
    bounded = hi_incl < sup
    es = []
    e = 2
    while True:
        Re = R_pp(p, e)
        if Re > hi_incl:
            break
        if Re > lo_strict:
            es.append(e)
        e += 1
        if e > cap:
            break
    return es, bounded


def solve_three(p1, p2, p3, cap=20000):
    sup2 = Fraction(p2, p2 - 1)
    sup3 = Fraction(p3, p3 - 1)
    minprod23 = R_pp(p2, 2) * R_pp(p3, 2)
    sols = []
    rigorous = True

    # level 1: bounds on R(p1^a)
    lo1 = Fraction(2) / (sup2 * sup3)        # strict lower
    hi1 = Fraction(2) / minprod23            # inclusive upper
    a_list, b1 = _exp_range(p1, lo1, hi1, cap)
    rigorous &= b1

    for a in a_list:
        target2 = Fraction(2) / R_pp(p1, a)
        # level 2: bounds on R(p2^b)
        lo2 = target2 / sup3
        hi2 = target2 / R_pp(p3, 2)
        b_list, b2 = _exp_range(p2, lo2, hi2, cap)
        rigorous &= b2
        for b in b_list:
            target3 = target2 / R_pp(p2, b)
            # level 3: is target3 == R(p3^c)?
            c = 2
            while True:
                Rc = R_pp(p3, c)
                if Rc == target3:
                    sols.append((a, b, c))
                    break
                if Rc > target3:
                    break
                c += 1
                if c > cap:
                    break
    return sols, rigorous


if __name__ == "__main__":
    # The three families of case IIIb (3|m, 2 not | m, omega=3):
    families = [(3, 5, 7), (3, 5, 11), (3, 5, 13)]
    print("Case IIIb families  (m = p1^a p2^b p3^c,  R(m)=2):")
    for (p1, p2, p3) in families:
        sols, rig = solve_three(p1, p2, p3)
        verdict = "RIGOROUS (all exponents provably bounded)" if rig else "searched to cap=20000"
        print(f"  R({p1}^a)R({p2}^b)R({p3}^c)=2 : solutions={sols}   [{verdict}]")

    # Sanity: the two-prime / known structure -- confirm 108 emerges as 2^2 3^3.
    # (Use a fake third prime won't apply; instead confirm 2,3 alone via two-prime.)
    print("\nSanity check: does the method find 108 = 2^2*3^3 in a {2,3,P} family?")
    for P in (5, 7, 11):
        sols, rig = solve_three(2, 3, P)
        print(f"  R(2^a)R(3^b)R({P}^c)=2 : {sols}  (expect none with all three >=2; 108 uses only 2,3)")
