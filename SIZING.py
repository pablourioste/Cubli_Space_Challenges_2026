"""
Cubli reaction wheel -- ring + N spokes + hexagonal bolt pockets.

Wheel seen from its spin axis = a DONUT (ring) held by N_spokes SPOKES.
  - Ring + spokes are PET-CF, all at one uniform thickness `t`.
  - Hub / axis structure is OMITTED (negligible inertia contribution).
  - Extra inertia comes from M6 STEEL BOLTS seated in hexagonal
    through-pockets cut in the ring.  Each pocket therefore does TWO
    things: it ADDS steel and it REMOVES plastic.

  Selected design: OD = 150 mm with 9 bolts (see the sweep below).
  (Was 130 mm / 15 bolts at M = 1.40 kg. The Stage 6 mass budget put the
   real cube at 1.722 kg, which raised I_w_target beyond what the 130 mm
   wheel delivers. omega_max is held at 6000 rpm per electrical/
   MOTOR_SPEED.md -- the sagged-pack ceiling is ~6900 rpm, so the
   ~7750 rpm the 130 mm wheel would have needed is not reachable.
   Closure therefore comes from wheel diameter, not wheel speed.)

Net effect per pocket (both mass and inertia):
    dm = m_nut - m_plastic_removed
    dI = I_nut - I_plastic_removed
Because rho_steel >> rho_petcf, dI > 0 and the pocket is a net win --
but the plastic loss is NOT negligible and is accounted for here.

Flow:
  STAGE 1  jump-up dynamics       -> required per-wheel inertia I_w_target
  STAGE 2  solid PET-CF ring+spokes -> baseline structural inertia & mass
  STAGE 3  hex nut + hex pocket   -> per-pocket dm, dI
  STAGE 4  solve N_nuts           -> how many pockets to hit the target
  STAGE 5  feasibility            -> do N pockets physically fit in the ring?
"""
import math

# =================================================================
# FIXED INPUT VARIABLES  (edit here)
# =================================================================
# --- cube / jump-up ---
M          = 1.410        # [kg]   total cube mass
                          #        PROVISIONAL, and a converged fixed point:
                          #        Stage 6 totals 1100 g known hardware + 610 g
                          #        structure allowance = 1710 g, which is the
                          #        value assumed here (step 6 of the closure
                          #        procedure closes on itself).
                          #        Was 1.40 kg, which the BOM did not support.
                          #        ~36% is still allowance -- revisit at CAD.
L          = 0.15         # [m]    cube edge length
g          = 9.81         # [m/s^2]
eta        = 1.05         # [-]    energy margin (1.02-1.05 recommended)
tau_b      = 5.0          # [N*m]  brake torque per wheel
rpm_max    = 6000         # [rpm]  max wheel speed
case       = "corner"     # "edge" or "corner" -- corner sizes the design

# --- wheel geometry ---
ring_width_mm = 1.5      # [mm]  ring radial width (r_out - r_in), FIXED
                          #       20 mm: leaves 4.0 mm radial wall each side of
                          #       an M6 pocket (12.01 mm across corners), above
                          #       the 2 mm minimum in BOTH nut orientations.
spoke_w_mm    = 10.0      # [mm]  spoke width
N_spokes      = 3         # [-]   number of spokes
t_mm          = 10.0      # [mm]  UNIFORM thickness of ring + spokes
                          #       12 mm: a 5.2 mm blind pocket leaves a 6.8 mm
                          #       plastic floor under each nut. At 10 mm the
                          #       ring needs so many nuts that the
                          #       circumferential wall goes negative.

# --- hex nut geometry ---
# For a REGULAR hexagon the side and apothem are not independent:
#     a = 2*m/sqrt(3)      (equivalently  m = a*sqrt(3)/2)
# The apothem is the measurable one (half the across-flats size, which
# is what a caliper or a spanner reads), so it is the input and the
# side is derived.
nut_apothem_mm  = 5.0     # [mm]  hexagon APOTHEM m = (across-flats)/2
                          #       M6 hex nut, ISO 4032: 10.0 mm across flats.
nut_side_mm     = 2*nut_apothem_mm/math.sqrt(3)   # [mm] DERIVED side a
nut_bore_d_mm   = 5.35    # [mm]  central bore DIAMETER (threaded hole)
                          #       M6 thread MINOR diameter -- the thread is
                          #       metal, so the minor dia is the honest hole
                          #       for a mass estimate (6.0 mm nominal would
                          #       over-remove and under-predict the mass).
