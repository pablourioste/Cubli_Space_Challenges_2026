# Cubli TDD v2 — Review Response and Action Plan

**Status:** draft for team review · **Prepared:** 18 Aug 2026 · **Covers:** all 21
assessor comments on TDD v1.0 (`docs/SC 2026 Documentation Feedback.csv`)

---

## How to read this

The v1.0 assessment produced 21 comments from three reviewers. This document
says, for each one, **whether it is actually fixed in the current draft** — not
whether the text around it changed. Every numeric claim was re-derived by hand
and `analysis/SIZING.py` was re-run (including a 5000 rpm variant) to check.

It also lists **new problems introduced since v1.0**. The design re-converged
from M = 1.772 kg to M = 1.4654 kg and from a 180 mm to a 150 mm cube. That was
the right call, but the re-convergence left stale numbers behind in places the
original review never touched.

Three sections are worth reading even if you skip the rest:

- **§3 — Two deliverables already exist in this repo and just aren't in the
  document.** Cheapest work in the plan.
- **§5 — The envelope that pins every wheel number is asserted, not evaluated,**
  and one BOM item appears not to fit inside it.
- **§6 — Work packages,** with owners and an order.

Reviewer G. Naso called this "the strongest document in the cohort" and said two
things would finish it: the requirements table and risk register, and following
the arithmetic through in four places. **One of those four is closed. Neither of
the two structural items has been started.** That is the whole job.

---

## 1. Scoreboard

| | Count | IDs |
|---|---|---|
| **Closed** | 5 | 004, 006, 007, 017, 020 |
| **Partial** | 4 | 003, 010, 012, 018 |
| **Open** | 12 | 001, 002, 005, 008, 009, 011, 013, 014, 015, 016, 019, 021 |

**What is genuinely fixed** — verified, not taken on trust:

- **Eq. (4) radical grouping** (007). Now `\sqrt{2g\lambda\kappa}`. I re-derived
  it: h_w,ideal = 0.15672, β = 1.2726, h_w = 0.19945 — reproduces Table 8's
  0.1994 exactly, and the edge case reproduces 0.1809. The sizing chain is now
  arithmetically sound end to end.
- **h_w vs h_w,ideal** (006). Δt is now 40 ms against h_w = 0.1994
  (0.1994 / 5 = 39.9 ms). The two paragraphs agree.
- **Dangling `??` references** (017). Zero undefined references in
  `build/main.log`.
- **Full-assembly CAD** (004). `images/armonia_assembly.pdf`, Figure `dwg_3d`.
- **ACDS → ADCS** (020). Gone from every section.

---

## 2. The twelve open comments, grouped by who can close them

### 2.1 Pablo — document assembly and programme

| ID | What is still wrong | Where |
|---|---|---|
| **019** | **Personal mobile numbers and private email addresses for all six of us are still in the document.** Unchanged since v1.0. This gets circulated to reviewers and mentors and may be published as a programme output. | `sections/02_project_organization.tex:23-62` |
| 001 / 008 | No requirements table. No IDs, no acceptance values, no verification methods. WBS task A3 still shows this closed on 25 Jul, and `docs/electrical/STATUS.md:45` marks "A3 requirements table support — done". | `01_introduction.tex:106-121` |
| 009 | No risk register. WBS task A5 still shows it closed 28–29 Jul. | `02_..._tasks.tex:29` |
| 015 | Gate M2 (frame freeze, "mass, inertia and CoM budget closed against the sizing analysis") is recorded as passing on 2 Aug, but the structure line is still an allowance and 6 of 10 driving CAD dimensions are TBD. Every WBS and gate date is now in the past. Cover still reads `v1.0`. | `02_project_organization.tex:140`, `11_cad_detail.tex:35-40`, `00_cover.tex:32` |
| 020 | Cover says "Armonia", every running header says "Cubli", and the header alternates between two forms. Figure title in the List of Figures still reads "Measured MN4006 shaft torque…" although the caption correctly says manufacturer bench data. | `00_cover.tex:30`, `main.tex:104-116`, `06_electronics.tex:168` |

**019 is ten minutes of work and it is the only item on this list with a
real-world consequence.** Keep the accountable-scope column — the reviewer
singled it out as the clearest ownership statement in the cohort. Replace only
the contact column.

