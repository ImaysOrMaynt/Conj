"""
Rigorous solver for  prod_i R(p_i^{e_i}) = target  (default 2) over a FIXED set of
primes p_1, ..., p_k, every exponent e_i >= 2.  Used to close case IIIb.

Branch-and-bound over exponent boxes.  Each coordinate of a box is either pinned
(e_i = e) or open (e_i = e, e+1, e+2, ...).  Since R(p^e) is strictly increasing in
e with supremum p/(p-1) (never attained), every product over a box lies in

        [ prod R(p_i^{e_i}),  prod (R(p_i^{e_i}) if pinned else p_i/(p_i-1)) ]

with the upper end EXCLUDED as soon as one coordinate is open.  A box whose range
misses the target is discarded; a fully pinned box is a point and is checked exactly;
otherwise the open coordinate with the widest factor range is split into
{e} and {e+1, e+2, ...}.  All arithmetic is exact (Fraction).

Why this is a proof and why it always terminates: extend R by R(p^oo) = p/(p-1),
making the exponent space compact.  Widest-first splitting shrinks every infinite
chain of boxes to one point x of that space.  If F(x) != target, continuity prunes
the chain; if F(x) = target with x finite, the chain ends at the point x itself; if
F(x) = target with some coordinate of x infinite, the chain is pruned as soon as the
finite coordinates are pinned, because then the box's (excluded) upper end is F(x).
So no infinite chain exists and the binary tree is finite (Koenig).  In particular
a FIXED set of primes is never an obstruction -- the solution set is always finite
and computable.  (The genuine walls come from primes that are not fixed.)

The old level-by-level squeeze (exponent of p_1 first, then p_2, ...) could not
bound the exponent of 3 for {3,5,11} and {3,5,13} and fell back to a search cap;
the branch-and-bound splits whichever coordinate is widest and closes both.
"""
from fractions import Fraction
from math import prod

from conj import R_pp


def solve_fixed(primes, target=Fraction(2), max_nodes=10**6):
    """All exponent vectors (e_1, ..., e_k), every e_i >= 2, with
    prod R(p_i^{e_i}) == target.

    Returns (solutions, nodes, complete).  complete=True means the search
    terminated, so `solutions` is provably the complete list; max_nodes is only a
    safety net (the search always terminates, see the module docstring)."""
    sups = [Fraction(p, p - 1) for p in primes]
    sols, nodes = [], 0
    stack = [tuple((2, True) for _ in primes)]     # (e, open): open means e, e+1, ...
    while stack:
        if nodes == max_nodes:
            return sorted(sols), nodes, False
        nodes += 1
        box = stack.pop()
        lows = [R_pp(p, e) for p, (e, _) in zip(primes, box)]
        highs = [s if is_open else r for s, r, (_, is_open) in zip(sups, lows, box)]
        lo, hi = prod(lows), prod(highs)
        any_open = any(is_open for _, is_open in box)
        if target < lo or target > hi or (any_open and target == hi):
            continue                                # target outside the box's range
        if not any_open:
            sols.append(tuple(e for e, _ in box))   # a point, and lo == hi == target
            continue
        i = max((j for j, (_, is_open) in enumerate(box) if is_open),
                key=lambda j: highs[j] / lows[j])
        e = box[i][0]
        stack.append(box[:i] + ((e, False),) + box[i + 1:])
        stack.append(box[:i] + ((e + 1, True),) + box[i + 1:])
    return sorted(sols), nodes, True


def solve_three(p1, p2, p3, target=Fraction(2)):
    """R(p1^a) R(p2^b) R(p3^c) = target.  Returns (solutions, rigorous)."""
    sols, _, complete = solve_fixed((p1, p2, p3), target)
    return sols, complete


if __name__ == "__main__":
    # The three families of case IIIb (3|m, 2 not | m, omega=3):
    families = [(3, 5, 7), (3, 5, 11), (3, 5, 13)]
    print("Case IIIb families  (m = p1^a p2^b p3^c,  R(m)=2):")
    for ps in families:
        sols, nodes, complete = solve_fixed(ps)
        verdict = (f"RIGOROUS (branch-and-bound terminated after {nodes} boxes)"
                   if complete else f"NOT proved (node cap hit after {nodes} boxes)")
        print(f"  R({ps[0]}^a)R({ps[1]}^b)R({ps[2]}^c)=2 : solutions={sols}   [{verdict}]")

    print("\nSanity checks:")
    sols, nodes, complete = solve_fixed((2, 3))
    print(f"  R(2^a)R(3^b)=2   : {sols}  complete={complete}  (expect [(2, 3)], i.e. 108)")
    for P in (5, 7, 11):
        sols, nodes, complete = solve_fixed((2, 3, P))
        print(f"  R(2^a)R(3^b)R({P}^c)=2 : {sols}  complete={complete}  (expect none)")
