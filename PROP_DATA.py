"""
T-MOTOR propeller bench data -- torque, speed and current.

Manufacturer test-stand data for ONE motor run with four different carbon-fibre
propellers, swept by throttle from 50% to 100%.

The single-motor point is confirmed by the user and it is what makes this data
worth more than four unrelated sweeps: the propeller is the ONLY thing that
changes between blocks, so differences across blocks are the motor's response
to load, not part-to-part variation. Every cross-propeller comparison below
depends on it. If a block ever turns out to be a different motor, the
efficiency comparison and the operating-point table stop being valid and the
data must be read row-by-row instead.

COLUMNS AS SUPPLIED (per throttle row):
    throttle [%], current [A], electrical power [W], speed [rpm],
    torque [N*m], thrust [g], efficiency [g/W]

The trailing per-propeller number in the source table (30, 37, 46, "HOT") is a
motor TEMPERATURE in degC at the end of the run, not a per-row quantity, so it
is stored once per propeller rather than in the sweep. The 16x5.4" run reports
"HOT" instead of a number -- recorded as None, since an unquantified thermal
abort is not a temperature and must not be plotted as one.

CAUTION ON THE TORQUE COLUMN: these are the values exactly as published. Torque
and electrical power are not independent -- P_elec * eta_motor = tau * omega --
so the published torque implies a motor efficiency that is worth checking
before the numbers are trusted for sizing. The script prints that check
(IMPLIED EFFICIENCY table) rather than silently assuming the data is coherent.
"""
import math

import matplotlib
matplotlib.use("Agg")           # file output only; no interactive backend needed
import matplotlib.pyplot as plt

# =================================================================
# DATA  (edit here)
# =================================================================
# Each row: (throttle_pct, current_A, power_W, rpm, torque_Nm, thrust_g, eff_g_per_W)
PROPS = [
    dict(
        name="13x4.4\" CF",
        diameter_in=13.0,
        pitch_in=4.4,
        temp_C=30,
        rows=[
            ( 50,  2.00,  48, 3719, 0.10,  544, 11.33),
            ( 55,  2.50,  60, 4528, 0.11,  656, 10.93),
            ( 60,  3.10,  74, 4840, 0.12,  753, 10.12),
            ( 65,  3.70,  89, 5155, 0.14,  853,  9.61),
            ( 75,  5.10, 122, 5451, 0.17, 1062,  8.68),
            ( 85,  6.80, 163, 6327, 0.21, 1286,  7.88),
            (100,  9.70, 233, 6515, 0.27, 1633,  7.01),
        ],
    ),
    dict(
        name="14x4.8\" CF",
        diameter_in=14.0,
        pitch_in=4.8,
        temp_C=37,
        rows=[
            ( 50,  2.40,  58, 3961, 0.12,  675, 11.72),
            ( 55,  3.20,  77, 4329, 0.14,  798, 10.39),
            ( 60,  3.80,  91, 4619, 0.16,  908,  9.96),
            ( 65,  4.70, 113, 4925, 0.18, 1033,  9.16),
            ( 75,  6.50, 156, 5485, 0.22, 1286,  8.24),
            ( 85,  8.50, 204, 6004, 0.27, 1576,  7.73),
            (100, 12.20, 293, 6731, 0.34, 1975,  6.75),
        ],
    ),
    dict(
        name="15x5\" CF",
        diameter_in=15.0,
        pitch_in=5.0,
        temp_C=46,
        rows=[
            ( 50,  3.10,  74, 3746, 0.15,  805, 10.82),
            ( 55,  4.10,  98, 4089, 0.18,  959,  9.75),
            ( 60,  4.80, 115, 4358, 0.20, 1093,  9.49),
            ( 65,  5.80, 139, 4634, 0.23, 1236,  8.88),
            ( 75,  8.30, 199, 5215, 0.29, 1561,  7.84),
            ( 85, 10.70, 257, 5627, 0.33, 1823,  7.10),
            (100, 15.00, 360, 6177, 0.40, 2228,  6.19),
        ],
    ),
    dict(
        name="16x5.4\" CF",
        diameter_in=16.0,
        pitch_in=5.4,
        temp_C=None,          # source says "HOT" -- thermally aborted, no number
        temp_note="HOT (thermal limit reached -- no figure published)",
        rows=[
            ( 50,  3.70,  89, 3495, 0.19,  928, 10.45),
            ( 55,  4.80, 115, 3817, 0.22, 1096,  9.51),
            ( 60,  5.90, 142, 4079, 0.25, 1258,  8.88),
            ( 65,  7.20, 173, 4326, 0.29, 1427,  8.26),
            ( 75, 10.00, 240, 4803, 0.34, 1740,  7.25),
            ( 85, 12.90, 310, 5119, 0.39, 1970,  6.36),
            (100, 17.50, 420, 5445, 0.45, 2309,  5.50),
        ],
    ),
]

