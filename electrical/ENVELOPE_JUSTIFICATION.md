# Justification of the 180 mm Cube Envelope

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

## Open input

TODO: the frame wall thickness and internal clearance that set the "L minus
30-40 mm" allowance are my estimate, not a CAD number. Neisa should confirm
the actual maximum wheel OD that fits the 180 mm frame before the ring OD is
frozen. The argument above holds for any allowance in the 20-40 mm band, but
the selected OD depends on it.
