# Electrical Status Tracker

Update daily. Tick the box, set State, add a date in Notes when it matters.
State: `todo` / `wip` / `done` / `blocked` / `cut`.
Created 27 Jul 2026 (day 5). Day 1 = 23 Jul, day 29 = 20 Aug.

**On re-run: checkbox states and Notes in this file are preserved. Do not reset them.**

---

## RE-BASELINE 31 Jul 2026 (day 9)

Status below was verified at the schedule review of 31 Jul, not assumed. The
consolidated re-baselined plan is in `sections/02_project_organization_tasks.tex`
and `sections/02_project_organization_gantt.tex`; the original EL dates are kept
in `schedule.yaml` as the historical record.

**Headline:** the electrical design (wiring scheme, component placement) is
issued and complete. **No bench electrical testing has been carried out yet.**
First powered bring-up is Sunday **2 Aug**, with **3 Aug held as a recovery
buffer**. Parameter measurement moves to **7-9 Aug**.

Decisions taken at the review:

- **Cube edge = 150 mm.** Closes the 150 vs 180 mm conflict (was Q-8 / wbs_patch item 3).
- **Jump-up (S3) is sacrificial scope.** It yields to edge and corner balance.
- **Procurement round 2** follows the 3D frame freeze; order by **5 Aug**.

Revised gates: M1 2 Aug (open-loop bring-up) - M4 7 Aug (closed loop) -
M6 9 Aug (parameters) - G3 12 Aug (rig balances) - G5 15 Aug (cube integrated) -
G6 17 Aug (edge) - G7 19 Aug (corner) - G8/G9 20 Aug.

---

## Assumed complete before today (verified 31 Jul)

| # | Task | Owner | Was due | Blocked by | State | Notes |
|---|---|---|---|---|---|---|
| [x] | C6 procurement order placed | Pablo | 24 Jul | â€” | done | arrived; further material also purchased |
| [x] | C6 motor/driver/encoder sets received | Pablo | 24 Jul | â€” | done | baseline is 3 complete sets |
| [ ] | **M6 nuts for wheel ballast** | Pablo | â€” | supplier | **blocked** | **NOT ARRIVED. Blocks wheel ballast, balancing and spin-test.** |
| [ ] | C6 bulk cap 470-1000 uF >= 50 V | Pablo | 24 Jul | â€” | todo | still to confirm; separate line, not the 16 V caps |
| [ ] | C6 XT30 pairs >= 4 | Pablo | 24 Jul | â€” | todo | drivers are XT30, battery is XT60 |
| [x] | C6 bench PSU available | Pablo | 24 Jul | â€” | done | current-limited |
| [x] | A3 requirements table support | Dejan+Pablo | 25 Jul | â€” | done | |
| [x] | **Wiring scheme + component placement designed** | Pablo | 31 Jul | â€” | **done** | design issued; the build reference for 2 Aug |
| [ ] | **Procurement round 2 (post 3D freeze)** | Pablo | **5 Aug** | 3D frame freeze | todo | new BOM once 3D design is sized |

## E1 â€” Bench power, safety, single-axis bring-up â€” RE-BASELINED to 2 Aug (day 11)

Original window was 27-29 Jul (days 5-7). No bench work took place in that
window; the effort went into the wiring and placement design instead. This is
now the **Sunday 2 Aug** session, with **3 Aug as the recovery buffer**.

Sunday target, in the owner's words: the 5 V rail calibrated and soldered, and
the driver and encoder mounted and fully functioning. Open loop only â€” driver
and DC bench supply, no control loop. Allow for partial failure; that is what
the 3 Aug buffer is for.

| # | Task | Owner | Due | Blocked by | State | Notes |
|---|---|---|---|---|---|---|
| [ ] | E1.1 Bench PSU + E-stop + fuse in bench loop | Pablo | 2 Aug | â€” | todo | |
| [ ] | E1.2 LiPo safety kit staged | Pablo | 2 Aug | â€” | todo | battery stays out until cube power-on |
| [ ] | E1.3 Incoming inspection, 3 motor sets | Pablo | 2 Aug | â€” | todo | phase R vs 194 mOhm |
| [ ] | **E1.7 5 V rail soldered + trimmed to 5.00 V** | Pablo | **2 Aug** | E1.1 | todo | **primary Sunday target**; characterise under load |
| [ ] | E1.4 moteus-n1 #1 bring-up, CAN ID, FOC cal | Pablo+Nicc | 2 Aug | E1.1, E1.3 | todo | on PSU only |
| [ ] | E1.5 MA600 mounted, gap fixture, record shim | Pablo | 2 Aug | E1.3 | todo | <= 1.5 mm, centred on 4 mm magnet |
| [ ] | E1.6 Open-loop spin, log no-load current + max RPM | Pablo | 2 Aug | E1.4, E1.5 | todo | containment required |
| [ ] | **Gate M1** rail trimmed, driver commutates, encoder reads | Pablo | **2 Aug** | all E1 | todo | buffer: 3 Aug |
| [ ] | **E1.B Recovery buffer** â€” finish anything E1 that did not close | Pablo | **3 Aug** | â€” | todo | protects all downstream dates |