# --- column accessors, so the tuple order is written down once ---
THROTTLE, CURRENT, POWER, RPM, TORQUE, THRUST, EFF = range(7)


def col(prop, idx):
    """Pull one column out of a propeller's sweep."""
    return [row[idx] for row in prop["rows"]]


# =================================================================
# STYLE  (ordinal blue ramp -- diameter is an ORDERED quantity)
# =================================================================
# Propeller diameter runs 13" -> 16", so this is an ordinal scale, not a set of
# unrelated identities: one hue, more-is-darker, so the ramp itself encodes
# "bigger prop" and the curves stay ordered in greyscale print.
#
# Steps are shifted one stop darker than the on-screen ramp (350/450/550/700
# rather than 250/400/500/650): the figure prints on WHITE, and the lightest
# on-screen step is too faint as a 1 pt line on paper. Monotone in lightness
# with visible separation between adjacent steps, which is what an ordinal
# ramp has to hold.
RAMP = ["#5598e7", "#2a78d6", "#1c5cab", "#0d366b"]

INK       = "#000000"      # axis text and labels -- black for print
INK_2     = "#333333"      # caption

# Reaction-wheel design speed ceiling, from electrical/MOTOR_SPEED.md. Shown
# on the TDD figure so the measured speeds read against the assumed limit.
OMEGA_MAX_RPM = 6000

# Marker shapes double the encoding, so the four curves remain separable in
# greyscale print and under colour-vision deficiency -- standard practice for
# a figure that will be photocopied or printed in a report appendix.
MARKERS = ["o", "s", "^", "D"]

# Engineering-report conventions: enclosed axes with inward ticks on all four
# sides, a light grid, and a plain sans face. This is the house style of a
# test report rather than a dashboard.
plt.rcParams.update({
    "figure.facecolor":  "white",
    "axes.facecolor":    "white",
    "savefig.facecolor": "white",
    "font.family":       "sans-serif",
    "font.sans-serif":   ["Arial", "Helvetica", "DejaVu Sans", "sans-serif"],
    "mathtext.fontset":  "dejavusans",
    "text.color":        INK,
    "axes.labelcolor":   INK,
    "xtick.color":       INK,
    "ytick.color":       INK,
    "axes.edgecolor":    "#444444",
    "axes.linewidth":    0.8,
    "grid.color":        "#cccccc",
    "font.size":         8.5,
    "axes.titlesize":    9,
    "axes.labelsize":    9,
    "legend.fontsize":   8.5,
    "xtick.labelsize":   8,
    "ytick.labelsize":   8,
})


def style_axes(ax):
    """Enclosed frame, inward minor+major ticks, light grid behind the data."""
    ax.grid(True, which="major", color="#cccccc", linewidth=0.5,
            linestyle="-", zorder=0)
    ax.grid(True, which="minor", color="#e8e8e8", linewidth=0.4,
            linestyle="-", zorder=0)
    ax.minorticks_on()
    ax.set_axisbelow(True)
    for side in ("top", "right", "left", "bottom"):
        ax.spines[side].set_visible(True)
        ax.spines[side].set_color("#444444")
        ax.spines[side].set_linewidth(0.8)
    # ticks on all four sides, pointing in -- the usual convention for
    # technical figures, and it makes values easier to read off the frame
    ax.tick_params(which="major", direction="in", length=4, width=0.7,
                   top=True, right=True)
    ax.tick_params(which="minor", direction="in", length=2, width=0.5,
                   top=True, right=True)