### 2.2 Andrea / Deyan — sizing and dynamics

| ID | What is still wrong |
|---|---|
| **005** | **The 5000 rpm over-dimensioning claim is still false.** See §4.1 — I re-ran it. |
| 014 | The ballast station load is described but never evaluated. **The number already exists in `SIZING.py`** — see §3.2. |
| 016 | Eq. (1) (`eq:omega_required`) is still never evaluated numerically, so the two independent jump-up derivations are still never cross-checked. The 1-DoF rig now exists, so this can produce a *testable predicted jump-up speed* rather than just a consistency check. |
| 010 | The structure-mass sensitivity is still not stated as a number. It is now **good news** — see §4.2. |
| 003 | Substantially closed: `SIZING.py` reproduces every headline figure. Undermined by the document still saying the procedure was "run to convergence by hand" (`03:288-289`, `03:469`) and by the script's own docstring still describing the v1.0 design. |

### 2.3 Pablo / Niccolo — electrical and control

| ID | What is still wrong |
|---|---|
| **011** | **Encoder magnet and air gap are still specified two ways, unchanged since v1.0.** BOM says "ring magnet, air-gap ≤0.5 mm"; Appendix C.1 says N35 ¼″×⅛″ *diametric disk* at 3.3 mm. Gate M1 and task E2 both enshrine 0.5 mm. `RISKS.md` RE3 rates this **H/H — the highest-likelihood risk in the register** — and notes it presents as a control bug, burning Andrea's and Niccolo's time on the wrong subsystem. |
| 012 | The missing load table now exists and the `??` is gone, but the two dominant loads (MG92B stall, MA600 supply) are "Not published" and the coincident worst case is still unevaluated. The servo-concurrency assumption is still not written into the mode logic. See §4.3 for the arithmetic. |
| 013 | τ_b is still validated only by work designated sacrificial. Task E10 remains "Sacrificial with C14/B13". β = 1.273 inflates the inertia requirement by 27% and may ship unmeasured. |
| 018 | `tab:params` still says K_m = "Motor datasheet" while §5.4.1 derives 0.023 N·m/A from bench data. The reviewer's extra point — that the 0.08 N·m intercept appears as a torque bias which the offset filter of Eqs. (10)–(11) absorbs — is still unwritten, and it is a genuine strength of the control design. |
| 002 | Overshoot recovery still not analysed. Acknowledged at `03:61-65` and `09:214-221`, but the motor's achievable spin-up rate is never checked against the correction required after an overshoot, and θ_th has no number anywhere. |

---

## 3. Two deliverables that already exist in this repo

This is the highest value-per-minute work in the plan. Both are cases of the
team having done the engineering and not having landed it in the document.

### 3.1 The risk register is written — `docs/electrical/RISKS.md`

Fourteen rows (RE1–RE14) with trigger, impact, severity, likelihood, owner and
mitigation, **plus a ready-to-paste LaTeX `longtable`** that already uses the
same `L{}` column type and `siunitx` conventions as
`02_project_organization_tasks.tex`. It was written for task A5 and
`docs/electrical/STATUS.md:114` still shows the hand-off to Deyan as `todo`.

It is not a straight paste. Before it goes in:

- **RE11 is obsolete as written.** It reads "fewer than four complete actuation
  sets" — three sets is now the confirmed baseline, so this should be rewritten
  as a *no-spare* risk: any motor, driver or encoder failure after integration
  loses an axis with no resupply lead time before 20 Aug. `AUDIT.md:289-302`
  already flags this and asks for a decision that was never recorded.
- **RE2's stored-energy figure is stale.** It says ~105 J per wheel, which came
  from the old 130 mm wheel. At the current design (I_w = 3.6903e-4, 628 rad/s)
  it is **72.8 J per wheel, 218 J across three**. Still more than enough to
  matter for the bus, but quote the right number.
- Task IDs reference an older WBS (E1.5, E4.2, E5.1). Re-map to the current
  E1–E10 / B / C series.
