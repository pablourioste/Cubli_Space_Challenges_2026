# Cubli â€” Day-by-Day Project Schedule

**30 July â€“ 20 August 2026.** 22 calendar days, 21 working days, **137.5 h**
total team capacity.

Calendar arithmetic and the fragmentation model live in
[`cubli_time_budget.md`](cubli_time_budget.md). This file is the assignment
plan.

> **Scope note.** This is the *team-wide* schedule keyed to real calendar block
> data. It does not replace `electrical/SCHEDULE.md`, which is generated from
> `electrical/schedule.yaml` and remains the authority on the 23 EL- electrical
> tasks and their exit criteria. Where the two disagree on a date, this file
> reflects the calendar reality and the YAML needs regenerating to match.

---

## Standing rules

These apply every day and are not repeated in each entry.

1. **FRAGMENTED days (3, 4, 7 Aug): no bench or lab assembly.** Documentation,
   TDD writing, CAD review and pitch scripting only. A day with a 1.0 h maximum
   block cannot hold an assembly step that costs 20 minutes of setup.
2. **HIGH-CONTIGUITY days (1, 8 Aug) are reserved for work that cannot be
   split.** Do not spend a 6.0 h block on anything that would fit in a 1.5 h
   fragment.
3. **Nasia's CAD is gated on Andrea & Deyan's sizing.** No frame geometry is
   frozen ahead of the inertia tensor. On any day the numbers are late, Nasia
   reviews frozen geometry instead of modelling against unconfirmed inputs.
4. **Brake / jump-up work is sacrificial.** It yields to balance work on the
   day, without discussion. Standing decision, `electrical/schedule.yaml` I-4.
5. **No work 12 Aug after 13:00, none 13 Aug, none 14 Aug before post-lunch.**

## Team

| Person(s) | Domain |
|---|---|
| **NiccolÃ² & Pablo** | Wiring, electronics setup, power distribution, electrical safety tests |
| **Andrea & Deyan** | Physical/analytical documentation, sizing calculations, inertia modeling, control budget |
| **Suvanna** | 1D functional prototype iterations, mechanical testbench, 1-DoF balance verification |
| **Nasia** | 3D CAD, frame design, mechanical enclosures â€” driven by Andrea & Deyan's constraints |
| **Combined / sub-groups** | Commercial script, 3-minute pitch, slide deck |

## Gate summary

| Gate | Was | Now | Note |
|---|---|---|---|
| Preliminary TDD | 3 Aug | **3 Aug** | unchanged â€” falls on a FRAGMENTED day, which suits it |
| **S3 Go/No-Go** | 13 Aug | **11 Aug EOD** | **moved** â€” 13 Aug is zero-work |
| Pitch rehearsal 1 | â€” | **18 Aug** | new |
| Dress rehearsal | â€” | **19 Aug** | new |
| Final presentation | 20 Aug | **20 Aug** | unchanged, external |

---

# WEEK 1 â€” 30 July â€“ 2 August

## Thursday 30 July

**Hours available: 8.0 Â· Longest block: 3.0 h Â· Class: STANDARD**

> **Milestone objective:** Close out documentation and 1D reprints; have the
> wiring and power-distribution bench *staged and ready* so that 31 July opens
> directly on continuity testing with no setup cost.

**NiccolÃ² & Pablo â€” wiring / PDB preparation**
- Lay out the power distribution board: 25 V bus entry, buck converter
  position, 5 V rail split, bulk capacitance footprint.
- Pre-cut and pre-tin all phase leads and bus wiring for tomorrow. Terminate
  bullet connectors, heat-shrink, label both ends of every run.
- Stage the safety loop as a unit: e-stop inline, fuse fitted, bench PSU
  current limit set and its trip point written on the bench.
- Confirm the PSU trips on a known resistive load **before** the fuse opens.
  This is the last chance to find that out on a day where it costs nothing.