## E2 â€” Board outline to Nasia â€” RE-BASELINED to 4-5 Aug (days 13-14)

Original window was 29-31 Jul with a hard 1 Aug hand-off. That date was not met.
It is re-planned against the new 3D design sequence: the frame is sized and
frozen on 2 Aug, so the board outline now lands inside the detail-CAD window
(D3d, 3-5 Aug) rather than ahead of it.

| # | Task | Owner | Due | Blocked by | State | Notes |
|---|---|---|---|---|---|---|
| [ ] | E2.1 Driver positions from SPI < 20 cm rule | Pablo | 4 Aug | E1.5 | todo | encoder cable dictates driver location |
| [ ] | E2.2 CAN routing, stubs < 10 cm, bus ends identified | Pablo | 4 Aug | E2.1 | todo | linear topology only |
| [ ] | E2.3 Perfboard floorplan, 15 x 9 cm | Pablo | 5 Aug | E2.1, E2.2 | todo | |
| [ ] | E2.4 **Board outline + connectors -> Nasia** | Pablo | **5 Aug** | E2.3 | todo | feeds detail CAD (D3d) |
| [ ] | E2.5 Electronics mass line -> Dejan | Pablo | 5 Aug | E2.4 | todo | TODO: weigh populated proto |
| [ ] | **Gate E2** outline frozen | Pablo | 5 Aug | E2.4 | todo | |

## E3 â€” 1-DoF rig + parameter measurement â€” RE-BASELINED to 4-9 Aug (days 13-18)

Original window was 31 Jul - 2 Aug. Confirmed blocked at the review: parameter
measurement waits until further bench testing has been done, so it moves to the
week of 3-9 Aug. **G3 (rig balances) moves from 2 Aug to 12 Aug.**

| # | Task | Owner | Due | Blocked by | State | Notes |
|---|---|---|---|---|---|---|
| [ ] | E3.1 Rig electrical assembly completed | Pablo+Nasia | 4 Aug | M1, C8b | todo | rig part-mounted; reinforced supports to print |
| [ ] | E3.2 Rig harness, 2-node CAN terminated both ends | Pablo | 5 Aug | E3.1, E2.2 | todo | |
| [ ] | E3.3 Powered rig checkout, closed loop | Pablo+Nicc | 6-7 Aug | E3.2, B6 | todo | disarm + watchdog verified = **M4** |
| [ ] | E3.4 Measurement setup for Kt / J / friction / latency | Pablo+Andrea | 7-9 Aug | E3.3 | todo | Andrea owns the numbers |
| [ ] | E3.5 **Deliver 4 measured params -> Andrea** | Pablo | **9 Aug** | E3.4 | todo | **M6**; gates B9 -> B11 -> B12 |
| [ ] | E3.6 Rig evidence + photos -> Dejan | Pablo | 9 Aug | E3.3 | todo | for A14 (TDD v2, 14 Aug) |
| [ ] | **Gate G3** rig balances >= 60 s | Pablo+Nicc | **12 Aug** | all E3, B7 | todo | was 2 Aug |

> **Downstream gates re-baselined 31 Jul.** The E4-E7 windows below still carry
> their original dates. The governing dates are now: **G5 cube integrated
> 15 Aug** (was 9 Aug), **G6 edge balance 17 Aug** (was 13 Aug), **G7 corner
> balance 19 Aug** (was 16 Aug), **G8 jump-up 20 Aug** (was 18 Aug, and
> sacrificial). Add roughly six days to each E4-E7 due date below.

## A5 support â€” risk register (due with TDD 3 Aug)

| # | Task | Owner | Due | Blocked by | State | Notes |
|---|---|---|---|---|---|---|
| [x] | Electrical risk rows -> Dejan | Pablo | 3 Aug | RISKS.md | done | ported into sections/15_risk_register.tex (Appendix F) |

## E4 â€” Perfboard + harness, C12 (3-6 Aug, days 12-15)

