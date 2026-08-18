"""
Cubli reaction wheel -- ring + N spokes + M6 bolts in ROUND THROUGH-HOLES.

Wheel seen from its spin axis = a DONUT (ring) held by N_spokes SPOKES.
  - Ring + spokes are PET-CF, all at one uniform thickness `t`.
  - Hub / axis structure is OMITTED (negligible inertia contribution).
  - Extra inertia comes from M6 STEEL BOLT + NUT sets fitted through
    CIRCULAR CLEARANCE HOLES drilled RADIALLY through the ring, from the
    ID to the OD. Each hole therefore does TWO things: it ADDS steel
    hardware and it REMOVES plastic.

GEOMETRY MODEL CHANGE (this revision):
  Previously the hole axis ran AXIALLY -- parallel to the spin axis,
  drilled through the wheel's FACE, positioned on a pitch circle
  somewhere between R_inner and R_outer, with hole diameter capped by the
  ring's radial width and hole depth equal to the thickness t.

  The hole is now turned 90 degrees: its axis runs RADIALLY, drilled
  through the ring's cross-section from the inner bore surface to the
  outer rim surface. Consequences, all of them physical:
    * hole DEPTH is now fixed at the ring width (R_outer - R_inner) --
      it is a true ID-to-OD through-hole, not a free choice of pitch
      radius. There is no more R_pcr to pick; the hole's centroid sits
      at R_mean = (R_inner + R_outer)/2 by construction.
    * hole DIAMETER is now capped by the wheel THICKNESS t (with an
      axial wall to the front/back faces), not by the ring width. This
      is the opposite constraint from before, and it is why the hole can
      now be as fat as t allows, at a much shorter grip length
      (~ring_width instead of ~t).
    * the OWN-AXIS inertia term changes shape. A hole/bolt whose axis is
      PARALLEL to the spin axis spins about its own long axis, so its
      own-axis term is the familiar disc value k^2 = r^2/2. A hole/bolt
      whose axis is RADIAL -- i.e. PERPENDICULAR to the spin axis -- is
      instead a rod-like cylinder rotating about a TRANSVERSE axis
      through its centroid, whose own-axis term is the standard solid
      cylinder result k^2 = r^2/4 + w^2/12 (w = its length = ring width).
      Both terms are still combined with the parallel-axis theorem using
      the perpendicular offset from the spin axis to the hole's centroid,
      which is now R_mean, not R_pcr.
    * adjacent holes are now radial SLOTS (straight sides, not points),
      and two radial lines from a common centre are closest together at
      their SMALLER radius. So the min-gap / N_max capacity check, which
      used to run at R_pcr, now runs at R_inner -- the true tightest
      point between two neighbouring holes -- instead.
    * the bolt is what retains the hardware, so no pocket floor exists
      and no floor check is needed; see the retention section for the
      new consideration this orientation raises (bolt head / nut now
      bear on the curved ID/OD surfaces, not a flat face).

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

omega_max is 5500 rpm per electrical/MOTOR_SPEED.md and the TDD, lowered
from 6000 rpm. I_w_target = h_w/omega_max, so a lower speed RAISES the
requirement and demands more ballast: 6 stations per wheel instead of 3.
Quote no margin at any other speed without re-running -- the 3-station
wheel this file previously described reached only 96.9% of target at
5000 rpm, contradicting an over-dimensioning claim made in an earlier
revision of this docstring.

M IS A FIXED POINT, NOT AN ASSUMPTION: M sets I_w_target (Stage 1), which
sets the ballast count, which sets the wheel mass, which feeds back into
M via Stage 6. The current point converges at M = 1.6638 kg with 6
stations per wheel, where Stage 6's roll-up reproduces the assumed value
to within 0.0 g.

Flow:
  STAGE 1  jump-up dynamics         -> required per-wheel inertia I_w_target
  STAGE 2  solid PET-CF ring+spokes -> baseline structural inertia & mass
  STAGE 3  radial hole + M6 hardware -> per-station dm, dI
  STAGE 4  solve N_holes            -> how many stations to hit the target
  STAGE 5  feasibility              -> axial fit (hole vs thickness), and
                                       the 2 mm edge-to-edge gap rule
                                       (checked at R_inner) that caps N at
                                       N_max
  STAGE 6  mass budget              -> closes the loop on the assumed cube mass
"""
import math

