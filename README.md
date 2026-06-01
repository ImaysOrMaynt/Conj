# Conj — an attack on σ(n) = 2σ\*(n) ⟹ n ≡ 108 (mod 216)

R. Stephan's conjecture #35 / **OEIS A063880**: if `σ(n) = 2σ*(n)` (σ = sum of
divisors, σ\* = sum of *unitary* divisors), then `n ≡ 108 (mod 216)`.

> **Bottom line:** this is **not solved here**, and a full proof would be a major
> result — it is equivalent to bounding `ω(n)` for an abundancy-type equation,
> a problem of the same grade as odd / unitary perfect numbers. This repo records
> a genuine attack: the known reductions reproduced and checked, **new** structural
> results that close further sub-cases, and an independent computational
> verification. See [`notes/progress.md`](notes/progress.md) for the full write-up
> and an honest map of exactly where the wall is.

## What's here

- **`notes/progress.md`** — the main document: honest status, the reduction to the
  *Crux* (only powerful `m` with `R(m) = 2` is 108), new results, and the open kernel.
- **`notes/source_paper.{pdf,txt}`** — the "Powerful solutions" notes this builds on.
- **`code/`** — all claims are backed by exact (integer/`Fraction`) computation:
  - `conj.py` — `R(m) = σ(m)/σ*(m)`, prime-power arithmetic, `R(108) = 2`, the collapse.
  - `local_identities.py` — the 2-adic identity (Thm 6) **and the new 3-adic identity**, verified.
  - `abundancy.py` — Proposition 8 abundancy table, reproduced and extended.
  - `three_primes.py` — **Theorem C**: no powerful solution `3ᵃ·5ᵇ·7ᶜ` (rigorous squeeze).
  - `residual.py` — the `6 | m` residual `R(M) = 100/91` reductions and empty search.
  - `fast_verify.py` / `search.py` — structural rational search; verifies **108 is the
    only powerful solution `≤ X`** (independently confirmed to `10¹⁷`–`10¹⁸`).

## New contributions (all verified in `code/`)

1. A **3-adic local identity** for solutions, complementing the known 2-adic one.
2. **`6 | m ⟹ ω(m) = 2` (i.e. `m = 108`) or `ω(m) ≥ 5`** — so no solution has
   `6 | m` with `ω ∈ {3,4}`; every `ω = 3` solution has exactly one of 2, 3, and the
   odd case collapses to a finite family `{3ᵃ5ᵇrᶜ : r ∈ {7,11,13}}`.
3. **Theorem C:** there is no powerful solution of the form `3ᵃ·5ᵇ·7ᶜ`.
4. Independent verification that **108 is the only powerful solution `≤ 10¹⁷`** (run to `10¹⁸`).

## Run it

Everything is pure-Python standard library (no third-party deps):

```bash
PYTHONPATH=code python3 code/conj.py
PYTHONPATH=code python3 code/local_identities.py
PYTHONPATH=code python3 code/abundancy.py
PYTHONPATH=code python3 code/three_primes.py
PYTHONPATH=code python3 code/residual.py
PYTHONPATH=code python3 code/fast_verify.py 1e14   # argument is the height bound X
```
