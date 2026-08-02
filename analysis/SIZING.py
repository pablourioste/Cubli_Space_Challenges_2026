"""
Cubli reaction wheel -- ring + N spokes + M6 bolts in ROUND THROUGH-HOLES.

Wheel seen from its spin axis = a DONUT (ring) held by N_spokes SPOKES.
  - Ring + spokes are PET-CF, all at one uniform thickness `t`.
  - Hub / axis structure is OMITTED (negligible inertia contribution).
  - Extra inertia comes from M6 STEEL BOLT + NUT sets fitted through
    CIRCULAR CLEARANCE HOLES drilled through the full ring thickness.
    Each hole therefore does TWO things: it ADDS steel hardware and it
    REMOVES plastic.

GEOMETRY MODEL CHANGE (this revision):
  Previously the ballast sat in HEXAGONAL BLIND POCKETS of depth ~t/2,
  and only the loose nut was counted as added mass. That model is
  replaced here by the as-built scheme: a round M6 clearance hole through
  the whole thickness, with a bolt passing through and a nut on the far
  side. Consequences, all of them physical:
    * the removed plastic is a full-depth cylinder, not a part-depth
      hexagonal prism, so MORE plastic is lost per station;
    * the added steel is bolt + nut, not nut alone, so MORE steel is
      gained per station;
    * the bolt is what retains the hardware, so the blind-pocket floor
      (previously the retention argument) no longer exists and its check
      is gone.

Net effect per hole (both mass and inertia):
    dm = m_hardware - m_plastic_removed          m_hardware = m_bolt + m_nut
    dI = I_hardware - I_plastic_removed
Because rho_steel >> rho_petcf, dI > 0 and the station is a net win --
but the plastic loss is NOT negligible and is accounted for here.

WHAT THE DESIGN NOW IS: OD = 120 mm with 15 M6 stations, 172.5 g/wheel,
reaching 111.7% of I_w_target. The diameter is NOT the sweep's choice --
it is PINNED by D_w_FIXED_mm because three orthogonal wheel modules plus
the battery have to fit inside the L = 150 mm cube. Left free, the
minimum-mass rule picks a much larger ring (I_zz goes as m*R^2, so mass
at a large radius is cheap inertia), but a wheel that does not fit the
cube is not a candidate, so the envelope outranks the mass objective.
The sweep is still computed and printed in full, as context for what the
constraint costs.

omega_max is 6000 rpm per electrical/MOTOR_SPEED.md and the TDD. The
sizing has also been run at 5000 rpm as an OVER-DIMENSIONING check:
I_w_target = h_w/omega_max, so the lower speed raises the requirement by
6/5 and demands more ballast. A wheel closing at 5000 closes at 6000 with
margin in hand.

M IS A FIXED POINT, NOT AN ASSUMPTION: M sets I_w_target (Stage 1), which
sets the ballast count, which sets the wheel mass, which feeds back into
M via Stage 6. Iterating from 1.700 kg converged in three passes to
M = 1.7716 kg, where Stage 6's roll-up reproduces the assumed value.

Flow:
  STAGE 1  jump-up dynamics         -> required per-wheel inertia I_w_target
  STAGE 2  solid PET-CF ring+spokes -> baseline structural inertia & mass
  STAGE 3  round hole + M6 hardware -> per-station dm, dI
  STAGE 4  solve N_holes            -> how many stations to hit the target
  STAGE 5  feasibility              -> radial fit, and the 2 mm edge-to-edge
                                       gap rule that caps N at N_max
  STAGE 6  mass budget              -> closes the loop on the assumed cube mass
"""
import math

# =================================================================
# FIXED INPUT VARIABLES  (edit here)
# =================================================================
# --- cube / jump-up ---
M          = 1.7716       # [kg]   total cube mass
                          #        PROVISIONAL, and a CONVERGED FIXED POINT:
                          #        Stage 6 totals 1161.6 g known hardware +
                          #        610 g structure allowance = 1771.6 g, which
                          #        is the value assumed here, so step 6 of the
                          #        closure procedure closes on itself
                          #        (delta ~0).
                          #        The loop is real, not decorative: M sets
                          #        I_w_target (Stage 1), which sets the ballast
                          #        count, which sets the wheel mass, which
                          #        feeds back into M. Iterating from 1.700 kg
                          #        converged in 3 passes
                          #        (1.700 -> 1.851 -> 1.772 -> 1.772).
                          #        ~34% is still allowance -- revisit at CAD.
L          = 0.15         # [m]    cube edge length
g          = 9.81         # [m/s^2]
eta        = 1.05         # [-]    energy margin (1.02-1.05 recommended)
tau_b      = 5.0          # [N*m]  brake torque per wheel
rpm_max    = 6000         # [rpm]  max wheel speed -- DESIGN VALUE, matches the
                          #        TDD (tab:jumpup_budget and the dashed ceiling
                          #        on the motor curve) and electrical/MOTOR_SPEED.md.
                          #        * The sizing has ALSO been run at 5000 rpm as
                          #        an over-dimensioning check: since
                          #        I_w_target = h_w/omega_max, the lower speed
                          #        raises the inertia requirement by 6/5 and so
                          #        demands MORE ballast. A wheel that closes at
                          #        5000 therefore closes at 6000 with margin in
                          #        hand. 6000 is what the design claims; 5000 is
                          #        the conservative case it was checked against.
case       = "corner"     # "edge" or "corner" -- corner sizes the design

