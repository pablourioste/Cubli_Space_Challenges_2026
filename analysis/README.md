# Analysis code

Standalone engineering calculations. Each script is self-contained, prints its
reasoning to stdout, and takes its inputs from a clearly marked block at the top
of the file — edit the numbers there, not in the logic.

Run from anywhere; output paths are resolved relative to the script, not the
working directory.

| Script | What it does | Writes |
| --- | --- | --- |
| `SIZING.py` | Reaction-wheel sizing: jump-up dynamics → required inertia, PET-CF ring + spokes + M6 steel bolt pockets, fit checks, and a Stage 6 mass budget that closes the loop on the assumed cube mass. | stdout only |
| `PROP_DATA.py` | T-MOTOR MN4006 bench data: torque / speed / thrust vs. current for four CF propellers, plus an implied-efficiency coherence check and a torque-constant fit. | `figures/`, `../images/` |

## Figure outputs

`PROP_DATA.py` writes two different figures on purpose:

- **`figures/prop_torque_rpm_vs_current.{png,pdf}`** — the full three-panel
  version including static thrust, self-captioned. This is the standalone
  reference figure; it is *not* used by the report.
- **`../images/mn4006_torque_speed_vs_current.{pdf,png}`** — the two-panel
  motor characterisation that the TDD actually includes, via
  `sections/05_hardware_design.tex`. The thrust panel is deliberately omitted
  (the Cubli drives reaction wheels, not propellers) and the caption is supplied
  by LaTeX.

**Re-running `PROP_DATA.py` regenerates a figure the report depends on.** That
is intended — it keeps the document in sync with the data — but it means the
`images/` PDF will show as modified in `git status` afterwards even if nothing
changed, because the PDF embeds a creation timestamp.

## Requirements

`PROP_DATA.py` needs `matplotlib`. `SIZING.py` is pure standard library.

```
pip install matplotlib
```

## Related

- `../electrical/` — electrical design notes and the schedule generator
  (`generate_schedule.py`, which reads `schedule.yaml`; needs `PyYAML`).
- `../images/` — figures consumed by the LaTeX report. Paths there are
  referenced directly by the `.tex` sources, so files in that folder must not
  be moved or renamed.