# =================================================================
# PLOT -- torque vs current, and rpm vs current
# =================================================================
# TWO SEPARATE AXES, NOT ONE WITH TWO Y-SCALES. Torque (~0.1-0.45 N*m) and
# speed (~3500-6700 rpm) share no scale; overlaying them on twin y-axes would
# invent a crossing point that is an artefact of where the two scales were
# pinned, not a fact about the motor.
#
# Panel (c), thrust vs current, is the one that answers "which propeller",
# and it is only meaningful because the motor is the same in all four blocks:
# with the motor held fixed, a curve sitting further left delivers the same
# thrust for less current. The caption states that; the axes do not editorialise.
PANELS = {
    "torque": (TORQUE, r"Shaft torque, $\tau$ [N$\cdot$m]", (0.05, 0.50), None),
    "speed":  (RPM,    "Rotational speed, N [rpm]",         (3000, 7000), None),
    "thrust": (THRUST, "Static thrust, T [g]",              (400, 2400),  None),
}


def build_figure(panel_keys, figsize, caption=None, mark_omega_max=False):
    """Render the sweep as one row of panels. Returns the Figure.

    panel_keys     which PANELS to draw, left to right
    caption        figure caption text, or None to let the host document
                   supply it (the LaTeX \\caption{} case)
    mark_omega_max annotate the 6000 rpm design ceiling on the speed panel
    """
    fig, axes = plt.subplots(1, len(panel_keys), figsize=figsize)
    axes = [axes] if len(panel_keys) == 1 else list(axes)

    for prop, color, mk in zip(PROPS, RAMP, MARKERS):
        I = col(prop, CURRENT)
        for ax, key in zip(axes, panel_keys):
            ax.plot(I, col(prop, PANELS[key][0]), color=color, linewidth=1.1,
                    marker=mk, markersize=3.4, markerfacecolor="white",
                    markeredgecolor=color, markeredgewidth=0.9,
                    label=prop["name"], zorder=3)

    # Panel captions in the (a)/(b)/(c) form a report cross-references.
    for i, (ax, key) in enumerate(zip(axes, panel_keys)):
        _, ylab, ylim, _ = PANELS[key]
        ax.set_xlabel("Current, I [A]")
        ax.set_ylabel(ylab)
        ax.set_title(f"({chr(97+i)})", fontsize=9, loc="left", pad=4)
        style_axes(ax)
        ax.set_xlim(0, 20)
        ax.set_xticks([0, 5, 10, 15, 20])
        ax.set_ylim(*ylim)

        if key == "speed" and mark_omega_max:
            # The design ceiling from electrical/MOTOR_SPEED.md. Drawn as a
            # reference line so the measured speeds can be read against the
            # limit the wheel sizing actually assumes.
            ax.axhline(OMEGA_MAX_RPM, color="#444444", linewidth=0.8,
                       linestyle="--", zorder=2)
            ax.text(19.4, OMEGA_MAX_RPM - 130,
                    r"design limit, 6000 rpm", fontsize=7,
                    color="#444444", ha="right", va="top")

    handles, labels = axes[0].get_legend_handles_labels()
    leg = fig.legend(handles, labels, loc="lower center", ncol=4,
                     frameon=True, fancybox=False, edgecolor="#444444",
                     framealpha=1.0, borderpad=0.5, columnspacing=1.6,
                     handlelength=2.4, bbox_to_anchor=(0.5, -0.012))
    leg.get_frame().set_linewidth(0.6)

    if caption:
        fig.text(0.5, -0.105, caption, ha="center", va="top", fontsize=7.5,
                 color=INK_2, linespacing=1.5)

    fig.tight_layout(rect=[0, 0.13, 1, 0.99])
    return fig


