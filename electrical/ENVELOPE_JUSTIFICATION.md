# Justification of the 180 mm Cube Envelope

> **REVISION 28 Jul (second pass):** written originally at 8400 rpm, then
> revised at 7327 rpm. The design speed is now fixed at **6000 rpm**
> (`MOTOR_SPEED.md`) and the wheel is 130 mm OD with a 20 x 12 mm ring
> (`WHEEL_130_M6.md`). **Read "Final: at 6000 rpm" at the end** — the tables in
> the body are at superseded speeds and are kept only to show the sensitivity
> structure. The conclusion (180 mm) is unchanged and is now more strongly
> supported than at either earlier speed.

Prepared for Section 5.2 (`sec:massbudget`). Numbers computed with the same
model as `SIZING.py`; sensitivity run in `electrical/` notes below.

Status of the decision: the document currently *asserts* 180 mm without
argument. Everything below is the missing argument. It is a genuine
justification, not a rationalisation: the constraint that fixes L is the wheel
inertia target, and it is decidable on paper.

## The coupling that sets the envelope

Cube edge length L enters the design three times, and they fight each other:

1. **Required momentum grows as L^1.5.**
   `h_w,ideal = sqrt(eta) * (sqrt(2 g lambda kappa)/n) * M * L^1.5`
   Bigger cube -> more momentum needed per wheel.
2. **Gravitational tip-over torque grows as L.**
   `tau_g = M g L / 2`, and the brake amplification `beta = tau_b/(tau_b - tau_g)`
   blows up as tau_g approaches the brake torque tau_b. Bigger cube -> the
   finite brake is less effective, a second penalty on top of (1).
3. **Available wheel inertia grows as OD^2 (roughly), and OD is capped by L.**
   The wheel must fit inside the frame with the motor, brake and contact
   features. Bigger cube -> a bigger wheel is *permitted*.

(1) and (2) push L down. (3) pushes L up. The envelope is the smallest L at
which (3) can still satisfy (1)+(2) with margin.

## Sensitivity: what each envelope demands and what it allows

Corner case (governs), M = 1.45 kg, tau_b = 5.0 N m, omega_max = 8400 rpm,
eta = 1.05:

| L (mm) | tau_g (N m) | beta | h_w (kg m^2/s) | I_w target (1e-4 kg m^2) |
|---|---|---|---|---|
| 150 | 1.067 | 1.271 | 0.1991 | 2.263 |
| 160 | 1.138 | 1.295 | 0.2234 | 2.539 |
| 170 | 1.209 | 1.319 | 0.2492 | 2.833 |
| **180** | **1.280** | **1.344** | **0.2767** | **3.146** |
| 200 | 1.422 | 1.398 | 0.3370 | 3.831 |

Inertia actually available from the bare PET-CF ring + 3 spokes
(17 mm radial width, 10 mm thick), before any ballast:

| Ring OD (mm) | I (1e-4 kg m^2) | Mass (g) |
|---|---|---|
| 100 | 1.074 | 70.0 |
| 110 | 1.504 | 78.8 |
| 120 | 2.037 | 87.6 |
| 130 | 2.686 | 96.4 |
| 140 | 3.460 | 105.3 |
| 150 | 4.372 | 114.1 |

## The argument for 180 mm

**Why not 150 mm.** A 150 mm cube needs I_w = 2.26e-4. The wheel that fits
inside a 150 mm frame is at most ~120 mm OD once the frame wall, the motor
boss and the corner contact features are allowed for (a 30 mm total
allowance). A 120 mm bare ring gives 2.04e-4 — *short of the target on its
own*, so the entire margin must come from ballast, and the ballast is exactly
what the radial-fit check shows does not comfortably fit in a 17 mm ring. The
150 mm option closes only on paper and only with zero tuning margin in the
direction that matters (adding inertia after fabrication).

**Why not 200 mm.** The penalty is superlinear: 200 mm needs 3.83e-4, a 22%
jump over 180 mm, and beta has degraded to 1.398 — the brake is losing 40% of
its impulse to gravity. It also spends mass on frame for no dynamic benefit.