# =================================================================
# FIXED INPUT VARIABLES  (edit here)
# =================================================================
# --- cube / jump-up ---
M          = 1.6638       # [kg]   total cube mass -- CONVERGED FIXED POINT
                          #        (487.6 g structure allowance, 6 ballast
                          #        stations per wheel, 5500 rpm).
                          #        PROVISIONAL, and a CONVERGED FIXED POINT:
                          #        Stage 6 totals 1176.2 g known hardware +
                          #        487.6 g structure allowance = 1663.8 g,
                          #        reproducing this assumption to within 0.0 g.
                          #        The loop is real, not decorative: M sets
                          #        I_w_target (Stage 1), which sets the ballast
                          #        count, which sets the wheel mass, which
                          #        feeds back into M via Stage 6.
                          #        Revised from the previous 1.4654 kg /
                          #        6000 rpm / 3-station point on two changes:
                          #          - the structure allowance was raised
                          #            374.0 -> 487.6 g (the 374 g figure was
                          #            optimistic against the frame and
                          #            subframe now in CAD);
                          #          - the electronics estimate was raised
                          #            74.2 -> 95.2 g on as-weighed figures
                          #            (Teensy with headers, MA600 breakout
                          #            plus its steel-backed ring magnet, and
                          #            the ESP32 antenna and pigtail).
                          #        omega_max was then dropped 6000 -> 5500 rpm.
                          #        Because the station count rounds to
                          #        multiples of 3, that lands the design on
                          #        the N=6 step, which carries MORE inertia
                          #        margin (106.2%) than the N=3 step did at
                          #        6000 rpm (103.8%), at a cost of +63.8 g of
                          #        cube mass. The N=6 step holds across a
                          #        200.8 g band of structure allowance
                          #        (364.1 - 564.9 g), against roughly 46 g of
                          #        headroom at the old point -- so this design
                          #        point absorbs a CAD overrun that the
                          #        previous one did not.
                          #        ~29% is still allowance -- revisit at CAD.
L          = 0.149         # [m]    cube edge length
g          = 9.81         # [m/s^2]
eta        = 1.05         # [-]    energy margin (1.02-1.05 recommended)
tau_b      = 5.0          # [N*m]  brake torque per wheel
rpm_max    = 5500         # [rpm]  max wheel speed -- DESIGN VALUE, matches the
                          #        TDD (tab:jumpup_budget and the dashed ceiling
                          #        on the motor curve) and electrical/MOTOR_SPEED.md.
                          #        Lowered from 6000 rpm. Since
                          #        I_w_target = h_w/omega_max, a lower speed
                          #        RAISES the inertia requirement and so demands
                          #        more ballast -- here 6 stations per wheel
                          #        instead of 3, +63.8 g of cube mass, in
                          #        exchange for 500 rpm of relief on the drive
                          #        and a wider tolerance band on the structure
                          #        allowance (see the note on M above).
                          #        NOTE: an earlier revision of this file
                          #        claimed the design had been checked at
                          #        5000 rpm as an over-dimensioning case. That
                          #        claim did not survive the reduction to 3
                          #        stations: the 3-station wheel closes at 6000
                          #        but reaches only 96.9% of target at 5000. The
                          #        6-station wheel set here closes at 5500 with
                          #        106.2%. Re-run before quoting any margin at a
                          #        speed other than the one set here.
case       = "corner"     # "edge" or "corner" -- corner sizes the design

# --- wheel geometry ---
# Named R_outer / R_inner / thickness below as well, after unit conversion,
# so the geometry functions read the way the drawing does.
ring_width_mm = 10.0      # [mm]  ring radial width (R_outer - R_inner), FIXED.
                          #       This is now also the HOLE DEPTH: each M6
                          #       station is a true ID-to-OD through-hole, so
                          #       its length is exactly the ring width, not a
                          #       free choice.
spoke_w_mm    = 10.0      # [mm]  spoke width
N_spokes      = 3         # [-]   number of spokes
t_mm          = 20       # [mm]  UNIFORM thickness of ring + spokes. With
                          #       radial holes this is now what caps the HOLE
                          #       DIAMETER (with an axial wall to the front
                          #       and back faces), the opposite role it had
                          #       when holes were axial. 20 mm keeps the wheel
                          #       axially thin so three orthogonal modules
                          #       clear each other inside the 150 mm cube.