**Andrea & Deyan â€” documentation close-out**
- Finish the outstanding analytical documentation sections.
- Freeze the sizing figures that Nasia's frame depends on: total mass, CoM,
  inertia tensor. Hand them over as explicit numbers, not as a document to be
  read and interpreted.
- Open the control budget: torque authority, saturation limits, loop-rate
  assumption.

**Suvanna â€” 1D CAD reprints**
- Complete the in-flight 1D prototype reprints.
- Dry-fit every printed part: motor mount, encoder bracket, hard stops. Find
  interference today, on the bench, not tomorrow during the electrical test.
- Confirm the reprinted parts hold the encoder air gap within spec when
  assembled.

**Nasia â€” CAD, gated**
- Take Andrea & Deyan's frozen sizing numbers and begin frame geometry against
  them.
- Until those numbers land: review existing enclosure geometry for wall
  thickness, fastener access and driver clearance.
- **Do not** freeze any frame dimension today that the inertia tensor could
  still move.

---

## Friday 31 July

**Hours available: 9.0 Â· Longest block: 4.0 h Â· Class: STANDARD â€” CRITICAL TARGET**

> **Milestone objective:** **First controlled open-loop rotation.** Electrical
> continuity and safety tests pass, motor connected, motor turns under command.
> This is the day the project stops being paper.

**NiccolÃ² & Pablo â€” continuity, safety, motor connection** *(joint with Suvanna)*
- Full continuity and isolation sweep **before any power is applied.** Phase-to-
  phase resistance on all three pairs against the 194 mÎ© datasheet figure;
  phase-to-ground isolation; confirm no 16 V-rated part sits anywhere on the
  25 V bus.
- Safety-test the loop live: e-stop opens the bus in one action, verified by
  measurement not by assumption. PSU current limit trips at its set value.
- Connect the motor. Driver boot, enumerate on CAN, FOC calibration against the
  encoder.
- **First controlled open-loop rotation.** Log no-load current and maximum RPM.
  Wheel containment in place before the first command.

**Andrea & Deyan â€” sizing and control budget**
- Deliver the completed inertia model and mass budget. Nasia is blocked on this.
- Complete the control budget constraints and hand the torque-authority and
  saturation figures to whoever owns controller tuning.
- Be reachable during the rotation test: the measured no-load current and RPM
  are model inputs, and capturing them today is cheaper than remeasuring.

**Suvanna â€” testbench operation** *(joint with NiccolÃ² & Pablo)*
- Own the mechanical side of the rotation test: rig rigid, wheel balanced and
  secured, hard stops fitted, containment adequate for a first spin.
- Verify the encoder air gap on the assembled rig and **record the shim value**
  â€” it becomes the assembly spec for every subsequent axis.
- Log everything mechanical from the first rotation: vibration, run-out, any
  audible bearing complaint.

**Nasia â€” frame design**
- Frame geometry against the now-frozen sizing. Driver positions, encoder
  clearance, harness routing paths.
- Enclosure: driver mounting, ventilation, service access.

---

## Saturday 1 August

**Hours available: 12.0 Â· Longest block: 6.0 h Â· Class: HIGH-CONTIGUITY**

> **Milestone objective:** Spend the first of only two 6.0 h blocks in the
> project on the work that genuinely cannot be fragmented â€” E2/E3 assembly and
> wheel balancing. Reach a closed-loop-capable 1-DoF rig.

**NiccolÃ² & Pablo â€” E2/E3 assembly, full block**
- Populate the distribution board properly. Two ground domains, **exactly one
  star point** â€” verify by continuity that there is precisely one connection
  between them. Measured, not assumed.
- 5 V rail: trim to 5.00 V, characterise under load to 1.5 A, log ripple and
  converter case temperature.
- Rig harness and the 2-node CAN bus. Split termination at the two physical bus
  ends; unpowered CANHâ€“CANL should read 60 Î© Â±3 Î©.
- Closed-loop bring-up. **Verify the watchdog and disarm path by deliberately
  stalling the control loop** before any balance attempt.

