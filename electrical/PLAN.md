# Cubli — Electrical/Electronics Workstream Plan

Owner: Pablo. Scope: circuits, perfboard layout, harnessing, electrical
manufacturing; support to system integration and documentation.

Calendar anchor: this plan runs from **today, 27 Jul 2026**, to the final
presentation on **20 Aug 2026**. The WBS day-numbering used in
`wbs_patch.tex` is unchanged (day 1 = 23 Jul 2026), so today is **day 5** and
20 Aug is day 29. Days 1-4 (23-26 Jul) are behind us and appear only as
"assumed-complete inputs" below.

Streams: A = documentation, B = control/software, C = hardware.
Tasks owned: C6, C7, C10, C12, C13. Supported: A3, A5, B4, C14.

---

## Invariants (do not reschedule past these)

| Date | Invariant | Gates |
|---|---|---|
| 1 Aug | Board outline + connector positions to Neisa | C5 mass freeze |
| 2 Aug | G3: 1-DoF rig balances AND Kt / wheel J / friction / loop latency to Andrea | B8 -> B9 |
| 3 Aug | G4: TDD deliverable | A12 |
| 9 Aug | G5: cube integrated | B10 -> B11 |
| 13 Aug | G6: edge balance. HARD KILL for S3 jump-up | B11 -> B12 |
| 20 Aug | G9: final presentation | D1 |

Andrea is the critical resource: she holds B9 -> B11 -> B12 sequentially.
Anything delivered late to her propagates to 20 Aug with no recovery path.
Brake work (C14) must never cannibalise the 13 Aug edge-balance gate.

## Technical invariants held by this plan

- 4 complete motor/driver/encoder sets, not 3. The fourth stays on the 1-DoF
  bench rig permanently as a development bench.
- MA600: air gap <= 0.5 mm, chip centred on the 4 mm magnet thickness, SPI
  cable < 20 cm. This dictates driver physical placement, not the reverse.
- CAN-FD 5 Mbps: linear topology only, stubs < 10 cm, split termination
  (2x 60.4 ohm + 4.7 nF) at exactly the two physical bus ends.
- The BOM 100 uF caps are 16 V, 5 V rail only. They never touch the 25 V bus.
  Bulk cap 470-1000 uF at >= 50 V is a separate procurement line.
- Battery XT90, drivers XT30: a distribution harness must be fabricated.
- Perfboard, not fabricated PCB. DECIDED. Fab turnaround does not fit C12.
- All firmware bring-up on a current-limited bench PSU, never on the battery.

---

## Assumed-complete inputs (days 1-4, 23-26 Jul)

These are prerequisites of the blocks below and are assumed done as of today.
If any is not, it is a blocker and belongs in STATUS.md as such.

| Ref | Item | Owner | Was due |
|---|---|---|---|
| C6 | Procurement order placed (long-lead) | Pablo (+Neisa) | 24 Jul |
| C1 | Envelope and layout study | Neisa (+Suvanna) | 24 Jul |
| A3 | Scope and requirements table | Dejan (+Pablo) | 25 Jul |
| C2 | Reaction-wheel design | Suvanna (+Neisa) | 26 Jul |
| B1 | Sim environment + 1-DoF plant | Andrea | 24 Jul |

---

## Block E1 — Bench power, safety, single-axis bring-up
**27-29 Jul (days 5-7).** Extends C7; adds the electrical items C7 does not name.

| ID | Task | Depends on | Days |
|---|---|---|---|
| E1.1 | Bench PSU set up, current limit verified against a known load; E-stop and inline fuse in the bench loop | C6 delivery | 27 Jul |
| E1.2 | LiPo safety kit staged: charger, safe bag, cell alarm. Battery stays out of the loop until E4.3 | C6 delivery | 27 Jul |
| E1.3 | Incoming inspection of 4 motor sets: continuity, phase resistance vs 194 mOhm datasheet, driver boot, encoder SPI read-back | C6 delivery | 27-28 Jul |
| E1.4 | moteus-n1 #1 bring-up on bench PSU: firmware, CAN-FD ID assignment, FOC calibration against MA600 | E1.1, E1.3 | 28 Jul |
| E1.5 | MA600 gap fixture: shim stack to set <= 0.5 mm and centre the chip on the 4 mm magnet. Record the shim value; it becomes the C10 and C13 assembly spec | E1.3 | 28-29 Jul |
| E1.6 | Open-loop wheel spin on a clamped motor, current-limited, containment in place. Log no-load current and max RPM vs the 7000 rpm derated figure | E1.4, E1.5 | 29 Jul |

**Exit gate E1:** one driver commutates a wheel closed-loop on current, MA600
reads absolute angle without error flags, PSU current limit demonstrably trips
before the fuse. Nothing has been connected to the battery.

## Block E2 — Board outline + connector positions (1 Aug hard date)
**29-31 Jul (days 7-9).** No existing WBS task owns this. It gates C5.