nut_mass_g      = 2.5     # [g]   MEASURED nut mass -- put one on a scale and
                          #       type the number here. Leave as None to have
                          #       it ESTIMATED from the hexagon + bore geometry.
                          #       A measured value overrides the geometry for
                          #       mass, but the geometric SHAPE is still used
                          #       for the mass distribution (radius of gyration).
nut_t_mm        = 5.2     # [mm]  nut thickness; None -> equals wheel t
                          #       M6 hex nut, ISO 4032 nominal.
pocket_depth_mm = None    # [mm]  POCKET depth into the ring. None -> equals
                          #       the nut thickness, i.e. a BLIND pocket just
                          #       deep enough to swallow the nut, leaving a
                          #       floor of (t - depth) plastic underneath.
                          #       Set equal to t_mm for a through-hole.
pocket_clear_mm = 0.2     # [mm]  radial clearance added to the POCKET only
                          #       (pocket is slightly bigger than the nut)
min_wall_mm     = 2.0     # [mm]  minimum plastic wall required around a pocket
N_round_to      = 3       # [-]   round N_nuts up to a multiple of this
                          #       (3 keeps it symmetric with 3 spokes)

# --- materials ---
rho_petcf  = 1290.0       # [kg/m^3]  ring + spokes
rho_steel  = 7850.0       # [kg/m^3]  hex nuts

# --- sweep ---
OD_list_mm = [80, 90, 100, 110, 120, 130, 140, 150,160,170,180]   # ring OUTER diameter

# =================================================================
# STAGE 1 -- JUMP-UP -> TARGET WHEEL INERTIA
# =================================================================
GEOM = {
    "edge":   dict(kappa=2/3,   lam=1/math.sqrt(2) - 0.5,  n=1.0),
    "corner": dict(kappa=11/12, lam=math.sqrt(3)/2 - 0.5,  n=math.sqrt(2)),
}
kappa, lam, n = GEOM[case]["kappa"], GEOM[case]["lam"], GEOM[case]["n"]
omega_max = rpm_max * 2*math.pi/60

C            = math.sqrt(2*g*lam*kappa) / n
h_w_ideal    = math.sqrt(eta) * C * M * L**1.5

tau_g = M * g * L / 2.0
if tau_b <= tau_g:
    raise ValueError(f"tau_b={tau_b} N*m below floor tau_g={tau_g:.3f} N*m "
                      "-- cube can never tip.")
beta       = tau_b / (tau_b - tau_g)
h_w        = h_w_ideal * beta
I_w_target = h_w / omega_max

print("=== STAGE 1: jump-up -> target wheel inertia ===")
print(f"case={case}  M={M} kg  L={L*1e3:.0f} mm  tau_b={tau_b} N*m  rpm_max={rpm_max}")
print(f"tau_g (floor)      = {tau_g:.3f} N*m")
print(f"beta               = {beta:.3f}")
print(f"h_w (per wheel)    = {h_w:.4f} kg*m^2/s")
print(f"I_w_target         = {I_w_target*1e4:.4f} x1e-4 kg*m^2\n")

# =================================================================
# STAGE 2 -- SOLID PET-CF RING + SPOKES  (before any pockets)
# =================================================================
t          = t_mm * 1e-3
w_spoke    = spoke_w_mm * 1e-3
ring_width = ring_width_mm * 1e-3

def ring_props(OD_mm):
    """Solid annular ring: fixed radial width, uniform thickness t."""
    r_out = OD_mm/2 * 1e-3
    r_in  = r_out - ring_width
    m     = math.pi*(r_out**2 - r_in**2) * t * rho_petcf
    I     = 0.5 * m * (r_out**2 + r_in**2)
    return m, I, r_in, r_out

def spokes_props(r_in):
    """N_spokes radial bars, centre -> ring inner edge, width w_spoke."""
    L_spoke = r_in
    m_one   = L_spoke * w_spoke * t * rho_petcf
    I_one   = (1/3)*m_one*L_spoke**2 + (1/12)*m_one*w_spoke**2
    return N_spokes*m_one, N_spokes*I_one

