# Document Audit — Errors and Incoherences

Full scan of `LATEX/` as of 28 Jul 2026. Every section file, `main.tex`,
and `SIZING.py` checked against each other and against the stated design
decisions. Nothing here has been fixed in Dejan's files; this is the list for
him and for the team to action.

Severity: **BLOCKER** (document is wrong or will not build) / **MAJOR**
(numbers disagree, a reader will catch it) / **MINOR** (polish).

---

## BLOCKER

### B-1. `08_bom.tex` merge conflict — RESOLVED 28 Jul
The `<<<<<<<` / `=======` / `>>>>>>>` markers are gone; the document compiles.
The conflict was resolved by keeping the empty side, so Tables 2 (derived
actuation parameters) and 3 (procurement gaps) are **deliberately deleted** —
confirmed as intended.

Follow-up applied the same day: the prose in `08_bom.tex` and
`05_hardware_design.tex` still referenced both deleted tables, which would
have rendered as "Table ??". Those references have been rewritten to point at
Sections~\ref{sec:jumpup_target} and~\ref{sec:rw_sizing} instead, and the
stale `main.aux` (which still carried the deleted labels) was cleared.
Verified: **43 labels, 50 references, 0 undefined, 0 duplicates.**

One consequence to note: the deleted gap table was the only record of the
consumables and bench equipment not in the supplied BOM — bench PSU, LiPo
charger and safety kit, E-stop and fuse, bus bulk capacitor, XT30 pairs, wire,
fasteners, filament. Several of these are mine to buy under C6. They are now
tracked in `electrical/PROCUREMENT.md` and the BOM prose points there
generically ("tracked separately in the build documentation").

### B-2. Wheel OD is sized for the wrong cube
Section 5.3 selects **OD = 120 mm with 21 nuts** and states this meets
`I_w,target = 3.15e-4 kg m^2`. It does not. Re-running the current
`SIZING.py` (17 mm ring width, measured 2.5 g nut) gives **30 nuts at 120 mm**,
not 21, and the circumferential wall comes out at **-4.7 mm** — the pockets
overlap. The 120 mm/21-nut result belongs to an older parameter set (15 mm
ring, 3.12 g nut). Either the table or the script is stale, and they cannot
both be published. See M-1 for the full divergence.

### B-3. Three motors, not four — contradicts the plan I just wrote
You have confirmed **3 complete motor/driver/encoder sets**. Every document
location assumes otherwise or is ambiguous:
- BOM Table 1 footnote: "so four of each are procured" — **now false**.
- BOM Table 3 lists "Spare motor + spare moteus-n1, qty 1 each" as a gap
  item — that spare does not exist.
- BOM intro paragraph: "a shortfall in the motor count would force the
  reduced-actuation one-wheel variant" — this risk is now live, not
  hypothetical, since there is no spare.
- `electrical/PLAN.md` and `RISKS.md` (mine) assumed 4 sets. **I have not yet
  updated them** — see "Action required from me" below.

**Consequence you need to decide on:** with 3 sets, the 1-DoF bench rig and
the cube compete for the same hardware. The rig cannot survive as a permanent
development bench past cube integration (7 Aug) unless one axis of the cube is
left unpopulated. Options in `PLAN.md` update, but this is your call, not
mine.

---

## MAJOR

### M-1. `SIZING.py` and Section 5.3 disagree on every wheel number
Script inputs have moved on from the published table. Side by side, 120 mm:

| Quantity | Section 5.3 table | `SIZING.py` today |
|---|---|---|
| Ring radial width | 15 mm | 17 mm |
| Nut mass | 3.12 g (measured) | 2.5 g (measured) |
| Nut across-flats | 11 mm | 13 mm |
| Nut thickness | not stated | 5 mm |
| Nuts at OD 120 | 21 | 30 |
| Wheel mass | 131.5 g | 132.5 g |
| I_w achieved | 3.31e-4 | 3.24e-4 |
| Circumferential wall | ~2.5 mm OK | **-4.7 mm (overlap)** |
| 3-wheel mass | 394.6 g | 397.5 g |
| Net mass per nut | +2.39 g | +1.497 g |
| Net inertia per nut | +1.55e-5 | not printed, but lower |