**Andrea & Deyan â€” parameter extraction**
- Work the rig with the electrical team to extract the four plant parameters:
  torque constant, wheel inertia by spin-down, viscous and Coulomb friction by
  coast-down, closed-loop latency.
- Each one measured with units and an uncertainty. Not assumed, not taken from
  the datasheet.
- Feed the measured values straight back into the model and report whether the
  sizing still holds.

**Suvanna â€” wheel balancing, full block**
- Static-balance every wheel. This is the canonical task for a 6.0 h block: it
  is iterative, it cannot be interrupted cheaply, and there is no other slot
  for it.
- Containment spin-test each wheel individually to above the intended operating
  speed.
- Then support 1-DoF balance verification on the rig, logging tuning iterations.

**Nasia â€” frame fabrication prep**
- Frame geometry to a print-ready state.
- Enclosure detail: cable exits, fastener pattern, keep-out volumes around each
  driver.
- Cross-check the frame against the harness routing NiccolÃ² & Pablo are
  physically building today â€” catch the conflict now, while both the CAD and
  the hardware are in the same room.

---

## Sunday 2 August

**Hours available: 0.0 Â· Class: REST**

> **Milestone objective:** None. No work scheduled.

Deliberate. The next two days are FRAGMENTED and carry the TDD deadline; the
following Saturday is the second and last 6.0 h block. Burning this day leaves
no recovery capacity for either.

---

# WEEK 2 â€” 3â€“9 August

## Monday 3 August

**Hours available: 3.0 Â· Longest block: 1.5 h Â· Class: FRAGMENTED**
**â€” PRELIMINARY TDD DUE**

> **Milestone objective:** Deliver the Preliminary TDD. Open the commercial
> sales script. **No bench work today** â€” the longest block is 1.5 h.

**NiccolÃ² & Pablo â€” documentation only**
- Write up the electrical results from 31 July and 1 August: continuity and
  safety test records, rail characterisation, CAN bus integrity, the parameters
  from the rotation and balance tests.
- Electrical figures for the TDD: block diagram, power tree.
- **No assembly.** Two 1.5 h fragments cannot hold a bench session.

**Andrea & Deyan â€” TDD delivery, lead**
- Own the Preliminary TDD submission. Consistency pass across all sections,
  figures, references.
- Integrate the measured 1 August parameters and state explicitly where they
  agree or disagree with the pre-build sizing.

**Suvanna â€” documentation**
- Write up the 1D prototype iteration history: what was reprinted, why, what
  changed. This is design rationale and it is worth more written down now than
  reconstructed later.
- Balance and spin-test records into the TDD.

**Nasia â€” CAD review**
- Review, don't model. Check the frame and enclosure package against the sizing
  constraints and the as-built harness routing.
- CAD figures for the TDD.

**Combined team â€” commercial script, opens today**
- **Draft the sales script and commercial narrative.** Fragmented time suits
  writing: what problem does the Cubli address, who is the customer, what is
  the value proposition.
- Target: a first narrative arc on paper by end of tomorrow.

---

## Tuesday 4 August

**Hours available: 2.5 Â· Longest block: 1.0 h Â· Class: FRAGMENTED**

> **Milestone objective:** Complete the sales script draft. Tighten TDD
> follow-ups. **No bench work** â€” 1.0 h maximum block, the most fragmented day
> in the project.

**NiccolÃ² & Pablo â€” planning only**
- Plan the 5â€“6 August wiring work on paper: harness lengths, connector
  inventory, what has to be ordered or found today to avoid stalling.
- Close out any TDD electrical feedback.

**Andrea & Deyan â€” analytical follow-up**
- Address TDD review comments.
- Refine the control budget against the measured parameters. If the measured
  inertia or friction moved the sizing, say so now and quantify it.

**Suvanna â€” documentation**
- Testbench procedure write-up: the repeatable version of the balance
  verification, so a second person can run it.
- Note every mechanical defect observed so far and its disposition.