# =================================================================
# STAGE 3 -- HEX POCKET + HEX NUT
# =================================================================
# Regular hexagon, side a, apothem m:
#     Area                      A   = 3 * a * m
#     Polar 2nd moment / area   k^2 = m^2/2 + a^2/24
# (check: with m = a*sqrt(3)/2 this gives k^2 = 5/12 * a^2, the
#  textbook value for a regular hexagon -- so the formula is right.)
a_nut  = nut_side_mm    * 1e-3
m_nut_ap = nut_apothem_mm * 1e-3
r_bore = nut_bore_d_mm/2 * 1e-3
t_nut  = (nut_t_mm if nut_t_mm is not None else t_mm) * 1e-3
t_pkt  = (pocket_depth_mm if pocket_depth_mm is not None
          else t_nut*1e3) * 1e-3          # blind-pocket depth
if t_pkt > t + 1e-12:
    raise ValueError(f"pocket depth {t_pkt*1e3:.1f} mm exceeds wheel "
                      f"thickness {t_mm:.1f} mm")
if t_nut > t_pkt + 1e-12:
    raise ValueError(f"nut ({t_nut*1e3:.1f} mm) is thicker than the pocket "
                      f"({t_pkt*1e3:.1f} mm) -- it will stand proud")
floor_mm = (t - t_pkt) * 1e3               # plastic left under the pocket

# pocket is the nut grown by the clearance (apothem grows by clearance,
# side grows by the same proportion so it stays a regular hexagon)
scale_p  = (nut_apothem_mm + pocket_clear_mm) / nut_apothem_mm
a_pkt    = a_nut    * scale_p
m_pkt_ap = m_nut_ap * scale_p

def hex_area(a, m_ap):
    return 3.0 * a * m_ap

def hex_k2(a, m_ap):
    """Radius of gyration squared about the hexagon's own centroidal axis."""
    return m_ap**2/2.0 + a**2/24.0

# --- steel nut: solid hexagon minus circular bore ---
A_hex_nut = hex_area(a_nut, m_nut_ap)
A_bore    = math.pi * r_bore**2
if A_bore >= A_hex_nut:
    raise ValueError("Bore is larger than the hexagon -- check nut geometry.")

m_nut_hex  = rho_steel * A_hex_nut * t_nut
m_nut_bore = rho_steel * A_bore    * t_nut
m_nut_geom = m_nut_hex - m_nut_bore                     # GEOMETRIC estimate

# Effective radius of gyration^2 of the nut cross-section (hexagon minus
# bore). This is a pure SHAPE property -- it does not depend on the total
# mass -- so it stays valid even when the mass is overridden by a
# measured value.
I0_nut_geom = (m_nut_hex * hex_k2(a_nut, m_nut_ap)
               - m_nut_bore * (r_bore**2/2.0))
k2_nut = I0_nut_geom / m_nut_geom

# --- choose which mass to use, and say so loudly ---
if nut_mass_g is None:
    m_nut       = m_nut_geom
    mass_source = "ESTIMATED from geometry (nut_mass_g is None)"
    reconcile   = None
else:
    m_nut       = nut_mass_g * 1e-3
    mass_source = "MEASURED -- user-supplied nut_mass_g"
    # what bore diameter would the geometry need to match the measurement?
    A_bore_eff = A_hex_nut - m_nut/(rho_steel*t_nut)
    reconcile  = (2*math.sqrt(A_bore_eff/math.pi)*1e3 if A_bore_eff > 0 else None)

I0_nut = m_nut * k2_nut

# --- plastic removed: full hexagonal pocket, through-thickness ---
A_pkt      = hex_area(a_pkt, m_pkt_ap)
m_removed  = rho_petcf * A_pkt * t_pkt          # <-- blind depth, not full t
I0_removed = m_removed * hex_k2(a_pkt, m_pkt_ap)

print("=== STAGE 3: hex pocket + hex nut (per unit) ===")
print(f"nut: apothem m={nut_apothem_mm:.3f} mm  ->  side a={nut_side_mm:.3f} mm (derived)")
print(f"     across flats = {2*nut_apothem_mm:.2f} mm   "
      f"across corners = {2*nut_side_mm:.2f} mm")