Also: the script's own consistency check reports the measured 2.5 g nut is
**-43.2% versus its geometry**, and that a 10.26 mm bore would be needed to
reconcile them (6.60 mm is the input). Either the nut is not the part the
geometry describes, or the measurement is of a different fastener. This needs
resolving before either number is published — the mass distribution
(`k2_nut`) still uses the geometric shape, so a wrong shape corrupts the
inertia even when the mass is overridden.

**Nobody should publish Table `tab:rw_sizing` until the script and the table
are reconciled.** Owner: Suvanna/Nasia with Dejan.

### M-2. Radial fit fails at every orientation, and the document understates it
Section 5.3's "Radial fit caveat" says 1.8 mm wall, "dropping to 0.9 mm if a
nut is seated corner-out", against a 2 mm minimum — presented as something to
fix "in the next design iteration". The current script says:

```
pocket across flats   = 13.40 mm  -> wall 1.80 mm each side [TOO THIN]
pocket across corners = 15.47 mm  -> wall 0.76 mm each side [TOO THIN]
ring radial width     = 17.00 mm
```

The ring width was **already increased to 17 mm** (the fix the document
proposes) and it *still fails both orientations*. The caveat as written
implies the problem is solvable by the change that has already been made and
did not work. This is a real design problem, not a footnote.