# --- hole pattern: ROUND M6 CLEARANCE THROUGH-HOLES, RADIAL ORIENTATION ---
hole_diameter_mm = 6.4    # [mm]  DRILLED hole diameter, through the full
                          #       ring width (ID to OD). 6.4 mm = ISO 273
                          #       "medium" clearance for M6.
                          #       (close fit 6.4 is standard; free fit 7.0.)
                          #       This is the hole, not the thread: the bolt
                          #       shank is 6.0 mm, so there is 0.4 mm total
                          #       diametral slop for assembly.
hole_axial_center_mm = None  # [mm] axial position of the hole centreline
                          #       within the thickness t, measured from one
                          #       face. None -> centred at t/2, which is both
                          #       the inertia-neutral choice (I_zz about the
                          #       spin axis does not depend on this anyway --
                          #       see STAGE 3) and the one that maximises the
                          #       axial wall on both faces. Set a number to
                          #       force it off-centre; the axial-fit check
                          #       below still polices it.
num_holes     = None      # [-]   FORCED number of holes. None -> the script
                          #       solves for the count that meets I_w_target
                          #       and then caps it at N_max. Set an integer to
                          #       impose a count; it is still gap-checked and
                          #       still capped, with a warning if it was cut.
min_gap_mm    = 2.0       # [mm]  MINIMUM edge-to-edge separation between two
                          #       adjacent radial holes, measured on the
                          #       straight chord between their centrelines AT
                          #       R_inner -- two radial lines from a common
                          #       centre are closest together at the smaller
                          #       radius, so that is the tightest point and
                          #       the one that sets N_max (see the derivation
                          #       in the docstring of max_holes_for_gap()).
min_wall_mm   = 2.0       # [mm]  minimum AXIAL plastic wall between a hole
                          #       edge and the wheel's front / back face
N_round_to    = 3         # [-]   round the solved hole count up to a multiple
                          #       of this (3 keeps 3-fold symmetry with the
                          #       3 spokes, so balance is unaffected)

# --- M6 hardware seated in each hole (bolt + nut) ---
# Both masses are per-item and are the things to put on a scale. They enter
# as POSITIVE mass; nothing about the hardware is modelled as a negative.
mass_m6_bolt_g = 5.0      # [g]   ONE M6 bolt, head + shank, of the length
                          #       actually used. Strongly length-dependent:
                          #       ISO 4762 M6x16 hex-socket cap is ~5.0 g.
                          #       The radial hole is now only ring_width_mm
                          #       (10 mm) deep instead of t_mm, so the grip
                          #       length is much shorter than the old axial
                          #       hole -- M6x16 through a 10 mm ring plus nut
                          #       is the stand-in. MEASURE the real one.
mass_m6_nut_g  = 2.5      # [g]   ONE M6 hex nut, MEASURED (ISO 4032 geometry
                          #       predicts 2.617 g, so 2.5 g is within normal
                          #       tolerance -- see electrical/WHEEL_130_M6.md).
mass_m6_washer_g = 0.0    # [g]   per-hole washer allowance, 0 if none used.
                          #       An M6 plain washer is ~0.9 g; two of them is
                          #       1.8 g per station, which is not nothing at
                          #       this radius.

# Radius of gyration of the hardware about its OWN axis (transverse, since
# the hole/bolt now runs radially -- perpendicular to the spin axis). A
# bolt+nut stack spanning ~10 mm of ring width sitting at R_mean ~ 55-65 mm
# has an own-axis term that is a few percent of its parallel-axis term.
# Modelled as a solid cylinder of diameter hole_diameter and length
# ring_width (k^2 = r^2/4 + ring_width^2/12), which slightly OVER-states it
# -- the conservative direction, since this term adds inertia.
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
# GEOMETRY HELPERS -- axial centring, axial fit, 2 mm gap capacity
# =================================================================
def axial_center_for(t):
    """Axial position [m] of the hole centreline within the thickness t.

    hole_axial_center_mm is honoured if the user set it; otherwise the
    hole is centred at t/2, which maximises the axial wall on both faces
    simultaneously. Unlike the old R_pcr choice, this position has NO
    effect on I_zz about the spin axis (see STAGE 3) -- it only matters
    for the axial-fit / wall check below.
    """
    if hole_axial_center_mm is not None:
        return hole_axial_center_mm * 1e-3
    return 0.5 * t


