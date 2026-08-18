# TDD v2 — Feedback Disposition and Change Plan

Audit of the current draft against the 21 v1.0 review comments in
`docs/SC 2026 Documentation Feedback.csv`, plus new findings of the same class
introduced since v1.0.

Method: every numeric claim in the sizing chain was re-derived and
`analysis/SIZING.py` was re-run (including a 5000 rpm variant) to confirm which
findings are genuinely closed and which are still open behind changed wording.

---

## 1. Disposition of the 21 v1.0 comments

| ID | Subject | Verdict | Evidence in the current draft |
|---|---|---|---|
| 001 | No requirements defined | **OPEN** | `sections/01_introduction.tex:106-121` — still prose capabilities, no IDs, values or verification methods |
| 002 | Overshoot recovery not analysed | **OPEN** | Acknowledged only: `03_preliminary_sizing.tex:61-65`, `09_conclusions.tex:214-221` |
| 003 | Analysis done by hand | **CLOSED in substance** | `analysis/SIZING.py` reproduces every headline number; wording and script docstring undercut it (§3.5) |
| 004 | Full-assembly CAD missing | **CLOSED** | `11_cad_detail.tex:166-189`, `images/armonia_assembly.pdf` |
| 005 | 5000 rpm claim unsupported | **OPEN — still false** | `03_preliminary_sizing.tex:151-157`; verified below |
| 006 | h_w vs h_w,ideal, 38 vs 52 ms | **CLOSED** | `03:213` Δt ≈ 40 ms against h_w = 0.1994 (0.1994/5 = 39.9 ms) |
| 007 | Eq. (4) radical scope | **CLOSED** | `03:87` now `\sqrt{2 g\,\lambda\,\kappa}`; reproduces 0.1994 exactly |
| 008 | No requirements table | **OPEN** | Same as 001; WBS task A3 still claims it closed 25 Jul (`02_..._tasks.tex:27`) |
| 009 | Risk register missing | **OPEN** | Only WBS A5 (`02_..._tasks.tex:29`) and the Gantt bar (`..._gantt.tex:112`) |
| 010 | Structure overrun eats wheel margin | **PARTIAL** | Allowance cut 610 → 374 g (`03:346`), still called dominant uncertainty (`03:353-362`), headroom still not stated |
| 011 | Magnet type / air gap: 0.5 vs 3.3 mm | **OPEN — unchanged** | `10_bom.tex:70`, `12_electrical_detail.tex:29-32`, gate M1 `02_project_organization.tex:139`, task E2 `..._tasks.tex:88`, `06_electronics.tex:107` |
| 012 | 5 V rail undersized; load table missing | **PARTIAL** | Table now exists (`12_electrical_detail.tex:56-76`) and the `??` is gone, but the two dominant loads are "Not published" and the worst case is unevaluated |
| 013 | τ_b validated only by sacrificial scope | **OPEN** | E10 still "Sacrificial with C14/B13" (`..._tasks.tex:97`); cross-reference fixed (`03:227`), programme risk unchanged |
| 014 | Ballast station load never evaluated | **OPEN in document** | `03:392-397` states the load path, gives no value — but `SIZING.py` already computes it (§3.3) |
| 015 | Gate M2 dated day of issue, criterion unmet | **OPEN, now worse** | Whole schedule is in the past; cover still `v1.0` (`00_cover.tex:32`); 6 of 10 driving CAD dimensions still TBD (`11_cad_detail.tex:35-40`) |
| 016 | Two jump-up analyses never cross-checked | **OPEN** | Eq. (1) at `03:42-45` still never evaluated numerically |
| 017 | Three `??` cross-references | **CLOSED** | No undefined references in `build/main.log` |
| 018 | K_m: three values, model form mismatch | **PARTIAL** | Good reasoning at `06_electronics.tex:139-155`; `tab:params` still says "Motor datasheet" (`04_methodology.tex:178`) |
| 019 | Personal mobile numbers and emails published | **OPEN — unchanged** | `02_project_organization.tex:23-62`, all six members |
| 020 | Name / acronym inconsistency | **PARTIAL** | ACDS→ADCS fixed; cover "Armonia" (`00_cover.tex:30`) vs headers "Cubli" (`main.tex:105,115`), still alternating; Figure title still "Measured…" (`06:168`) |
| 021 | Overall: fix the four arithmetic gaps | **1 of 4 closed** | Eq. (4) grouping closed; 5000 rpm, ballast load and the h_w/Δt-class checks still outstanding |