- Add the non-electrical rows the reviewer explicitly listed: structure mass
  overrun against the headroom in §4.2, τ_b never measured (013), printed-part
  failure at a ballast station, encoder gap disturbed at assembly, final-week
  schedule compression, and the learned-control reservations at `09:97-106`.

**Owner: Pablo → Deyan. Effort: an afternoon, mostly re-baselining.**

### 3.2 The ballast station load is already computed — `SIZING.py`

Comment 014 asked for a number that the script has been printing all along:

```
=== Through-bolt retention load ===
hardware mass per station = 7.50 g (bolt 5.00 + nut 2.50)
at 6000 rpm and R_mean = 55.0 mm:
  F = m·ω²·R = 163 N  (16.6 kgf)
  vs M6 class 8.8 proof load ~12.7 kN — the BOLT is not the limit (1.28% of proof)
  bearing stress under the head/nut face (46.4 mm²) = 3.51 MPa,
  against PET-CF compressive strength of order 60–90 MPa — also not the limit
```

163 N per station, ~489 N across the three stations on a wheel. The script also
carries the reviewer's exact follow-up point about the head and nut bearing on
the curved ID/OD surfaces rather than a flat face (`SIZING.py:870-875`), which
`03:392-397` paraphrases without the number or the spot-facing conclusion.

**Bonus:** the reviewer's sub-point about balance is now satisfied and worth
stating as a positive result — **3 stations on a 3-spoke wheel divides evenly**,
so no static imbalance is introduced. In v1.0 it was 15 stations on 3 spokes,
which does not.

**Owner: Andrea/Deyan. Effort: 20 minutes.**

---

## 4. The arithmetic, re-checked

### 4.1 The 5000 rpm claim does not hold — and there is a better argument available

Table 8's footnote still says the sizing "has additionally been run at 5000 rpm
as an over-dimensioning check" and that "a wheel that closes at 5000 rpm
therefore closes at 6000 rpm with margin in hand". I re-ran `SIZING.py` with
`rpm_max = 5000`:

| | 6000 rpm | 5000 rpm |
|---|---|---|
| I_w,target (corner) | 3.1735e-4 | **3.8081e-4** kg·m² |
| Wheel as designed (N = 3) | 3.6903e-4 → **116.3 %** | 3.6903e-4 → **96.9 %** |
| Stations actually required | 3 (exact 0.60) | **6** (exact 3.55, rounded to a multiple of 3) |
| Wheel mass | 149.11 g | 170.4 g (+21.3 g each, +63.8 g/cube) |

The footnote's *logic* is right and the reviewer said so explicitly. The design
simply does not close at 5000 rpm.

**Recommendation: drop the claim rather than close it — and replace it with the
argument that already exists in `docs/electrical/MOTOR_SPEED.md`.** That file
derives the realistically achievable ceiling as **6917 rpm on a sagged pack**
(after winding IR drop and sinusoidal-drive derating), which makes 6000 rpm
13 % conservative *against the worst pack state*. That is a far stronger
justification than an arbitrary 5000 rpm case, it is already written, and it
matches the reasoning the TDD gives at `03:172-194` without the number.

If you would rather close it at 5000 rpm instead, note that it is a
**re-convergence, not an edit**: +63.8 g feeds back through h_w ∝ M and through
τ_g into β, so Stage 1 has to be re-run.

Either way, `SIZING.py:66-70` and `:123-133` repeat the same claim and must move
with the document.

### 4.2 Structure mass headroom — comment 010 is now good news

The reviewer asked for the sensitivity to be stated as a hard budget. Worked
through for the current design:

| Estimate | Method | Headroom on M |
|---|---|---|
| Naive | h_w ∝ M alone; wheel at 116.3 % → M may grow 16.3 % | **+239 g** |
| Correct | carries β = τ_b/(τ_b − τ_g) with τ_g = MgL/2; solve h_w(M) = I_w·ω_max → M_max ≈ 1.647 kg | **+181 g** |

So the structure has **~181 g of headroom on a 374 g allowance** — it can come
in 48 % over before the wheel needs re-ballasting. Compare v1.0, where the
margin was 207 g against a 610 g allowance and the reviewer called it a 34 %
overrun tolerance. **The re-convergence materially improved this position and
the document does not say so.**