print(f"     bore d={nut_bore_d_mm:.2f} mm   t_nut={t_nut*1e3:.1f} mm")
print(f"  hex area          = {A_hex_nut*1e6:8.2f} mm^2")
print(f"  bore area         = {A_bore*1e6:8.2f} mm^2")
print(f"  -- NUT MASS SOURCE: {mass_source}")
print(f"     geometric estimate = {m_nut_geom*1e3:8.3f} g")
if nut_mass_g is not None:
    delta = (m_nut - m_nut_geom)/m_nut_geom*100
    print(f"     measured value     = {m_nut*1e3:8.3f} g   ({delta:+.1f}% vs geometry)")
    if reconcile is not None:
        print(f"     -> a bore of {reconcile:.2f} mm would reconcile geometry "
              f"with the measurement (you set {nut_bore_d_mm:.2f} mm)")
    else:
        print(f"     -> measurement is heavier than a SOLID hexagon of this size; "
              f"check apothem/thickness/density")
print(f"  ** NUT MASS IN USE  = {m_nut*1e3:8.3f} g **")
print(f"  nut k^2 (shape)   = {k2_nut*1e6:8.4f} mm^2")
print(f"  nut I0 (own axis) = {I0_nut*1e7:8.4f} x1e-7 kg*m^2")
print(f"pocket (nut + {pocket_clear_mm:.1f} mm clearance), "
      f"depth {t_pkt*1e3:.1f} mm of {t_mm:.1f} mm wheel "
      f"-> {floor_mm:.1f} mm plastic floor:")
print(f"  pocket area       = {A_pkt*1e6:8.2f} mm^2")
print(f"  PLASTIC REMOVED   = {m_removed*1e3:8.3f} g")
print(f"  removed I0        = {I0_removed*1e7:8.4f} x1e-7 kg*m^2")
print(f"  NET mass per pocket = {(m_nut - m_removed)*1e3:+8.3f} g\n")

# =================================================================
# STAGE 4+5 -- SOLVE N_nuts PER OD, THEN CHECK IT FITS
# =================================================================
print("=== STAGE 4+5: solve number of nuts per ring OD ===")
print(f"fixed: ring_width={ring_width_mm:.0f} mm  spoke_w={spoke_w_mm:.0f} mm  "
      f"N_spokes={N_spokes}  t={t_mm:.1f} mm  N rounded to multiple of {N_round_to}")

hdr = (f"\n{'OD':>5} | {'ID':>5} | {'r_nut':>6} | {'solid I':>8} | {'N':>4} | "
       f"{'PLASTIC g':>9} | {'STEEL g':>8} | {'TOTAL g':>8} || "
       f"{'I_plast':>8} | {'I_steel':>8} | {'I_tot':>7} | {'gap mm':>7}")
print(hdr)
print("-"*len(hdr))

rows = []
for OD in OD_list_mm:
    m_ring, I_ring, r_in, r_out = ring_props(OD)
    m_spk,  I_spk = spokes_props(r_in)
    m_solid = m_ring + m_spk
    I_solid = I_ring + I_spk

    # pockets sit centred in the ring width
    r_nut = (r_out + r_in) / 2.0

    # inertia of one nut / one removed pocket, about the SPIN axis
    I_nut_at_r     = I0_nut     + m_nut     * r_nut**2
    I_removed_at_r = I0_removed + m_removed * r_nut**2
    dI = I_nut_at_r - I_removed_at_r          # net inertia gain per pocket
    dm = m_nut - m_removed                     # net mass gain per pocket

    I_needed = I_w_target - I_solid
    if I_needed <= 0:
        rows.append(dict(OD=OD, note="solid ring already exceeds target"))
        print(f"{OD:>5} | {OD-2*ring_width_mm:>5.0f} | {r_nut*1e3:>6.1f} | "
              f"{I_solid*1e4:>8.4f} |  --  |   --      |   --     |   --     || "
              f"   --    |    --    |   --    |   --     <-- solid ring already "
              f"exceeds target")
        continue

    N_exact = I_needed / dI
    N_nuts  = int(math.ceil(N_exact / N_round_to) * N_round_to)

    m_plastic = m_solid - N_nuts * m_removed
    m_steel   = N_nuts * m_nut
    m_wheel   = m_plastic + m_steel

    I_plastic = I_solid - N_nuts * I_removed_at_r
    I_steel   = N_nuts * I_nut_at_r
    I_wheel   = I_plastic + I_steel

    # circumferential fit: wall of plastic left between adjacent pockets
    pitch_mm = 2*math.pi*r_nut*1e3 / N_nuts
    # worst-case circumferential extent of a hexagon = across corners = 2a
    gap_mm   = pitch_mm - 2*a_pkt*1e3

    flag = ""
    if gap_mm < min_wall_mm:
        flag = f"  <-- WALL {gap_mm:.1f} mm < {min_wall_mm:.1f} mm min"

    rows.append(dict(OD=OD, N=N_nuts, N_exact=N_exact, r_nut=r_nut*1e3,
                     m_plastic=m_plastic*1e3, m_steel=m_steel*1e3,
                     m_wheel=m_wheel*1e3, I_plastic=I_plastic*1e4,
                     I_steel=I_steel*1e4, I_wheel=I_wheel*1e4,
                     gap=gap_mm, pitch=pitch_mm, dI=dI, dm=dm))

    print(f"{OD:>5} | {OD-2*ring_width_mm:>5.0f} | {r_nut*1e3:>6.1f} | "
          f"{I_solid*1e4:>8.4f} | {N_nuts:>4d} | {m_plastic*1e3:>9.2f} | "
          f"{m_steel*1e3:>8.2f} | {m_wheel*1e3:>8.2f} || "
          f"{I_plastic*1e4:>8.4f} | {I_steel*1e4:>8.4f} | {I_wheel*1e4:>7.4f} | "
          f"{gap_mm:>7.1f}{flag}")