# --- wheel geometry ---
# Named R_outer / R_inner / thickness below as well, after unit conversion,
# so the geometry functions read the way the drawing does.
ring_width_mm = 15.0      # [mm]  ring radial width (R_outer - R_inner), FIXED
                          #       15 mm: a 6.4 mm M6 clearance hole centred in
                          #       the width leaves 4.30 mm of radial wall on
                          #       each side, over twice the 2 mm minimum.
                          #       A round hole has no orientation, so unlike
                          #       the old hexagonal pocket there is only ONE
                          #       radial case to check, not two.
spoke_w_mm    = 10.0      # [mm]  spoke width
N_spokes      = 3         # [-]   number of spokes
t_mm          = 5.0       # [mm]  UNIFORM thickness of ring + spokes
                          #       = the through-hole depth. It no longer has to
                          #       cover a nut plus a floor, but it still sets
                          #       the bolt grip length and the ring's own
                          #       inertia. 5 mm keeps the wheel axially thin so
                          #       three orthogonal modules clear each other
                          #       inside the 150 mm cube.

# --- hole pattern: ROUND M6 CLEARANCE THROUGH-HOLES ---
hole_diameter_mm = 6.4    # [mm]  DRILLED hole diameter, through the full t.
                          #       6.4 mm = ISO 273 "medium" clearance for M6.
                          #       (close fit 6.4 is standard; free fit 7.0.)
                          #       This is the hole, not the thread: the bolt
                          #       shank is 6.0 mm, so there is 0.4 mm total
                          #       diametral slop for assembly.
R_pcr_mm      = None      # [mm]  Pitch Circle Radius of the hole pattern.
                          #       None -> centred in the ring width, i.e.
                          #       (R_inner + R_outer)/2, which is both the
                          #       inertia-neutral choice and the one that
                          #       maximises the radial wall on both sides.
                          #       Set a number to force it off-centre; the
                          #       boundary check below will still police it.
num_holes     = None      # [-]   FORCED number of holes. None -> the script
                          #       solves for the count that meets I_w_target
                          #       and then caps it at N_max. Set an integer to
                          #       impose a count; it is still gap-checked and
                          #       still capped, with a warning if it was cut.
min_gap_mm    = 2.0       # [mm]  MINIMUM edge-to-edge separation between two
                          #       adjacent holes, measured on the straight
                          #       chord between their centres. This is what
                          #       sets N_max (see the derivation in the
                          #       docstring of max_holes_for_gap()).
min_wall_mm   = 2.0       # [mm]  minimum radial plastic wall between a hole
                          #       edge and the ring's inner / outer boundary
N_round_to    = 3         # [-]   round the solved hole count up to a multiple
                          #       of this (3 keeps 3-fold symmetry with the
                          #       3 spokes, so balance is unaffected)

# --- M6 hardware seated in each hole (bolt + nut) ---
# Both masses are per-item and are the things to put on a scale. They enter
# as POSITIVE mass; nothing about the hardware is modelled as a negative.
mass_m6_bolt_g = 6.5      # [g]   ONE M6 bolt, head + shank, of the length
                          #       actually used. Strongly length-dependent:
                          #       ISO 4762 M6x20 hex-socket cap is ~6.0 g,
                          #       M6x25 ~7.0 g, M6x30 ~8.0 g. 7.5 g stands in
                          #       for an M6x25-30 through a 12 mm ring plus
                          #       nut. MEASURE the real one.
mass_m6_nut_g  = 2.5      # [g]   ONE M6 hex nut, MEASURED (ISO 4032 geometry
                          #       predicts 2.617 g, so 2.5 g is within normal
                          #       tolerance -- see electrical/WHEEL_130_M6.md).
mass_m6_washer_g = 0.0    # [g]   per-hole washer allowance, 0 if none used.
                          #       An M6 plain washer is ~0.9 g; two of them is
                          #       1.8 g per station, which is not nothing at
                          #       this radius.

# Radius of gyration of the hardware about its OWN axis. A bolt+nut stack is
# a compact cluster ~6-10 mm across sitting at R_pcr ~ 65 mm, so its own-axis
# term is ~(8/65)^2 ~ 1.5% of its parallel-axis term. Modelled as a solid
# cylinder of diameter hole_diameter (k^2 = r^2/2), which slightly OVER-states
# it -- the conservative direction, since this term adds inertia.
hardware_own_axis_model = "cylinder"   # "cylinder" or "point" (k^2 = 0)

# --- materials ---
rho_petcf  = 1290.0       # [kg/m^3]  ring + spokes
rho_steel  = 7850.0       # [kg/m^3]  M6 bolts and nuts

# --- sweep ---
OD_list_mm = [80, 90, 100, 110, 120, 130, 140, 150,160,170,180]   # ring OUTER diameter

# --- FIXED ENVELOPE CONSTRAINT ---------------------------------------------
# The wheel OD is IMPOSED by the packaging envelope, not chosen by the sweep.
# Three orthogonal wheel modules plus the battery have to fit inside the
# L = 150 mm cube, and that fixes the ring at 120 mm. The sweep is still run
# and printed in full, but only as CONTEXT: it shows what the constraint
# costs. Set to None to hand selection back to the minimum-mass rule.
#
# Without this pin the selector picks OD = 180 mm, which is lighter per wheel
# (I_zz goes as m*R^2, so mass at a large radius is cheap inertia) but does
# not fit the cube. A design that does not fit is not a candidate, so the
# constraint outranks the mass objective.
D_w_FIXED_mm = 120.0

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
print(f"I_w_target         = {I_w_target*1e4:.4f} x1e-4 kg*m^2")

