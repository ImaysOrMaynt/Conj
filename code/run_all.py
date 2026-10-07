"""
Smoke test: run every module's checks and assert the key facts hold.
Usage:  PYTHONPATH=code python3 code/run_all.py
"""
from fractions import Fraction
from conj import R_of, R_pp
from local_identities import D3_formula, D3_direct, v, vQ
from abundancy import min_omega_given_least_prime
from three_primes import solve_three, solve_fixed
from dickson import solve_free, Primes
from residual import search_target
from fast_verify import solutions_upto
from conj import primes_upto


def check(name, cond):
    print(f"  [{'PASS' if cond else 'FAIL'}] {name}")
    assert cond, name


print("conj / collapse:")
check("R(108) == 2", R_of(108) == 2)
check("R(2^2)*R(3^3) == 2", R_pp(2, 2) * R_pp(3, 3) == 2)

print("local identities:")
primes = primes_upto(500)
check("3-adic per-prime formula (p<=500, a=2..30)",
      all(D3_formula(p, a) == D3_direct(p, a) for p in primes for a in range(2, 31)))

print("abundancy (Prop 8):")
check("least-prime 5 -> omega>=7", min_omega_given_least_prime(5)[0] == 7)
check("least-prime 11 -> omega>=27", min_omega_given_least_prime(11)[0] == 27)

print("Theorems C, C' (case IIIb closed):")
sols23, _, complete23 = solve_fixed((2, 3))
check("branch-and-bound rediscovers 108: R(2^a)R(3^b)=2 <=> (a,b)=(2,3)",
      sols23 == [(2, 3)] and complete23)
planted = R_pp(3, 4) * R_pp(7, 3) * R_pp(11, 2)
check("branch-and-bound finds a planted solution (3^4 7^3 11^2)",
      (4, 3, 2) in solve_fixed((3, 7, 11), planted)[0])
for r in (7, 11, 13):
    sols, rigorous = solve_three(3, 5, r)
    check(f"R(3^a)R(5^b)R({r}^c)=2 has NO solution (rigorous)", sols == [] and rigorous)

print("free-prime Dickson prover (dickson.py):")
for k in (1, 2, 3, 4):
    sols, _, complete = solve_free(2, k, Primes(lo=3))
    check(f"no odd powerful solution with omega={k} (rigorous)", sols == [] and complete)
for k in (1, 2, 3):
    sols, _, complete = solve_free(Fraction(100, 91), k, Primes(lo=5))
    check(f"residual R(M)=100/91 has no M with omega(M)={k} (rigorous)", sols == [] and complete)
planted = R_pp(5, 3) * R_pp(13, 2) * R_pp(31, 4)
check("free-prime prover finds a planted solution (5^3 13^2 31^4)",
      ((5, 3), (13, 2), (31, 4)) in solve_free(planted, 3, Primes(lo=3))[0])

print("residual R(M)=100/91:")
check("no residual M coprime to 6 below 1e12", search_target(Fraction(100, 91), 10**12, 5, (2, 3)) == [])

print("structural verification:")
check("only powerful solution <= 1e12 is 108", solutions_upto(10**12) == [108])

print("\nALL CHECKS PASSED.")
