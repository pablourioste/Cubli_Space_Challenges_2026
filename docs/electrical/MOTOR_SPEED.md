# Maximum Wheel Speed — Accurate Derivation and Design Value

**DESIGN VALUE: omega_max = 6000 rpm (628 rad/s).** Conservative, deliberate,
and used everywhere in the project. Justification below.

Resolves AUDIT.md M-4 (BOM said 7000 rpm, sizing said 8400 rpm). Neither was
correct as an unqualified "max speed", and both were optimistic.

Inputs: T-Motor MN4006 KV380 (Kv = 380 rpm/V, R_phase = 194 mOhm, 18N24P ->
12 pole pairs), mjbots moteus-n1, Turnigy 6S LiPo.
Kt = 9.5493/380 = **0.02513 N m/A**.

## What the motor can theoretically reach

### 1. Ideal no-load, Kv * V

| Pack state | Bus V | Kv*V (rpm) |
|---|---|---|
| Charged (4.20 V/cell) | 25.2 | 9576 |
| Nominal (3.70 V/cell) | 22.2 | 8436 |
| Loaded/sagged (3.50 V/cell) | 21.0 | 7980 |

The document's old 8400 rpm was `Kv x 22.2 V` — nominal pack, **no load, zero
losses**. An upper bound, never an operating point.

### 2. Winding IR drop, omega = Kv*(V - I*R_ll), R_ll = 2*R_phase = 0.388 ohm

| I (A) | Torque (N m) | 25.2 V | 22.2 V | 21.0 V |
|---|---|---|---|---|
| 0 | 0.000 | 9576 | 8436 | 7980 |
| 2 | 0.050 | 9281 | 8141 | 7685 |
| 5 | 0.126 | 8839 | 7699 | 7243 |
| 8 | 0.201 | 8396 | 7256 | 6800 |
| 12 | 0.302 | 7807 | 6667 | 6211 |
| 16 | 0.402 | 7217 | 6077 | 5621 |

### 3. Modulation ceiling

moteus-n1 runs sinusoidal FOC with SVPWM. Available phase voltage is below the
raw bus figure Kv is rated against; the practical derate for sinusoidal drive
against a trapezoidally-rated Kv is 0.85-0.95. Taking 0.90.

### 4. Driver electrical-frequency ceiling — not binding

12 pole pairs, f_e = rpm/60 * 12:

| Mechanical | f_e |
|---|---|
| **6000 rpm** | **1200 Hz** |
| 7000 rpm | 1400 Hz |
| 8400 rpm | 1680 Hz |

A 2000 Hz ceiling is **10000 rpm mechanical** — above every voltage-limited
figure. The BOM's framing ("1400 Hz vs 2000 Hz driver ceiling", implying the
driver constrains us) is misleading. The battery constrains us, not the driver.

TODO: confirm the moteus-n1 electrical-frequency limit against mjbots
documentation. 2000 Hz is our BOM's figure, unverified against source. At
6000 rpm / 1200 Hz we have 40% margin even if it is correct.

### 5. Realistically achievable ceiling (spin-up at ~2 A against drag)

| Pack state | After IR | After modulation | Achievable |
|---|---|---|---|
| Charged 25.2 V | 9281 | 8353 | 8353 rpm (875 rad/s) |
| Nominal 22.2 V | 8141 | 7327 | 7327 rpm (767 rad/s) |
| Sagged 21.0 V | 7685 | 6917 | 6917 rpm (724 rad/s) |

## Why the design value is 6000 rpm, below all of these

**6000 rpm is 13% below even the sagged-pack figure.** That is deliberate
margin, and it is the right call for this project:

1. **The jump-up is attempted repeatedly across a session.** Sizing to a
   charged-pack number gives a machine that works on the first attempt after
   charging and degrades as the pack drains — the worst failure mode for a
   demo day. 6000 rpm holds across essentially the whole discharge curve.
2. **The operating point is comfortable, not marginal.** 6000 rpm needs only
   15.79 V of back-EMF, **71% of the nominal 22.2 V bus**, leaving **37%
   voltage headroom against a charged pack**. Even at 8 A of accelerating
   current the motor needs 18.89 V of a 25.2 V pack. The controller never
   runs into the voltage ceiling, so the wheel accelerates predictably right
   up to its commanded top speed instead of soft-limiting.
3. **Every derived quantity gets safer.** Stored energy 89 J/wheel instead of
   133 J at 7327. Nut retention load 54 N instead of 81 N. Hoop stress
   1.54 MPa. Rim speed 40.8 m/s. Bearing loads, containment requirements and
   brake energy all scale with speed squared.
4. **It absorbs the open unknowns.** Motor Kv tolerance, unmodelled bearing
   and aerodynamic drag, controller derating, and the still-unresolved mass
   figure (AUDIT.md M-6) all erode achievable speed. 6000 rpm has room for
   all of them without a redesign.

The cost is a larger wheel: I_w scales as 1/omega_max, so 6000 rpm demands
**4.404e-4** against 3.146e-4 at 8400 rpm — 40% more inertia. The 130 mm
wheel absorbs this with 18 M6 nuts and all fit checks passing
(`WHEEL_130_M6.md`), so the conservatism is affordable. **Buy the margin.**

## Design figures at 6000 rpm — use these everywhere

| Quantity | Value |
|---|---|
| **omega_max** | **6000 rpm = 628 rad/s** |
| Electrical frequency | 1200 Hz (12 pole pairs) |
| Back-EMF at speed | 15.79 V (71% of nominal bus) |
| tau_g (180 mm, 1.45 kg) | 1.280 N m |
| beta (tau_b = 5.0 N m) | 1.344 |
| h_w, corner | 0.2767 kg m^2/s |
| h_w, edge | 0.2510 kg m^2/s |
| **I_w target, corner (governs)** | **4.404e-4 kg m^2** |
| I_w target, edge | 3.995e-4 kg m^2 |
| Corner vs edge | corner 10.2% more demanding |

At the selected 130 mm wheel (I = 4.5115e-4, 102.4% of target):

| Quantity | Value |
|---|---|
| Stored energy per wheel | 89.1 J |
| Stored energy, three wheels | 267 J |
| Angular momentum per wheel | 0.2835 kg m^2/s |
| Rim speed at r = 65 mm | 40.8 m/s |
| Hoop stress in PET-CF | 1.54 MPa |
| Centrifugal force per M6 nut | 54.3 N |

## How to state it in the TDD

> The maximum wheel speed is set to 6000 rpm (628 rad/s). This is
> deliberately conservative: the MN4006 at KV380 reaches approximately
> 8400 rpm unloaded on a nominal 6S pack, and around 6900 rpm once winding
> losses, sinusoidal-drive derating and end-of-charge pack voltage are
> accounted for. Designing to 6000 rpm requires only 71% of the nominal bus
> voltage as back-EMF, so the wheel reaches its commanded speed across the
> whole usable discharge range rather than only on a freshly charged pack,
> and it leaves margin for motor tolerance, bearing and aerodynamic drag and
> the residual uncertainty in the mass budget. The cost is a 40% larger wheel
> inertia requirement than a top-of-range assumption would give, which the
> selected 130 mm ballasted wheel meets with 2.4% margin.