The second half is worth a sentence on its own: **β amplification eats a quarter
of the naive headroom.** That is the same nonlinearity the document already
warns about at `03:164-169`, shown biting a real budget — which is exactly the
kind of thing this document does well and should keep doing.

### 4.3 The 5 V rail — what the concurrency assumption is worth

Comment 012 asked for the worst case to be evaluated and the servo-concurrency
assumption to be stated. The assumption is *already implicit in the dynamics*:
`04_methodology.tex:289-291` says jump-up brakes one wheel, then a second —
never three at once. It just is not written into the mode logic or the
electrical section, so the converter has no stated design case.

| Load | Qty | Current each | Source |
|---|---|---|---|
| Teensy 4.1 | 1 | ~100 mA | PJRC community data |
| XIAO ESP32-C6 | 1 | ~300 mA | TX burst, BOM |
| BMI270 | 1 | ~0.7 mA | Bosch datasheet |
| MA600 encoder | 3 | **not published** (~15–25 mA typical for TMR) | measure at bring-up |
| MG92B servo | 3 | **not published** (~0.7–1.0 A stall for this class) | measure at bring-up |

| Case | Total | vs LM2596 (2–3 A, derates without heatsink) |
|---|---|---|
| **A — sequential braking** (one servo stalls) | **≈1.4 A** | comfortable |
| **B — three servos concurrent** | **≈3.2 A** | at or over rating; ~4–5 W dissipation |

**The concurrency assumption is worth about 1.8 A** — the difference between
comfortable and over-rating. Writing it into the mode table costs one row and
turns an open risk into a design constraint. `RISKS.md` RE8 already tracks this,
and task E10 already calls for an "isolated 5 V rail" — but **only one LM2596
appears in the BOM and in the power tree**, so the design that anticipates the
split does not yet contain it.

---

## 5. New problems introduced since v1.0

The re-convergence to M = 1.4654 kg and L = 150 mm left five split values behind.
These are exactly the class of finding the review was about, so they should be
swept before v2 goes out, not after.

### 5.1 Wheel axial thickness: 20 mm or 5 mm?

- `03_preliminary_sizing.tex:418` — `t` = **20 mm**
- `11_cad_detail.tex:34` — `t_r` = **5 mm**

Not cosmetic. `t` caps the ballast hole diameter by construction, and
`SIZING.py` raises a hard error if `hole_diameter >= t_mm`. A 6.4 mm hole plus
the 2 mm wall rule needs 10.4 mm minimum. **A 6.4 mm ballast hole cannot exist
in a 5 mm wheel.** The CAD parameter table is declared at `11_cad_detail.tex:16-19`
to be "the single source of the driving dimensions" and currently contradicts
the analysis the wheel was sized by. Resolve to 20 mm.

### 5.2 Ballast station count appears as 3, 15, 16 and 45

- `03_preliminary_sizing.tex:426` — N = **3** (of N_max = 37) ← correct
- `11_cad_detail.tex:76` — W3, "M6, 3×15", qty **45**
- `11_cad_detail.tex:181` — drawing caption, "the **3×16** M6 ballast bolt-and-nut set"
- `SIZING.py:56` — "15 M6 stations"; `SIZING.py:912-919` — "6 RADIAL M6 stations … 112.5%"

15 and 16 are v1.0 residue. Three is correct.

**Procurement note:** `docs/electrical/STATUS.md:41` lists M6 nuts as **blocked —
not arrived**, and calls it a blocker on ballast, balancing and spin-test. At
3 stations per wheel that is **9 bolt/nut sets for the cube**, not 45. This risk
has largely retired and the status tracker has not caught up.

### 5.3 Cube edge length: 149 mm or 150 mm?

- `03_preliminary_sizing.tex:139`, `SIZING.py:119` — **149 mm**
- `11_cad_detail.tex:31`, gate M2, task D1 — **150 mm**

Small (h_w ∝ L^1.5, so ~1 %), but 150 mm is the figure the frame-freeze gate is
written against. Pick one and propagate.

### 5.4 Appendix D is empty, and five sections promise it content