def check_axial_fit(t, z_center, r_hole):
    """Enforce  r_hole < z_center < t - r_hole,  with walls.

    Returns (ok, wall_front_mm, wall_back_mm, messages). Mirrors the old
    radial-fit check, but across the wheel's thickness instead of the
    ring's radial width, since the hole diameter is now capped by t
    rather than by the ring width.
    """
    wall_front = z_center - r_hole             # plastic to the near face
    wall_back  = (t - z_center) - r_hole        # plastic to the far face
    msgs = []
    ok = True
    if wall_front <= 0:
        ok = False
        msgs.append(f"hole breaks through the near face "
                    f"(front wall {wall_front*1e3:+.2f} mm)")
    elif wall_front < min_wall_mm*1e-3:
        ok = False
        msgs.append(f"front wall {wall_front*1e3:.2f} mm < "
                    f"{min_wall_mm:.1f} mm minimum")
    if wall_back <= 0:
        ok = False
        msgs.append(f"hole breaks through the far face "
                    f"(back wall {wall_back*1e3:+.2f} mm)")
    elif wall_back < min_wall_mm*1e-3:
        ok = False
        msgs.append(f"back wall {wall_back*1e3:.2f} mm < "
                    f"{min_wall_mm:.1f} mm minimum")
    return ok, wall_front*1e3, wall_back*1e3, msgs


def edge_gap(N, R_check, r_hole):
    """Edge-to-edge gap [m] between two adjacent radial holes of N stations.

    Each hole is now a radial SLOT running from R_inner to R_outer, not a
    point. Two radial lines from a common centre, Delta_theta = 2*pi/N
    apart, are closest together at their SMALLER radius (the chord
    2*R*sin(Delta_theta/2) grows with R), so the tightest point between
    two neighbouring holes is at R_check = R_inner, not at the pattern's
    mean radius. Passing R_inner here is what makes this the correct,
    conservative check for the radial-hole geometry; the chord formula
    itself is unchanged from the point-hole case:

        gap = 2*R_check*sin(pi/N) - 2*r_hole

    The chord is used, not the arc length 2*pi*R_check/N: the arc
    OVER-estimates spacing (arc >= chord always), so sizing on the arc
    would report a gap the part does not have.
    """
    if N < 2:
        return math.inf
    return 2.0*R_check*math.sin(math.pi/N) - 2.0*r_hole


def max_holes_for_gap(R_check, r_hole, gap_min):
    """Largest N whose adjacent-hole edge gap is still >= gap_min.

    Invert  2*R_check*sin(pi/N) - 2*r_hole >= gap_min:

        sin(pi/N) >= (r_hole + gap_min/2) / R_check  ==  s
        pi/N      >= asin(s)                    (both in (0, pi/2])
        N         <= pi / asin(s)

    so N_max = floor(pi / asin(s)). If s >= 1 not even two holes fit and
    N_max = 0. Monotonicity check: sin(pi/N) decreases as N grows, so the
    constraint is a genuine upper bound on N -- there is no second branch.
    R_check is R_inner for the radial-hole geometry (see edge_gap()).
    """
    s = (r_hole + 0.5*gap_min) / R_check
    if s >= 1.0:
        return 0
    n_max = int(math.floor(math.pi / math.asin(s)))
    return max(n_max, 0)

# =================================================================
# STAGE 3 -- RADIAL THROUGH-HOLE + M6 BOLT/NUT HARDWARE (per station)
# =================================================================
# The hole is a CYLINDER through the full ring width, axis RADIAL (i.e.
# PERPENDICULAR to the spin axis):
#     V   = pi * r_hole^2 * ring_width           (depth is now the ring
#                                                 width, not t)
#     m   = rho_petcf * V                       (mass removed, positive number,
#                                                subtracted where it is used)
# Its own-axis term about the SPIN axis is therefore NOT the disc value
# r^2/2 (that is for an axis parallel to the cylinder's own length). The
# spin axis is PERPENDICULAR to the hole's axis, so this is the standard
# solid-cylinder transverse moment about a diameter through its centroid:
#     k^2 = r_hole^2/4 + ring_width^2/12
# (r_hole^2/4 from the circular cross-section, ring_width^2/12 from the
# cylinder acting like a rod of length ring_width). This combines with
# the parallel-axis offset R_mean = (R_inner+R_outer)/2 in STAGE 4+5 to
# give the exact I_zz of a straight radial cylinder about the spin axis.
# The hardware is bolt + nut + optional washers, entering as POSITIVE mass.
r_hole = hole_diameter_mm/2 * 1e-3