**Why 180 mm.** It needs I_w = 3.146e-4. A 180 mm frame accommodates a
130-140 mm wheel with the same 30-40 mm allowance. The bare 130 mm ring gives
2.69e-4 (85% of target) and the bare 140 mm ring gives 3.46e-4 (110%). So the
target is reachable *from the ring alone* at 140 mm, or with modest ballast at
130 mm. This is the design property that matters: the wheel can be trimmed in
**both** directions after fabrication — add nuts if the measured inertia falls
short, omit them if it overshoots — which is the whole point of the ballast
scheme and the only defence against the parameter uncertainty the document
admits to in Section 4.2.

**Statement for the document:**

> The 180 mm envelope is set by the corner-case jump-up requirement. Required
> per-wheel momentum scales as `M L^1.5` and the finite-brake penalty
> `beta = tau_b/(tau_b - MgL/2)` degrades with L, so a larger cube is doubly
> penalised; conversely the achievable wheel inertia scales with the square of
> a diameter that the frame caps at roughly `L` minus 30-40 mm. At 150 mm the
> largest wheel that fits (about 120 mm OD) yields 2.04e-4 kg m^2 against a
> 2.26e-4 kg m^2 requirement, closing only with ballast at full stretch and no
> capacity to trim the wheel upward after fabrication. At 180 mm the
> requirement is 3.15e-4 kg m^2 while a 130-140 mm wheel provides
> 2.69-3.46e-4 kg m^2 from the printed ring alone, so the ballast serves its
> intended purpose as a bidirectional trim rather than as the primary means of
> reaching the target. 180 mm is therefore the smallest envelope that closes
> the inertia budget with margin in both directions.

## Consequences to state alongside the decision

- The introduction cites ETH's 150 mm prototype. The document should say
  explicitly that this design is **larger than** the ETH Cubli and why
  (printed PET-CF ballasted wheel rather than a machined steel flywheel, so a
  lower achievable density-at-radius, compensated with radius).
- The 150 mm figure in the BOM Table 2 caption and any 150 mm assumption
  elsewhere must be corrected to 180 mm (see AUDIT.md, I-2).
- The selected wheel OD in Section 5.3 is 120 mm, which is the wheel sized for
  a **150 mm** cube, not a 180 mm one. This is the single largest technical
  inconsistency in the document (AUDIT.md, I-1).

## Revised at 7327 rpm (SUPERSEDED — see "Final: at 6000 rpm" below)

Redone with the corrected speed and the 20 mm x 12 mm ring section:

| L (mm) | I_w target (1e-4) | Max wheel OD (L-30) | Bare I at that OD | Bare I at 130 mm |
|---|---|---|---|---|
| 150 | 2.595 | 120 | 2.629 | 3.486 |
| 160 | 2.911 | 130 | 3.486 | 3.486 |
| **180** | **3.606** | **150** | **5.728** | **3.486** |
| 200 | 4.392 | 170 | 8.780 | 3.486 |

**This changes the shape of the argument and I should be explicit about it.**
At the corrected speed and the thicker 20x12 ring section, a 150 mm cube also
closes: target 2.595e-4 against 2.629e-4 available from a 120 mm bare ring.
The original "150 mm does not close" claim was an artefact of the thinner
17x10 section, not a property of the envelope.

The honest justification for 180 mm is therefore **not** that smaller is
infeasible. It is:

1. **Trim authority.** At 150 mm the 120 mm wheel clears the target by 1.3%
   with the bare ring — no room to trim *down*, and adding nuts to trim up
   runs into the same circumferential-wall wall that killed the original
   120 mm design. At 180 mm the 130 mm wheel sits at 96.7% bare and reaches
   target with 3 nuts, adjustable in both directions.
2. **Packaging, which is now the real driver.** A 150 mm cube must fit three
   120 mm wheels plus three MN4006 motors (44.35 mm dia x 21 mm), a ~600 g
   6S pack, the perfboard (150 x 90 mm — note this alone is 150 mm across,
   i.e. it does **not** fit inside a 150 mm cube with any wall at all), three
   moteus-n1 drivers, and the brake servos. The 150 x 90 mm board is by
   itself a decisive argument for 180 mm.
3. **Mass, which cuts the other way.** A bigger cube means more frame mass,
   and M is already over budget (AUDIT.md M-6). This is the cost of the
   decision and should be stated, not hidden.