# --- BOTH CONTACT CASES, for the record -----------------------------------
# The design is sized on the CORNER case, but the TDD reports both so the
# claim "corner is the critical one" is visible rather than asserted. Only
# the geometry factor C differs between them: tau_g and beta are properties
# of the cube and the brake, not of which feature it is standing on, so they
# are shared. A wheel meeting the corner requirement meets the edge one with
# the margin printed below.
print("\n  contact case comparison (same M, L, eta, tau_b, omega_max):")
print(f"  {'case':<8} | {'C':>7} | {'h_w':>9} | {'I_w_target':>12} | "
      f"{'vs corner':>9}")
print("  " + "-"*56)
_cases = {}
for _c, _p in GEOM.items():
    _C   = math.sqrt(2*g*_p["lam"]*_p["kappa"]) / _p["n"]
    _hw  = math.sqrt(eta) * _C * M * L**1.5 * beta
    _cases[_c] = (_C, _hw, _hw/omega_max)
_I_corner = _cases["corner"][2]
for _c in ("edge", "corner"):
    _C, _hw, _It = _cases[_c]
    _mark = " <- sizing case" if _c == case else ""
    print(f"  {_c:<8} | {_C:>7.4f} | {_hw:>9.4f} | "
          f"{_It*1e4:>9.4f}e-4 | {_It/_I_corner*100:>8.1f}%{_mark}")
print(f"  the corner case demands "
      f"{(1 - _cases['edge'][2]/_I_corner)*100:.1f}% more inertia than the "
      f"edge case,\n  so it is the one the design is sized on.\n")

# =================================================================
# STAGE 2 -- SOLID PET-CF RING + SPOKES  (before any holes)
# =================================================================
thickness  = t_mm * 1e-3          # [m]  wheel thickness == through-hole depth
t          = thickness            #      short alias used in the formulae
w_spoke    = spoke_w_mm * 1e-3
ring_width = ring_width_mm * 1e-3

def ring_props(OD_mm):
    """Solid annular ring: fixed radial width, uniform thickness t.

    I_zz of an annulus about its own axis:  I = 1/2 * m * (R_o^2 + R_i^2)
    Returns (mass, I_zz, R_inner, R_outer) in SI units.
    """
    R_outer = OD_mm/2 * 1e-3
    R_inner = R_outer - ring_width
    if R_inner <= 0:
        raise ValueError(f"OD {OD_mm} mm is smaller than twice the ring width "
                         f"{ring_width_mm} mm -- the ring has no bore.")
    m = math.pi*(R_outer**2 - R_inner**2) * thickness * rho_petcf
    I = 0.5 * m * (R_outer**2 + R_inner**2)
    return m, I, R_inner, R_outer

def spokes_props(R_inner):
    """N_spokes radial bars, centre -> ring inner edge, width w_spoke.

    Each bar is a slender rectangle rotating about one end:
        I = 1/3 m L^2   (radial extent)  +  1/12 m w^2  (its own width)
    """
    L_spoke = R_inner
    m_one   = L_spoke * w_spoke * thickness * rho_petcf
    I_one   = (1/3)*m_one*L_spoke**2 + (1/12)*m_one*w_spoke**2
    return N_spokes*m_one, N_spokes*I_one


# =================================================================
# GEOMETRY HELPERS -- pitch circle, radial fit, 2 mm gap capacity
# =================================================================
def pcr_for(R_inner, R_outer):
    """Pitch Circle Radius of the hole pattern.

    R_pcr_mm is honoured if the user set it; otherwise the pattern is
    centred in the ring width, which maximises the radial wall on both
    sides simultaneously.
    """
    if R_pcr_mm is not None:
        return R_pcr_mm * 1e-3
    return 0.5 * (R_inner + R_outer)


def check_radial_fit(R_inner, R_outer, R_pcr, r_hole):
    """Enforce  R_inner + r_hole < R_pcr < R_outer - r_hole,  with walls.

    Returns (ok, wall_inner_mm, wall_outer_mm, messages). The strict
    inequality of the brief is the ok=False case at zero wall; the
    min_wall_mm test is the stricter engineering requirement layered on
    top of it, because a hole that merely 'fits' with 0.1 mm of plastic
    left is not a manufacturable feature.
    """
    wall_inner = (R_pcr - r_hole) - R_inner        # plastic inboard of the hole
    wall_outer = R_outer - (R_pcr + r_hole)        # plastic outboard of the hole
    msgs = []
    ok = True
    if wall_inner <= 0:
        ok = False
        msgs.append(f"hole breaks through the ring ID "
                    f"(inner wall {wall_inner*1e3:+.2f} mm)")
    elif wall_inner < min_wall_mm*1e-3:
        ok = False
        msgs.append(f"inner wall {wall_inner*1e3:.2f} mm < "
                    f"{min_wall_mm:.1f} mm minimum")
    if wall_outer <= 0:
        ok = False
        msgs.append(f"hole breaks through the ring OD "
                    f"(outer wall {wall_outer*1e3:+.2f} mm)")
    elif wall_outer < min_wall_mm*1e-3:
        ok = False
        msgs.append(f"outer wall {wall_outer*1e3:.2f} mm < "
                    f"{min_wall_mm:.1f} mm minimum")
    return ok, wall_inner*1e3, wall_outer*1e3, msgs


def edge_gap(N, R_pcr, r_hole):
    """Edge-to-edge gap [m] between two adjacent holes of N on the pitch circle.

    N hole centres equally spaced on a circle of radius R_pcr subtend
    Delta_theta = 2*pi/N. The CHORD between adjacent centres is

        c = 2 * R_pcr * sin(pi/N)

    and since both holes have radius r_hole, the material left between
    their edges along that chord is

        gap = c - 2*r_hole = 2*R_pcr*sin(pi/N) - 2*r_hole

    The chord is used, not the arc length 2*pi*R_pcr/N: the arc
    OVER-estimates centre spacing (arc >= chord always), so sizing on the
    arc would report a gap that the part does not have. The old script
    used exactly that arc-pitch and so was optimistic by (arc - chord),
    which at small N is not a rounding error -- at N = 6 the arc is 4.7%
    longer than the chord.
    """
    if N < 2:
        return math.inf
    return 2.0*R_pcr*math.sin(math.pi/N) - 2.0*r_hole