if hole_diameter_mm >= t_mm:
    raise ValueError(
        f"hole diameter {hole_diameter_mm:.2f} mm does not fit in the wheel "
        f"thickness t = {t_mm:.2f} mm.")
if hole_diameter_mm + 2*min_wall_mm > t_mm:
    print(f"!! WARNING: a {hole_diameter_mm:.2f} mm hole plus "
          f"2 x {min_wall_mm:.1f} mm wall needs "
          f"{hole_diameter_mm + 2*min_wall_mm:.2f} mm of thickness, "
          f"but the wheel is only {t_mm:.2f} mm thick.\n"
          f"   No axial position can satisfy the wall rule.")

# --- plastic removed per hole: full-width cylinder, axis radial ---
V_hole     = math.pi * r_hole**2 * ring_width
m_removed  = rho_petcf * V_hole
I0_removed = m_removed * (r_hole**2/4 + ring_width**2/12)   # own-axis, transverse

# --- steel hardware added per hole: bolt + nut (+ washers) ---
m_bolt     = mass_m6_bolt_g   * 1e-3
m_nut      = mass_m6_nut_g    * 1e-3
m_washer   = mass_m6_washer_g * 1e-3
m_hardware = m_bolt + m_nut + m_washer
if m_hardware <= 0:
    raise ValueError("M6 hardware mass is zero or negative -- set "
                     "mass_m6_bolt_g / mass_m6_nut_g.")

if hardware_own_axis_model == "cylinder":
    k2_hardware = r_hole**2/4 + ring_width**2/12   # fills the hole envelope,
                                                    # same transverse model
elif hardware_own_axis_model == "point":
    k2_hardware = 0.0
else:
    raise ValueError("hardware_own_axis_model must be 'cylinder' or 'point'")
I0_hardware = m_hardware * k2_hardware

print("=== STAGE 3: radial M6 through-hole + bolt/nut (per station) ===")
print(f"hole: d = {hole_diameter_mm:.2f} mm (M6 clearance), "
      f"r = {r_hole*1e3:.2f} mm, THROUGH ring width = {ring_width_mm:.1f} mm")
print(f"  hole area         = {math.pi*r_hole**2*1e6:8.2f} mm^2")
print(f"  hole volume       = {V_hole*1e9:8.2f} mm^3")
print(f"  PLASTIC REMOVED   = {m_removed*1e3:8.3f} g   (rho = {rho_petcf:.0f} kg/m^3)")
print(f"  removed I0        = {I0_removed*1e7:8.4f} x1e-7 kg*m^2  (own axis, transverse)")
print(f"hardware per hole (POSITIVE mass added back):")
print(f"  M6 bolt           = {m_bolt*1e3:8.3f} g")
print(f"  M6 nut            = {m_nut*1e3:8.3f} g")
if m_washer > 0:
    print(f"  washer(s)         = {m_washer*1e3:8.3f} g")
print(f"  ** m_hardware     = {m_hardware*1e3:8.3f} g **")
print(f"  hardware k^2      = {k2_hardware*1e6:8.4f} mm^2 "
      f"({hardware_own_axis_model} model)")
print(f"  hardware I0       = {I0_hardware*1e7:8.4f} x1e-7 kg*m^2  (own axis, transverse)")
print(f"NET mass per station = {(m_hardware - m_removed)*1e3:+8.3f} g "
      f"(steel gained - plastic lost)\n")