# --- standalone figure: all three panels, self-captioned ----------------
fig = build_figure(
    ["torque", "speed", "thrust"],
    figsize=(9.6, 3.3),
    caption=(
        "Figure 1. Measured torque, rotational speed and static thrust against "
        "motor current for four carbon-fibre propellers on a single T-MOTOR "
        "unit.\nSymbols are measured points at throttle settings of 50, 55, 60, "
        "65, 75, 85 and 100 %; lines join successive points and are not fits. "
        "Static bench\ntest data, manufacturer supplied. The 16x5.4 in. run "
        "reached the motor thermal limit at 100 % throttle."
    ),
)
fig.savefig("prop_torque_rpm_vs_current.png", dpi=300, bbox_inches="tight")
fig.savefig("prop_torque_rpm_vs_current.pdf", bbox_inches="tight")  # vector
plt.close(fig)
print("wrote prop_torque_rpm_vs_current.png / .pdf")

# --- TDD figure: motor characterisation only ----------------------------
# The thrust panel is DELIBERATELY OMITTED here. The Cubli drives reaction
# wheels, not propellers: propeller thrust is irrelevant to it, and a thrust
# curve in the TDD would invite the reader to think the vehicle flies. What
# transfers is the MOTOR characterisation -- torque and speed against current
# for the MN4006 -- which is evidence for the torque and current figures the
# document already asserts. LaTeX supplies the caption, so none is drawn.
fig = build_figure(["torque", "speed"], figsize=(6.6, 3.2),
                   mark_omega_max=True)
fig.savefig("images/mn4006_torque_speed_vs_current.pdf", bbox_inches="tight")
fig.savefig("images/mn4006_torque_speed_vs_current.png", dpi=300,
            bbox_inches="tight")
plt.close(fig)
print("wrote images/mn4006_torque_speed_vs_current.pdf / .png")


# =================================================================
# TABLE VIEW -- every plotted value, readable without the chart
# =================================================================
print("\n" + "=" * 78)
print("T-MOTOR PROPELLER BENCH DATA".center(78))
print("=" * 78)

for prop in PROPS:
    if prop["temp_C"] is None:
        temp = prop.get("temp_note", "not published")
    else:
        temp = f'{prop["temp_C"]} degC'
    print(f'\n--- {prop["name"]}   (motor temp: {temp}) ---')
    hdr = (f'{"thr %":>6} | {"I [A]":>6} | {"P [W]":>6} | {"rpm":>6} | '
           f'{"tau [N*m]":>9} | {"thrust g":>8} | {"g/W":>6}')
    print(hdr)
    print("-" * len(hdr))
    for r in prop["rows"]:
        print(f'{r[THROTTLE]:>6} | {r[CURRENT]:>6.2f} | {r[POWER]:>6} | '
              f'{r[RPM]:>6} | {r[TORQUE]:>9.2f} | {r[THRUST]:>8} | {r[EFF]:>6.2f}')


# =================================================================
# COHERENCE CHECK -- does the published torque agree with the power?
# =================================================================
# Mechanical shaft power is  P_mech = tau * omega.  Dividing by the published
# ELECTRICAL power gives the motor efficiency the table implies. A plausible
# figure for a motor of this class is roughly 70-85% at mid throttle. Values
# far outside that mean the torque column is not shaft torque as assumed --
# so this check has to be read before the torque numbers are used for sizing.
print("\n" + "=" * 78)
print("IMPLIED MOTOR EFFICIENCY  (tau*omega / P_elec)".center(78))
print("=" * 78)
print("Sanity check on the supplied torque column, NOT a measurement.")

hdr = f'{"propeller":<14} | ' + " | ".join(f'{r[0]:>4}%' for r in PROPS[0]["rows"])
print("\n" + hdr)
print("-" * len(hdr))

suspect = []
for prop in PROPS:
    cells = []
    for r in prop["rows"]:
        omega = r[RPM] * 2 * math.pi / 60.0        # rpm -> rad/s
        eta   = r[TORQUE] * omega / r[POWER]
        cells.append(eta)
        if not (0.55 <= eta <= 0.95):
            suspect.append((prop["name"], r[THROTTLE], eta))
    print(f'{prop["name"]:<14} | ' + " | ".join(f'{e*100:>4.0f}%' for e in cells))