`sections/13_control_algorithm_detail.tex` is a heading and nothing else. It is
promised as the home of the pseudocode, fixed gains, tuning parameters, timing
budget and fault responses at `07_control_algorithms.tex:11-12`, `:189-190` and
`:325-327`, and referenced again from `05` and `06`.

This is comment 017's exact failure mode — pointing at content that does not
exist — in a form LaTeX cannot warn about, because the label resolves. A
reviewer following the cross-reference finds a blank page.

`sections/code.cpp` is in the tree and `\input` nowhere. If that is the intended
source, it belongs here.

### 5.5 Section 8 tests against acceptance criteria that do not exist

The Results section is new since v1.0 and opens with:

> "This subsection reports evidence against the acceptance criteria of
> Table~\ref{tab:traceability}" — `08_Results.tex:5-6`

`tab:traceability` contains prose capabilities, not acceptance criteria. It also
closes with "fully satisfying the requirements defined in the testing plan"
(`08_Results.tex:81`) — there is no testing plan in the document.

**This upgrades comments 001/008 from a completeness gap to a correctness one.**
In v1.0 the document had nothing to verify against; it now also *claims* to be
verifying against it.

---

## 6. The envelope that pins every wheel number is asserted, not evaluated

This one is new, it is not on the assessor's list, and it is probably the most
consequential thing in this document.

Everything in the sizing chain hangs off **D_w = 120 mm, pinned by the
packaging envelope**. `SIZING.py:225-236` states it plainly: the sweep does not
choose the diameter, the envelope does, and without that pin the optimiser picks
180 mm. The document says the same at `03:456-466`.

**But the envelope is never evaluated.** `03:243-252` says L is "the smallest
edge length containing that volume plus wall thickness and contact features" —
and `V_min`, the wheel-to-subframe clearance `c_w`, the inter-module clearance
`c_o`, the motor axis offset and the corner contact radius are **all still TBD**
in `tab:cad_params` (`11_cad_detail.tex:35-40`). The constraint that outranks
every other consideration in the sizing is the one number nobody has computed.

Worse, the repo contains an analysis that reached the **opposite** conclusion.
`docs/electrical/ENVELOPE_JUSTIFICATION.md` concludes, at the 6000 rpm design
speed:

> "At 6000 rpm the earlier ambiguity disappears. The 150 mm envelope now fails
> outright: the largest wheel that fits gives 2.629e-4 against a 3.168e-4
> requirement, 17 % short, and no amount of ballast recovers it."

Then `docs/electrical/STATUS.md:25` records the 31 Jul review decision:
**"Cube edge = 150 mm. Closes the 150 vs 180 mm conflict."**

The decision is defensible — the wheel section changed from 17×10 mm to
20×10 mm and M dropped from 1.772 to 1.4654 kg, and at those inputs 150 mm does
close (3.045e-4 bare ring + 3 stations → 3.6903e-4 against 3.1735e-4). But
**`ENVELOPE_JUSTIFICATION.md` was never updated and now argues against the
design**, and the TDD carries no justification for 150 mm at all.

### The specific thing to check before v2

`ENVELOPE_JUSTIFICATION.md:141-145` makes a packaging argument that has never
been retired:

> "the perfboard (150 × 90 mm — note this alone is 150 mm across, i.e. it does
> **not** fit inside a 150 mm cube with any wall at all)"

The BOM still specifies a **15 × 9 cm double-sided perfboard**
(`10_bom.tex:97`), and `tab:cad_params` still gives L = 150 mm with a 5 mm wall
— a **140 mm internal dimension**. A 150 mm board does not fit in a 140 mm cavity.

Either the board is split or cut down, or the envelope is wrong. **This is a
build-stopping question, not a documentation one**, and it should be answered
before anything else in §6. `ENVELOPE_JUSTIFICATION.md:220-223` already flags it
as an open TODO owned by Pablo.

**Owner: Pablo + Nasia. Do this first.**

---

## 7. Requirements table — seed

Comment 008's point was that the numbers already exist scattered through the
text and only need collecting. They do. This is a starting set harvested from
the current draft; it needs values agreed, gaps filled and a verification method
confirmed per row.