**Score: 5 closed, 4 partial, 12 open.** The two the reviewer called structural
(001/008 requirements, 009 risk register) are both untouched, and the one with
real-world consequence (019, personal contact details) is untouched.

---

## 2. What the good comments were actually doing — and how to reinforce it

Naso's comments are not a list of typos. Four reusable methods sit underneath
them, and each one generalises to material introduced *since* v1.0. Reinforcing
the method is worth more than closing the individual finding.

### 2.1 "Follow the arithmetic through where a number is asserted rather than evaluated"

This is comment 021's closing instruction and the engine behind 005, 006, 007
and 014. It caught four errors in v1.0 because four numbers were stated without
being reproduced.

**Reinforce by:** making the document reproduce its own arithmetic. Every
headline number in Section 3 now comes out of `analysis/SIZING.py`; print the
one worked substitution the reviewer asked for (007's recommendation, still not
taken) under Eq. (4), and add a short "reproduce this" appendix block giving the
script invocation and its Stage 1 output verbatim. That converts the whole
sizing chain from *assertable* to *checkable* in one move, and it retires this
entire comment class rather than the four instances of it.

### 2.2 "One quantity, one value, everywhere"

Comments 005, 006, 011 and 018 are all the same shape: one physical quantity
carrying two or three different values in different parts of the document. 011
is the dangerous one because a gate criterion enshrines the wrong value.

**Reinforce by:** running a split-value sweep before v2 goes out. The audit
below found four *new* instances of this class (§3.1, §3.2, §3.6). Suggested
practice: any quantity appearing in more than one file gets a single owning
table, and every other mention cites that table rather than restating the number.

### 2.3 "There is nothing to verify against and nothing prioritised"

Comments 001, 008 and 009. In v1.0 this was a completeness gap. In the current
draft it has become a **correctness** gap, because Section 8 now exists and
opens with:

> "This subsection reports evidence against the acceptance criteria of
> Table~\ref{tab:traceability}" — `08_Results.tex:5-6`

`tab:traceability` contains no acceptance criteria. Section 8 also closes with
"fully satisfying the requirements defined in the testing plan"
(`08_Results.tex:81`), and no testing plan exists in the document. The Results
section is now writing cheques the requirements baseline cannot cash.

**Reinforce by:** building the requirements table *and* pointing Section 8's
result tables at requirement IDs. The numbers already exist scattered through
the text: 60 s balance, 150 mm envelope, 1 kHz loop, 6000 rpm, I_w,target,
encoder gap, ≥24° recovery envelope, wheel-speed cap, 1 ms outer-loop deadline.

### 2.4 "Decouple the measurement from the demonstration"

Comment 013. The recommendation was a brake bench test that needs no cube, no
balancing and no controller — so the sizing assumption survives the loss of the
jump-up demo. Still not adopted: E10 remains sacrificial alongside C14 and B13.

**Reinforce by:** either running the standalone spin-down test or stating
explicitly that β = 1.273 will ship unmeasured, and what that means for the
structural case. The document's own honesty standard (it already separates the
sizing τ_b from the structural τ_b at `03:221-231`) makes silence here the
weaker option.

---

## 3. New findings of the same class, introduced since v1.0

These are what the same reviewer would write against the current draft. Each is
listed with the check that confirms it.

### 3.1 Wheel axial thickness is specified two ways, differing by 4×

- `03_preliminary_sizing.tex:418` — `t` (wheel axial thickness) = **20 mm**
- `11_cad_detail.tex:34` — `t_r` (wheel axial thickness) = **5 mm**

This is not cosmetic. `t` caps the ballast hole diameter by construction
(`03:418`, `SIZING.py:146-152`), and `SIZING.py` raises a hard error if
`hole_diameter >= t_mm`. A 6.4 mm hole cannot exist in a 5 mm wheel, and the
2 mm axial wall rule needs 10.4 mm minimum. The CAD parameter table — declared
at `11_cad_detail.tex:16-19` to be "the single source of the driving dimensions"
— currently contradicts the analysis the wheel was sized by. **Resolve to 20 mm
and correct `tab:cad_params`, or the ballast architecture does not close.**

