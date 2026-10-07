# Toward the Crux of σ(n) = 2σ*(n) ⟹ n ≡ 108 (mod 216)

*Working notes — an attack on R. Stephan's conjecture #35 / OEIS A063880, building
on the "Powerful solutions" notes.*

---

## 0. Honest status (read this first)

The conjecture is **σ(n) = 2σ\*(n) ⟹ n ≡ 108 (mod 216)**, where σ\* is the
sum of unitary divisors. As the source notes establish, this is *equivalent* to
the

> **Crux.** The only powerful number `m` with `R(m) = 2` is `m = 108 = 2²·3³`,
> where `R(m) := σ(m)/σ*(m) = ∏_{pᵃ‖m} (1+p+⋯+pᵃ)/(pᵃ+1)`.

and the Crux is in turn equivalent to: *every powerful solution has v₂ = 2 and
v₃ = 3*. I did **not** find a complete proof, and I want to be candid about why:
the residual difficulty is **controlling ω(m)** (the number of distinct primes).
Bounding `ω` for an abundancy-type target `σ/σ* = 2` is of the same grade as the
open problems on odd perfect and unitary perfect numbers; no current technique
supplies it, and the source notes already identify this wall. (Correction, §5.2: a
bound on `ω` is *not* known to make the Crux decidable by itself, contrary to the
source's Theorem 9 — when `2 | m` and `3 ∤ m` the exponent of 2 escapes Dickson's
method, and the smallest such case, IIIa at `ω = 3`, is open.) I therefore did
**not** manufacture a proof. Claiming one would be wrong.

What this document *does* contribute, all checked by exact computation in `code/`:

1. **A new local identity at the prime 3** (§2), complementing the known 2-adic
   identity. It fits a clean general "ℓ-adic obstruction" framework; ℓ = 2 and
   ℓ = 3 are the two cases with a closed form.
2. **Sharp small-ω structure** (§3): a clean corollary that **`6 | m` forces
   `ω(m) = 2` (i.e. `m = 108`) or `ω(m) ≥ 5`** — so *no* solution has `6 | m` with
   `ω ∈ {3,4}`. Combined with the abundancy bound this pins the shape of every
   `ω = 3` solution and reduces the odd case to a **finite** family.
3. **A closed case: IIIb is empty.** There is **no powerful solution with
   `ω(m) = 3`, `3 | m`, `2 ∤ m`** — the three families `3ᵃ·5ᵇ·7ᶜ`, `3ᵃ·5ᵇ·11ᶜ`,
   `3ᵃ·5ᵇ·13ᶜ` are each ruled out by an exact squeeze (Theorems C, C′, §3.3). So
   every `ω = 3` solution has the form `2ᵃqᵇrᶜ` with `3 ∤ m` (IIIa). The squeeze is
   implemented as a branch-and-bound that provably terminates for *any* fixed set
   of primes, so fixed-prime families are never the obstruction.
4. **Independent verification** that 108 is the only powerful solution
   `≤ 10¹⁷` (and a run to `10¹⁸` reproducing the OEIS record), via a structural
   rational search rather than naïve enumeration (§4).
5. **Reproduction and extension** of the abundancy table (§4) and an exact check
   that the `6 | m` residual `R(M) = 100/91` has no solution in range.

Everything below is either a recap (clearly marked), a result with a proof, or a
computational statement with the script that produces it.

*Literature check (2026-10-07):* the `openai/math` collection (722 model-generated
manuscripts, released 2026-10-06) contains nothing on `σ*`, unitary or odd perfect
numbers, or A063880 (full-text search of all its sources).

---

## 1. Setup and the reduction (recap)

For `n = ∏ pᵢ^{aᵢ}`, σ is multiplicative with `σ(pᵃ) = 1+p+⋯+pᵃ`, and σ\* is
multiplicative with `σ*(pᵃ) = pᵃ + 1` (the two unitary divisors `1`, `pᵃ`). Hence
`R = σ/σ*` is multiplicative with

```
R(pᵃ) = (1 + p + ⋯ + pᵃ)/(pᵃ + 1) = (p^{a+1} − 1)/((p−1)(pᵃ + 1)).
```

Elementary facts (Lemma 1 of the source): `R(p) = 1`; `R(pᵃ)` is strictly
increasing in `a`; `1 < R(pᵃ) < p/(p−1)` for `a ≥ 2`, with `R(pᵃ) ↑ p/(p−1)`.
Because `R(p) = 1`, squarefree prime factors are invisible: `R(n) = R(m)` for the
**powerful core** `m` of `n`. So `σ(n) = 2σ*(n) ⟺ R(m) = 2`, and the Crux ⟹ every
solution is `108·s` with `s` squarefree, coprime to 6 ⟹ `n ≡ 108 (mod 216)`.

**The collapse (recap).** `R(2²)·R(3³) = (7/5)·(10/7) = 2` *exactly*. So if a
powerful solution has `4 ‖ m` and `27 ‖ m`, writing `m = 2²·3³·M` gives
`R(m) = 2·R(M)`, forcing `R(M) = 1`, hence `M = 1` and `m = 108`. Thus
`2²·3³` exactly exhausts the budget `R = 2`. (Verified: `code/conj.py`.)