| ID | Requirement | Value | Verification | Source | Status |
|---|---|---|---|---|---|
| R-BAL-01 | Unassisted edge balance, 1-DoF rig | ≥ 60 s | Timed run | Gate G3 | **Met** (§8.1) |
| R-BAL-02 | Unassisted edge balance, cube | ≥ 60 s | Timed run | Gate G6 | Open |
| R-BAL-03 | Corner balance and commanded slew | demonstrated | Timed run + video | Gate G7 | Open |
| R-BAL-04 | Disturbance recovery from initial tilt | ≥ 12° (24° demonstrated) | Release from measured angle | §8.1 | **Met** (1-DoF) |
| R-ENV-01 | Cube edge length | ≤ 150 mm | CAD + measurement | D1, M2 | **Conflicted** (§5.3) |
| R-ENV-02 | Reaction-wheel outer diameter | ≤ 120 mm | CAD | `tab:rw_params` | **Unevaluated** (§6) |
| R-DYN-01 | Per-wheel inertia, corner case | ≥ 3.1735e-4 kg·m² | CAD roll-up + spin-down | `tab:inertia_cases` | Met by analysis, 116.3 % |
| R-DYN-02 | Max sustained wheel speed | 6000 rpm across discharge curve | Bench spin, sagged pack | `MOTOR_SPEED.md` | Open |
| R-DYN-03 | Total cube mass | ≤ 1.4654 kg design; 1.647 kg absolute | Weigh assembly | §4.2 | Allowance pending CAD |
| R-DYN-04 | Brake torque (sizing value) | 5 N·m mean, impulse-equivalent | Spin-down test | `03:226-231` | Open — **sacrificial scope** (013) |
| R-CTL-01 | Outer control-loop rate | 1 kHz, worst case bounded by construction | Loop-timing measurement | `07:293-307` | Open |
| R-CTL-02 | Tilt capture band θ_th | **TBD** | Simulation + rig | `07:164-178` | **No value defined** (002) |
| R-SEN-01 | Encoder air gap | **0.5 mm or 3.3 mm** | Feeler/shim + field check | — | **Conflicted** (011) |
| R-SEN-02 | Encoder resolution | 16-bit, 65536 counts/rev | Datasheet + read-back | BOM row 3 | Met |
| R-PWR-01 | 5 V rail worst-case load | < LM2596 rating with heatsink | Measure under coincident load | §4.3 | Open (012) |
| R-PWR-02 | Motor-bus bulk capacitance | ≥ 50 V rating | Inspection | `06:194-198` | Open — not yet ordered |
| R-PWR-03 | Runtime per charge under balance load | **TBD** | Endurance run | `tab:electrical_measured` | Open |
| R-SAF-01 | Disarm path and watchdog verified before any balance attempt | pass/fail | Fault injection | Gate M4 | Open |
| R-SAF-02 | CAN-FD error frames at 5 Mbit/s | zero, sustained soak | Scope + counter log | Task E8 | Open |
| R-STR-01 | Ballast station retention at ω_max | F = 163 N; < 5 % bolt proof; bearing < 10 MPa | Analysis + spin test | `SIZING.py` §3.2 | **Met, unpublished** |

Once this exists, point the Table 3 gate criteria and the Section 8 result
tables at the IDs. That closes 001, 008 and the §5.5 correctness problem in one
move.

**Owner: Pablo (table) with Deyan (dynamics rows), Niccolo (control/safety),
Andrea (sizing).**

---

## 8. Work packages

Ordered by dependency and by value per hour. Times are for the edit, not the
underlying engineering.

### P0 — before anything else

| # | Action | Owner | Effort |
|---|---|---|---|
| 0 | **Answer the perfboard/envelope question** (§6). Does a 150 × 90 mm board fit a 150 mm cube? If not, split the board or revisit L. Build-stopping. | Pablo + Nasia | — |
| 1 | **Strip personal phone numbers and private emails** (019). Keep the scope column. | Pablo | 10 min |
| 2 | **Decide the 5000 rpm question** (005): drop the claim and cite the 6917 rpm sagged-pack figure from `MOTOR_SPEED.md`, or re-converge at 6 stations. Design call. | Andrea + Deyan | 15 min or a re-run |
| 3 | **Resolve the encoder magnet and air gap** (011) — which magnet is supplied, what gap the 20–80 mT window implies — then correct all five places including gate M1 and task E2. `RISKS.md` RE3 rates this H/H. | Pablo | 30 min after the bench answer |
| 4 | **Resolve wheel thickness** (20 vs 5 mm) and **station count** (3 vs 15/16/45) | Nasia + Suvanna | 20 min |