### 3.2 The ballast station count appears as 3, 15, 16 and 45

- `03_preliminary_sizing.tex:426` — N = **3** (of N_max = 37), the converged value
- `11_cad_detail.tex:76` — W3, "Ballast bolt and nut set (M6, 3×15)", qty **45**
- `11_cad_detail.tex:181` — assembly drawing caption, "the **3×16** M6 ballast bolt-and-nut set"
- `analysis/SIZING.py:56` (docstring) — "15 M6 stations", `SIZING.py:912` (comment) — "6 RADIAL M6 stations … 112.5%"

The 15/16 figures are v1.0 residue that survived the re-convergence to
M = 1.4654 kg. Three stations is correct for the current design and, usefully,
divides evenly across the three spokes — which retires the static-imbalance
concern raised in comment 014. **Fix the three stale mentions; keep the balance
observation, it is now a positive result.**

### 3.3 The ballast station load (comment 014) is already computed — just not in the document

`SIZING.py` prints, for the selected wheel:

```
F = m·ω²·R = 163 N  (16.6 kgf)  at 6000 rpm, R_mean = 55.0 mm
  vs M6 class 8.8 proof load ~12.7 kN — 1.28% of proof; the bolt is not the limit
bearing stress under head/nut face (46.4 mm²) = 3.51 MPa
  against PET-CF compressive strength of order 60–90 MPa — also not the limit
```

Total across three stations: ~489 N. The script even carries the reviewer's
exact follow-up point about the head and nut bearing on the curved ID/OD
surfaces (`SIZING.py:870-875`), which `03:392-397` paraphrases without the
number. **This is a three-line paste into Section 3.3 and it closes comment 014
outright.** Highest value-per-minute item in the plan.

### 3.4 The 5000 rpm claim (comment 005) is still arithmetically false

Re-ran the sizing at `rpm_max = 5000`:

| | 6000 rpm | 5000 rpm |
|---|---|---|
| I_w,target | 3.1735e-4 | 3.8081e-4 kg·m² |
| Wheel as designed (N = 3) | 3.6903e-4 → **116.3 %** | 3.6903e-4 → **96.9 %** |
| Stations actually required | 3 (exact 0.60) | **6** (exact 3.55, rounded to a multiple of 3) |
| Wheel mass | 149.11 g | 170.4 g (+21.3 g each, +63.8 g cube) |

The footnote's *logic* is right and the reviewer said so; the design simply does
not close at 5000 rpm. Two honest options:

1. **Drop the claim** — say the design closes at 6000 rpm, and that 5000 rpm
   would require six stations rather than three.
2. **Close it** — populate 6 stations, then re-run Stage 6, since +63.8 g feeds
   back through h_w ∝ M and through τ_g into β. Given that ω_max is explicitly
   the primary relief variable and depends on pack voltage across the discharge
   curve, this is defensible — but it is a re-convergence, not an edit.

Either way, `SIZING.py`'s docstring (lines 66-70) and the `rpm_max` comment
block (lines 123-133) carry the same unsupported claim and must move with the
document.

### 3.5 `SIZING.py`'s narrative is stale against its own inputs