**Nasia â€” CAD review**
- Continue the review pass. Tolerance stack-up on the frame joints.
- Prepare the print queue so that 5 August opens with parts going onto a
  printer, not with decisions being made.

**Combined team â€” commercial script, closes today**
- **Complete the sales script and commercial narrative draft.**
- Fix the three-minute story spine: hook, technical differentiator, ask. Deck
  construction starts 7 August against this spine, so it needs to be settled.

---

## Wednesday 5 August

**Hours available: 8.0 Â· Longest block: 3.0 h Â· Class: STANDARD**

> **Milestone objective:** Return to the bench. Replicate actuation sets and
> scale the bus toward three axes.

**NiccolÃ² & Pablo â€” actuation replication and bus scaling**
- Replicate the commissioned actuation set onto the remaining sets: phase
  wiring, FOC calibration, unique CAN ID per driver, magnet bonding to the
  recorded 31 July shim value.
- Scale the CAN bus to four nodes. Every stub short, split termination relocated
  to the two new physical bus ends. Error soak at full rate.
- Battery power chain: XT60 lead, anti-spark, e-stop, fuse sized and
  **justified in amps** against the transient, bulk capacitance fitted and its
  working voltage verified by part marking.

**Andrea & Deyan â€” 3D modeling**
- 3D dynamics model and the edge/corner control design, using the CAD inertia
  tensor rather than an estimate.
- Update the control budget for three-axis operation.

**Suvanna â€” 1-DoF iteration**
- Continue 1-DoF balance verification and disturbance-recovery logging while
  the rig still exists as an independent testbench. Once the sets are absorbed
  into the cube, this capability is gone.
- Mechanical prep for three-axis assembly.

**Nasia â€” printing and fit**
- Print the structural frame set.
- Test-fit printed parts against the actual motors, drivers and harness as they
  come together.

---

## Thursday 6 August

**Hours available: 8.0 Â· Longest block: 3.5 h Â· Class: STANDARD**

> **Milestone objective:** Full harness fabricated and routed. Telemetry up.
> Everything staged so 8 August's 6.0 h block is spent on assembly, not
> preparation.

**NiccolÃ² & Pablo â€” harness and telemetry**
- Fabricate the full distribution harness: battery lead to per-driver drops at
  the correct gauge, CAN chain, encoder runs kept short, IMU link.
- Route clear of the wheel sweep. **Verify by rotating each wheel through a
  full revolution by hand.** Pull-test every power joint. Strain-relieve and
  label.
- Telemetry link on the logic rail, antenna clear of the frame. Measure rail
  sag during a transmit burst â€” untethered operation is mandatory on a
  balancing cube, a tether applies disturbance torque and can catch.

**Andrea & Deyan â€” estimator**
- 3D estimator with gyro-bias states. Characterise the yaw drift.
- Pre-compute the expected behaviour for 8 August's integrated power-on, so the
  test has a prediction to be compared against rather than just an outcome.

**Suvanna â€” assembly preparation**
- Stage every mechanical sub-assembly for Saturday. Parts, fasteners, tools,
  torque values, laid out and checked.
- Final 1-DoF verification runs.

**Nasia â€” enclosure completion**
- Complete and fit the mechanical enclosures.
- Confirm assembly access: every fastener reachable with the harness installed.
  Find that out today, not during Saturday's block.

---

## Friday 7 August

**Hours available: 3.0 Â· Longest block: 1.5 h Â· Class: FRAGMENTED**

> **Milestone objective:** Open the deck build. **No bench work** â€” protect
> tomorrow's 6.0 h block by not starting anything today that could leave the
> hardware in a part-assembled state.

**NiccolÃ² & Pablo â€” procedure writing**
- Write tomorrow's integration and power-on procedure as an ordered checklist:
  continuity and isolation, PSU smoke test with wheels removed, PSU test with
  wheels at reduced current limit, then battery. In that order, no skipping.