def max_holes_for_gap(R_pcr, r_hole, gap_min):
    """Largest N whose adjacent-hole edge gap is still >= gap_min.

    Invert  2*R_pcr*sin(pi/N) - 2*r_hole >= gap_min:

        sin(pi/N) >= (r_hole + gap_min/2) / R_pcr  ==  s
        pi/N      >= asin(s)                    (both in (0, pi/2])
        N         <= pi / asin(s)

    so N_max = floor(pi / asin(s)). If s >= 1 not even two holes fit and
    N_max = 0. Monotonicity check: sin(pi/N) decreases as N grows, so the
    constraint is a genuine upper bound on N -- there is no second branch.
    """
    s = (r_hole + 0.5*gap_min) / R_pcr
    if s >= 1.0:
        return 0
    n_max = int(math.floor(math.pi / math.asin(s)))
    return max(n_max, 0)

# =================================================================
# STAGE 3 -- ROUND THROUGH-HOLE + M6 BOLT/NUT HARDWARE (per station)
# =================================================================
# The hole is a CYLINDER through the full thickness:
#     V   = pi * r_hole^2 * t
#     m   = rho_petcf * V                       (mass removed, positive number,
#                                                subtracted where it is used)
#     k^2 = r_hole^2 / 2                        (own-axis, solid disc)
# The hardware is bolt + nut + optional washers, entering as POSITIVE mass.
r_hole = hole_diameter_mm/2 * 1e-3

if hole_diameter_mm >= ring_width_mm:
    raise ValueError(
        f"hole diameter {hole_diameter_mm:.2f} mm does not fit in the ring "
        f"radial width R_outer - R_inner = {ring_width_mm:.2f} mm.")
if hole_diameter_mm + 2*min_wall_mm > ring_width_mm:
    print(f"!! WARNING: a {hole_diameter_mm:.2f} mm hole plus "
          f"2 x {min_wall_mm:.1f} mm wall needs "
          f"{hole_diameter_mm + 2*min_wall_mm:.2f} mm of ring width, "
          f"but the ring is only {ring_width_mm:.2f} mm wide.\n"
          f"   No pitch circle radius can satisfy the wall rule.")

# --- plastic removed per hole: full-depth cylinder ---
V_hole     = math.pi * r_hole**2 * thickness
m_removed  = rho_petcf * V_hole
I0_removed = 0.5 * m_removed * r_hole**2          # own-axis, solid disc

# --- steel hardware added per hole: bolt + nut (+ washers) ---
m_bolt     = mass_m6_bolt_g   * 1e-3
m_nut      = mass_m6_nut_g    * 1e-3
m_washer   = mass_m6_washer_g * 1e-3
m_hardware = m_bolt + m_nut + m_washer
if m_hardware <= 0:
    raise ValueError("M6 hardware mass is zero or negative -- set "
                     "mass_m6_bolt_g / mass_m6_nut_g.")

if hardware_own_axis_model == "cylinder":
    k2_hardware = 0.5 * r_hole**2
elif hardware_own_axis_model == "point":
    k2_hardware = 0.0
else:
    raise ValueError("hardware_own_axis_model must be 'cylinder' or 'point'")
I0_hardware = m_hardware * k2_hardware

print("=== STAGE 3: round M6 through-hole + bolt/nut (per station) ===")
print(f"hole: d = {hole_diameter_mm:.2f} mm (M6 clearance), "
      f"r = {r_hole*1e3:.2f} mm, THROUGH t = {t_mm:.1f} mm")
print(f"  hole area         = {math.pi*r_hole**2*1e6:8.2f} mm^2")
print(f"  hole volume       = {V_hole*1e9:8.2f} mm^3")
print(f"  PLASTIC REMOVED   = {m_removed*1e3:8.3f} g   (rho = {rho_petcf:.0f} kg/m^3)")
print(f"  removed I0        = {I0_removed*1e7:8.4f} x1e-7 kg*m^2  (own axis)")
print(f"hardware per hole (POSITIVE mass added back):")
print(f"  M6 bolt           = {m_bolt*1e3:8.3f} g")
print(f"  M6 nut            = {m_nut*1e3:8.3f} g")
if m_washer > 0:
    print(f"  washer(s)         = {m_washer*1e3:8.3f} g")
print(f"  ** m_hardware     = {m_hardware*1e3:8.3f} g **")
print(f"  hardware k^2      = {k2_hardware*1e6:8.4f} mm^2 "
      f"({hardware_own_axis_model} model)")
print(f"  hardware I0       = {I0_hardware*1e7:8.4f} x1e-7 kg*m^2  (own axis)")
print(f"NET mass per station = {(m_hardware - m_removed)*1e3:+8.3f} g "
      f"(steel gained - plastic lost)\n")

