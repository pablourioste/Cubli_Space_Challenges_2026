# Electrical Risk Register

Rows for A5 (risk register, All +Pablo, 28-29 Jul, delivered with the TDD 3 Aug).
Format follows the A5 scope line in `02_project_organization_tasks.tex`:
trigger, impact, owner, mitigation. LaTeX-ready version at the bottom.

Severity S and likelihood L: H / M / L. Owner is the person who acts, not the
person who notices.

| ID | Risk | Trigger | Impact | S | L | Owner | Mitigation |
|---|---|---|---|---|---|---|---|
| RE1 | 16 V cap on the 25 V bus | Build error at E4.2: the BOM 100 uF parts are 16 V and physically fit the bus rail | Electrolytic vents or explodes on first battery power-on. Board destroyed, 25 V bus shorted, possible driver loss. Recovery >= 3 days, straight through the 9 Aug G5 gate | H | M | Pablo | 16 V parts marked and physically segregated at build time; 5 V rail only. Bus bulk cap is a separate 470-1000 uF >= 50 V procurement line. Explicit check item at E5.2 before any power |
| RE2 | Bulk cap absent at regen brake | Wheel decelerates hard (brake test, disarm, or jump-up); ~105 J per wheel pumps back into the bus with no reservoir | Bus overvoltage trips or damages a moteus-n1. Loses one axis; spare consumes the 4th set and kills the bench rig | H | M | Pablo | Confirm bulk cap ordered (open question 2). No aggressive decel commanded until the cap is fitted and verified at E4.3. Drivers configured with a bus-overvoltage fault limit |
| RE3 | MA600 air gap out of spec | Gap > 0.5 mm or chip off-centre on the 4 mm magnet, typically after mechanical assembly at E5.1 | Angle noise or dropout, FOC commutation degrades, balance impossible. Presents as a control bug and burns Andrea's and Nicc's time on the wrong subsystem | H | H | Pablo | Shim value fixed and recorded at E1.5, re-verified on every axis at E5.1. Encoder error flags logged during every balance run (E6.2) so a mechanical fault is not mistaken for a control fault |
| RE4 | SPI run exceeds 20 cm | Layout or repackaging moves a driver away from its encoder | Encoder read corruption at 6 MHz; same failure signature as RE3 | H | M | Pablo | Driver positions are derived from the encoder positions at E2.1, frozen in the E2.4 outline. Any later mechanical change that moves a driver is an electrical change request, not a CAD detail |
| RE5 | CAN-FD unreliable at 5 Mbps | Stub > 10 cm, termination not at the two physical bus ends, or star topology introduced during integration | Error frames and dropped commands under vibration. Intermittent, hard to diagnose, appears only when wheels spin | H | M | Pablo | Linear topology enforced, bus ends identified at E2.2, split termination 2x 60.4 ohm + 4.7 nF at exactly those two ends. Scope + soak test at E4.5 before integration. CAN error counters logged at E6.2 |
| RE6 | Board outline late to Nasia | E2.4 slips past 1 Aug | C5 mass freeze slips, C11 frame print slips, cascades to the 9 Aug G5 gate | H | M | Pablo | E2 block starts 29 Jul with 2 days of float. If E1 slips, the outline is issued from the layout study with conservative keep-outs rather than delayed |
| RE7 | Rig parameters late to Andrea | E3.5 slips past 2 Aug because C9 (wheel balance, due 31 Jul) or C10 slips | Andrea is the critical resource holding B9 -> B11 -> B12 sequentially. A one-day slip here propagates directly to 20 Aug with no recovery path | H | M | Pablo | Zero float exists on this chain. Escalate to Suvanna on 30 Jul if C9 is not on track. Fallback: deliver Kt and loop latency from bench measurement (E1.6, no wheel needed) on 2 Aug and wheel J plus friction on 3 Aug, so Andrea starts B9 with three of four numbers |
| RE8 | LM2596 5 V rail undersized | Teensy + XIAO ESP32-C6 (300 mA TX burst) + BMI270 + MG92B stall drawn simultaneously | 5 V rail sags, MCU browns out mid-balance. Cube falls; may be misread as a control failure | M | M | Pablo | Sum the load budget (open question 6) before E4.2. Heatsink the module. Bulk on the 5 V rail plus the 1N5819 back-feed diode. Measure sag at E4.3 under worst-case simultaneous load |
| RE9 | Battery bring-up incident | Battery connected before the bench sequence completes, or connected without anti-spark switch and fuse | Arc on connection, LiPo fire. Injury and total project loss | H | L | Pablo | Battery physically stays out of the loop until E5.5 on 9 Aug. All bring-up on a current-limited PSU. Anti-spark switch, inline fuse, cell alarm, safe bag, fire-safe area, second person present |
| RE10 | XT90/XT30 harness fails under load | Cold solder joint or under-gauge wire on a bus that can pull 40-60 A | Voltage drop, connector melt, or open circuit mid-demo | M | M | Pablo | 14 AWG minimum on the bus, fabricated at E4.1, pull-tested and thermal-imaged during E4.5 soak. Spare harness in the demo kit (E7.3) |
| RE11 | Only 3 complete motor sets exist | 4th set was not ordered, or an incoming unit fails inspection at E1.3 | The 1-DoF bench rig must be cannibalised to complete the cube. Loses the permanent development bench: every later firmware experiment then competes with the flight article | M | M | Pablo | Verify at E1.3 that 4 sets are present and functional. If short, escalate procurement on 28 Jul while lead time still fits before 7 Aug integration |
| RE12 | Brake work cannibalises edge balance | C14 brake build (10-13 Aug) runs concurrently with the 13 Aug G6 hard kill date | Missing G6 cuts the S3 jump-up stretch goal entirely, and the brake exists only to serve S3 | M | M | Pablo | E6.3 is explicitly the sacrificial task. Any conflict between brake support and edge-balance support resolves to edge balance, no discussion required at the time |
| RE13 | Vibration-induced connector failure | Wheels at up to 6000 rpm shake connectors loose during extended balance runs | Intermittent axis dropout, cube falls, damage to structure and wheels | M | H | Pablo | Strain relief and labelling at E4.7, threadlocker and retention on every connector, connector reseat check as first action in every E6.1 support call |
| RE14 | Perfboard rework consumes C12 float | C12 is 4 days with no slack; a wiring error found at E4.5 needs rework | Board late to E5.1, cascades to the 9 Aug G5 gate | M | M | Pablo | Point-to-point wiring checked against the E2.3 floorplan before power. Rails brought up incrementally (E4.3 before E4.4 before E4.6) so a fault is localised to one subsystem |