| ID | Task | Depends on | Days |
|---|---|---|---|
| E2.1 | Fix driver positions from the MA600 SPI < 20 cm rule: each moteus-n1 sits within 20 cm cable of its own encoder. Three positions, one per axis | E1.5, C1 | 29-30 Jul |
| E2.2 | Fix CAN bus routing: linear chain across the three drivers + Teensy, stubs < 10 cm, and identify the two physical bus ends where termination goes | E2.1 | 30 Jul |
| E2.3 | Perfboard floorplan on the 15 x 9 cm double-sided board: 25 V bus in, LM2596, 5 V rail, bulk cap footprint, Teensy, XIAO ESP32-C6, BMI270 breakout, servo header, CAN termination network | E2.1, E2.2 | 30-31 Jul |
| E2.4 | **Deliver to Neisa:** board outline DXF/PDF, mounting hole pattern, keep-out heights, connector positions and exit directions, board mass estimate (TODO: weigh the populated proto) | E2.3 | **1 Aug** |
| E2.5 | Supply the same numbers to Dejan for the TDD mass budget electronics line | E2.4 | 1 Aug |

**Exit gate E2:** Neisa has an outline she can cut structure to; C5 mass freeze
is unblocked. Deliverable is frozen — later electrical changes must fit inside
this outline, not move it.

## Block E3 — 1-DoF rig assembly and parameter measurement
**31 Jul - 2 Aug (days 9-11).** C10, plus the electrical half of B8.
Feeds G3 on 2 Aug. Zero float — see the dependency check.

| ID | Task | Depends on | Days |
|---|---|---|---|
| E3.1 | Assemble rig electrical: motor set #4, MA600 at the E1.5 shim spec, BMI270 on the rig body, hard stops wired to the disarm input | C9 wheels balanced, C4 rig CAD, E1.5 | 31 Jul |
| E3.2 | Rig harness: bench PSU to driver (XT30), CAN from driver to Teensy with correct termination at both ends, I2C to BMI270 | E3.1, E2.2 | 31 Jul - 1 Aug |
| E3.3 | Powered rig checkout with Nicc: sensor read-back, disarm path, watchdog trip | E3.2, B6 | 1 Aug |
| E3.4 | **Support B8 measurement:** instrument for Kt (current-step vs torque), wheel J (spin-down), friction (coast-down), loop latency (command-to-encoder timestamp). Pablo provides the electrical measurement setup; Andrea owns the numbers | E3.3, B7 | 1-2 Aug |
| E3.5 | **Deliver to Andrea:** measured Kt, wheel J, viscous + Coulomb friction, loop latency, with units and uncertainty | E3.4 | **2 Aug** |

**Exit gate E3 (= G3):** rig balances >= 60 s and Andrea has four measured
numbers. B9 starts 3 Aug on measured, not assumed, parameters.

## Block E4 — Perfboard build + harness (C12)
**3-6 Aug (days 12-15).** Four days, as decided. Perfboard, not PCB.

| ID | Task | Depends on | Days |
|---|---|---|---|
| E4.1 | Fabricate the distribution harness: XT90 battery lead to 3x XT30 driver drops, 14 AWG, anti-spark switch and inline fuse inline. This item is in no existing WBS task | C6 (XT30 pairs, wire) | 3 Aug |
| E4.2 | Populate the perfboard: LM2596 5 V rail, 1N5819 back-feed diode, 100 uF/16 V on the 5 V rail only, 100 nF local decoupling, bulk 470-1000 uF >= 50 V on the 25 V bus | E2.3, bulk cap received | 3-4 Aug |
| E4.3 | Rail bring-up on bench PSU: 5 V under load, ripple check, thermal check on the LM2596 (it derates without a heatsink) | E4.2 | 4 Aug |
| E4.4 | CAN harness for the cube: linear chain, stubs < 10 cm, split termination 2x 60.4 ohm + 4.7 nF at the two ends only | E4.2, E2.2 | 4-5 Aug |
| E4.5 | Bus integrity check at 5 Mbps: scope the differential pair, confirm eye and no error frames over a sustained soak with all 3 drivers addressed | E4.4 | 5 Aug |
| E4.6 | Servo brake wiring: MG92B off the 5 V rail with its own decoupling, PWM from Teensy, current headroom checked against the LM2596 2-3 A rating | E4.3 | 5-6 Aug |
| E4.7 | Label, strain-relieve and photograph the harness for the TDD/final deck | E4.4, E4.6 | 6 Aug |

**Exit gate E4:** board and harness pass a full bench power-on with all three
drivers on the bus, still on the PSU. Battery has not been connected.

## Block E5 — Cube integration and power-on (C13)
**7-9 Aug (days 16-18).** Gated by G5 on 9 Aug.