# =================================================================
# STAGE 4+5 -- SOLVE N_holes PER OD, THEN CHECK IT FITS
# =================================================================
def wheel_properties(OD_mm, N_forced=None):
    """Full mass / I_zz model of one wheel at a given ring OD.

    Returns a dict. The inertia bookkeeping is, for N holes on R_pcr:

        I_zz = I_ring + I_spokes
               - N * (I0_hole     + m_removed  * R_pcr^2)     <- plastic gone
               + N * (I0_hardware + m_hardware * R_pcr^2)     <- steel added

    Both correction terms use the Parallel Axis Theorem about the SPIN
    axis; neither is a bare m*R^2, because a 6.4 mm feature at ~65 mm
    still has an own-axis term and dropping it is a free, avoidable error.
    """
    m_ring, I_ring, R_inner, R_outer = ring_props(OD_mm)
    m_spk,  I_spk = spokes_props(R_inner)
    m_solid = m_ring + m_spk
    I_solid = I_ring + I_spk

    R_pcr = pcr_for(R_inner, R_outer)
    radial_ok, wall_in, wall_out, radial_msgs = check_radial_fit(
        R_inner, R_outer, R_pcr, r_hole)

    # per-station contributions about the SPIN axis (parallel axis theorem)
    I_removed_at_r  = I0_removed  + m_removed  * R_pcr**2
    I_hardware_at_r = I0_hardware + m_hardware * R_pcr**2
    dI = I_hardware_at_r - I_removed_at_r      # net inertia gain per station
    dm = m_hardware - m_removed                # net mass gain per station

    N_max = max_holes_for_gap(R_pcr, r_hole, min_gap_mm*1e-3)

    # --- choose N ---------------------------------------------------
    note    = None
    capped  = False
    N_exact = None
    if N_forced is not None:
        N = int(N_forced)
        note = "N forced by num_holes"
    else:
        I_needed = I_w_target - I_solid
        if I_needed <= 0:
            N = 0
            note = "solid ring already meets target -- no ballast needed"
        elif dI <= 0:
            N = 0
            note = ("hardware is LIGHTER than the plastic it displaces "
                    "(dI <= 0) -- holes would REDUCE inertia")
        else:
            N_exact = I_needed / dI
            N = int(math.ceil(N_exact / N_round_to) * N_round_to)

    if N > N_max:
        capped = True
        # keep the N_round_to symmetry while respecting the cap
        N = (N_max // N_round_to) * N_round_to
        note = (f"N capped by the {min_gap_mm:.1f} mm gap rule "
                f"(N_max = {N_max})")

    # --- totals -----------------------------------------------------
    m_plastic = m_solid - N * m_removed
    m_steel   = N * m_hardware
    m_wheel   = m_plastic + m_steel

    I_plastic = I_solid - N * I_removed_at_r
    I_steel   = N * I_hardware_at_r
    I_wheel   = I_plastic + I_steel

    gap = edge_gap(N, R_pcr, r_hole) if N >= 2 else math.inf

    return dict(
        OD=OD_mm, R_inner=R_inner, R_outer=R_outer, R_pcr=R_pcr,
        m_solid=m_solid, I_solid=I_solid,
        N=N, N_exact=N_exact, N_max=N_max, capped=capped, note=note,
        m_plastic=m_plastic, m_steel=m_steel, m_wheel=m_wheel,
        I_plastic=I_plastic, I_steel=I_steel, I_wheel=I_wheel,
        dI=dI, dm=dm, gap=gap,
        radial_ok=radial_ok, wall_in=wall_in, wall_out=wall_out,
        radial_msgs=radial_msgs,
        meets_target=(I_wheel >= I_w_target),
    )


print("=== STAGE 4+5: solve number of M6 through-holes per ring OD ===")
print(f"fixed: ring_width={ring_width_mm:.1f} mm  spoke_w={spoke_w_mm:.1f} mm  "
      f"N_spokes={N_spokes}  t={t_mm:.1f} mm")
print(f"       hole d={hole_diameter_mm:.2f} mm through  "
      f"min_gap={min_gap_mm:.1f} mm  min_wall={min_wall_mm:.1f} mm  "
      f"N rounded to multiple of {N_round_to}")
print(f"       R_pcr = " + ("centred in ring width" if R_pcr_mm is None
                            else f"{R_pcr_mm:.2f} mm (forced)"))

hdr = (f"\n{'OD':>5} | {'ID':>5} | {'R_pcr':>6} | {'solid I':>8} | {'N':>4} | "
       f"{'Nmax':>4} | {'PLASTIC g':>9} | {'STEEL g':>8} | {'TOTAL g':>8} || "
       f"{'I_plast':>8} | {'I_steel':>8} | {'I_tot':>7} | {'gap mm':>7}")
print(hdr)
print("-"*len(hdr))

rows = []
for OD in OD_list_mm:
    r = wheel_properties(OD, N_forced=num_holes)
    rows.append(r)

    gap_txt = "   inf " if math.isinf(r['gap']) else f"{r['gap']*1e3:>7.2f}"
    flags = []
    if r['capped']:
        flags.append(f"CAPPED at N_max={r['N_max']}")
    if not math.isinf(r['gap']) and r['gap'] < min_gap_mm*1e-3:
        flags.append(f"GAP {r['gap']*1e3:.2f} mm < {min_gap_mm:.1f} mm")
    if not r['radial_ok']:
        flags.append("RADIAL: " + "; ".join(r['radial_msgs']))
    if not r['meets_target']:
        flags.append(f"SHORT of target "
                     f"({r['I_wheel']/I_w_target*100:.1f}%)")
    flag = ("  <-- " + " | ".join(flags)) if flags else ""

    print(f"{r['OD']:>5} | {(r['R_inner']*2e3):>5.0f} | {r['R_pcr']*1e3:>6.1f} | "
          f"{r['I_solid']*1e4:>8.4f} | {r['N']:>4d} | {r['N_max']:>4d} | "
          f"{r['m_plastic']*1e3:>9.2f} | {r['m_steel']*1e3:>8.2f} | "
          f"{r['m_wheel']*1e3:>8.2f} || "
          f"{r['I_plastic']*1e4:>8.4f} | {r['I_steel']*1e4:>8.4f} | "
          f"{r['I_wheel']*1e4:>7.4f} | {gap_txt}{flag}")

for r in rows:
    if r['note']:
        print(f"  note OD={r['OD']}: {r['note']}")

# =================================================================
# INERTIA SPLIT (%) AND 3-WHEEL BUDGET
# =================================================================
print(f"\n{'OD':>5} | {'I_plastic %':>11} | {'I_steel %':>10} | "
      f"{'I_tot / target':>14} | {'x3 wheels g':>12} | {'% of cube':>10}")
print("-"*78)
for r in rows:
    tot = r['I_wheel']
    if tot <= 0:
        continue
    print(f"{r['OD']:>5} | {r['I_plastic']/tot*100:>10.1f}% | "
          f"{r['I_steel']/tot*100:>9.1f}% | "
          f"{tot/I_w_target*100:>13.1f}% | "
          f"{3*r['m_wheel']*1e3:>12.2f} | "
          f"{3*r['m_wheel']/M*100:>9.1f}%")

# =================================================================
# SOLID vs MODIFIED SUMMARY  (the headline comparison)
# =================================================================
# Among the ODs that satisfy EVERY check (meets I_w_target, not cut short
# by the gap rule, passes the radial wall rule), pick the LIGHTEST wheel.
#
# Minimum mass, not minimum diameter, is the correct objective. I_zz goes
# as m*R^2, so mass parked at a large radius buys inertia quadratically
# more cheaply than mass at a small one. Sizing on the smallest OD that
# "works" therefore does the expensive thing: it forces the shortfall to
# be made up with a large number of dense bolts, and three wheels of
# ballast is mass the cube then has to throw. The sweep shows the effect
# plainly -- the 90 mm ring needs 24 bolts (308 g/wheel) while a bare
# 140 mm ring beats the target outright at 140 g/wheel.
#
# "Capped" is NOT by itself disqualifying. A capped wheel is one that could
# not take every hole that was asked for; if it still meets I_w_target with
# the holes it can legally hold, it is a perfectly good wheel. What
# disqualifies a design is failing the requirement or failing the wall
# rule. (Capping only kills a design when the cap is why it fell short --
# which the meets_target test already catches.) Treating capped as fatal
# made a forced num_holes report "no OD passes" even when every OD met the
# target with room to spare.
viable = [r for r in rows if r['meets_target'] and r['radial_ok']]
if D_w_FIXED_mm is not None:
    # The envelope has already chosen the diameter; the sweep does not get a
    # vote. Report on the pinned ring whether or not it is the lightest, and
    # say plainly what the pin cost against the free optimum.
    sel = next((r for r in rows if r['OD'] == D_w_FIXED_mm), None)
    if sel is None:
        raise ValueError(f"D_w_FIXED_mm = {D_w_FIXED_mm} mm is not in "
                         f"OD_list_mm = {OD_list_mm} -- add it to the sweep.")
    _free = min(viable, key=lambda r: r['m_wheel']) if viable else None
    print(f"\n[OD PINNED to {D_w_FIXED_mm:.0f} mm by the packaging envelope]")
    if _free is not None and _free['OD'] != sel['OD']:
        print(f"  the free minimum-mass optimum would be OD = {_free['OD']} mm "
              f"at {_free['m_wheel']*1e3:.2f} g/wheel;")
        print(f"  the constraint costs "
              f"{(sel['m_wheel']-_free['m_wheel'])*1e3:+.2f} g/wheel "
              f"({3*(sel['m_wheel']-_free['m_wheel'])*1e3:+.2f} g over three), "
              f"and it does not fit.")
    if not sel['meets_target']:
        print(f"  !! the pinned ring is SHORT of target at "
              f"{sel['I_wheel']/I_w_target*100:.1f}% -- the constraint and the "
              f"requirement are incompatible as set.")
else:
    sel = min(viable, key=lambda r: r['m_wheel']) if viable else None

print("\n" + "="*72)
print("SOLID vs MODIFIED WHEEL".center(72))
print("="*72)
if sel is None:
    print("!! No OD in the sweep passes all of {target, gap rule, radial wall}.")
    print("   Widen OD_list_mm, or relax ring_width / thickness / speed.")
    best = max(rows, key=lambda r: r['I_wheel'])
    print(f"   Closest on inertia: OD = {best['OD']} mm at "
          f"{best['I_wheel']/I_w_target*100:.1f}% of target.")
else:
    dm_pct = (sel['m_wheel'] - sel['m_solid'])/sel['m_solid']*100
    dI_pct = (sel['I_wheel'] - sel['I_solid'])/sel['I_solid']*100
    print(f"SELECTED: OD = {sel['OD']:.0f} mm  "
          f"(ID = {sel['R_inner']*2e3:.0f} mm, ring width "
          f"{ring_width_mm:.1f} mm, t = {t_mm:.1f} mm)")
    print(f"  N holes = {sel['N']}  of N_max = {sel['N_max']}  "
          f"on R_pcr = {sel['R_pcr']*1e3:.2f} mm")
    if sel['N_exact'] is not None:
        print(f"  (exact requirement was {sel['N_exact']:.2f} holes, "
              f"rounded up to a multiple of {N_round_to})")
    if sel['capped']:
        print(f"  NOTE: the hole count was CUT to {sel['N']} by the "
              f"{min_gap_mm:.1f} mm edge-gap rule (N_max = {sel['N_max']}).")
        print(f"        The wheel still meets the requirement at "
              f"{sel['I_wheel']/I_w_target*100:.1f}% of target, so the cap "
              f"cost margin, not closure.")
    print()
    print(f"{'quantity':<26} | {'SOLID':>12} | {'MODIFIED':>12} | {'delta':>12}")
    print("-"*72)
    print(f"{'mass [g]':<26} | {sel['m_solid']*1e3:>12.2f} | "
          f"{sel['m_wheel']*1e3:>12.2f} | "
          f"{(sel['m_wheel']-sel['m_solid'])*1e3:>+12.2f}")
    print(f"{'  = PET-CF [g]':<26} | {sel['m_solid']*1e3:>12.2f} | "
          f"{sel['m_plastic']*1e3:>12.2f} | "
          f"{(sel['m_plastic']-sel['m_solid'])*1e3:>+12.2f}")
    print(f"{'  = M6 steel [g]':<26} | {0.0:>12.2f} | "
          f"{sel['m_steel']*1e3:>12.2f} | {sel['m_steel']*1e3:>+12.2f}")
    print(f"{'I_zz [1e-4 kg m^2]':<26} | {sel['I_solid']*1e4:>12.4f} | "
          f"{sel['I_wheel']*1e4:>12.4f} | "
          f"{(sel['I_wheel']-sel['I_solid'])*1e4:>+12.4f}")
    print("-"*72)
    print(f"{'relative change':<26} | {'--':>12} | {'--':>12} | "
          f"mass {dm_pct:+.1f}% / I {dI_pct:+.1f}%")
    print()
    print(f"I_w_target            = {I_w_target*1e4:.4f} x1e-4 kg m^2")
    print(f"I_zz achieved         = {sel['I_wheel']*1e4:.4f} x1e-4 kg m^2  "
          f"({sel['I_wheel']/I_w_target*100:.1f}% of target)")
    if sel['N'] >= 2:
        print(f"edge-to-edge gap      = {sel['gap']*1e3:.2f} mm   "
              f"(minimum {min_gap_mm:.1f} mm) "
              f"[{'OK' if sel['gap'] >= min_gap_mm*1e-3 else 'FAIL'}]")
        print(f"chord between centres = "
              f"{2*sel['R_pcr']*math.sin(math.pi/sel['N'])*1e3:.2f} mm")
    else:
        print(f"edge-to-edge gap      = n/a ({sel['N']} hole(s)); "
              f"the gap rule would allow up to {sel['N_max']}")
    print(f"radial wall inner/outer = {sel['wall_in']:.2f} / "
          f"{sel['wall_out']:.2f} mm   (minimum {min_wall_mm:.1f} mm) "
          f"[{'OK' if sel['radial_ok'] else 'FAIL'}]")
    print(f"three wheels          = {3*sel['m_wheel']*1e3:.1f} g  "
          f"({3*sel['m_wheel']/M*100:.1f}% of the {M:.3f} kg cube)")
    if sel['N'] == 0:
        print()
        print("  The lightest compliant wheel carries NO ballast: at this")
        print("  diameter the bare PET-CF ring already exceeds I_w_target, so")
        print("  every bolt added would be mass with no requirement behind it.")
        print("  The M6 hole pattern is retained as a TRIM feature -- see the")
        print("  gap-rule table for how much upward trim is available, and the")
        print("  demonstration below for what a populated pattern would cost.")

# =================================================================
# GAP-RULE DEMONSTRATION  (exercises the 2 mm constraint explicitly)
# =================================================================
# The selected wheel may need no ballast, which would leave the hole-pattern
# checks untested in a normal run. This block forces the pattern onto the
# selected ring and walks N upward through the cap, so the constraint is
# visible rather than merely implemented.
if sel is not None:
    print(f"\n=== Gap rule exercised on the selected {sel['OD']:.0f} mm ring "
          f"(R_pcr = {sel['R_pcr']*1e3:.2f} mm) ===")
    print(f"{'N':>5} | {'chord mm':>9} | {'gap mm':>8} | {'verdict':<22} | "
          f"{'+mass g':>8} | {'+I 1e-4':>8}")
    print("-"*76)
    _N_probe = sorted({3, 6, 12, sel['N_max'], sel['N_max']+1,
                       sel['N_max']+3} - {0, 1, 2})
    for N in _N_probe:
        chord = 2*sel['R_pcr']*math.sin(math.pi/N)
        gap   = edge_gap(N, sel['R_pcr'], r_hole)
        ok    = gap >= min_gap_mm*1e-3
        verdict = "OK" if ok else f"VIOLATES {min_gap_mm:.1f} mm min"
        if N > sel['N_max']:
            verdict += " (> N_max)"
        d_mass = N * (m_hardware - m_removed)
        d_I    = N * ((I0_hardware + m_hardware*sel['R_pcr']**2)
                      - (I0_removed + m_removed*sel['R_pcr']**2))
        print(f"{N:>5d} | {chord*1e3:>9.2f} | {gap*1e3:>8.2f} | {verdict:<22} | "
              f"{d_mass*1e3:>+8.2f} | {d_I*1e4:>+8.4f}")
    print(f"N_max = {sel['N_max']} is the largest count with gap >= "
          f"{min_gap_mm:.1f} mm; the solver caps any request above it.")

# =================================================================
# RADIAL FIT CHECK (independent of OD -- a round hole has no orientation)
# =================================================================
print("\n=== Radial fit of the M6 hole inside the ring ===")
print(f"hole diameter      = {hole_diameter_mm:.2f} mm")
print(f"ring radial width  = {ring_width_mm:.2f} mm  "
      f"(R_outer - R_inner)")
print(f"width needed       = {hole_diameter_mm + 2*min_wall_mm:.2f} mm  "
      f"(hole + 2 x {min_wall_mm:.1f} mm wall)")
_slack = ring_width_mm - hole_diameter_mm - 2*min_wall_mm
print(f"slack              = {_slack:+.2f} mm  "
      f"[{'OK' if _slack >= 0 else 'TOO NARROW'}]")
print("A round hole is rotationally symmetric, so there is a single radial")
print("case -- the two hexagon orientations the previous model had to check")
print("separately no longer exist.")
if R_pcr_mm is None:
    print(f"With R_pcr centred, the wall is {_slack/2 + min_wall_mm:.2f} mm "
          f"on each side, the maximum available.")

# =================================================================
# GAP-RULE CAPACITY TABLE  (N_max vs OD)
# =================================================================
print(f"\n=== Hole capacity from the {min_gap_mm:.1f} mm edge-gap rule ===")
print("N_max = floor(pi / asin((r_hole + gap_min/2) / R_pcr))")
print(f"\n{'OD':>5} | {'R_pcr':>7} | {'N_max':>5} | {'gap at N_max':>12} | "
      f"{'N used':>6} | {'gap at N used':>13}")
print("-"*66)
for r in rows:
    g_max = edge_gap(r['N_max'], r['R_pcr'], r_hole) if r['N_max'] >= 2 else math.inf
    g_use = r['gap']
    f_max = "     inf" if math.isinf(g_max) else f"{g_max*1e3:8.2f}"
    f_use = "      inf" if math.isinf(g_use) else f"{g_use*1e3:9.2f}"
    print(f"{r['OD']:>5} | {r['R_pcr']*1e3:>7.2f} | {r['N_max']:>5d} | "
          f"{f_max:>12} | {r['N']:>6d} | {f_use:>13}")

# =================================================================
# THROUGH-BOLT RETENTION LOAD
# =================================================================
# With a through-hole the bolt is the retention: the nut is threaded onto it
# and clamps the ring, so nothing depends on a plastic floor any more. What
# the joint must survive is the centrifugal pull of its own hardware mass,
# reacted by the bolt in tension and by bearing of the head/nut faces on the
# PET-CF.
print("\n=== Through-bolt retention load ===")
# Evaluated at the SELECTED wheel's pitch circle, not at the largest R_pcr in
# the sweep: the sweep contains rings that are not the design, and quoting a
# retention load from a ring nobody is building overstates the number by the
# ratio of the radii. Falls back to the sweep maximum only if no wheel was
# selected, where a conservative bound is the right default.
_r_max = sel['R_pcr'] if sel is not None else max(r['R_pcr'] for r in rows)
F_c = m_hardware * omega_max**2 * _r_max
_bearing_area = math.pi*((10.0e-3/2)**2 - r_hole**2)   # ~M6 head/nut face
print(f"hardware mass per station = {m_hardware*1e3:.2f} g "
      f"(bolt {m_bolt*1e3:.2f} + nut {m_nut*1e3:.2f}"
      + (f" + washer {m_washer*1e3:.2f}" if m_washer > 0 else "") + ")")
print(f"at {rpm_max} rpm and R_pcr = {_r_max*1e3:.1f} mm:")
print(f"  F = m*omega^2*R = {F_c:.0f} N  ({F_c/9.81:.1f} kgf)")
print(f"  vs M6 class 8.8 proof load ~ 12.7 kN -- the BOLT is not the "
      f"limit ({F_c/12.7e3*100:.2f}% of proof).")
print(f"  bearing stress under the head/nut face "
      f"({_bearing_area*1e6:.1f} mm^2) = {F_c/_bearing_area/1e6:.2f} MPa,")
print(f"  against PET-CF compressive strength of order 60-90 MPa -- also not "
      f"the limit.")
print("  -> the through-bolt IS the retention feature. Use a nyloc or "
      "threadlocked nut so")
print("     vibration cannot back it off; the old blind-pocket floor check is "
      "obsolete.")
print(f"  NOTE: F scales with omega^2 -- at 7327 rpm this becomes "
      f"{m_hardware*(7327*2*math.pi/60)**2*_r_max:.0f} N.")


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
    # OD = 120 mm is a FIXED CONSTRAINT (D_w_FIXED_mm), not a sweep result:
    # three orthogonal wheel modules plus the battery have to fit the
    # 150 mm cube, so the diameter is imposed and the sweep is consulted
    # only for what that diameter costs. At 120 mm the bare PET-CF ring
    # falls well short of I_w_target (0.957 vs 4.119 x1e-4), so this wheel
    # IS ballasted: 15 M6 bolt+nut stations on R_pcr = 52.5 mm bring it to
    # 111.7% of target.
    #   172.51 g = 37.51 g PET-CF (ring + 3 spokes, t = 5 mm, 15 mm width,
    #              already net of the 15 drilled holes)
    #            + 135.00 g steel (15 x 9.00 g bolt + nut)
    # Net per station is +8.79 g (9.00 g hardware - 0.21 g displaced
    # plastic), so trimming the count by 3 holes moves this by ~26.4 g.
    # Kept as a literal so this stage stays decoupled from stages 1-5;
    # update it if the wheel design changes.
    ("Reaction wheel (PET-CF, 120 mm, 15x M6)", 172.51, 3, "Wheels"),

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

CLOSURE_TOL_g = 1.0     # [g] treat |delta| under this as converged. The fixed
                        # point is only ever reached to within the rounding of
                        # the BOM literals, so an exact-zero test would flag a
                        # converged design as open on a 0.04 g residual.
if delta_g > CLOSURE_TOL_g:
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