### M-3. Cube edge length stated inconsistently across the document
| Location | Value |
|---|---|
| §4.3.1 `tab:jumpup_budget` | 180 mm |
| §5.2 volume constraint | 180 mm |
| `SIZING.py` `L` | 0.18 m |
| BOM Table 2 caption | **"assuming a 150 mm, 2 kg cube"** |
| §1.1 (ETH reference) | 15x15x15 cm (that is ETH's, not ours — acceptable) |

The BOM Table 2 caption is wrong on **both** numbers: 150 mm should be 180 mm
and 2 kg should be 1.45 kg. Every derived figure in that table inherits the
error. See M-4.

### M-4. BOM Table 2 derived figures contradict Section 4/5
Computed on the wrong cube (150 mm, 2 kg), so they disagree with the real
sizing:

| Quantity | BOM Table 2 | §4/§5 (as written) | **DECIDED** |
|---|---|---|---|
| Required jump-up momentum | ~0.29 kg m^2/s (edge, 1.5x margin) | 0.277 corner / 0.251 edge | 0.2767 corner |
| Target wheel inertia | >= 3.9e-4 | 3.15e-4 | **4.404e-4** |
| omega_max | 7000 rpm (733 rad/s) | 8400 rpm (880 rad/s) | **6000 rpm (628 rad/s)** |

**RESOLVED 28 Jul: the design speed is 6000 rpm.** Neither of the two figures
in the document was right — both were optimistic. 8400 rpm is `Kv x 22.2 V`,
i.e. nominal pack with no load and no losses. The realistic ceiling once
winding IR drop, sinusoidal-drive derating and end-of-charge pack voltage are
included is ~6900 rpm, and 6000 rpm is set deliberately below that so the
machine performs across the whole discharge curve rather than only on a fresh
pack. Full derivation and the justification paragraph for the TDD are in
`MOTOR_SPEED.md`.

Every occurrence of 7000, 8400 or 733/880 rad/s in the document must be
replaced. The inertia target rises to **4.404e-4 kg m^2** (corner), which the
selected 130 mm wheel meets at 4.5115e-4 (102.4%).

### M-5. Brake torque 5.0 N m is asserted with no source, and the supplied servo cannot produce it
`SIZING.py` and `tab:jumpup_budget` use `tau_b = 5.0 N m` per wheel. The BOM
servo (TowerPro MG92B) is **~0.29 N m** — seventeen times smaller. The brake
is a barrier struck by a bolt head (§4.3), so the servo torque is not directly
the braking torque — the servo only *holds* the barrier while the wheel's
momentum does the work. But 5.0 N m is then a structural/impulse figure that
appears nowhere else and is unjustified. `beta` depends on it directly, and
beta sets the inertia target.
TODO: state where 5.0 N m comes from, or measure it. If tau_b is lower, beta
rises sharply — at tau_b = 2.5 N m and L = 180 mm, beta = 2.05 versus 1.34,
which would raise the inertia target by 53% and break the wheel design.

### M-6. Mass budget is 5 of 6 rows TBD, yet M = 1.45 kg drives everything
`tab:massbudget` has only the wheels populated (395 g). Motors, frame,
battery, electronics, wiring are all TBD, but the 1.45 kg total is used as a
hard input to the jump-up sizing everywhere. Two known figures already
contradict it: the **battery alone is ~600 g** (BOM Table 1) and **3 motors
are 204 g** (68 g each). Wheels 395 + battery 600 + motors 204 = **1199 g, or
83% of the 1.45 kg target, with no frame, no electronics, no fasteners and no
brake**. The target is very likely unachievable, and if M rises the required
inertia rises with it (h_w scales with M), which feeds straight back into the
wheel that is already failing its fit checks.
This is the mass-inertia fixed point the introduction warns about, and the
document is currently on the wrong side of it. Owner: Nasia + Dejan, urgent.

### M-7. Motor count in BOM Table 1 versus the footnote versus reality
Table 1 lists qty **3** for motors, drivers and encoders; the footnote says
four are procured; you now confirm three. The table body happens to be right
for the wrong reason. Fix the footnote, delete the spare row in Table 3, and
update the procurement narrative (B-3).

### M-8. BOM procures a steel wheel; Section 5.3 designs a plastic one
BOM Table 3 orders "Reaction-wheel rims, qty 3 ... laser-/water-cut steel
ring, ~120 mm OD, 3-4 mm thick", flagged **H** lead-time risk and described in
the BOM intro as gating the entire build. Section 5.3 designs a **printed
PET-CF ring with steel hex-nut ballast** — no cut steel rim at all. These are
two incompatible wheels, and the one being procured is the one with the long
lead time. Either the procurement line is obsolete (likely, since the ballast
scheme post-dates it) or the wheel design is not the one being built.
Given C6 procurement was due 24 Jul, this needs checking against what was
actually ordered. Now also wrong on diameter: 130 mm, not 120 mm.

### M-9. Driver electrical-frequency ceiling is misrepresented
BOM Table 2: "Electrical frequency: 12 pole pairs x 116.7 s^-1 at 7000 rpm =
1400 Hz vs 2000 Hz driver ceiling" — framed as though the driver constrains
top speed. A 2000 Hz ceiling is 10000 rpm mechanical, above every
voltage-limited figure. The binding constraint is the battery, not the driver.
See `MOTOR_SPEED.md`.

### M-10. Section 5.2 claims three coupled constraints, then only closes two
The volume constraint paragraph says the wheel OD is capped by the envelope
but never states the cap. No number is given for the maximum wheel OD that
fits, which is precisely the number needed to justify 180 mm (see
`ENVELOPE_JUSTIFICATION.md`). The constraint is asserted, not evaluated.

---

## MINOR

### m-1. `main.tex` defines `mfcol` but never uses it
Line 47: `\definecolor{mfcol}{HTML}{C55A11} % manufacturing & circuits`. The
Gantt uses `pfcol`, `ctcol`, `cdcol`, `mscol` only. Either the manufacturing
stream was meant to be colour-separated in the Gantt (my C15-C17 patch rows
would be candidates) or the definition is dead. Same for `p0col` (P0
critical-path highlight) — defined, never used.

### m-2. Three new images are unreferenced
`LATEX/images/` now contains `cubli_full_system_loop.png`,
`cubli_power_tree.png`, `teensy_software_pipeline.png`. No `\includegraphics`
anywhere in any section references them. Section 5.1 (System Architecture),
5.4.2 (Electrical Diagram) and 6 are empty comment stubs that these images
appear designed to fill. Two of the three are mine to place (power tree,
system loop). Flagging so they are not forgotten.

### m-3. Team roles in §2.1 do not match the WBS owners
`tab:team_roles` describes Pablo as "System integration and lead: digital
actuator and sensor coding, embedded software" — but in the WBS, firmware is
Nicc's (B4) and I own circuits, perfboard, harness and electrical
manufacturing (C6, C7, C10, C12, C13). Nicc/"Niccolo" has no contact details
and no surname.

The related naming defect is **resolved**: the WBS previously called
Athanasia Nikolova "Neisa", a misspelling, so §2.1 and the WBS read as two
different people. All WBS and planning references now use the correct short
form "Nasia".

### m-4. Objectives are referenced but never defined
`sec:objectives` is referenced from §1.1, §3.3, §4 intro and §5.2 — the label
is **never defined** in any section file. `grep` finds no
`\label{sec:objectives}`. Every one of those cross-references will render as
`??`. Likely intended to live in §1.3 or §3.1.

### m-5. `sec:2dequilibria` promises a linearization it defers entirely
"its linearization is presented with the control design in
Section~\ref{sec:control2d}" — §4.4.1 then gives only `x := (theta_b,
theta_b_dot, theta_w_dot)` and says "with A, B built from the parameters in
Table 4.1". The A and B matrices are never written down. For a TDD whose
central claim is a validated control design, the linearised plant should
appear explicitly.

### m-6. Empty stub sections heading into a 3 Aug deliverable
Wholly comment-only: §3.1 Scope, §3.2 Actuation trade-off, §3.4 Coordinate
frames, §5.1 System architecture, §5.3.1 2D prototype build, §5.3.2 3D cube
frame, §5.4.2 Electrical diagram, §5.5 System integration, and **all five
subsections of §6 Testing**. §6 is entirely empty. `07_future_work.tex` not
yet reviewed in detail — it is also short.

### m-7. Traceability table verifies everything against "Sec. 6"
`tab:traceability` maps all four objectives to `Sec.~\ref{sec:testing}`
without distinguishing which test verifies which. Since §6 is empty, the
traceability chain the table claims to establish does not exist yet.

### m-8. Inconsistent decimal/unit style in `tab:jumpup_budget`
`omega_max` given as "8400 rpm (880 rad/s)". 8400 rpm = 879.6 rad/s, fine, but
elsewhere the BOM uses 733 rad/s for 7000 rpm. Mixing the two speeds across
tables (M-4) makes the rounding look like a third value. Now superseded: the
design value is **6000 rpm = 628 rad/s**, to be stated identically everywhere.

---

## Cross-cutting: the numbers that must be closed before 3 Aug

Ranked by how much else depends on them:

| # | Open number | Blocks | Owner | State |
|---|---|---|---|---|
| 1 | ~~omega_max~~ | inertia target, wheel design | Pablo | **CLOSED: 6000 rpm** |
| 2 | Real total mass M | h_w, tau_g, beta, the whole jump-up budget | Nasia + Dejan | open, urgent |
| 3 | tau_b provenance (5.0 N m) | beta, inertia target | Dejan + Suvanna | open |
| 4 | ~~Nut identity~~ | wheel inertia, ballast count | Suvanna | **CLOSED: M6, -4.5%** |
| 5 | Max wheel OD inside 180 mm frame | ring OD selection | Nasia | open |
| 6 | 3-motor architecture consequences | bench rig survival, spares, risk register | Pablo + you | open |
| 7 | Nut retention method | wheel safety at 54 N/nut | Suvanna/Nasia | open, new |
| 8 | Pocket placement vs spokes | wheel CAD | Nasia | open, new |

With omega_max and the nut geometry closed, **the mass budget (row 2) is now
the single most consequential open number** — it feeds h_w linearly, and the
wheels+battery+motors alone are already 83% of the 1.45 kg target.

---

## Action required from me

`electrical/PLAN.md`, `STATUS.md` and `RISKS.md` were written assuming four
motor sets. With three confirmed, these need updating:
- RE11 ("fewer than four complete actuation sets") is no longer a risk — it is
  the baseline. It should be rewritten as a **no-spare** risk: any motor,
  driver or encoder failure after 7 Aug loses an axis with no replacement and
  no resupply lead time before 20 Aug. That is a higher-severity row than the
  one it replaces.
- E1.3 "incoming inspection of 4 motor sets" -> 3 sets.
- The bench rig plan (E3, and the "permanent development bench" premise
  throughout) must change: the rig uses one of the three cube sets and must be
  stripped at cube integration on 7 Aug, or the cube runs on two axes.
- `wbs_patch.tex` note 2 (the 3-vs-4 BOM discrepancy) should be rewritten to
  say the correct number is 3 and the footnote is the error.

Tell me which way you want the rig/cube hardware conflict resolved and I will
update all four files in one pass.