| ID | Task | Depends on | Days |
|---|---|---|---|
| E5.1 | Install board and harness in the frame; three axes wired; every MA600 re-checked at the E1.5 gap spec after mechanical assembly | C11 frame, E4.7 | 7 Aug |
| E5.2 | Continuity and isolation check before any power: bus-to-chassis, 5 V-to-25 V separation, confirm no 16 V cap sits on the 25 V bus | E5.1 | 7 Aug |
| E5.3 | Bench PSU smoke test, current-limited, wheels removed. All three drivers enumerate on CAN; IMU and encoders read | E5.2 | 8 Aug |
| E5.4 | Bench PSU test with wheels installed, low current limit, open-loop spin per axis | E5.3 | 8 Aug |
| E5.5 | **First battery power-on.** Anti-spark switch, fuse verified, LiPo alarm on, fire-safe area. Measure inrush against the bulk cap | E5.4 | 9 Aug |
| E5.6 | Hand over to Nicc/Andrea: all axes addressable, telemetry link up on the XIAO ESP32-C6 | E5.5 | 9 Aug |

**Exit gate E5 (= G5):** cube integrated and powered, all axes addressable
from the flight computer, on battery. B10/B11 unblocked.

## Block E6 — Edge-balance electrical support
**10-13 Aug (days 19-22).** Protect the 13 Aug hard kill date.

| ID | Task | Depends on | Days |
|---|---|---|---|
| E6.1 | On-call electrical support to B11 edge balance: connector reseating, encoder gap drift, thermal watch on drivers and LM2596 | E5.6 | 10-13 Aug |
| E6.2 | Vibration-induced fault hunting: log CAN error counters and encoder error flags during balance runs, correlate with wheel speed | E6.1 | 10-12 Aug |
| E6.3 | Support C14 brake build (Suvanna owns): servo mounting current draw, brake actuation timing on the scope | E4.6, C14 | 11-13 Aug |
| E6.4 | Battery endurance measurement: runtime per charge under balance load; report to the team for demo-day planning | E6.1 | 12-13 Aug |

**Exit gate E6 (= G6):** edge balance achieved 13 Aug with no open electrical
defect. If G6 slips, E6.3 stops first — the brake is the sacrificial item,
never the balance.

## Block E7 — Corner balance, jump-up, presentation
**14-20 Aug (days 23-29).**

| ID | Task | Depends on | Days |
|---|---|---|---|
| E7.1 | Electrical support to B12 corner balance and slew | E6 gate | 14-16 Aug |
| E7.2 | Brake circuit support for B13 jump-up (only if G6 passed by 13 Aug) | E6.3, G6 pass | 17-18 Aug |
| E7.3 | Spares and field-repair kit for demo day: spare harness, spare driver, spare encoder, tools, charged batteries | — | 17 Aug |
| E7.4 | Electrical content for the TDD final revision and the deck: block diagram, power tree, harness photos, measured numbers | E4.7, E6.4 | 18-19 Aug |
| E7.5 | Final presentation support, 20 Aug | all | 20 Aug |

**Exit gate E7 (= G9):** demonstration runs on battery without electrical
intervention.

---

## Deliverable summary — what leaves my desk

| Date | Deliverable | To | Blocks |
|---|---|---|---|
| 1 Aug | Board outline, connector positions, mass estimate | Neisa | C5 mass freeze |
| 1 Aug | Electronics mass line for the budget | Dejan | A11/A12 |
| 2 Aug | Measured Kt, wheel J, friction, loop latency | Andrea | B9 -> B11 -> B12 |
| 2 Aug | Rig electrical evidence + photos | Dejan | A11 TDD deepen |
| 3 Aug | Electrical risk rows | Dejan | A5 risk register |
| 6 Aug | Board + harness bench-verified | Nicc | firmware on real hardware |
| 9 Aug | Cube powered, all axes addressable | Nicc, Andrea | B10, B11 |
| 13 Aug | Brake circuit verified | Nicc | B13 |
| 19 Aug | Electrical figures and numbers | Suvanna, Dejan | D1 deck |

## Open questions (numbers I do not have — not invented)

1. Populated perfboard mass. TODO: weigh the proto before E2.4 or Neisa's
   budget carries an unknown.
2. Bulk cap 470-1000 uF >= 50 V: ordered under C6, or still open? Lead time
   unknown. E4.2 depends on it.
3. XT30 pairs quantity received. Need >= 4 (3 drivers + rig).
4. Bench PSU actual current ceiling. The gap table says >= 5 A; a 3-driver
   bench test may exceed that.
5. JST-PH3 CAN cable conductor gauge — the BOM itself flags this as TODO.
   Affects whether stock cables are usable or the harness is hand-made.
6. LM2596 total 5 V load: Teensy + XIAO (300 mA TX burst) + BMI270 + MG92B
   stall. TODO: sum it. The module is rated 2-3 A and derates without a
   heatsink.
7. Was the 4th complete motor set actually ordered under C6? The BOM table
   says qty 3 and lists spares as an unbought gap item.
8. Cube edge length: 150 mm (stated invariant) or 180 mm (hardware section).
   Changes the perfboard keep-out.