# =================================================================
# STAGE 4+5 -- SOLVE N_holes PER OD, THEN CHECK IT FITS
# =================================================================
def wheel_properties(OD_mm, N_forced=None):
    """Full mass / I_zz model of one wheel at a given ring OD.

    Returns a dict. Each hole is now a radial cylinder spanning the full
    ring width, so its centroid radius is FORCED to R_mean =
    (R_inner+R_outer)/2 -- there is no free pitch-circle choice any more.
    The inertia bookkeeping is, for N holes:

        I_zz = I_ring + I_spokes
               - N * (I0_hole     + m_removed  * R_mean^2)    <- plastic gone
               + N * (I0_hardware + m_hardware * R_mean^2)    <- steel added

    Both correction terms use the Parallel Axis Theorem about the SPIN
    axis, with I0_hole / I0_hardware the TRANSVERSE own-axis term derived
    in STAGE 3 (r_hole^2/4 + ring_width^2/12), because the hole's own
    axis is radial -- perpendicular to the spin axis, not parallel to it.

    The gap / N_max capacity check, by contrast, is NOT evaluated at
    R_mean: two adjacent radial slots are closest together at their
    SMALLER radius, so that check runs at R_inner (see edge_gap()).
    """
    m_ring, I_ring, R_inner, R_outer = ring_props(OD_mm)
    m_spk,  I_spk = spokes_props(R_inner)
    m_solid = m_ring + m_spk
    I_solid = I_ring + I_spk

    R_mean = 0.5 * (R_inner + R_outer)         # forced hole centroid radius
    z_center = axial_center_for(thickness)
    axial_ok, wall_front, wall_back, axial_msgs = check_axial_fit(
        thickness, z_center, r_hole)

    # per-station contributions about the SPIN axis (parallel axis theorem)
    I_removed_at_r  = I0_removed  + m_removed  * R_mean**2
    I_hardware_at_r = I0_hardware + m_hardware * R_mean**2
    dI = I_hardware_at_r - I_removed_at_r      # net inertia gain per station
    dm = m_hardware - m_removed                # net mass gain per station

    # gap / capacity check uses R_inner -- the tightest point between
    # two adjacent radial slots, not R_mean
    N_max = max_holes_for_gap(R_inner, r_hole, min_gap_mm*1e-3)

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

    gap = edge_gap(N, R_inner, r_hole) if N >= 2 else math.inf

    return dict(
        OD=OD_mm, R_inner=R_inner, R_outer=R_outer, R_mean=R_mean,
        m_solid=m_solid, I_solid=I_solid,
        N=N, N_exact=N_exact, N_max=N_max, capped=capped, note=note,
        m_plastic=m_plastic, m_steel=m_steel, m_wheel=m_wheel,
        I_plastic=I_plastic, I_steel=I_steel, I_wheel=I_wheel,
        dI=dI, dm=dm, gap=gap,
        axial_ok=axial_ok, wall_front=wall_front, wall_back=wall_back,
        axial_msgs=axial_msgs,
        meets_target=(I_wheel >= I_w_target),
    )


print("=== STAGE 4+5: solve number of M6 through-holes per ring OD ===")
print(f"fixed: ring_width={ring_width_mm:.1f} mm  spoke_w={spoke_w_mm:.1f} mm  "
      f"N_spokes={N_spokes}  t={t_mm:.1f} mm")
print(f"       hole d={hole_diameter_mm:.2f} mm through  "
      f"min_gap={min_gap_mm:.1f} mm  min_wall={min_wall_mm:.1f} mm  "
      f"N rounded to multiple of {N_round_to}")
print("       R_mean = (R_inner+R_outer)/2, forced by the ID-to-OD hole  |  "
      "hole axial position = " +
      ("centred in t" if hole_axial_center_mm is None
       else f"{hole_axial_center_mm:.2f} mm (forced)"))