**Revised statement for the document:**

> The 180 mm envelope is set by internal packaging rather than by the jump-up
> energy budget alone. Each of the three faces must carry a 130 mm reaction
> wheel and an MN4006 motor, and the interior must additionally accommodate a
> 6S battery, three moteus-n1 drivers and a 150 x 90 mm power/signal board —
> the last of which does not fit within a 150 mm envelope at any wall
> thickness. On the dynamics side, a 180 mm cube requires 3.61e-4 kg m^2 of
> per-wheel inertia at the design speed of 7327 rpm, which the selected
> 130 mm ring supplies to within 3.5% from its printed structure alone, with
> hex-nut ballast providing bidirectional trim about that point. A 150 mm
> envelope would also close the inertia budget, but only with a wheel sitting
> at the top of its adjustment range and with no room for the electronics
> stack.

## Final: at 6000 rpm (the design speed)

Redone at the fixed design speed, with the 20 x 12 mm ring section:

| L (mm) | I_w target (1e-4) | Max wheel OD (L-30) | Bare I at that OD | Verdict |
|---|---|---|---|---|
| 150 | 3.168 | 120 | 2.629 | **short by 17%** |
| 160 | 3.555 | 130 | 3.486 | short by 2% |
| **180** | **4.404** | **150** | **5.728** | **clears with room** |
| 200 | 5.363 | 170 | 8.780 | clears, but heavier and beta worse |

**At 6000 rpm the earlier ambiguity disappears.** The 150 mm envelope now
fails outright: the largest wheel that fits gives 2.629e-4 against a 3.168e-4
requirement, 17% short, and no amount of ballast recovers it because the
ballast sits at a smaller radius than the ring it displaces. My earlier note
that "150 mm also closes" was true at 7327 rpm and is **not** true at the
conservative speed we have adopted. The lower the design speed, the more
inertia is required, and the more the envelope matters.

The 130 mm wheel selected for the 180 mm cube provides 3.486e-4 bare and
4.5115e-4 with 18 nuts, against the 4.404e-4 target — 102.4%, with upward trim
available to 21 nuts.

**Final statement for the document:**

> The 180 mm envelope follows from the jump-up inertia requirement at the
> adopted design speed, reinforced by internal packaging. Sizing the wheels to
> a conservative 6000 rpm (Section, `MOTOR_SPEED.md`) requires
> 4.40e-4 kg m^2 of per-wheel inertia in the governing corner case. Within a
> 150 mm envelope the largest wheel that clears the frame, motor and contact
> features is approximately 120 mm in diameter, which yields 2.63e-4 kg m^2 —
> 17% short of the requirement, and not recoverable by ballast, which
> necessarily sits inboard of the ring it displaces. The 180 mm envelope
> admits a 130 mm wheel providing 3.49e-4 kg m^2 from its printed structure
> and 4.51e-4 kg m^2 with hex-nut ballast installed, meeting the requirement
> with 2.4% margin and retaining adjustment capacity in both directions.
> Packaging independently requires the larger envelope: the 150 x 90 mm
> power and signal board does not fit within a 150 mm cube at any wall
> thickness, and the interior must additionally carry three motors, three
> drivers, a 6S battery and the brake servos.

Note the brake-torque coupling, unchanged by the speed decision: beta rises
from 1.271 at 150 mm to 1.344 at 180 mm to 1.398 at 200 mm. This is the
penalty for a larger cube and is why 200 mm is not chosen despite its easier
wheel packaging — and it depends entirely on the unverified tau_b = 5.0 N m
(AUDIT.md M-5).

## Open input

TODO: the frame wall thickness and internal clearance that set the "L minus
30 mm" allowance are my estimate, not a CAD number. Neisa should confirm the
actual maximum wheel OD that fits the 180 mm frame before the ring OD is
frozen. The argument above holds for any allowance in the 20-40 mm band, but
the selected OD depends on it.

TODO: confirm the perfboard is really 150 x 90 mm and cannot be split into
two smaller boards. If it can be split, packaging argument (2) weakens
considerably and the envelope decision rests more heavily on trim authority.
That is mine to answer and it feeds E2.3 on 31 Jul.