if suspect:
    print(f'\n  !! {len(suspect)} of '
          f'{sum(len(p["rows"]) for p in PROPS)} points fall outside a '
          f'plausible 55-95% motor efficiency.')
    print("     The published torque and the published electrical power are")
    print("     therefore not mutually consistent as shaft torque. Treat the")
    print("     torque column as indicative until the source is confirmed --")
    print("     do not size a drivetrain on it without checking.")
    worst = max(suspect, key=lambda s: abs(s[2] - 0.75))
    print(f'     Worst: {worst[0]} at {worst[1]}% -> {worst[2]*100:.0f}%')
else:
    print("\n  OK: every point implies a plausible motor efficiency.")

# =================================================================
# TORQUE CONSTANT -- the figure quoted in the TDD
# =================================================================
# Torque vs current is the motor's own property, independent of what it
# drives, so ALL points from all four blocks belong to one fit.
#
# Two numbers, and the difference between them matters. The free fit's SLOPE
# is the useful torque per extra ampere. The through-origin ratio is what you
# get by dividing torque by current at a single point -- it is larger, because
# it charges the losses at the intercept to the shaft as if they produced
# torque. The document quotes the slope and says why.
def _fit_kt():
    pts = [(r[CURRENT], r[TORQUE]) for p in PROPS for r in p["rows"]]
    n   = len(pts)
    sx  = sum(x for x, _ in pts)
    sy  = sum(y for _, y in pts)
    sxx = sum(x * x for x, _ in pts)
    sxy = sum(x * y for x, y in pts)
    syy = sum(y * y for _, y in pts)
    slope = (n * sxy - sx * sy) / (n * sxx - sx * sx)
    icept = (sy - slope * sx) / n
    kt0   = sxy / sxx                       # forced through the origin
    r     = ((n * sxy - sx * sy)
             / math.sqrt((n * sxx - sx * sx) * (n * syy - sy * sy)))
    return slope, icept, kt0, r


kt_slope, kt_icept, kt_origin, kt_r = _fit_kt()

print("\n" + "=" * 78)
print("TORQUE CONSTANT  (all 28 points, all four blocks)".center(78))
print("=" * 78)
print(f"  free fit    : tau = {kt_slope:.4f}*I + {kt_icept:.4f}   (r = {kt_r:.3f})")
print(f"  through zero: tau = {kt_origin:.4f}*I")
print(f"\n  Use {kt_slope:.3f} N*m/A as the torque constant. The "
      f"{kt_icept:+.3f} N*m intercept is")
print("  magnetising/iron loss plus bearing friction -- torque paid for but not")
print(f"  delivered to the shaft. Quoting {kt_origin:.3f} N*m/A (torque over")
print("  current at a point) counts those losses as useful output.")

# --- the thermal flag, stated rather than silently dropped -------------
hot = [p["name"] for p in PROPS if p["temp_C"] is None]
if hot:
    print("\n" + "-" * 78)
    print(f'THERMAL: {", ".join(hot)} reached the motor thermal limit during the')
    print('run ("HOT" in the source, no figure given). Its 100% row is not a')
    print("continuous-duty operating point.")


# =================================================================
# CROSS-PROPELLER COMPARISON -- valid ONLY because it is one motor
# =================================================================
# Comparing propellers at equal THROTTLE is meaningless: throttle is a duty
# cycle, not an operating point, and each propeller loads the motor
# differently at the same duty. The comparison that means something is at
# equal THRUST -- the same job done -- because that is what an airframe
# actually demands. Current, torque and speed are then the PRICE each
# propeller charges the motor for that job.
#
# Thrust is monotonic in throttle in every block, so linear interpolation
# between bracketing rows is well posed. Values outside a block's measured
# thrust range are reported as "--" rather than extrapolated: a propeller
# that never reached the thrust is not a propeller with a faint guess at it.
def interp_at_thrust(prop, thrust_g, idx):
    """Linear-interpolate column `idx` at a given thrust. None if out of range."""
    rows = prop["rows"]
    lo, hi = rows[0][THRUST], rows[-1][THRUST]
    if not (lo <= thrust_g <= hi):
        return None
    for a, b in zip(rows, rows[1:]):
        if a[THRUST] <= thrust_g <= b[THRUST]:
            span = b[THRUST] - a[THRUST]
            f = 0.0 if span == 0 else (thrust_g - a[THRUST]) / span
            return a[idx] + f * (b[idx] - a[idx])
    return None