### 1.1 The conjecture *is* the Crux — so the targets are local, not families

The conjecture is `n ≡ 108 (mod 216)`. By CRT (`216 = 8·27`) this is
`v₂(n) = 2` **and** `27 | n`, and since both involve exponents `≥ 2` they are
conditions on the powerful core: `v₂(m) = 2` and `v₃(m) ≥ 3`. Note we need only
`v₃ ≥ 3`, **not** `v₃ = 3`, and **not** "no other primes." But those two *local*
conditions already force everything:

> **Proposition 0 (the local conditions are the whole conjecture).** If `m` is
> powerful with `R(m) = 2`, `v₂(m) = 2`, and `v₃(m) ≥ 3`, then `m = 108`.
>
> *Proof.* `R(m) = R(2²)·R(3^{v₃})·R(rest) = (7/5)·R(3^{v₃})·R(rest)` with `rest`
> powerful and coprime to 6. As `R` is strictly increasing, `v₃ ≥ 3 ⟹
> R(3^{v₃}) ≥ R(3³) = 10/7`, and `R(rest) ≥ 1`. Hence `2 = R(m) ≥ (7/5)(10/7)(1)
> = 2`, so equality holds throughout: `R(3^{v₃}) = 10/7` (so `v₃ = 3`) and
> `R(rest) = 1` (so `rest = 1`). Therefore `m = 2²·3³ = 108`. ∎

So **conjecture ⟺ Crux** (they are equivalent, not merely one-way), and the
equivalence has a payoff: a proof never has to bound `ω(m)` or rule out large
primes — the budget step does that for free. The whole problem collapses to
**local divisibility**:

> **conjecture ⟺ every powerful solution `m` satisfies `2 | m`, `3 | m`, and
> `v₃(m) ≠ 2`.**

Indeed, once `6 | m`, the source's Theorem 4 gives `v₂ = 2` and `v₃ ∈ {2,3}`;
Proposition 0 turns `v₃ = 3` into `m = 108`; so only three global lemmas remain,
**none mentioning `ω`**:

- **(α)** no powerful solution is odd (`2 | m`);
- **(β)** every powerful solution is divisible by 3 (`3 | m`);
- **(γ)** no solution has `v₃(m) = 2` — equivalently `R(M) = 100/91` is unsolvable
  for powerful `M` coprime to 6.

This is the correct way to aim the attack: prove (α), (β), (γ) as divisibility
statements, **not** by enumerating `ω = 2, 3, …` families. §3.4 records where each
stands.

---

## 2. A new local identity at the prime 3