# =================================================================
# INERTIA SPLIT (%) AND 3-WHEEL BUDGET
# =================================================================
print(f"\n{'OD':>5} | {'I_plastic %':>11} | {'I_steel %':>10} | "
      f"{'I_tot / target':>14} | {'x3 wheels g':>12} | {'% of cube':>10}")
print("-"*78)
for r in rows:
    if "note" in r:
        continue
    tot = r['I_plastic'] + r['I_steel']
    print(f"{r['OD']:>5} | {r['I_plastic']/tot*100:>10.1f}% | "
          f"{r['I_steel']/tot*100:>9.1f}% | "
          f"{tot/(I_w_target*1e4)*100:>13.1f}% | "
          f"{3*r['m_wheel']:>12.2f} | {3*r['m_wheel']/1e3/M*100:>9.1f}%")

# =================================================================
# RADIAL FIT CHECK (independent of OD)
# =================================================================
print("\n=== Radial fit of pocket inside the ring ===")
across_flats_mm   = 2*m_pkt_ap*1e3
across_corners_mm = 2*a_pkt*1e3
print(f"pocket across flats   = {across_flats_mm:.2f} mm")
print(f"pocket across corners = {across_corners_mm:.2f} mm")
print(f"ring radial width     = {ring_width_mm:.2f} mm")
for label, dim in (("flats radial", across_flats_mm),
                   ("corners radial", across_corners_mm)):
    wall = (ring_width_mm - dim) / 2.0
    status = "OK" if wall >= min_wall_mm else "TOO THIN"
    print(f"  orientation '{label:<15s}': wall each side = {wall:5.2f} mm  [{status}]")

# =================================================================
# BLIND-POCKET FLOOR CHECK
# =================================================================
# The pockets are BLIND, not through-holes: each nut sits in a recess with a
# plastic floor beneath it. That floor is what retains the nut against
# centrifugal load, so it is a structural item and not just leftover material.
print("\n=== Blind-pocket floor (nut retention) ===")
print(f"wheel thickness  = {t_mm:.1f} mm")
print(f"pocket depth     = {t_pkt*1e3:.1f} mm  (= nut thickness)")
floor_status = "OK" if floor_mm >= min_wall_mm else "TOO THIN"
print(f"plastic floor    = {floor_mm:.1f} mm  [{floor_status}]")
if floor_mm <= 0:
    print("  !! floor <= 0: this is a THROUGH hole, nuts are not retained")
elif floor_mm < min_wall_mm:
    print(f"  !! floor below the {min_wall_mm:.1f} mm minimum -- increase t_mm "
          f"to at least {t_pkt*1e3 + min_wall_mm:.1f} mm")

# Centrifugal load on one nut at max speed, for the floor/adhesive check.
# The floor carries this in shear+bending if the nut is not otherwise bonded.
r_nut_max = (max(OD_list_mm)/2*1e-3) - ring_width*0.5
F_c = m_nut * omega_max**2 * r_nut_max
print(f"centrifugal force per nut at {rpm_max} rpm, r={r_nut_max*1e3:.0f} mm:")
print(f"  F = m*omega^2*r = {F_c:.0f} N  ({F_c/9.81:.1f} kgf)")
print("  -> nuts must be bonded or capped; the floor alone is not a retention "
      "plan at this load.")