hdr = (f"\n{'OD':>5} | {'ID':>5} | {'R_mean':>6} | {'solid I':>8} | {'N':>4} | "
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
    if not r['axial_ok']:
        flags.append("AXIAL: " + "; ".join(r['axial_msgs']))
    if not r['meets_target']:
        flags.append(f"SHORT of target "
                     f"({r['I_wheel']/I_w_target*100:.1f}%)")
    flag = ("  <-- " + " | ".join(flags)) if flags else ""

    print(f"{r['OD']:>5} | {(r['R_inner']*2e3):>5.0f} | {r['R_mean']*1e3:>6.1f} | "
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
viable = [r for r in rows if r['meets_target'] and r['axial_ok']]
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
    print("!! No OD in the sweep passes all of {target, gap rule, axial wall}.")
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
          f"on R_mean = {sel['R_mean']*1e3:.2f} mm (radial hole centroid)")
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
        print(f"chord at R_inner       = "
              f"{2*sel['R_inner']*math.sin(math.pi/sel['N'])*1e3:.2f} mm "
              f"(tightest point between two adjacent radial slots)")
    else:
        print(f"edge-to-edge gap      = n/a ({sel['N']} hole(s)); "
              f"the gap rule would allow up to {sel['N_max']}")
    print(f"axial wall front/back = {sel['wall_front']:.2f} / "
          f"{sel['wall_back']:.2f} mm   (minimum {min_wall_mm:.1f} mm) "
          f"[{'OK' if sel['axial_ok'] else 'FAIL'}]")
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
          f"(gap checked at R_inner = {sel['R_inner']*1e3:.2f} mm) ===")
    print(f"{'N':>5} | {'chord mm':>9} | {'gap mm':>8} | {'verdict':<22} | "
          f"{'+mass g':>8} | {'+I 1e-4':>8}")
    print("-"*76)
    _N_probe = sorted({3, 6, 12, sel['N_max'], sel['N_max']+1,
                       sel['N_max']+3} - {0, 1, 2})
    for N in _N_probe:
        chord = 2*sel['R_inner']*math.sin(math.pi/N)
        gap   = edge_gap(N, sel['R_inner'], r_hole)
        ok    = gap >= min_gap_mm*1e-3
        verdict = "OK" if ok else f"VIOLATES {min_gap_mm:.1f} mm min"
        if N > sel['N_max']:
            verdict += " (> N_max)"
        d_mass = N * (m_hardware - m_removed)
        d_I    = N * ((I0_hardware + m_hardware*sel['R_mean']**2)
                      - (I0_removed + m_removed*sel['R_mean']**2))
        print(f"{N:>5d} | {chord*1e3:>9.2f} | {gap*1e3:>8.2f} | {verdict:<22} | "
              f"{d_mass*1e3:>+8.2f} | {d_I*1e4:>+8.4f}")
    print(f"N_max = {sel['N_max']} is the largest count with gap >= "
          f"{min_gap_mm:.1f} mm; the solver caps any request above it.")
    print("(chord/gap use R_inner, the tightest point between adjacent "
          "radial slots; +I uses R_mean, the hole's actual centroid radius.)")

# =================================================================
# AXIAL FIT CHECK (independent of OD -- a round hole has no orientation)
# =================================================================
print("\n=== Axial fit of the M6 hole inside the wheel thickness ===")
print(f"hole diameter      = {hole_diameter_mm:.2f} mm")
print(f"wheel thickness    = {t_mm:.2f} mm")
print(f"thickness needed   = {hole_diameter_mm + 2*min_wall_mm:.2f} mm  "
      f"(hole + 2 x {min_wall_mm:.1f} mm wall)")
_slack = t_mm - hole_diameter_mm - 2*min_wall_mm
print(f"slack              = {_slack:+.2f} mm  "
      f"[{'OK' if _slack >= 0 else 'TOO NARROW'}]")
print("A round hole is rotationally symmetric, so there is a single axial")
print("case -- the two hexagon orientations the old pocket model had to check")
print("separately don't exist here either.")
if hole_axial_center_mm is None:
    print(f"With the hole centred in t, the wall is "
          f"{_slack/2 + min_wall_mm:.2f} mm on each face, the maximum "
          f"available.")

# =================================================================
# GAP-RULE CAPACITY TABLE  (N_max vs OD)
# =================================================================
print(f"\n=== Hole capacity from the {min_gap_mm:.1f} mm edge-gap rule ===")
print("N_max = floor(pi / asin((r_hole + gap_min/2) / R_inner))")
print(f"\n{'OD':>5} | {'R_inner':>7} | {'N_max':>5} | {'gap at N_max':>12} | "
      f"{'N used':>6} | {'gap at N used':>13}")
