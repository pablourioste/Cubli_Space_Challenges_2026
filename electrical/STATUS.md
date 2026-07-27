# Electrical Status Tracker

Update daily. Tick the box, set State, add a date in Notes when it matters.
State: `todo` / `wip` / `done` / `blocked` / `cut`.
Created 27 Jul 2026 (day 5). Day 1 = 23 Jul, day 29 = 20 Aug.

**On re-run: checkbox states and Notes in this file are preserved. Do not reset them.**

---

## Assumed complete before today (verify, do not assume)

| # | Task | Owner | Was due | Blocked by | State | Notes |
|---|---|---|---|---|---|---|
| [ ] | C6 procurement order placed | Pablo | 24 Jul | — | todo | verify all lines landed, esp. 4th motor set + bulk cap |
| [ ] | C6 4x complete motor/driver/encoder sets confirmed | Pablo | 24 Jul | — | todo | BOM says qty 3; invariant says 4 |
| [ ] | C6 bulk cap 470-1000 uF >= 50 V ordered | Pablo | 24 Jul | — | todo | separate line, not the 16 V caps |
| [ ] | C6 XT30 pairs >= 4 ordered | Pablo | 24 Jul | — | todo | drivers are XT30, battery is XT90 |
| [ ] | C6 bench PSU available | Pablo | 24 Jul | — | todo | current-limited, 0-30 V, >= 5 A |
| [ ] | A3 requirements table support | Dejan+Pablo | 25 Jul | — | todo | electrical requirement rows in? |

## E1 — Bench power, safety, single-axis bring-up (27-29 Jul, days 5-7)

| # | Task | Owner | Due | Blocked by | State | Notes |
|---|---|---|---|---|---|---|
| [ ] | E1.1 Bench PSU + E-stop + fuse in bench loop | Pablo | 27 Jul | C6 | todo | |
| [ ] | E1.2 LiPo safety kit staged | Pablo | 27 Jul | C6 | todo | battery stays out until 9 Aug |
| [ ] | E1.3 Incoming inspection, 4 motor sets | Pablo | 28 Jul | C6 | todo | phase R vs 194 mOhm |
| [ ] | E1.4 moteus-n1 #1 bring-up, CAN ID, FOC cal | Pablo+Nicc | 28 Jul | E1.1, E1.3 | todo | on PSU only |
| [ ] | E1.5 MA600 gap fixture, record shim value | Pablo | 29 Jul | E1.3 | todo | <= 0.5 mm, centred on 4 mm magnet |
| [ ] | E1.6 Open-loop spin, log no-load current + max RPM | Pablo | 29 Jul | E1.4, E1.5 | todo | containment required |
| [ ] | **Gate E1** driver commutates, encoder clean, limit trips | Pablo | 29 Jul | all E1 | todo | |

## E2 — Board outline to Neisa (29-31 Jul, days 7-9) — HARD 1 Aug

| # | Task | Owner | Due | Blocked by | State | Notes |
|---|---|---|---|---|---|---|
| [ ] | E2.1 Driver positions from SPI < 20 cm rule | Pablo | 30 Jul | E1.5, C1 | todo | encoder cable dictates driver location |
| [ ] | E2.2 CAN routing, stubs < 10 cm, bus ends identified | Pablo | 30 Jul | E2.1 | todo | linear topology only |
| [ ] | E2.3 Perfboard floorplan, 15 x 9 cm | Pablo | 31 Jul | E2.1, E2.2 | todo | |
| [ ] | E2.4 **Board outline + connectors -> Neisa** | Pablo | **1 Aug** | E2.3 | todo | gates C5 mass freeze |
| [ ] | E2.5 Electronics mass line -> Dejan | Pablo | 1 Aug | E2.4 | todo | TODO: weigh populated proto |
| [ ] | **Gate E2** outline frozen, C5 unblocked | Pablo | 1 Aug | E2.4 | todo | |

## E3 — 1-DoF rig + parameter measurement (31 Jul - 2 Aug, days 9-11) — HARD 2 Aug

| # | Task | Owner | Due | Blocked by | State | Notes |
|---|---|---|---|---|---|---|
| [ ] | E3.1 Rig electrical assembly, motor set #4 | Pablo+Neisa | 31 Jul | C9, C4, E1.5 | todo | zero float, see dep check |
| [ ] | E3.2 Rig harness, CAN terminated both ends | Pablo | 1 Aug | E3.1, E2.2 | todo | |
| [ ] | E3.3 Powered rig checkout with Nicc | Pablo+Nicc | 1 Aug | E3.2, B6 | todo | disarm + watchdog verified |
| [ ] | E3.4 Measurement setup for Kt / J / friction / latency | Pablo+Andrea | 2 Aug | E3.3, B7 | todo | Andrea owns the numbers |
| [ ] | E3.5 **Deliver 4 measured params -> Andrea** | Pablo | **2 Aug** | E3.4 | todo | gates B9 -> B11 -> B12 |
| [ ] | E3.6 Rig evidence + photos -> Dejan | Pablo | 2 Aug | E3.3 | todo | for A11 |
| [ ] | **Gate E3 = G3** rig balances >= 60 s, params delivered | Pablo | 2 Aug | all E3 | todo | |

## A5 support — risk register (due with TDD 3 Aug)