The script closes comment 003 in substance — but its docstring still describes
the v1.0 design (`SIZING.py:56-75`: "15 M6 stations, 172.5 g/wheel, 111.7% of
target", "M = 1.7716 kg", "L = 150 mm cube"), and the `M` comment block
(lines 99-118) reconciles against "610 g structure allowance … 1771.6 g". The
live inputs are M = 1.4654 kg, L = 0.149 m, 374 g allowance. Anyone auditing the
tool reads a description of a design that no longer exists.

Meanwhile the document still says the procedure was "run to convergence by hand"
(`03:288-289`) and "run by hand" (`03:469`) — which hands comment 003 back to
the reviewer after it had been earned. **Change both to name the script, and
sync the docstring.**

### 3.6 Cube edge length: 149 mm in the analysis, 150 mm everywhere else

- `03_preliminary_sizing.tex:139` and `SIZING.py:119` — L = **149 mm**
- `11_cad_detail.tex:31` — L = **15 cm**; gate M2 `02_project_organization.tex:140` and task D1 `..._tasks.tex:77` — **150 mm**

Small (h_w ∝ L^1.5, so ~1 %), but it is the envelope figure the frame freeze
gate is written against, and it is exactly the class of split value the reviewer
flagged in 011. **Pick one and propagate.**

### 3.7 Appendix D is empty and five sections forward-reference it

`sections/13_control_algorithm_detail.tex` is a heading and nothing else. It is
promised as the home of the pseudocode, fixed gains, tuning parameters, timing
budget and fault responses at `07_control_algorithms.tex:11-12, 189-190,
325-327` and `05`/`06` cross-references. This is comment 017's exact failure mode
— pointing at content that does not exist — surviving in a form LaTeX cannot
warn about, because the label resolves.

Note also `sections/code.cpp` and `sections/code.exe` are in the tree but not
`\input` anywhere; if that is the intended pseudocode source, it belongs in
Appendix D.

### 3.8 The structure headroom number (comment 010) is now good news — say it

The reviewer asked for the sensitivity to be stated as a hard budget. Working it
through for the current design:

- Naive linear estimate (h_w ∝ M alone): wheel at 116.3 % → M may grow ~16.3 % → **+239 g**
- Correct estimate, carrying β = τ_b/(τ_b − τ_g) with τ_g = MgL/2: solving
  h_w(M) = I_w·ω_max gives M_max ≈ **1.647 kg** → **+181 g**

So the structure has ~181 g of headroom on a 374 g allowance — it could come in
48 % over and still not need re-ballasting. **And the β amplification eats a
quarter of the naive headroom**, which is worth one sentence on its own: it is
the same nonlinearity the document already warns about at `03:164-169`, shown
biting a real budget. This turns v1.0's most uncomfortable finding into a
demonstration of the document's own method.

### 3.9 The Eq. (1) cross-check (comment 016) now has data to land on

In v1.0 the reviewer wanted Eq. (3) evaluated against the Eq. (4) edge case as
the cheapest available validation. The 1-DoF rig now exists and Section 8
reports real balance and recovery numbers. Evaluating `eq:omega_required` for
the rig's as-built I_b, I_w, m_b, l_b, m_w, l gives a **predicted jump-up wheel
speed the rig can be tested against** — which is exactly the "useful evidence
for the v2 submission" the reviewer anticipated, and it is now cheaper than it
was, because the parameters are measurable rather than assumed.

### 3.10 Document identity and status are stale

- Cover: `\coverVersion{v1.0}` (`00_cover.tex:32`), subtitle "Armonia", date `\today`
- Headers: "Technical Design Document" / "Cubli", alternating with and without "Space Challenges 2026" (`main.tex:104-116`)
- Every WBS date and every gate date is in the past; gate M2 (frame freeze, "mass, inertia and CoM budget closed against the sizing analysis") is still open in fact, since the structure line is still an allowance
- Figure title in the List of Figures still reads "Measured MN4006 shaft torque…" (`06:168`) although both the caption and the body now correctly say manufacturer bench data

---

## 4. Work packages

Ordered by (value × reversibility) ÷ effort. Times are for the edit, not for
the underlying engineering.

### P0 — Do first, no dependencies

| # | Action | Files | Effort |
|---|---|---|---|
| 1 | **Remove personal mobile numbers and private emails** (019). Keep the accountable-scope column — the reviewer singled it out as the best in the cohort. Replace contacts with institutional addresses or names/roles only | `02_project_organization.tex:23-62` | 10 min |
| 2 | **Paste the ballast station load** (014) from `SIZING.py`: 163 N/station, 489 N total, 1.28 % of M6 proof, 3.51 MPa bearing vs 60–90 MPa PET-CF; add the curved-seat note and the 3-stations-on-3-spokes balance result | `03_preliminary_sizing.tex` §3.3 | 20 min |
| 3 | **Fix or drop the 5000 rpm claim** (005). Decide option 1 or 2 in §3.4 — this is a design call, not an edit | `03:151-157`, `SIZING.py:56-75,123-133` | 15 min or a re-convergence |
| 4 | **Resolve wheel thickness 20 vs 5 mm** (§3.1) and the station count 3/15/16/45 (§3.2) | `11_cad_detail.tex:34,76,181`, `SIZING.py` docstring | 20 min |
| 5 | **Resolve the encoder magnet and air gap** (011): which magnet is supplied, what gap the 20–80 mT window implies, then correct all five places including gate M1 and task E2 | `10_bom.tex:70`, `12_electrical_detail.tex:29-32`, `02_project_organization.tex:139`, `..._tasks.tex:88`, `06_electronics.tex:107` | 30 min after the bench answer |
| 6 | **Update cover version, project name and running headers** (020, 015) | `00_cover.tex:30-32`, `main.tex:104-116`, `06:168` | 15 min |

### P1 — The two structural gaps

| # | Action | Notes |
|---|---|---|
| 7 | **Requirements table** (001/008) — IDs, parent objective, quantified value, verification method. Seed from numbers already in the text; then point gate criteria (Table 3) and the Section 8 result tables at the IDs, which also repairs Section 8's false claim to be testing acceptance criteria | New subsection in §1.3 or §3.2 |
| 8 | **Risk register** (009) — trigger, likelihood, impact, owner, mitigation. Candidates already written in prose: structure mass overrun against the 181 g headroom (§3.8), τ_b never measured (013), printed part failure at a ballast station, loss of one actuation set with no spare (`10_bom.tex:26-33`), encoder gap disturbed at assembly, final-week schedule compression, learned-control reservations (`09:97-106`) | New appendix or §2.4 |

### P2 — Reinforce the analysis

| # | Action | Notes |
|---|---|---|
| 9 | **State the structure headroom** (010): +181 g, and why β eats a quarter of the naive +239 g | §3.8 above; one paragraph under `tab:massbudget` |
| 10 | **Worked substitution under Eq. (4)** (007 recommendation) plus a "reproduce this" block quoting `SIZING.py` Stage 1 output | Retires comment class 2.1 |
| 11 | **Evaluate Eq. (1) against the rig** (016) and report the predicted jump-up speed as a testable prediction | §3.9 above |
| 12 | **Replace "run by hand" with the script** (003) and sync the `SIZING.py` docstring to its live inputs | `03:288-289,469`; `SIZING.py:56-75,99-118,912-919` |
| 13 | **Set K_m to "bench data, incremental slope"** in `tab:params` (018), and add the one sentence the reviewer asked for: the 0.08 N·m intercept appears as a torque bias which the offset filter of Eqs. (10)–(11) absorbs | `04_methodology.tex:178`, `07_control_algorithms.tex` §7.1 |
| 14 | **Analyse overshoot recovery** (002): motor spin-up rate against the correction required after an overshoot, and give θ_th a number | `03` §3.1 / `07` §7.3 |

### P3 — Programme and completeness

| # | Action | Notes |
|---|---|---|
| 15 | **Populate Appendix D or mark it to-be-issued** (§3.7) — five sections currently promise content that is not there | `13_control_algorithm_detail.tex`; consider `sections/code.cpp` |
| 16 | **Re-baseline the schedule** (015): record M2 as closed or open with a real date, update the Gantt to the as-run calendar, and reconcile L = 149 vs 150 mm (§3.6) | `02_*` + `11_cad_detail.tex:31` |
| 17 | **Decouple the brake measurement from the jump-up demo** (013), or state that β ships unmeasured and what that means for the structural case | `..._tasks.tex:97`, `03:221-231` |
| 18 | **Close the 5 V worst-case rail load** (012): measure MG92B stall and MA600 supply, evaluate the coincident case, and write the servo-concurrency assumption into the mode table rather than leaving it implicit | `12_electrical_detail.tex:56-76`, `07:361-379` |

---

## 5. One-line summary

The arithmetic findings the reviewer raised were largely fixed and the sizing
chain now reproduces exactly — but the two structural gaps (requirements, risk
register) are untouched, the privacy finding is untouched, the encoder gap
contradiction is untouched, the 5000 rpm claim is still false, and the
re-convergence to M = 1.4654 kg introduced four new split-value inconsistencies
of exactly the kind the review was about.