- Pre-brief the safety plan for the first battery connection: fire-safe area,
  cell alarm on, second person present, anti-spark, fuse verified.

**Andrea & Deyan â€” documentation**
- Update the analytical documentation with the 5â€“6 August results.
- Define the pass/fail criteria for tomorrow's power-on numerically, before the
  test rather than after it.

**Suvanna â€” review**
- Review the assembly sequence against the printed parts. Confirm nothing is
  missing before a 6.0 h block depends on it.

**Nasia â€” CAD review**
- Final CAD review pass against the as-built hardware.

**Combined team â€” deck build, opens today**
- **Begin the 3-minute presentation deck structure** against the 3â€“4 August
  script.
- Slide-by-slide skeleton with a time budget per slide. Three minutes is
  roughly 8â€“10 slides; decide the cut now, not on 18 August.
- Deck build continues 8â€“10 Aug.

---

## Saturday 8 August

**Hours available: 12.0 Â· Longest block: 6.0 h Â· Class: HIGH-CONTIGUITY**

> **Milestone objective:** **Cube integrated and powered on battery, all axes
> addressable.** The second and last 6.0 h block. First battery connection of
> the project.

**NiccolÃ² & Pablo â€” integration and first battery power-on, full block**
- Install the board and harness into the frame. **Re-check every encoder air
  gap against the 31 July shim spec â€” the gap drifts during mechanical
  assembly.**
- Continuity and isolation before power. Confirm again that no 16 V-rated part
  is on the 25 V bus, by inspection against part markings.
- PSU smoke test with wheels removed. Then wheels on, reduced current limit,
  open-loop per axis.
- **First battery power-on.** Full safety protocol. Record inrush current.
- Three-axis transient test: verify the bus holds up under a simultaneous
  three-axis current step, measured at the board and not at the battery
  terminals. No fuse opening, no driver undervoltage fault.
- Thermal characterisation: three drivers plus the converter in a sealed
  printed volume with no forced convection. Log case temperatures to steady
  state under a balance-representative load.

**Andrea & Deyan â€” model correlation**
- Present during integration. Correlate the measured three-axis behaviour
  against prediction and report the discrepancy.
- Update the control budget with real thermal and electrical limits.

**Suvanna â€” mechanical assembly, full block**
- Own the three-axis mechanical assembly: motors, balanced wheels, encoder
  brackets to the shim spec, hard stops.
- Verify wheel clearance and that no conductor sits in any wheel's sweep
  envelope.
- Support the power-on sequence mechanically.

**Nasia â€” assembly support**
- On hand for fit issues. Frame and enclosure adjustments as integration
  reveals them.
- Document every as-built deviation from CAD. Undocumented deviations become
  next week's mystery.

---

## Sunday 9 August

**Hours available: 0.0 Â· Class: REST**

> **Milestone objective:** None. No work scheduled.

The S3 Go/No-Go is now 11 Aug EOD, two days out. Rest is load-bearing here.

---

# WEEK 3 â€” 10â€“16 August

## Monday 10 August

**Hours available: 8.0 Â· Longest block: 3.5 h Â· Class: STANDARD**

> **Milestone objective:** Edge balance achieved and stable. This is the
> substantive evidence the S3 gate will be judged on tomorrow.

**NiccolÃ² & Pablo â€” balance support and brake circuit**
- On-call electrical support to balance testing. **This takes priority over
  everything else today.**
- Hunt vibration-induced faults: CAN and encoder error counters, correlated
  against wheel speed.
- Battery endurance under sustained balance load â€” needed for demo-day
  planning.
- Brake servo circuit on its isolated rail, PWM drive, flyback protection â€”
  **only if balance work does not need the time.** Sacrificial per standing
  rule 4.

**Andrea & Deyan â€” edge balance tuning**
- Retune the edge controller on the assembled cube.
- Log disturbance recovery quantitatively.
- Assemble the S3 evidence package for tomorrow's gate: what works, what
  doesn't, with numbers.

