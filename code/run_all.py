"""
Smoke test: run every module's checks and assert the key facts hold.
Usage:  PYTHONPATH=code python3 code/run_all.py
"""
from fractions import Fraction
from conj import R_of, R_pp
from local_identities import D3_formula, D3_direct, v, vQ
from abundancy import min_omega_given_least_prime
from three_primes import solve_three
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

print("Theorem C and IIIb families:")
sols357, rig357 = solve_three(3, 5, 7)
check("R(3^a)R(5^b)R(7^c)=2 has NO solution", sols357 == [])
check("...and the squeeze is rigorous (exponents provably bounded)", rig357 is True)
check("R(3^a)R(5^b)R(11^c)=2 none to cap", solve_three(3, 5, 11)[0] == [])
check("R(3^a)R(5^b)R(13^c)=2 none to cap", solve_three(3, 5, 13)[0] == [])

print("residual R(M)=100/91:")
check("no residual M coprime to 6 below 1e12", search_target(Fraction(100, 91), 10**12, 5, (2, 3)) == [])

print("structural verification:")
check("only powerful solution <= 1e12 is 108", solutions_upto(10**12) == [108])

print("\nALL CHECKS PASSED.")