## Notes for Dejan

- RE7 is the row that matters most to the schedule. It is the only risk whose
  realisation cannot be recovered before 20 Aug.
- RE1 and RE9 are the two safety rows. Both are procedural, not design, risks.
- RE12 is a decision already taken, recorded here so it is not re-litigated
  under pressure on 12 Aug.

---

## LaTeX version (paste into A5)

Requires `longtable`, `booktabs`, `array`, `ragged2e` and `\newcolumntype{L}`
as already used in `02_project_organization_tasks.tex`.

```latex
% Electrical rows for the risk register (A5). Owner: Pablo.
{\small
\setlength{\tabcolsep}{4pt}%
\begin{longtable}{@{}L{0.9cm} L{2.6cm} L{3.4cm} L{3.4cm} c c L{1.5cm} L{4.2cm}@{}}
\toprule
\textbf{ID} & \textbf{Risk} & \textbf{Trigger} & \textbf{Impact} & \textbf{S} & \textbf{L} & \textbf{Owner} & \textbf{Mitigation} \\
\midrule\endfirsthead
\toprule
\textbf{ID} & \textbf{Risk} & \textbf{Trigger} & \textbf{Impact} & \textbf{S} & \textbf{L} & \textbf{Owner} & \textbf{Mitigation} \\
\midrule\endhead
\bottomrule\endfoot
\multicolumn{8}{@{}l}{\textbf{Electrical and Power}} \\
\midrule
RE1 & \qty{16}{\volt} capacitor on the \qty{25}{\volt} bus & Build error: the BOM \qty{100}{\micro\farad} parts are \qty{16}{\volt} and fit the bus rail & Capacitor vents; board destroyed and bus shorted; ${\ge}\,3$~day recovery through the 9~Aug gate & H & M & Pablo & \qty{16}{\volt} parts segregated at build, \qty{5}{\volt} rail only; bulk cap is a separate \qtyrange{470}{1000}{\micro\farad}, ${\ge}\,\qty{50}{\volt}$ item; explicit pre-power check \\
RE2 & No bulk capacitance at regenerative braking & Hard wheel deceleration returns ${\approx}\,\qty{105}{\joule}$ to the bus & Bus overvoltage damages a moteus-n1; loses one axis and the bench-rig spare & H & M & Pablo & Fit and verify the \qty{50}{\volt} bulk capacitor before any commanded deceleration; driver bus-overvoltage fault limit \\
RE3 & MA600 air gap out of specification & Gap ${>}\,\qty{0.5}{\milli\metre}$ or chip off-centre after mechanical assembly & Angle dropout and degraded commutation; presents as a control fault and misdirects debugging & H & H & Pablo & Shim value fixed on the bench and re-verified per axis at integration; encoder error flags logged in every balance run \\
RE4 & SPI run exceeds \qty{20}{\centi\metre} & Repackaging moves a driver away from its encoder & Encoder corruption at \qty{6}{\mega\hertz}; same signature as RE3 & H & M & Pablo & Driver positions derived from encoder positions and frozen in the board outline; later moves are electrical change requests \\
RE5 & CAN-FD unreliable at \qty{5}{\mega\bit\per\second} & Stub ${>}\,\qty{10}{\centi\metre}$, mis-placed termination, or star topology at integration & Error frames and dropped commands under vibration; intermittent and hard to diagnose & H & M & Pablo & Linear topology; split termination $2\times\qty{60.4}{\ohm}+\qty{4.7}{\nano\farad}$ at the two physical bus ends only; scope and soak test before integration \\
RE6 & Board outline late to CAD & Layout slips past 1~Aug & Mass freeze (C5) and frame print (C11) slip, cascading to the 9~Aug integration gate & H & M & Pablo & Two days of float; if bring-up slips, issue the outline with conservative keep-outs rather than delay it \\
RE7 & Rig parameters late to control & Wheel balance (C9) or rig assembly (C10) slips past 2~Aug & Blocks the sequential B9\,$\rightarrow$\,B11\,$\rightarrow$\,B12 chain; propagates to 20~Aug with no recovery & H & M & Pablo & Escalate on 30~Jul if C9 is off track; fallback delivers $K_t$ and loop latency from bench measurement on 2~Aug and wheel inertia and friction on 3~Aug \\
RE8 & \qty{5}{\volt} rail undersized & Teensy, XIAO (\qty{300}{\milli\ampere} burst), IMU and servo stall draw together & Rail sag and MCU brown-out mid-balance; misread as a control failure & M & M & Pablo & Sum the load budget before build; heatsink the LM2596; bulk plus back-feed diode; measure sag under worst-case load \\
RE9 & Battery bring-up incident & Battery connected before the bench sequence completes, or without anti-spark switch and fuse & Arc or LiPo fire; injury and total project loss & H & L & Pablo & All bring-up on a current-limited supply; battery introduced only at the 9~Aug power-on, with anti-spark switch, fuse, cell alarm, safe bag and a second person present \\
RE10 & Power harness fails under load & Cold joint or under-gauge wire on a \qtyrange{40}{60}{\ampere} bus & Voltage drop, connector melt, or open circuit mid-demonstration & M & M & Pablo & \qty{14}{\awg} minimum, pull-tested and thermally imaged during soak; spare harness in the demonstration kit \\
RE11 & Fewer than four complete actuation sets & Fourth set not ordered, or a unit fails incoming inspection & The bench rig is cannibalised for the cube, losing the permanent development bench & M & M & Pablo & Verify four working sets at incoming inspection; escalate procurement on 28~Jul while lead time still permits \\
RE12 & Brake work displaces edge balance & C14 runs concurrently with the 13~Aug edge-balance gate & Missing the gate cuts the jump-up stretch goal, which the brake exists to serve & M & M & Pablo & Brake support is the designated sacrificial task; conflicts resolve to edge balance by standing decision \\
RE13 & Vibration loosens connectors & Sustained running at up to \qty{6000}{\rpm} & Intermittent axis dropout; cube falls and damages structure & M & H & Pablo & Strain relief, labelling and connector retention; reseat check as the first action of every support call \\
RE14 & Perfboard rework consumes its float & Wiring error found at bus test; C12 has four days and no slack & Board late to integration, cascading to the 9~Aug gate & M & M & Pablo & Wiring checked against the floorplan before power; rails brought up incrementally so faults localise \\
\end{longtable}
}
```
