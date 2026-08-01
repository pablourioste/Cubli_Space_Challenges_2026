# 130 mm Reaction Wheel — Sizing (SUPERSEDED)

> **SUPERSEDED 28 Jul by `WHEEL_130_M6.md`. Do not use the numbers below.**
>
> Two inputs changed after this was written:
> 1. The nut was a mixed-up geometry (13 mm across flats = M8, with an M6 bore
>    and M6 thickness), which is why its mass was -43% against its own shape.
>    The real part is an **M6, 10 mm across flats**.
> 2. The design speed is fixed at **6000 rpm**, not the 7327 rpm assumed here.
>
> The selected geometry is now **130 mm OD, 20 mm ring width, 12 mm thick,
> 18 M6 nuts in 5.2 mm blind pockets**, with all fit checks passing. This file
> is kept only for the OD trade-study reasoning; every number in it is stale.

Decision: **OD = 130 mm** (replaces the 120 mm selection in Section 5.3).
Speed basis: see `MOTOR_SPEED.md`.

## The problem with 130 mm at the current ring geometry

130 mm bare ring + 3 spokes, 17 mm radial width, 10 mm thick PET-CF:
**I = 2.686e-4 kg m^2, mass 96.4 g, ballast radius 56.5 mm.**

Nuts needed to reach the target depends entirely on which speed you size to:

| omega_max | Target (1e-4) | Nuts | I achieved | Wheel mass | Circumferential wall |
|---|---|---|---|---|---|
| 8400 rpm (document) | 3.146 | 12 | 3.265 | 114.4 g | 14.1 mm OK |
| 8353 rpm (charged) | 3.163 | 12 | 3.265 | 114.4 g | 14.1 mm OK |
| **7327 rpm (recommended)** | **3.606** | **21** | **3.699** | **127.9 g** | **1.4 mm TOO THIN** |
| 6917 rpm (sagged) | 3.820 | 24 | 3.844 | 132.4 g | -0.7 mm OVERLAP |

**The 130 mm wheel closes comfortably only at the optimistic speed.** At the
speed we should actually design to, the 17 mm ring cannot hold enough nuts —
the same circumferential wall failure the 120 mm wheel has (AUDIT.md B-2),
just less severe. And the radial wall is 0.8 mm at 17 mm width regardless of
nut count, which already fails the 2 mm minimum (AUDIT.md M-2).

## Geometry that does close at 7327 rpm

Sweeping ring width and thickness, target 3.606e-4:

| Ring width | Thickness | Bare I | Nuts | I | Wheel mass | 3 wheels | Circ wall | Radial wall | Verdict |
|---|---|---|---|---|---|---|---|---|---|
| 17 | 10 | 2.686 | 21 | 3.699 | 127.9 | 384 g | 1.4 | 0.8 | fails both |
| 17 | 12 | 3.223 | 9 | 3.657 | 129.2 | 388 g | 24.0 | 0.8 | fails radial |
| **20** | **12** | **3.486** | **3** | **3.624** | **132.4** | **397 g** | **99.7** | **2.3** | **OK** |
| 22 | 10 | 3.028 | 15 | 3.690 | 135.4 | 406 g | 7.1 | 3.3 | OK |
| 22 | 12 | 3.634 | 0 | 3.634 | 135.5 | 407 g | — | 3.3 | bare exceeds +1% |
| 25 | 10 | 3.182 | 12 | 3.683 | 139.8 | 419 g | 12.0 | 4.8 | OK |
| 25 | 15 | 4.773 | 0 | 4.773 | 182.8 | 548 g | — | 4.8 | bare exceeds +26% |

### Recommended: 130 mm OD, 20 mm ring width, 12 mm thick, 3 nuts

- I = 3.624e-4 against a 3.606e-4 target (100.5%).
- Radial wall 2.3 mm — clears the 2 mm minimum, which no 17 mm variant does.
- Circumferential wall is a non-issue at 3 nuts.
- **Trim range is the real argument:** the bare ring gives 3.486e-4 (96.7% of
  target) and each nut adds 0.048e-4. Three nuts is a *small* correction on a
  ring that nearly closes on its own, so the wheel can be trimmed in both
  directions after fabrication — up by adding nuts (plenty of room), down by
  omitting them. This is what the ballast scheme was for, and the 120 mm and
  17 mm designs had lost it.
- 3 nuts also sits symmetric with the 3 spokes (`N_round_to = 3`).

Alternative if you want more upward trim authority: **22 mm width, 10 mm
thick, 15 nuts** (3.690e-4, 135.4 g, both walls pass). Heavier by 3 g/wheel
and more nuts to install, but a larger adjustment range.

## Mass consequence

3 wheels at 132.4 g = **397 g**, essentially unchanged from the 394.6 g the
document currently budgets, so `tab:massbudget` does not move. That does *not*
rescue the mass budget — see AUDIT.md M-6, which is a separate and larger
problem (wheels + battery + motors alone are already 83% of the 1.45 kg
target).

## What must change in the document

| Location | Now | Should be |
|---|---|---|
| §5.3 selected design | OD 120, 21 nuts | OD 130, 20 mm width, 12 mm thick, 3 nuts |
| §5.3 ring geometry | 120 mm OD, 15 mm width, 10 mm thick | 130 / 20 / 12 |
| §5.3 nut spec | 11 mm A/F, 3.12 g | 13 mm A/F, 2.5 g (pending M-1 resolution) |
| §5.3 trade table | whole table | regenerate from updated SIZING.py |
| §5.3 radial caveat | "increase to >=17 mm" | resolved at 20 mm; delete or restate |
| §4.3.1 omega_max | 8400 rpm | 7327 rpm (or 7300) |
| §4.3.1 I_w target | 3.15e-4 | 3.606e-4 |
| §5.2 inertia cases | 2.85 / 3.15e-4 | recompute both at 7327 rpm |
| BOM Table 2 | 7000 rpm, >=3.9e-4, 150 mm/2 kg cube | 7327 rpm, 3.606e-4, 180 mm/1.45 kg |
| BOM Table 3 | rims "~120 mm OD, 3-4 mm steel" | 130 mm OD — and note the wheel is printed PET-CF + nuts, not cut steel |

Last row is a substantive contradiction I had not previously flagged: **BOM
Table 3 procures laser-cut steel rims, while Section 5.3 designs a printed
PET-CF ring with nut ballast.** Those are two different wheels. Adding to
AUDIT.md.

## `SIZING.py` changes to apply

```python
L          = 0.18      # unchanged
rpm_max    = 7327      # was 8400  -- see MOTOR_SPEED.md
ring_width_mm = 20.0   # was 17.0
t_mm          = 12.0   # was 10.0
OD_list_mm = [110, 120, 130, 140, 150]   # 130 is the selection
```

Unresolved input, unchanged by this: the 2.5 g measured nut is -43% against
its own geometry (AUDIT.md M-1). Every number here inherits that uncertainty
through `k2_nut`. Resolve the nut identity before cutting anything.
