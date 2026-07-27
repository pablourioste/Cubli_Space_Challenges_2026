# Procurement — Items Not in the Supplied BOM

Preserved from the BOM gap table, which was removed from the TDD on 28 Jul.
The supplied BOM is electronics-only; everything below must still be bought or
fabricated. Kept here because several lines are mine under C6 and would
otherwise have no record anywhere.

Lead-time risk: H / M / L. Tick when confirmed received.

## Mechanical / structural

| # | Item | Qty | Driven by | Risk | State |
|---|---|---|---|---|---|
| [ ] | Frame stock (Al angle / extrusion / CF tube) | 1 set | Three mutually orthogonal, rigid motor faces | H | todo |
| [ ] | Filament, PET-CF | — | Reaction wheels (130 mm ring + spokes) | M | todo |
| [ ] | Filament, PETG / TPU | — | Printed structure and brackets | L | todo |
| [ ] | M6 steel hex nuts, ISO 4032 | 60+ | Wheel ballast: 18/wheel x 3, plus trim spares | L | todo |
| [ ] | M3 fasteners + heat-set inserts + threadlocker | 1 set | Vibration-proof assembly | L | todo |

Note: the deleted table listed "laser-/water-cut steel wheel rims, 3 off,
~120 mm OD" as an H-risk long-lead item. **That is not the wheel being built.**
The wheel is a printed PET-CF ring with M6 nut ballast
(`WHEEL_130_M6.md`), so the steel rim line is obsolete and is not carried
forward. If it was already ordered under C6, that spend needs review.

## Electrical / power — mine

| # | Item | Qty | Driven by | Risk | State |
|---|---|---|---|---|---|
| [ ] | Bus bulk capacitor, 470-1000 uF, >= 50 V, low-ESR | 1 | Regen-braking transient, 89 J/wheel at 6000 rpm | L | todo |
| [ ] | XT30 connector pairs | 4+ | moteus-n1 power connector; BOM supplies XT90 only | L | todo |
| [ ] | Wire, 14 AWG (bus) + 24-26 AWG (signal) | 1 set | Power and signal harness | L | todo |
| [ ] | Bullet connectors, heat-shrink | 1 set | Motor phase leads, harness termination | L | todo |
| [ ] | E-stop / anti-spark switch + inline fuse | 1 | Safety: cut energy on the 40-60 A bus | M | todo |

## Bench / safety — mine, needed before any bring-up

| # | Item | Qty | Driven by | Risk | State |
|---|---|---|---|---|---|
| [ ] | Bench PSU, current-limited, 0-30 V, >= 5 A | 1 | All firmware bring-up; never on the battery | M | todo |
| [ ] | LiPo charger | 1 | Battery charging | M | todo |
| [ ] | LiPo safe bag + cell alarm | 1 | Battery storage and discharge safety | M | todo |

## Spares — status changed

The deleted table listed "spare motor + spare moteus-n1, 1 each" at H risk.
**Confirmed 28 Jul: three complete actuation sets, no spare.** This line is
therefore not a procurement item but an accepted risk — see RE11 in
`RISKS.md`, which needs rewriting on that basis. Resupply lead time does not
fit before 20 Aug, so a failed motor or driver after integration loses an axis
permanently.

## Open questions

1. Which of the above were actually ordered under C6 (due 24 Jul)? The whole
   list needs reconciling against what arrived.
2. Bulk capacitor lead time — E4.2 on 3 Aug depends on it.
3. Bench PSU current ceiling: >= 5 A was the spec, but a three-driver bench
   test may exceed that.