### P1 — the two structural gaps

| # | Action | Owner | Notes |
|---|---|---|---|
| 5 | **Port the risk register** from `RISKS.md`, re-baselined per §3.1 | Pablo → Deyan | LaTeX already written |
| 6 | **Build the requirements table** from the §7 seed, then repoint the gate criteria and the Section 8 result tables at the IDs | Pablo + all | Closes 001, 008 and §5.5 |

### P2 — reinforce the analysis

| # | Action | Owner |
|---|---|---|
| 7 | Paste the ballast station load (§3.2) into §3.3, with the balance result and the spot-facing note | Andrea/Deyan |
| 8 | State the 181 g structure headroom and the β effect (§4.2) under `tab:massbudget` | Deyan |
| 9 | Add one worked numerical substitution under Eq. (4) and a "reproduce this" block quoting `SIZING.py` Stage 1 — the reviewer asked for this and it retires the whole "asserted vs evaluated" comment class | Deyan |
| 10 | Evaluate Eq. (1) against the rig and report a predicted jump-up speed (016) | Andrea |
| 11 | Replace "run by hand" with the script (003) and sync the `SIZING.py` docstring to its live inputs | Andrea |
| 12 | Set K_m to "bench data, incremental slope" in `tab:params`, and add the one sentence on the torque bias being absorbed by the offset filter (018) | Niccolo |
| 13 | Evaluate the 5 V worst case, write the servo-concurrency assumption into the mode table, and reconcile the "isolated 5 V rail" of E10 against the single-converter BOM (012, §4.3) | Pablo |

### P3 — completeness and programme

| # | Action | Owner |
|---|---|---|
| 14 | Populate Appendix D or mark it explicitly to-be-issued (§5.4) | Niccolo |
| 15 | Re-baseline the schedule and gates; record M2 honestly; update cover to v2 (015, 020) | Pablo |
| 16 | Analyse overshoot recovery and give θ_th a number (002) | Niccolo + Andrea |
| 17 | Decouple the brake measurement from the jump-up demo, or state that β ships unmeasured and what that means structurally (013) | Suvanna + Niccolo |
| 18 | Reconcile L = 149 vs 150 mm (§5.3) | Deyan + Nasia |

---

## 9. What was checked, and how

So that anything here can be challenged:

- **Sizing chain re-derived by hand** from Eq. (4) through to
  `tab:inertia_cases`: κ, λ, n for both contact cases; h_w,ideal = 0.15672;
  τ_g = 1.0710 N·m; β = 1.2726; h_w = 0.19945; I_w,target = 3.1735e-4. All
  reproduce the published values.
- **`analysis/SIZING.py` re-run as-is**, and re-run with `rpm_max = 5000` from a
  scratch copy (the repo file was not modified).
- **Structure headroom** solved from h_w(M) = I_w·ω_max carrying β(M), giving
  M_max ≈ 1.647 kg, against the naive linear estimate of 1.704 kg.
- **`build/main.log` checked** for undefined references and duplicate labels:
  none.
- **Every section file read** against every comment; file and line references
  above are from the current working tree.
- **`docs/electrical/*`** read for prior analysis: `RISKS.md`, `AUDIT.md`,
  `MOTOR_SPEED.md`, `ENVELOPE_JUSTIFICATION.md`, `STATUS.md`.

Numbers I could **not** verify and which need a bench or a CAD answer: MG92B
stall current, MA600 supply current, the actual maximum wheel OD inside the
frame, V_min, and whether the perfboard fits.

---

## 10. One-line summary

The arithmetic findings were largely fixed and the sizing chain now reproduces
exactly — but the two structural gaps the reviewer called decisive are
untouched, the privacy finding is untouched, the encoder gap contradiction is
untouched, the 5000 rpm claim is still false, the re-convergence introduced five
new split values, and the envelope that pins every wheel number has still never
been evaluated.
