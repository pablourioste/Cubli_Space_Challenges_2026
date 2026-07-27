# 130 mm Wheel with M6 Nuts in Blind Pockets — Final Sizing

Supersedes the geometry section of `WHEEL_130.md` (which was computed with the
old mixed-up nut). Speed basis in `MOTOR_SPEED.md`.

## The nut error is resolved

The script previously had a nut that matched no real fastener:

| Input | Old value | Implies |
|---|---|---|
| Across-flats | 13.0 mm | **M8** |
| Bore | 6.6 mm | M6 clearance |
| Thickness | 5.0 mm | M6 |

That mixture is why the measured 2.5 g was **-43% against its own geometry**.
With the real M6 (ISO 4032: 10.0 mm A/F, 5.2 mm thick, 5.35 mm minor-diameter
bore), the geometric estimate is 2.617 g against the measured 2.5 g — **-4.5%**,
which is ordinary manufacturing tolerance and plating variation. The geometry
and the scale now agree.

Reference masses computed from DIN 934 geometry, as a sanity check:

| Nut | A/F | Thickness | Calculated | Typical actual |
|---|---|---|---|---|
| M5 | 8.0 | 4.0 | 1.124 g | ~1.2 g |
| **M6** | **10.0** | **5.2** | **2.617 g** | **~2.2-2.5 g** |
| M8 | 13.0 | 6.5 | 4.903 g | ~4.9 g |

## Selected geometry

**130 mm OD, 20 mm ring width, 12 mm thick, M6 nuts in 5.2 mm blind pockets.**

Applied to `SIZING.py` (ring_width_mm 17 -> 20, t_mm 10 -> 12).

At the design speed **omega_max = 6000 rpm** (`MOTOR_SPEED.md`), target
4.404e-4 kg m^2:

| Check | Value | Limit | Status |
|---|---|---|---|
| Nuts required | 18 | — | — |
| Inertia achieved | 4.512e-4 (102.4%) | >= target | OK |
| Circumferential wall | 7.2 mm | >= 2 mm | **OK** |
| Radial wall, flats-radial | 4.80 mm | >= 2 mm | **OK** |
| Radial wall, corners-radial | 4.00 mm | >= 2 mm | **OK** |
| Blind-pocket floor | 6.8 mm | >= 2 mm | **OK** |
| Wheel mass | 161.6 g | — | — |
| Three wheels | 485 g | — | 33.4% of 1.45 kg |

**All four fit checks pass.** This is the first wheel geometry in the project
that does. The nut orientation no longer needs to be constrained — it fits
either way round, which removes an assembly error mode.

## Why the pockets are blind, and what that costs

The pockets are recesses, not through-holes: a 5.2 mm pocket in a 12 mm ring
leaves a **6.8 mm plastic floor** under each nut. This is deliberate — the
floor is what stops a nut leaving the wheel radially.

I added a floor check to `SIZING.py`, because the script computed `floor_mm`
and then never tested it. It also now reports the centrifugal load:

At the ballast radius of 55 mm, the load per nut at the 6000 rpm design speed
is **54.3 N (5.5 kgf)**. It scales with the square of speed, so any later
decision to raise omega_max raises this quadratically: ~81 N at 7327 rpm,
~106 N at 8400 rpm. The 6.8 mm PET-CF floor carries it in bending and will
hold, but the nut is a loose steel mass in a plastic pocket on a wheel
spinning next to people.

**Retention is required and is not currently in the design.** Options, in
order of preference:
1. Retaining cap or cover plate over the pocket mouths (positive retention,
   reversible, keeps the trim adjustability).
2. Threadlocker or epoxy per nut (simple, but destroys the "re-tune after
   fabrication" property that justified the ballast scheme).
3. Bolt through each nut into the floor (adds mass at the worst radius, and
   the bolt head then needs its own pocket).

Option 1 preserves what the ballast scheme is for. This is Suvanna/Neisa's
call, but it must be decided before the wheels are printed.

## Sensitivity to the speed decision

The speed is now fixed at **6000 rpm** (`MOTOR_SPEED.md`). For reference, had
a less conservative figure been chosen:

| omega_max | Target | Nuts at 20x12 | Circ wall | Verdict |
|---|---|---|---|---|
| **6000 (design)** | **4.404e-4** | **18** | **7.2 mm** | **OK** |
| 7327 | 3.606e-4 | 3 | 103 mm | OK, wide margin |
| 8400 | 3.146e-4 | 0 | — | bare ring exceeds by 11% |

The 20 x 12 ring works across the whole range, so the geometry is not
sensitive to a later revision of the speed. Note the asymmetry: at 6000 rpm
the wheel uses 18 nuts with room for up to 21 (see the spoke-clash limit
below), so it can still be trimmed **upward**. Had we designed at 8400 rpm the
bare ring would already overshoot, leaving no way to trim down except by
removing structure. The conservative speed preserves adjustability in the
direction that matters.

## Pocket placement — the script cannot check this

`SIZING.py` models the ring as a bare annulus and has no knowledge of where
the spokes attach, so its "gap mm" column is a *circumferential pitch* check
only. Placement must be checked separately, and it fails the obvious layout:

- Spoke half-angle at the ring ID (r = 45 mm, 10 mm wide): 6.38 deg
- Pocket half-angle at r = 55 mm (12.01 mm across corners): 6.27 deg
- Required spoke-centre to pocket-centre separation: **12.65 deg**

With N = 18 and 3 spokes, 18/3 = 6 exactly, so a uniform 20 deg pitch puts
**every sixth pocket directly on a spoke root**. Offsetting by half a pitch
does not fix it (10.00 deg separation, still short of 12.65). No uniform pitch
clears the spokes at any usable nut count — 15, 18, 21 and 24 all clash.

**Fix: group the pockets into the three sectors between the spokes.**

| Parameter | Value |
|---|---|
| Usable arc per sector (after spoke keep-outs) | 94.70 deg |
| 18 nuts = 6 per sector, span | 73.10 deg — fits, 21.6 deg spare |
| Even spread within sector: pitch | 18.94 deg |
| Resulting wall between pockets | 6.1 mm |
| Maximum per sector | 7 (21 total) |

This keeps 3-fold symmetry so balance is unaffected, and it caps the upward
trim range at 21 nuts. **This is a CAD constraint for Neisa/Suvanna** — the
script will keep reporting OK regardless, because placement is outside its
model.

## Remaining open items

- **Nut retention method** — required, see above. Not yet designed.
- **Pocket placement** — must follow the sector grouping above, not a uniform
  pitch. Needs to reach whoever draws the wheel.
- **Weigh a real nut.** 2.5 g is in the script as "measured"; the geometry says
  2.617 g. Confirm which, since 18 nuts x 0.12 g is only 2 g on the wheel but
  it shifts the inertia slightly.
- The BOM still procures **laser-cut steel rims** (AUDIT.md M-8). This wheel is
  printed PET-CF with M6 ballast. The procurement line is for a different
  wheel and needs correcting before anything is cut.
- Wheel balance: 18 nuts at 55 mm radius, each 2.5 g. A single missing or
  misplaced nut is a 2.5 g imbalance at 55 mm. The introduction already warns
  that "a wheel half a gram out of balance at rim radius can render a perfectly
  correct estimator unusable" — with 18 discrete masses this is a real
  assembly-control problem, and C9 (balance and spin-test) should explicitly
  cover nut-count verification per wheel.