For a solution, `R(m) = 2`, so for **every** prime ℓ, `v_ℓ(R(m)) = v_ℓ(2)`, i.e.
`0` for odd ℓ and `1` for ℓ = 2. Expanding `v_ℓ(R(m)) = Σ_{pᵃ‖m} D_ℓ(p,a)` with
`D_ℓ(p,a) := v_ℓ(σ(pᵃ)) − v_ℓ(pᵃ+1)` and computing each `D_ℓ` by lifting-the-
exponent (LTE) gives an identity in the *exponents*. Two primes have a clean
closed form: ℓ = 2 (the source's Theorem 6) and ℓ = 3 (new, here).

### 2.1 The per-prime 3-adic contribution

> **Lemma (3-adic local term).** For a prime `p ≠ 3` and `a ≥ 1`,
> ```
> D₃(p,a) = v₃(σ(pᵃ)) − v₃(pᵃ+1) =
>     v₃(a+1)                  if p ≡ 1 (mod 3),
>     0                         if p ≡ 2 (mod 3) and a even,
>     v₃(a+1) − v₃(a)           if p ≡ 2 (mod 3) and a odd,
> ```
> and `D₃(3,a) = 0`.

*Proof.* Write `ord₃(p) =: d ∈ {1,2}` (the order of `p` mod 3); `d = 1 ⇔ p ≡ 1`,
`d = 2 ⇔ p ≡ 2`.

- `p ≡ 1 (mod 3)` (`d=1`). Then `pᵃ ≡ 1`, so `pᵃ+1 ≡ 2`, `v₃(pᵃ+1)=0`. And
  `σ(pᵃ) = (p^{a+1}−1)/(p−1)`; since `3 | p−1`, LTE gives
  `v₃(p^{a+1}−1) = v₃(p−1) + v₃(a+1)`, so `v₃(σ(pᵃ)) = v₃(a+1)`. Hence
  `D₃ = v₃(a+1)`.

- `p ≡ 2 (mod 3)` (`d=2`), `a` even. Then `pᵃ ≡ 1`, so `v₃(pᵃ+1)=0`; and
  `p^{a+1} ≡ p ≡ 2`, so `p^{a+1}−1 ≡ 1`, `v₃(σ(pᵃ)) = 0`. Hence `D₃ = 0`.

- `p ≡ 2 (mod 3)`, `a` odd. Then `3 | p+1`. By LTE (odd exponent),
  `v₃(pᵃ+1) = v₃(p+1) + v₃(a)`. For σ, write `a+1 = 2t` (even); using `p² ≡ 1`,
  `v₃(p^{a+1}−1) = v₃(p²−1) + v₃(t) = v₃(p+1) + v₃(a+1)` (as `v₃(t)=v₃(a+1)`),
  and `v₃(p−1)=0`, so `v₃(σ(pᵃ)) = v₃(p+1) + v₃(a+1)`. Hence
  `D₃ = v₃(a+1) − v₃(a)`.

- `p = 3`: `σ(3ᵃ) ≡ 1 (mod 3)` and `3ᵃ+1 ≡ 1 (mod 3)`, both `v₃ = 0`. ∎

(Checked directly against `v₃(σ(pᵃ)) − v₃(pᵃ+1)` for every prime `p ≤ 2000`
and `2 ≤ a ≤ 40` in `code/local_identities.py`: **all match**.)

### 2.2 The identity

> **Proposition (3-adic identity for solutions).** If `R(m) = 2` then
> ```
>   Σ_{p≡1(3)} v₃(aₚ+1)  +  Σ_{p≡2(3), aₚ odd} ( v₃(aₚ+1) − v₃(aₚ) )  =  0.   (★)
> ```

*Proof.* Sum the Lemma over `pᵃ ‖ m`; the total is `v₃(R(m)) = v₃(2) = 0`. ∎

Verified on 4000 random powerful `m` that `Σ D₃ = v₃(R(m))` exactly
(`code/local_identities.py`).

### 2.3 What (★) says

The only **negative** terms come from primes `p ≡ 2 (mod 3)` whose exponent is an
*odd multiple of 3* (i.e. `aₚ ≡ 3 (mod 6)`), contributing `−v₃(aₚ)`. The **positive**
terms come from `p ≡ 1 (mod 3)` with `3 | aₚ+1`, and from `p ≡ 2 (mod 3)`, `aₚ`
odd with `3 | aₚ+1`. So (★) is a balance:

> **Corollary.** If no prime `p ≡ 2 (mod 3)` divides `m` to an exponent `≡ 3 (mod 6)`,
> then every prime `p ≡ 1 (mod 3)` has `aₚ ≢ 2 (mod 3)` and every prime
> `p ≡ 2 (mod 3)` with odd exponent has `aₚ ≢ 2 (mod 3)`.

For `m = 108 = 2²·3³`: prime 2 (`≡2`, exponent 2 even) contributes 0, prime 3
contributes 0, and (★) reads `0 = 0`. The identity is a genuine sieve on exponent
residues but, like the 2-adic one, does **not** bound `ω` — see §5.

---

## 3. Sharp structure for small ω

### 3.1 `6 | m` forces `ω ∈ {2} ∪ [5,∞)`

> **Proposition A (new corollary of the source's Theorem 4).** If `m` is a powerful
> solution with `6 | m`, then either `m = 108` (so `ω(m) = 2`) or `ω(m) ≥ 5`.

*Proof.* Theorem 4 of the source: a powerful solution with `6 | m` has `v₂(m) = 2`
and `v₃(m) ∈ {2,3}` (if `v₂ ≥ 3` then `R(m) ≥ R(2³)R(3²) = (5/3)(13/10) = 13/6 > 2`).
If `v₃ = 3`, then `m = 2²3³M` with `R(M) = 1`, so `M = 1` and `m = 108`. If
`v₃ = 2`, then `m = 2²3²M` with `M` powerful, coprime to 6, and
`R(M) = 2/(R(2²)R(3²)) = 2/(91/50) = 100/91`; the source shows every such `M` has
`ω(M) ≥ 3`. Then `ω(m) = 2 + ω(M) ≥ 5`. ∎

In particular **no solution has `6 | m` and `ω ∈ {3,4}`.**

### 3.2 Every `ω = 3` solution has exactly one of 2, 3 as a factor; the odd case is finite

The abundancy bound (Proposition 8 of the source, reproduced/extended in
`code/abundancy.py`): since `R(pᵃ) < p/(p−1)`,
```
∏_{p|m} p/(p−1) > 2.
```
If `m` is coprime to 6 this forces `ω(m) ≥ 7`. Together with Proposition A:

> **Proposition B.** A powerful solution with `ω(m) = 3` has **exactly one** of 2, 3
> dividing `m`. Writing the three primes as the cases below:
>
> - **(IIIa) `2 | m`, `3 ∤ m`:** `m = 2ᵃ qᵇ rᶜ`, `5 ≤ q < r`. *(Abundancy gives no
>   restriction on `q, r` — the prime 2 alone supplies the factor 2.)*
> - **(IIIb) `3 | m`, `2 ∤ m`:** `m = 3ᵃ qᵇ rᶜ`, and abundancy
>   `(3/2)(q/(q−1))(r/(r−1)) > 2` forces `(q,r) ∈ {(5,7), (5,11), (5,13)}` —
>   a **finite** family, and in fact an **empty** one (Theorems C, C′, §3.3).

(Both bullet computations: `code/` — the IIIb enumeration returns exactly those
three pairs; IIIa returns an unbounded list.)

### 3.3 Theorems C, C′: case IIIb is empty

> **Theorem C (new).** The equation `R(3ᵃ)R(5ᵇ)R(7ᶜ) = 2` has **no** solution with
> `a,b,c ≥ 2`. Equivalently, no powerful solution has core `3ᵃ·5ᵇ·7ᶜ`.

*Proof (exact interval squeeze; `code/three_primes.py`).* Use `R(p²) ≤ R(pᵉ) < p/(p−1)`,
`R` strictly increasing.

- **Exponent of 3 is forced to `a = 3`.** Feasibility needs
  `R(5²)R(7²) ≤ 2/R(3ᵃ) < (5/4)(7/6)`. The lower bound `2/R(3ᵃ) ≥ R(5²)R(7²) =
  (31/26)(57/50) = 1767/1300` gives `R(3ᵃ) ≤ 2·1300/1767 = 2600/1767 ≈ 1.4715 < 3/2`,
  so `a` is **bounded**; explicitly `R(3³) = 10/7 ≈ 1.4286 ≤ 1.4715 < R(3⁴) ≈ 1.4756`,
  and the upper bound `2/R(3ᵃ) < 35/24` gives `R(3ᵃ) > 48/35 ≈ 1.3714 > R(3²)=1.3`,
  so `a ∉ {2}`. Hence `a = 3`.
- **No exponent of 5 works.** With `a = 3`, `R(5ᵇ)R(7ᶜ) = 2/R(3³) = 7/5`. Then
  `R(5ᵇ) = (7/5)/R(7ᶜ)` with `R(7ᶜ) ∈ [R(7²), 7/6) = [57/50, 7/6)`, so
  `R(5ᵇ) ∈ (6/5, 70/57] = (1.2, 1.22807…]`. But `R(5²) = 31/26 = 1.1923… < 1.2`
  and `R(5³) = 26/21 = 1.2381… > 70/57`, with `R(5ᵇ)` increasing. No `b` lands in
  the interval. ∎

> **Theorem C′ (new).** Neither `R(3ᵃ)R(5ᵇ)R(11ᶜ) = 2` nor `R(3ᵃ)R(5ᵇ)R(13ᶜ) = 2`
> has a solution with `a,b,c ≥ 2`. With Theorem C and Proposition B: **case IIIb is
> empty** — no powerful solution has `ω(m) = 3`, `3 | m`, `2 ∤ m`.

The trick is the order of elimination: squeezing the exponent of 3 first is vacuous
here (see the remark below), but splitting on the exponent of **5** first closes both.
Write `X = R(3ᵃ) ∈ [13/10, 3/2)`, `Y = R(5ᵇ) ∈ [31/26, 5/4)`; all steps are exact
(`code/three_primes.py`, and every inequality below was re-checked in `Fraction`s).

*Proof for `3·5·11`* (`Z = R(11ᶜ) ∈ [133/122, 11/10)`).
- `b = 2` is impossible: `XZ = 2/R(5²) = 52/31 > 33/20 = (3/2)(11/10) > XZ`.
- So `b ≥ 3`, `Y ∈ [26/21, 5/4)`, `XZ ∈ (8/5, 21/13]`, hence
  `X ∈ (16/11, 366/247] = (1.4545…, 1.4817…]`. As `R(3³) = 10/7 < 16/11` and
  `R(3⁵) = 91/61 > 366/247`, this forces `a = 4`, `X = 121/82`.
- Then `YZ = 164/121`, so `Y ∈ (1640/1331, 20008/16093] = (1.2321…, 1.2432…]`, which
  contains only `R(5³) = 26/21` (`R(5²) < 1.2321`, `R(5⁴) = 781/626 > 1.2433`): `b = 3`.
- Then `Z = 1722/1573 = 1.09472…`, strictly between `R(11²) = 133/122` and
  `R(11³) = 122/111`. No `c`. ∎

*Proof for `3·5·13`* (`W = R(13ᶜ) ∈ [183/170, 13/12)`).
- `b = 2` is impossible: `XW = 52/31 > 13/8 = (3/2)(13/12)`.
- `b = 3`: `XW = 21/13`. If `c = 2` then `X = (21/13)(170/183) > 3/2`, impossible. If
  `c ≥ 3` then `X ∈ (252/169, 3297/2210] = (1.49112…, 1.49185…]`, which contains only
  `R(3⁵) = 91/61 = 1.49180…`; then `W = 183/169 = 1.08284…`, strictly between
  `R(13³) = 170/157` and `R(13⁴) = 30941/28562`. No `c`.
- `b = 4`: `XW = 2/R(5⁴) = 1252/781`, so `X ∈ (1.47976…, 1.48919…]`, strictly between
  `R(3⁴) = 1.47561…` and `R(3⁵) = 1.49180…`. No `a`.
- `b ≥ 5`: `Y ∈ [R(5⁵), 5/4) = [651/521, 5/4)`, so `X ∈ (96/65, 1.48691…]
  = (1.47692…, 1.48691…]`, again strictly between `R(3⁴)` and `R(3⁵)`. No `a`. ∎

**Remark (why the first squeeze stalled; fixed primes are never the wall).** The first
version of this section eliminated the exponent of 3 first. For `(3,5,11)` and
`(3,5,13)` its bound `R(3ᵃ) ≤ 2/(R(5²)R(p²))` exceeds `3/2`, so it bounds nothing; I
recorded those families as "verified to exponent 20000" and read this as the global
obstruction in miniature. That was wrong — it was only a bad elimination order.
`code/three_primes.py` now runs a branch-and-bound over exponent boxes: split the
widest open coordinate into `{e}` and `{e+1, e+2, …}`, and discard a box whose exact
range misses 2 (the upper end excluded while some exponent is open). Extending `R` by
`R(p^∞) = p/(p−1)` makes the exponent space compact, and the search provably
terminates for **every** fixed set of primes and every target (argument in the
module docstring): the three IIIb families close after 7, 13 and 17 boxes, and the
same code rediscovers `108` as the unique solution over `{2, 3}`. The genuine
obstruction is primes that are **not** fixed — e.g. IIIa, where `q, r` range over all
primes `≥ 5` (§5.2).

### 3.4 Status of the three local targets (α), (β), (γ)

By Proposition 0 (§1.1) the conjecture is equivalent to `(α) 2|m`, `(β) 3|m`,
`(γ) v₃(m)≠2` for every powerful solution `m`. This reframing is the right one —
it eliminates the false goal "bound `ω`" — but it does **not** make the wall
vanish; it concentrates it into each target:

- **(α) `2 | m`** ⟺ no *odd* powerful solution. An odd solution is exactly a
  powerful `m` coprime to 2 with `∏_{p|m} R(pᵃ) = 2` — an abundancy-`2` equation in
  odd primes with no a-priori bound on the number of primes. So (α) is the original
  difficulty restricted to odd `m`; the 2-adic identity is consistent with odd `m`
  (it never sees `v₂`), and Theorem D's construction can be made odd, so no local
  invariant kills it.
- **(β) `3 | m`** ⟺ no powerful solution coprime to 3 — again abundancy-`2` over
  primes `≠ 3`, unbounded prime count. The 3-adic identity (★) is satisfiable with
  `3 ∤ m` (e.g. Theorem D's `m_K`), so it does not force `3 | m`.
- **(γ) `v₃ ≠ 2`** ⟺ `R(M) = 100/91` unsolvable for `M` coprime to 6 — abundancy
  with target `100/91`, again unbounded prime count (large primes contribute
  `≈ 1`). Its nontrivial denominator `91 = 7·13` forces `7,13 | σ*(M)` but does not
  pin a unique prime, so a Pomerance-`93/40`-style argument does not obviously apply.

**Honest assessment.** The weakening clarifies the goal and removes any need to
control large primes *in the conclusion*, but each of (α),(β),(γ) is itself an
"abundancy = constant with unbounded `ω`" statement — the same wall, now in three
sharp pieces. If a proof exists, the most likely entry point is (α) or (β): a
*global* obstruction to a solution avoiding a single small prime (a parity/character
or genus-type argument peculiar to the missing prime), which is a different kind of
statement from "bound `ω`." I did not find one. I record this as the precise open
problem rather than a case ladder.

### 3.5 An honest attempt at (α) and (β), and why the local route is closed

I tried to prove (α) "no odd solution" and (β) "`3 ∣ m`" directly. Every natural
obstruction turns out to be *consistent* with avoiding the prime, and this can be
made into a theorem — a barrier specific to (α) and (β):

> **Theorem E (local invariants don't force `2 ∣ m` or `3 ∣ m`).** For every `K`:
> (a) there is an **odd** powerful `m` with `ω(m) ≥ K` satisfying the two-sided
> abundancy window and both the 2-adic and 3-adic identities; (b) likewise there is
> a powerful `m` **coprime to 3** with `ω(m) ≥ K` satisfying all three. Hence no
> argument from those invariants can prove (α) or (β).

*Proof.* (b) is Theorem D verbatim: its `m_K = 2²·p_1^{e_1}·p_2²⋯p_{K−1}²` with all
`p_i ≡ 2 (mod 3)` is already coprime to 3. (a) Drop the `2²` and rebalance: take the
prime set `{3,5,7} ∪ {K−3` large odd primes`}` (so `∏ p/(p−1) ≥ (3/2)(5/4)(7/6) =
35/16 > 2`, and `∏ R(p²) = (13/10)(31/26)(57/50)·∏_{large}R(p²) ≤ 2` once the large
primes are big enough that `∏_{large} R(p²) ≤ 10·16/(35·… ) `, i.e. their reciprocal
sum is small). Give one large prime `≡ 2 (mod 3)` an odd exponent `e` with
`v₂(e+1)=1+ω` and `e ≡ 1 (mod 3)` (possible by choosing the odd part of `e+1` mod 3);
give every prime `≡ 1 (mod 3)` an even exponent `≡ 1 (mod 3)` (e.g. `4`, so
`3∤a+1`); give the rest exponent `2`. Then `O` is the single odd-exponent prime, the
2-adic identity reads `v₂(e+1)=1+ω`, and every 3-adic term `D₃(p,a)` vanishes, so
(★) holds. `m` is odd, powerful, `ω = K`. ∎

The moral: the 2-adic and 3-adic identities, and abundancy, are **blind to the
presence of any single small prime** — they constrain *exponents and prime counts*,
never *which* primes occur. So (α) and (β) cannot be theorems of these invariants;
they would require a genuinely global mechanism (e.g. forcing a specific small prime
to divide `σ*(m)` and then to divide `m`, of the kind that closes Pomerance's
`93/40` but is not available for the denominator-`1` target `2`). I did not find such
a mechanism, and I do not believe one is currently within reach — this is the same
barrier, honestly located. The conjecture is, as far as method goes, of odd /
unitary-perfect grade.

---

## 4. Computational verification (independent)

All via the structural rational search in `code/fast_verify.py` (exact `R`; the
only float is a pruning *over-estimate* inflated by a safety margin, so the search
can only over-explore — never miss a solution). It enumerates powerful `m ≤ X`
with `R(m) = 2` by walking primes in increasing order and pruning any branch whose
optimistic reachable `R` falls below 2.

| bound `X` | only solution | method |
|---|---|---|
| `10⁸`  | 108 | naïve powerful-number enumeration (`code/conj.py`) — cross-check |
| `10¹⁴` | 108 | structural search, ~5 s |
| `10¹⁷` | 108 | structural search, ~158 s |
| `10¹⁸` | 108 | structural search (reproduces the OEIS/Eldar record) |

**Residual.** `R(M) = 100/91` with `M` powerful, coprime to 6 — searched with the
same engine (`code/residual.py`): **no solution** with `M ≤ 10¹⁴` (i.e. `36M ≤
3.6·10¹⁵`). Confirmed exactly that primes `≤ 7` cannot divide `M` (`R(5²), R(7²) >
100/91`) and that `100/91` lies strictly between `R(11²) = 133/122` and
`R(11³) = 122/111`, so `ω(M) ≥ 2`, consistent with the source's `ω(M) ≥ 3`.

**Abundancy table** (`code/abundancy.py`), reproducing the source row and extending it:

| least prime of `m` | 5 | 7 | 11 | 13 | 17 | 19 | 23 | 29 | 31 | 37 | 41 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| forces `ω(m) ≥` | 7 | 15 | 27 | 41 | 62 | 85 | 115 | 150 | 186 | 229 | 274 |

The complementary "upper window" `∏_{p|m} R(p²) ≤ 2` does **not** cap `ω`: the
product of `R(p²)` over the first 1000 primes `≥ 101` is only `≈ 1.93`, growing like
`log`.

---

## 5. The open kernel — why ω is the wall

Every result above is consistent with, and circles, one missing bound. Concretely:

- **Lower abundancy** `∏_{p|m} p/(p−1) > 2` bounds only the *least* prime, not the
  count. With `2 | m` the factor `2/1 = 2` already meets the bound, leaving the
  remaining primes free to be arbitrarily many and large.
- **Upper window** `∏_{p|m} R(p²) ≤ 2` cannot cap `ω` because `R(p²) → 1`.
- **Local identities** (§2 and the 2-adic Theorem 6) constrain exponent *residues*
  but are invisible to the *number* of primes.
- **Logarithmically**, `Σ_{p|m} 1/p ≈ ln 2`, and a single small prime (the prime 2,
  with `R(2ᵃ) = 2 − 3/(2ᵃ+1) ↑ 2`) can absorb almost the whole budget, leaving
  `ω − 1` arbitrarily large primes contributing `≈ 0`.

This is the same wall that leaves **unitary perfect numbers** open (Subbarao–Warren
1966) and that makes the abundancy target `σ/σ* = 2 = 2/1` "hard" — its denominator
1 imposes no constraint, unlike Pomerance's `93/40` (solutions `{80, 200}`), which
closes only because the denominator 40 forces specific small primes. (An earlier
version cited a "microcosm" here — `3·5·7` closing while `3·5·11`, `3·5·13` did not;
that was an artifact of elimination order, and all three close, §3.3. With the
primes fixed there is no wall at all: it lives entirely in primes that can escape to
`∞` while a small prime absorbs the budget.)

The source's one-line summary was: *the Crux is decidable the moment `ω(m)` is
bounded (Dickson + linear forms in logs), and bounding `ω(m)` is the whole problem.*
The first half needs a correction — see §5.2.

### 5.1 A barrier theorem: the standard invariants provably cannot bound ω

The four bullets above are not just "we haven't managed it." One can *prove* that
the entire toolkit of **local** invariants — the two-sided abundancy window, the
2-adic identity, and the new 3-adic identity (★) — is logically too weak to force a
bound on `ω`. So any proof of the Crux must use something genuinely non-local.

> **Theorem D (local invariants do not bound ω).** For every `K` there is a powerful
> integer `m_K` with `ω(m_K) ≥ K` that simultaneously satisfies every condition that a
> solution of `R(m)=2` must satisfy of the following "local" type:
> 1. the two-sided abundancy window `∏_{p|m_K} R(p²) ≤ 2 < ∏_{p|m_K} p/(p−1)`;
> 2. the 2-adic identity `Σ_{P odd, e_P odd} v₂(e_P+1) = 1 + ω_odd(m_K)` (Thm 6);
> 3. the 3-adic identity (★).
>
> Consequently, no theorem deduced solely from (1)–(3) can imply `ω(m) ≤ B` for any
> constant `B`, and in particular none can prove the Crux.

*Proof.* Fix `K`. By Dirichlet there are infinitely many primes `≡ 2 (mod 3)`; pick
`K−1` of them, `p_1 < ⋯ < p_{K−1}`, all so large that `∏_{i} p_i/(p_i−1) ≤ 10/7`
(possible since the tail of `∑ 1/p` is arbitrarily small). Put

```
   m_K = 2² · p_1^{e_1} · p_2² · p_3² · ⋯ · p_{K−1}²,
```

where the exponent `e_1` is chosen as follows: take `e_1` odd with `v₂(e_1+1) = K`
and `e_1 ≡ 1 (mod 3)`. Such `e_1` exists — write `e_1+1 = 2^K t` with `t` odd; then
`e_1 ≡ 1 (mod 3)` becomes `(−1)^K t ≡ 2 (mod 3)`, solvable for `t ∈ {1,5}` according
to the parity of `K`. `m_K` is powerful (all exponents `≥ 2`) and `ω(m_K) = K`.

- **(1)** `∏ p/(p−1) = 2 · ∏_i p_i/(p_i−1) > 2`. And `∏ R(p²) = R(2²) · ∏_i R(p_i²) <
  (7/5) · ∏_i p_i/(p_i−1) ≤ (7/5)(10/7) = 2`. ✓
- **(2)** The only odd prime of `m_K` with an odd exponent is `p_1` (the others have
  exponent 2); so `O = {p_1}` and `Σ_{O} v₂(e+1) = v₂(e_1+1) = K = 1 + (K−1) =
  1 + ω_odd(m_K)`. ✓
- **(3)** Every `p_i ≡ 2 (mod 3)`. For `i ≥ 2` the exponent 2 is even, so its 3-adic
  term `D₃(p_i,2) = 0`. For `p_1` (`≡ 2`, exponent `e_1` odd) the term is
  `v₃(e_1+1) − v₃(e_1)`; since `e_1 ≡ 1 (mod 3)` we have `3 ∤ e_1` and `3 ∤ e_1+1`,
  so the term is `0`. The prime 2 (`≡ 2 (mod 3)`, even exponent) also contributes `0`.
  Hence the left side of (★) is `0`. ✓ ∎

Theorem D is the rigorous form of "the prime 2 frees the budget": once `2² ‖ m`, the
factor `7/5` it costs in the upper window leaves exactly the room `10/7` that an
unbounded supply of large primes can fill while *all* the residue/valuation
bookkeeping stays consistent. The genuine equation `R(m) = 2` is a single
*global* rational identity that these local shadows cannot see. (Theorem D does
**not** include the cyclotomic entanglement of Thm 7, a semi-global condition; but
no bound on `ω` is known even with it, and the convergent powerful-number heuristic
— not any provable inequality — is what underwrites the belief in finiteness.)

### 5.1′ Free-prime Dickson prover: new small-ω exclusions

`code/dickson.py` extends the §3.3 branch-and-bound to free primes (chosen in
increasing order; an unchosen block of `j` primes `≥ P` contributes a factor in
`(1, ∏_{i<j} qᵢ/(qᵢ−1))`; the last prime is solved in closed form from
`R(qᵉ) − 1 ∈ (1/(q+1), 1/(q−1))`). Exact arithmetic; it terminates — and its "none"
is then a proof — unless a two-sided limit hits the target exactly (§5.2), in which
case its node cap trips. Results (all in `code/run_all.py` except the per-`a` runs):

- **No odd powerful solution has `ω(m) ≤ 5`** (`ω ≤ 4` in `run_all.py`; `ω = 5` takes
  1.30M nodes, ~40 s: `solve_free(2, 5, Primes(lo=3))`).
- **No powerful solution coprime to 6 has `ω(m) ≤ 8`** (abundancy alone gives `≥ 7`;
  `ω = 7` takes 1001 nodes, `ω = 8` takes 1.85M nodes, ~1 min:
  `solve_free(2, k, Primes(lo=5))`). So a counterexample coprime to 6 needs `ω ≥ 9`.
- **The residual `R(M) = 100/91` has no solution with `ω(M) ≤ 4`** (source: `≥ 3`; `ω ≤ 3`
  in `run_all.py`, `ω = 4` takes 3.69M nodes, ~100 s), so a `6 | m` counterexample needs
  `ω(m) ≥ 7`. (`ω(M) = 5` did not finish within 10⁸ nodes.)
- **IIIa** `2ᵃqᵇrᶜ` (`3 ∤ m`): no solution for each `2 ≤ a ≤ 22` (exact, per `a`), well
  beyond the `a ≲ 12` implied by the `10¹⁸` search. Not a proof for all `a` (§5.2).

### 5.2 Correction: Dickson's method needs more than bounded ω when 2 | m, 3 ∤ m

The source's Theorem 9 ("Dickson's 1913 method carries over verbatim: for each fixed
`k`, effectively finitely many powerful solutions with `ω(m) = k`") and the one-liner
above overstate what Dickson's method gives here.

Dickson's argument passes to a limit along a hypothetical infinite sequence of
solutions with `ω = k`: each prime either stabilises (with a stable exponent, or an
exponent `→ ∞`, contributing `p/(p−1)`) or tends to `∞` (contributing `R → 1`), and
the limit must equal the target exactly. Saturating exponents approach from below and
escaping primes from above, so the only dangerous limits are **two-sided** ones (some
exponent saturating *and* some prime escaping). For odd perfect numbers Dickson kills
these: clearing denominators, the largest saturated prime divides one side but not
the other. Here:

- **For `p = 2` there is nothing to kill.** `R(2ᵃ) ↑ 2`, which *is* the target, so
  "`a → ∞` and every other prime `→ ∞`" is a consistent two-sided limit, and the
  recursion cannot bound the odd primes — the same phenomenon that lets even perfect
  numbers `2ᵃ(2^{a+1}−1)` form a potentially infinite family, and why Dickson's
  theorem has to be restricted to *odd* perfect numbers. Theorem 4 pins `v₂ = 2` when
  `6 | m`, so the gap is exactly the solutions with `2 | m`, `3 ∤ m`. The smallest
  instance is **IIIa**, `m = 2ᵃqᵇrᶜ`: for each fixed `a` only finitely many `(q, r)`
  are possible (`R(qᵇ)R(rᶜ) = 1 + 3/(2^{a+1}−1)` with `R(q²) < R(qᵇ)R(rᶜ) <
  (q/(q−1))²` forces `(2^{a+1}−4)/3 < q < (2^{a+2}+3)/3`), but nothing bounds `a`.
  So IIIa is open **even though `ω = 3` is fixed**.
- **Even for odd `m` the transfer is not verbatim.** For `σ*` the largest saturated
  prime may divide some `pᵉ + 1` on the other side, so Dickson's closing step fails.
  The recursion still decides a fixed `ω` *provided* no two-sided limit hits 2
  exactly, but that has to be checked rather than assumed. (For a fixed *set* of
  primes there is no escaping prime, which is why the branch-and-bound of §3.3
  always terminates.)

Corrected summary: **with `ω` bounded, the cases `2 ∤ m` and `6 | m` reduce to
Dickson-type recursions (modulo the two-sided check); the case `2 | m`, `3 ∤ m` needs
a new idea already at `ω = 3`.**

---

## 6. What would actually close it

In rough order of plausibility:

1. **An `ω` bound for the target `2`** — necessary, but by §5.2 not known to be
   sufficient on its own: it would settle `2 ∤ m` and `6 | m` (Dickson, modulo the
   two-sided check), not `2 | m`, `3 ∤ m`. This is the genuine open problem.
2. **Close (IIIa)** `2ᵃ qᵇ rᶜ` (`q,r ≥ 5`, `3 ∤ m`): now the **only** open `ω = 3`
   case (IIIb is empty, §3.3), and the smallest instance of the prime-2 obstruction
   of §5.2 — so not a finite check. What is needed is a bound on `a` (e.g. via a
   primitive-prime/Zsigmondy entanglement between `2^{a+1}−1`, `2ᵃ+1` and
   `qᵇ+1`, `rᶜ+1`); that would settle `ω = 3` outright.
3. ~~**Finish IIIb**~~ — done (Theorem C′, §3.3).
4. **Sharpen the residual** `R(M) = 100/91` to empty, removing the `v₃ = 2` branch of
   the `6 | m` case and proving `6 | m ⟹ m = 108`.

Item 4 is concrete; items 1 and 2 are the deep ones, of different kinds (a bound on
the number of primes vs. a bound on the exponent of 2).

---

### Reproducing everything

```
PYTHONPATH=code python3 code/conj.py             # core identities, R(108)=2
PYTHONPATH=code python3 code/local_identities.py # 2-adic (Thm 6) + new 3-adic, verified
PYTHONPATH=code python3 code/abundancy.py        # Prop 8 table, reproduced + extended
PYTHONPATH=code python3 code/three_primes.py     # Theorems C, C': case IIIb empty
PYTHONPATH=code python3 code/residual.py         # R(M)=100/91 reductions + empty search
PYTHONPATH=code python3 code/fast_verify.py 1e14 # only 108 below X (rigorous prune)
```