**Suvanna â€” balance verification**
- Run edge-balance verification and log every attempt, including failures.
  Failure distribution matters more than best-case duration at a gate review.
- Mechanical fault investigation as issues surface.

**Nasia â€” enclosure finalisation**
- Finalise enclosures against the as-built cube.
- Begin the physical presentation and demo setup: how the cube is displayed and
  handled on 20 August.

**Combined team â€” deck build continues**
- Deck structure toward complete. Technical results from 8â€“10 August go in as
  real content.

---

## Tuesday 11 August

**Hours available: 14.5 Â· Longest block: 5.0 h Â· Class: STANDARD**
**â€” S3 GO/NO-GO GATE, EOD**

> **Milestone objective:** **S3 Go/No-Go decision by end of day.** Moved from
> 13 August, which is zero-work. Heaviest day in the project at 14.5 h â€”
> deliberately loaded, because the gate lost two days of run-up and this is the
> only place to partly recover them.

**NiccolÃ² & Pablo â€” gate support**
- All electrical systems verified and stable for the gate review: no open
  electrical defect, error counters clean, battery endurance figure in hand.
- Brake circuit rail stability under sustained servo stall â€” the brake stalls
  by design against a spinning wheel, not as a fault condition. Measure stall
  current and confirm neither rail browns out.
- Electrical readiness statement for the gate: state it as a position, not a
  hope.

**Andrea & Deyan â€” gate decision, lead**
- Own the **S3 Go/No-Go** analysis and recommendation.
- Assess jump-up feasibility against measured performance: available torque
  authority, wheel speed achievable, energy budget.
- **Deliver an explicit Go or No-Go by EOD.** A deferred decision is a No-Go
  with worse consequences, because it consumes the post-trip window that the
  pitch also needs.

**Suvanna â€” verification for the gate**
- Final balance verification runs for the gate evidence.
- Mechanical readiness assessment of the brake mechanism if S3 stays alive.

**Nasia â€” demo preparation**
- Presentation and demo hardware preparation.
- Any mechanical work the gate outcome makes necessary.

**Combined team â€” deck**
- Deck structure complete by EOD.
- **Fold the gate outcome into the narrative.** If S3 is a No-Go, the pitch
  story changes today, not on 18 August during the first rehearsal.

---

## Wednesday 12 August

**Hours available: 3.0 Â· Longest block: 3.0 h Â· Class: STANDARD until 13:00**
**â€” BLACKOUT BEGINS 13:00**

> **Milestone objective:** Secure the hardware and hand off cleanly. Work stops
> at 13:00 and does not resume until 14 August post-lunch â€” a 48-hour gap.
> Anything left ambiguous will cost time to reconstruct.

**All work ends 13:00. No exceptions.**

**NiccolÃ² & Pablo â€” safe shutdown**
- **Disconnect and safely store the battery.** Not left connected across a
  48-hour unattended gap.
- Power down, secure the harness, protect exposed connectors.
- Write the state note: what works, what is mid-repair, what the next person
  touching it needs to know.

**Andrea & Deyan â€” checkpoint**
- Commit all analysis and documentation to the repository. Nothing important
  living only on a laptop across the trip.
- Write the post-trip priority list. On 14 August the team gets 4.5 h and needs
  to open on a decision already made.

**Suvanna â€” testbench secure**
- Secure the testbench and cube mechanically.
- Log outstanding mechanical items.

**Nasia â€” CAD commit**
- Commit the CAD state. Note what is frozen and what is still open.

---

## Thursday 13 August

**Hours available: 0.0 Â· Class: BLACKOUT â€” FIELD TRIP**

> **Milestone objective:** None. **Zero project work.**

The original S3 Go/No-Go gate sat on this date. It moved to 11 August EOD.

---

## Friday 14 August

**Hours available: 4.5 Â· Longest block: 3.0 h Â· Class: STANDARD, post-lunch start**