print("-"*66)
for r in rows:
    g_max = edge_gap(r['N_max'], r['R_inner'], r_hole) if r['N_max'] >= 2 else math.inf
    g_use = r['gap']
    f_max = "     inf" if math.isinf(g_max) else f"{g_max*1e3:8.2f}"
    f_use = "      inf" if math.isinf(g_use) else f"{g_use*1e3:9.2f}"
    print(f"{r['OD']:>5} | {r['R_inner']*1e3:>7.2f} | {r['N_max']:>5d} | "
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
# Evaluated at the SELECTED wheel's R_mean (the hardware's actual centroid
# radius now that the hole spans the full ring width), not at the largest
# R_mean in the sweep: the sweep contains rings that are not the design, and
# quoting a retention load from a ring nobody is building overstates the
# number by the ratio of the radii. Falls back to the sweep maximum only if
# no wheel was selected, where a conservative bound is the right default.
_r_max = sel['R_mean'] if sel is not None else max(r['R_mean'] for r in rows)
F_c = m_hardware * omega_max**2 * _r_max
_bearing_area = math.pi*((10.0e-3/2)**2 - r_hole**2)   # ~M6 head/nut face
print(f"hardware mass per station = {m_hardware*1e3:.2f} g "
      f"(bolt {m_bolt*1e3:.2f} + nut {m_nut*1e3:.2f}"
      + (f" + washer {m_washer*1e3:.2f}" if m_washer > 0 else "") + ")")
print(f"at {rpm_max} rpm and R_mean = {_r_max*1e3:.1f} mm:")
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
print("  NOTE: with the hole now radial, the bolt head bears on the curved")
print("     ID surface and the nut on the curved OD surface, not on a flat")
print("     face as before. Spot-face both ends flat (or use a curved/")
print("     spherical washer) so the head and nut seat squarely -- a washer")
print("     resting on an unmachined curved surface bears on its edge, not")
print("     its face, and the bearing-area figure above assumes a flat seat.")


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
    # falls short of I_w_target (3.0450 vs 4.0813 x1e-4), so this wheel IS
    # ballasted: 6 RADIAL M6 bolt+nut stations (ID-to-OD through-holes, one
    # per station, on R_mean = 55.0 mm) bring it to 4.3356e-4, i.e. 106.2%
    # of target at 5500 rpm.
    #   170.37 g = 125.37 g PET-CF (ring + 3 spokes, t = 20 mm, 10 mm width,
    #              already net of the 6 drilled holes)
    #            + 45.00 g steel (6 x 7.50 g bolt + nut)
    # Net per station is +7.085 g (7.50 g hardware - 0.415 g displaced
    # plastic). 18 bolts and 18 nuts on the cube. Kept as a literal so this
    # stage stays decoupled from stages 1-5; update it if the wheel changes.
    ("Reaction wheel (PET-CF, 120 mm, 6x M6 radial)", 170.37, 3, "Wheels"),

    # --- power -----------------------------------------------------
    ("Tattu R-Line V5.0 6S 1550 mAh LiPo, 22.2 V", 254.0, 1, "Power"),
    ("XT60 connector pair",                15.0,  1, "Power"),
    ("LM2596 step-down regulator",         10.0,  1, "Power"),

    # --- control & sensing -----------------------------------------
    # Revised upward from the first-pass estimate (74.2 -> 95.2 g total) on
    # as-weighed rather than bare-board figures: the Teensy carries headers,
    # the MA600 breakout is quoted with its steel-backed ring magnet, and the
    # ESP32 figure now includes the antenna and its pigtail.
    ("mjbots moteus-n1 driver",            14.6,  3, "Electronics"),
    ("mjbots MA600 breakout + magnet",      6.0,  3, "Electronics"),
    ("Teensy 4.1",                         11.0,  1, "Electronics"),
    ("CAN-FD adapter for Teensy 4.1",       6.0,  1, "Electronics"),
    ("mjcanfd-usb-1x",                      3.4,  1, "Electronics"),
    ("Seeed XIAO ESP32-C6 + antenna",       8.0,  1, "Electronics"),
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
# Raised 374.0 -> 487.6 g total, holding the same relative split, after the
# 374 g figure proved optimistic against the frame and subframe now in CAD.
ALLOWANCE_g = {
    "Inner structure / motor subframe": 199.5,
    "Outer frame / contact features":   239.9,
    "Fasteners / wiring harness":        48.2,
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