# =================================================================
# =================================================================
# STAGE 6 -- MASS BUDGET  (DECOUPLED from stages 1-5)
# =================================================================
# Self-contained: it reads NOTHING from the sizing code above except the
# assumed cube mass M, which it exists to CHECK. Every mass is a variable
# below -- edit the numbers there, not in the logic.
#
# WHY THIS MATTERS: M is not a free assumption. It is an input to
# I_w_target (Stage 1), which sets the wheel, whose mass feeds back into
# M. This stage closes that loop: it totals the real bill of materials
# and compares it against the M assumed at the top of the file.
# =================================================================

# --- what the sizing above ASSUMED, so we can check it ---
M_ASSUMED_g = M * 1e3        # [g] the cube mass Stage 1 was run with

# Bill of materials.
#   (label, unit_mass_g, qty, category)
# unit_mass_g is the mass of ONE item; qty is how many are on the cube.
# Set unit mass to None for an item whose mass is not yet known -- it is
# then reported as UNKNOWN and excluded from the total, so a missing
# number can never silently masquerade as zero.
BOM = [
    # --- actuation -------------------------------------------------
    ("T-Motor MN4006 KV380",              68.0,  3, "Motors"),
    ("TowerPro MG92B brake servo",        13.8,  3, "Motors"),

    # --- reaction wheels -------------------------------------------
    # From the OD=150 mm SOLID ring selected in Stage 4 above: at this
    # diameter the plain PET-CF ring already exceeds I_w_target, so no
    # steel nuts are needed at all. Kept as a literal so this stage
    # stays decoupled; update it if the wheel design changes.
    ("Reaction wheel (PET-CF, 150 mm, no nuts)", 151.98, 3, "Wheels"),

    # --- power -----------------------------------------------------
    ("Turnigy 6S 3600 mAh LiPo, 22.2 V",  254.0, 1, "Power"),
    ("XT90 connector pair",                15.0,  1, "Power"),
    ("LM2596 step-down regulator",         10.0,  1, "Power"),

    # --- control & sensing -----------------------------------------
    ("mjbots moteus-n1 driver",            14.6,  3, "Electronics"),
    ("mjbots MA600 breakout + magnet",      3.0,  3, "Electronics"),
    ("Teensy 4.1",                          5.0,  1, "Electronics"),
    ("CAN-FD adapter for Teensy 4.1",       5.0,  1, "Electronics"),
    ("mjcanfd-usb-1x",                      3.4,  1, "Electronics"),
    ("Seeed XIAO ESP32-C6 + antenna",       3.0,  1, "Electronics"),
    ("SparkFun BMI270 IMU (Qwiic)",         5.0,  1, "Electronics"),

    # --- interconnect & passives -----------------------------------
    ("JST PH3 cable",                       3.0,  3, "Wiring"),
    ("Protoboard 15 x 9 cm double-sided",  25.0,  1, "Wiring"),
    ("60.4 ohm 1/2 W resistor (CAN)",       0.253, 2, "Wiring"),
    ("100 uF 16 V electrolytic cap",        1.0,  3, "Wiring"),
    ("100 nF 50 V cap",                     1.0,  3, "Wiring"),
    ("4.7 nF cap (CAN)",                    1.0,  2, "Wiring"),
    ("1N5819 Schottky diode",               3.0,  1, "Wiring"),

    # --- structure: NOT YET KNOWN, pending CAD ---------------------
    # Declared explicitly rather than omitted, so the budget reports
    # them as missing instead of quietly totalling without them.
    ("Inner structure / motor subframe",   None,  1, "Structure"),
    ("Outer frame / contact features",     None,  1, "Structure"),
    ("Fasteners / wiring harness",         None,  1, "Structure"),
]

# Allowances for items above whose unit mass is still None. These are
# ESTIMATES, flagged as such in the output and totalled separately, so
# the known-hardware figure and the projected figure never get confused.
ALLOWANCE_g = {
    "Inner structure / motor subframe": 250.0,
    "Outer frame / contact features":   300.0,
    "Fasteners / wiring harness":        60.0,
}

CATEGORY_ORDER = ["Motors", "Wheels", "Power", "Electronics", "Wiring",
                  "Structure"]

print("\n\n" + "="*72)
print("STAGE 6: MASS BUDGET".center(72))
print("="*72)

# ---- itemised list ----------------------------------------------
hdr6 = (f"\n{'Item':<38} | {'unit g':>7} | {'qty':>3} | {'total g':>8} | "
        f"{'category':<11}")