> **Milestone objective:** Restart cleanly and re-verify before trusting
> anything. 48 hours unattended is enough for connections to work loose and for
> assumptions to go stale.

**No work before post-lunch.**

**NiccolÃ² & Pablo â€” power-up verification**
- **Re-run continuity and isolation checks before applying power.** The cube sat
  unattended for two days; verify, don't assume.
- Reconnect the battery under the full safety protocol. Confirm all axes
  addressable and telemetry live.
- Brake closure-time measurement on the scope, command edge to barrier contact,
  averaged over at least ten actuations with the spread stated â€” if S3 is Go.

**Andrea & Deyan â€” corner balance**
- Open corner balance and commanded slew work.
- Re-baseline against the pre-trip measurements: confirm nothing has drifted.

**Suvanna â€” mechanical re-verification**
- Re-verify wheel balance and encoder gaps after the gap.
- Support corner-balance testing.

**Nasia â€” demo setup**
- Physical demo setup and presentation logistics for 20 August.

---

## Saturday 15 August

**Hours available: 10.0 Â· Longest block: 5.0 h Â· Class: STANDARD**

> **Milestone objective:** Corner balance and commanded slew demonstrated. The
> last substantial technical day before the pitch work takes over.

**NiccolÃ² & Pablo â€” support and brake measurement**
- Electrical support to corner-balance and slew testing.
- Spin-down brake-torque measurement: log wheel speed through the braking event
  and differentiate. This is where the assumed brake torque figure finally gets
  a measured source â€” if S3 is Go.
- Demo-day spares and a field-repair kit: spare harness, driver, encoder.

**Andrea & Deyan â€” corner balance and slew**
- Coupled three-axis corner balance and a commanded slew manoeuvre.
- Report the attitude-control metrics â€” these are the technical results the
  pitch rests on.

**Suvanna â€” verification**
- Corner-balance verification runs, logged.
- Mechanical support to jump-up preparation if S3 is Go.

**Nasia â€” capture**
- Demo and presentation hardware finalised.
- Photograph and video the cube for the deck. Capture it while it is working â€”
  there may not be a second chance.

---

## Sunday 16 August

**Hours available: 0.0 Â· Class: REST**

> **Milestone objective:** None. No work scheduled.

Four days to the presentation. Two of them are rehearsals.

---

# WEEK 4 â€” 17â€“20 August

## Monday 17 August

**Hours available: 8.0 Â· Longest block: 3.5 h Â· Class: STANDARD**

> **Milestone objective:** Last technical day. Jump-up attempt if S3 is Go;
> otherwise all capacity moves to the deck. **Technical work stops at EOD** â€”
> 18 and 19 August belong to the pitch.

**NiccolÃ² & Pablo â€” jump-up support or deck support**
- *If S3 is Go:* support the jump-up attempt. Brake circuit live, spin-up to
  the design wheel speed, monitor bus and rails through the release transient â€”
  the largest single energy event the electrical system sees. Record peak bus
  voltage.
- *If S3 is No-Go:* electrical figures and results plots for the deck. Block
  diagram, power tree, measured performance.
- Either way: demo-day electrical readiness confirmed, spares kit packed.

**Andrea & Deyan â€” results consolidation**
- *If S3 is Go:* spin-up profile and brake-release sequencing for the jump-up.
- Consolidate all analytical results into presentation form.
- Final technical numbers for the deck. Nothing goes on a slide unmeasured.

**Suvanna â€” verification and capture**
- Support the jump-up attempt mechanically if it runs.
- Final mechanical verification and demo rehearsal of the physical handling.

**Nasia â€” visual assets**
- Demo hardware final state.
- CAD renders and visuals for the deck.

**Combined team â€” deck content**
- Deck content complete: real results, real numbers, real images.
- **Technical results freeze at EOD.** Two rehearsals cannot absorb changing
  content underneath them.

---

## Tuesday 18 August

**Hours available: 8.0 Â· Longest block: 3.0 h Â· Class: STANDARD**
**â€” FIRST TIMED PITCH REHEARSAL**