| # | Task | Owner | Due | Blocked by | State | Notes |
|---|---|---|---|---|---|---|
| [ ] | E4.1 XT60 -> 3x XT30 distribution harness | Pablo | 3 Aug | C6 | todo | no WBS task owns this |
| [ ] | E4.2 Populate perfboard, rails + bulk cap | Pablo | 4 Aug | E2.3, bulk cap | todo | 16 V caps on 5 V rail ONLY |
| [ ] | E4.3 Rail bring-up, ripple, LM2596 thermal | Pablo | 4 Aug | E4.2 | todo | derates without heatsink |
| [ ] | E4.4 CAN harness, split termination at 2 ends | Pablo | 5 Aug | E4.2, E2.2 | todo | 2x 60.4 ohm + 4.7 nF |
| [ ] | E4.5 5 Mbps bus integrity, scope + soak | Pablo | 5 Aug | E4.4 | todo | no error frames |
| [ ] | E4.6 Servo brake wiring, 5 V headroom check | Pablo | 6 Aug | E4.3 | todo | MG92B stall current |
| [ ] | E4.7 Label, strain-relieve, photograph | Pablo | 6 Aug | E4.4, E4.6 | todo | |
| [ ] | **Gate E4** full bench power-on, 3 drivers, on PSU | Pablo | 6 Aug | all E4 | todo | |

## E5 â€” Cube integration + power-on, C13 (7-9 Aug, days 16-18) â€” G5 9 Aug

| # | Task | Owner | Due | Blocked by | State | Notes |
|---|---|---|---|---|---|---|
| [ ] | E5.1 Install board + harness, re-check all MA600 gaps | Pablo+Nasia | 7 Aug | C11, E4.7 | todo | gap drifts on assembly |
| [ ] | E5.2 Continuity + isolation before power | Pablo | 7 Aug | E5.1 | todo | confirm no 16 V cap on 25 V bus |
| [ ] | E5.3 PSU smoke test, wheels off | Pablo | 8 Aug | E5.2 | todo | all 3 drivers enumerate |
| [ ] | E5.4 PSU test, wheels on, open-loop per axis | Pablo | 8 Aug | E5.3 | todo | |
| [ ] | E5.5 **First battery power-on** | Pablo | 9 Aug | E5.4 | todo | anti-spark, fuse, alarm, safe area |
| [ ] | E5.6 Handover: all axes addressable, telemetry up | Pablo | 9 Aug | E5.5 | todo | to Nicc + Andrea |
| [ ] | **Gate E5 = G5** cube integrated and powered | Pablo | 9 Aug | all E5 | todo | |

## E6 â€” Edge-balance support (10-13 Aug, days 19-22) â€” HARD KILL 13 Aug

| # | Task | Owner | Due | Blocked by | State | Notes |
|---|---|---|---|---|---|---|
| [ ] | E6.1 On-call support to B11 | Pablo | 13 Aug | E5.6 | todo | priority over everything |
| [ ] | E6.2 Vibration fault hunt, CAN + encoder error counters | Pablo | 12 Aug | E6.1 | todo | correlate with wheel speed |
| [ ] | E6.3 C14 brake support (Suvanna owns) | Pablo | 13 Aug | E4.6, C14 | todo | SACRIFICIAL if G6 at risk |
| [ ] | E6.4 Battery endurance under balance load | Pablo | 13 Aug | E6.1 | todo | for demo-day planning |
| [ ] | **Gate E6 = G6** edge balance, no open electrical defect | Pablo | 13 Aug | E6.1 | todo | S3 cut if missed |

## E7 â€” Corner, jump-up, presentation (14-20 Aug, days 23-29)

| # | Task | Owner | Due | Blocked by | State | Notes |
|---|---|---|---|---|---|---|
| [ ] | E7.1 Support B12 corner balance + slew | Pablo | 16 Aug | E6 gate | todo | |
| [ ] | E7.2 Brake circuit support for B13 jump-up | Pablo | 18 Aug | E6.3, G6 pass | todo | only if G6 passed 13 Aug |
| [ ] | E7.3 Demo-day spares + field-repair kit | Pablo | 17 Aug | â€” | todo | spare harness/driver/encoder |
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
| [x] | Cube edge 150 mm or 180 mm | **RESOLVED 31 Jul: 150 mm** |
| [ ] | M6 nut delivery date (blocks wheel ballast + balancing) | **blocked â€” chase supplier** |
| [ ] | Procurement round 2 scope, post 3D freeze | todo â€” order by 5 Aug |