| # | Task | Owner | Due | Blocked by | State | Notes |
|---|---|---|---|---|---|---|
| [ ] | Electrical risk rows -> Dejan | Pablo | 3 Aug | RISKS.md | todo | see electrical/RISKS.md |

## E4 — Perfboard + harness, C12 (3-6 Aug, days 12-15)

| # | Task | Owner | Due | Blocked by | State | Notes |
|---|---|---|---|---|---|---|
| [ ] | E4.1 XT90 -> 3x XT30 distribution harness | Pablo | 3 Aug | C6 | todo | no WBS task owns this |
| [ ] | E4.2 Populate perfboard, rails + bulk cap | Pablo | 4 Aug | E2.3, bulk cap | todo | 16 V caps on 5 V rail ONLY |
| [ ] | E4.3 Rail bring-up, ripple, LM2596 thermal | Pablo | 4 Aug | E4.2 | todo | derates without heatsink |
| [ ] | E4.4 CAN harness, split termination at 2 ends | Pablo | 5 Aug | E4.2, E2.2 | todo | 2x 60.4 ohm + 4.7 nF |
| [ ] | E4.5 5 Mbps bus integrity, scope + soak | Pablo | 5 Aug | E4.4 | todo | no error frames |
| [ ] | E4.6 Servo brake wiring, 5 V headroom check | Pablo | 6 Aug | E4.3 | todo | MG92B stall current |
| [ ] | E4.7 Label, strain-relieve, photograph | Pablo | 6 Aug | E4.4, E4.6 | todo | |
| [ ] | **Gate E4** full bench power-on, 3 drivers, on PSU | Pablo | 6 Aug | all E4 | todo | |

## E5 — Cube integration + power-on, C13 (7-9 Aug, days 16-18) — G5 9 Aug

| # | Task | Owner | Due | Blocked by | State | Notes |
|---|---|---|---|---|---|---|
| [ ] | E5.1 Install board + harness, re-check all MA600 gaps | Pablo+Neisa | 7 Aug | C11, E4.7 | todo | gap drifts on assembly |
| [ ] | E5.2 Continuity + isolation before power | Pablo | 7 Aug | E5.1 | todo | confirm no 16 V cap on 25 V bus |
| [ ] | E5.3 PSU smoke test, wheels off | Pablo | 8 Aug | E5.2 | todo | all 3 drivers enumerate |
| [ ] | E5.4 PSU test, wheels on, open-loop per axis | Pablo | 8 Aug | E5.3 | todo | |
| [ ] | E5.5 **First battery power-on** | Pablo | 9 Aug | E5.4 | todo | anti-spark, fuse, alarm, safe area |
| [ ] | E5.6 Handover: all axes addressable, telemetry up | Pablo | 9 Aug | E5.5 | todo | to Nicc + Andrea |
| [ ] | **Gate E5 = G5** cube integrated and powered | Pablo | 9 Aug | all E5 | todo | |

## E6 — Edge-balance support (10-13 Aug, days 19-22) — HARD KILL 13 Aug

| # | Task | Owner | Due | Blocked by | State | Notes |
|---|---|---|---|---|---|---|
| [ ] | E6.1 On-call support to B11 | Pablo | 13 Aug | E5.6 | todo | priority over everything |
| [ ] | E6.2 Vibration fault hunt, CAN + encoder error counters | Pablo | 12 Aug | E6.1 | todo | correlate with wheel speed |
| [ ] | E6.3 C14 brake support (Suvanna owns) | Pablo | 13 Aug | E4.6, C14 | todo | SACRIFICIAL if G6 at risk |
| [ ] | E6.4 Battery endurance under balance load | Pablo | 13 Aug | E6.1 | todo | for demo-day planning |
| [ ] | **Gate E6 = G6** edge balance, no open electrical defect | Pablo | 13 Aug | E6.1 | todo | S3 cut if missed |

## E7 — Corner, jump-up, presentation (14-20 Aug, days 23-29)

| # | Task | Owner | Due | Blocked by | State | Notes |
|---|---|---|---|---|---|---|
| [ ] | E7.1 Support B12 corner balance + slew | Pablo | 16 Aug | E6 gate | todo | |
| [ ] | E7.2 Brake circuit support for B13 jump-up | Pablo | 18 Aug | E6.3, G6 pass | todo | only if G6 passed 13 Aug |
| [ ] | E7.3 Demo-day spares + field-repair kit | Pablo | 17 Aug | — | todo | spare harness/driver/encoder |
| [ ] | E7.4 Electrical figures for TDD final + deck | Pablo | 19 Aug | E4.7, E6.4 | todo | block diagram, power tree |
| [ ] | E7.5 Final presentation support | Pablo | 20 Aug | all | todo | |
| [ ] | **Gate E7 = G9** demo runs on battery, no intervention | Pablo | 20 Aug | all | todo | |

## Open questions log (mirror of PLAN.md, tick when answered)

| # | Question | State |
|---|---|---|
| [ ] | Populated perfboard mass | todo |
| [ ] | Bulk cap >= 50 V ordered / lead time | todo |
| [ ] | XT30 pairs received, count | todo |
| [ ] | Bench PSU actual current ceiling | todo |
| [ ] | JST-PH3 CAN cable gauge (BOM flags TODO) | todo |
| [ ] | Total 5 V load vs LM2596 rating | todo |
| [ ] | 4th complete motor set actually ordered | todo |
| [ ] | Cube edge 150 mm or 180 mm | todo |