> **Milestone objective:** **First full timed run of the 3-minute pitch.**
> Find out today what actually fits in three minutes, while there is still a
> day to fix it.

**Combined team â€” rehearsal, primary activity**
- **Full timed rehearsal. Time it with a clock, out loud, standing up.** Three
  minutes is shorter than everyone expects.
- Cut to fit. If it runs long, remove content rather than speaking faster.
- Assign speaker roles and rehearse the handoffs â€” transitions are where timed
  pitches lose control.
- Q&A preparation: the three hardest questions and an answer for each.

**NiccolÃ² & Pablo**
- Technical accuracy review of every electrical claim on every slide.
- Demo hardware ready and rehearsed in the presentation configuration.

**Andrea & Deyan**
- Technical accuracy review of every analytical and performance claim.
- Own the technical depth in Q&A.

**Suvanna**
- Live demo rehearsal: the physical sequence, timed alongside the script.

**Nasia**
- Slide visual polish, and the physical setup rehearsed as it will be on the
  day.

---

## Wednesday 19 August

**Hours available: 8.0 Â· Longest block: 3.0 h Â· Class: STANDARD**
**â€” FINAL DRESS REHEARSAL**

> **Milestone objective:** **Full dress rehearsal, script and slides together.**
> Everything is final at EOD. Nothing changes on presentation morning.

**Combined team â€” dress rehearsal, primary activity**
- **Full dress rehearsal: final script, final slides, final demo, timed.**
- Run it at least twice. The second run is where the timing settles.
- Freeze the deck. **No slide changes after today.**
- Contingency rehearsal: run the pitch once assuming the live demo fails. It is
  the single most likely thing to go wrong and the cheapest to prepare for.

**NiccolÃ² & Pablo**
- Final electrical check on the demo configuration.
- Spares and field-repair kit packed and verified against a list.

**Andrea & Deyan**
- Commercial deck and technical documentation finalised.
- Q&A responses rehearsed.

**Suvanna**
- Demo sequence rehearsed to a repeatable routine.

**Nasia**
- Presentation materials and physical setup complete.

---

## Thursday 20 August

**Hours available: 8.0 Â· Longest block: 4.0 h Â· Class: PRESENTATION**

> **Milestone objective:** **Deliver the 3-minute pitch and the commercial
> deck.** Project close.

**Morning â€” setup and final run**
- Full setup in the presentation space.
- One final timed run-through. No content changes.
- Demo hardware powered, verified, and left in a known-good state.

**NiccolÃ² & Pablo**
- Demo hardware live and stable. Spares kit within reach.

**Andrea & Deyan**
- Technical Q&A ownership.

**Suvanna**
- Live demo operation.

**Nasia**
- Presentation delivery and physical setup ownership.

**Presentation â€” 3-minute pitch + commercial deck.**

**After: project close-out.** Commit everything. Final documentation to the
repository.

---

## Appendix â€” capacity reconciliation

| Segment | Hours | Status |
|---|---|---|
| Pre-trip, 30 Jul â€“ 11 Aug | 88.0 | matches given |
| 12 Aug | 3.0 | matches given |
| 13 Aug | 0.0 | matches given |
| Post-trip, 14 â€“ 20 Aug | 46.5 | matches given |
| **Total** | **137.5** | **matches given** |

Day-level splits within each segment are derived, not given â€” see
[`cubli_time_budget.md`](cubli_time_budget.md) Â§3, where every figure is tagged.

**Two hard bottlenecks, stated plainly.** First, 1 and 8 August are the only
6.0 h blocks in the entire project, and wheel balancing, three-axis assembly
and the first battery power-on all need one. There is no third such block and no
in-window recovery if either is lost. Second, moving the S3 gate to 11 August
removes two days of integration run-up; the 14.5 h loaded onto 11 August
recovers part of that, and the rest is paid for out of the brake and jump-up
scope, which is sacrificial by standing decision.