print(hdr6)
print("-"*len(hdr6))

known_total   = 0.0
unknown_items = []
cat_known     = {c: 0.0 for c in CATEGORY_ORDER}

for label, unit, qty, cat in BOM:
    if unit is None:
        unknown_items.append((label, qty, cat))
        print(f"{label:<38} | {'--':>7} | {qty:>3} | {'UNKNOWN':>8} | {cat:<11}")
        continue
    tot = unit * qty
    known_total += tot
    cat_known[cat] = cat_known.get(cat, 0.0) + tot
    print(f"{label:<38} | {unit:>7.2f} | {qty:>3} | {tot:>8.2f} | {cat:<11}")

print("-"*len(hdr6))
print(f"{'SUBTOTAL -- known hardware':<38} | {'':>7} | {'':>3} | "
      f"{known_total:>8.2f} |")

# ---- allowances for the unknowns --------------------------------
allow_total = 0.0
if unknown_items:
    print(f"\n--- Allowances for items with no measured mass "
          f"({len(unknown_items)}) ---")
    for label, qty, cat in unknown_items:
        a = ALLOWANCE_g.get(label)
        if a is None:
            print(f"{label:<38} |  NO ALLOWANCE SET -- budget is incomplete")
            continue
        tot = a * qty
        allow_total += tot
        cat_known[cat] = cat_known.get(cat, 0.0) + tot
        print(f"{label:<38} | {a:>7.2f} | {qty:>3} | {tot:>8.2f} | "
              f"{cat:<11} (est.)")

M_est_g = known_total + allow_total

# ---- category rollup --------------------------------------------
print(f"\n{'Category':<14} | {'mass g':>9} | {'% of est. total':>15}")
print("-"*45)
for c in CATEGORY_ORDER:
    v = cat_known.get(c, 0.0)
    if v == 0.0:
        continue
    print(f"{c:<14} | {v:>9.2f} | {v/M_est_g*100:>14.1f}%")
print("-"*45)
print(f"{'TOTAL':<14} | {M_est_g:>9.2f} |")

# ---- the actual comparison --------------------------------------
print("\n=== Reconciliation against the assumed cube mass ===")
print(f"known hardware (measured/spec)   = {known_total:8.1f} g")
print(f"structure allowance (ESTIMATED)  = {allow_total:8.1f} g")
print(f"ESTIMATED TOTAL M                = {M_est_g:8.1f} g  "
      f"({M_est_g/1e3:.3f} kg)")
print(f"ASSUMED M used in Stage 1        = {M_ASSUMED_g:8.1f} g  "
      f"({M_ASSUMED_g/1e3:.3f} kg)")

delta_g   = M_est_g - M_ASSUMED_g
delta_pct = delta_g / M_ASSUMED_g * 100
print(f"DELTA (estimate - assumed)       = {delta_g:+8.1f} g  ({delta_pct:+.1f}%)")

if delta_g > 0:
    print("\n  !! The build is HEAVIER than Stage 1 assumed.")
    print("     h_w scales as M*L^1.5, so the wheel requirement rises:")
    scale = (M_est_g/M_ASSUMED_g)
    print(f"     I_w_target would grow by x{scale:.3f} "
          f"-> {I_w_target*scale*1e4:.4f} x1e-4 kg*m^2")
    print(f"     tau_g floor would rise to "
          f"{M_est_g/1e3*g*L/2:.3f} N*m (tau_b = {tau_b} N*m)")
    if tau_b <= M_est_g/1e3*g*L/2:
        print("     !! BRAKE TORQUE NOW BELOW THE FLOOR -- design does not close.")
    else:
        beta_new = tau_b/(tau_b - M_est_g/1e3*g*L/2)
        print(f"     beta would rise {beta:.3f} -> {beta_new:.3f}")
        print(f"     combined I_w_target -> "
              f"{I_w_target*scale*(beta_new/beta)*1e4:.4f} x1e-4 kg*m^2")
    print("     -> re-run Stage 1 with the updated M (step 6 of the closure).")
else:
    print("\n  OK: the build is at or under the assumed mass; Stage 1 stands.")

if unknown_items:
    print(f"\n  NOTE: {len(unknown_items)} structural item(s) carry ESTIMATED "
          f"allowances, not measured\n        masses. "
          f"{allow_total/M_est_g*100:.0f}% of the total is allowance -- "
          f"treat this as provisional\n        until CAD closes.")