print("\n\n" + "=" * 78)
print("SAME MOTOR, DIFFERENT PROPELLER -- COST OF EQUAL THRUST".center(78))
print("=" * 78)
print("One motor throughout, so these columns are directly comparable.")
print("Compared at equal thrust, not equal throttle. '--' = outside the")
print("thrust range that propeller actually reached on the stand.")

# thrust levels common to as many blocks as possible
THRUST_LEVELS = [1000, 1250, 1500, 1750, 2000]

hdr = (f'\n{"thrust":>7} | ' +
       " | ".join(f'{p["name"].split()[0]:>17}' for p in PROPS))
print(hdr)
print(f'{"[g]":>7} | ' + " | ".join(f'{"I[A]  rpm  N*m":>17}' for _ in PROPS))
print("-" * len(hdr))

for T in THRUST_LEVELS:
    cells = []
    for prop in PROPS:
        I   = interp_at_thrust(prop, T, CURRENT)
        rpm = interp_at_thrust(prop, T, RPM)
        tau = interp_at_thrust(prop, T, TORQUE)
        if I is None:
            cells.append(f'{"--":>17}')
        else:
            cells.append(f'{I:>5.1f} {rpm:>5.0f} {tau:>5.2f}')
    print(f'{T:>7} | ' + " | ".join(cells))

# --- the headline: current drawn for the same thrust -------------------
print("\n--- Current for the same thrust (the number that sizes your ESC/pack) ---")
for T in THRUST_LEVELS:
    draws = [(p["name"], interp_at_thrust(p, T, CURRENT)) for p in PROPS]
    draws = [(n, i) for n, i in draws if i is not None]
    if len(draws) < 2:
        continue
    best  = min(draws, key=lambda d: d[1])
    worst = max(draws, key=lambda d: d[1])
    saving = (worst[1] - best[1]) / worst[1] * 100
    print(f'  {T:>4} g: cheapest {best[0]:<12} {best[1]:>5.1f} A   '
          f'vs {worst[0]:<12} {worst[1]:>5.1f} A   '
          f'-> {saving:.0f}% less current')

# --- where the "bigger is better" rule stops holding --------------------
# The usual rule of thumb is that a larger propeller is always cheaper for a
# given static thrust (more air, moved more slowly). This data only obeys
# that at LOW thrust. Rather than assert the rule, find where it breaks:
# report which diameter is actually cheapest at each thrust level.
print("\n--- Does 'bigger is always cheaper' hold here? ---")
crossover = []
for T in THRUST_LEVELS:
    draws = [(p["diameter_in"], interp_at_thrust(p, T, CURRENT)) for p in PROPS]
    draws = [(d, i) for d, i in draws if i is not None]
    if len(draws) < 2:
        continue
    best_d   = min(draws, key=lambda x: x[1])[0]
    largest_d = max(d for d, _ in draws)
    crossover.append((T, best_d, largest_d))

if all(b == l for _, b, l in crossover):
    print("  Yes -- the largest propeller available is cheapest at every level.")
else:
    print("  NO. The largest propeller is cheapest only at low thrust:")
    for T, best_d, largest_d in crossover:
        mark = "" if best_d == largest_d else "   <-- largest is NOT cheapest"
        print(f'    {T:>4} g -> cheapest is {best_d:g}"  '
              f'(largest tested here: {largest_d:g}"){mark}')
    print("\n  The 16\" wins at low thrust and then loses to the 15\". That is the")
    print("  motor, not the aerodynamics: the implied-efficiency table above")
    print("  shows the 16\" falling to 61% at full throttle while the 15\" holds")
    print("  72%. Past roughly 1500 g the 16\" is loading the motor beyond its")
    print("  efficient range, so the aerodynamic gain is eaten by motor losses --")
    print("  which is also why it is the block that ran HOT.")

print("\nRecommendation: below ~1500 g per motor the 16x5.4\" is the most")
print("efficient choice; at and above it the 15x5\" both draws less current and")
print("runs the motor in a cooler, more efficient regime. The 15x5\" is the")
print("safer default unless you are certain of staying at low thrust.")
