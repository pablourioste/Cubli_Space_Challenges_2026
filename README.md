# Cubli — Space Challenges 2026

Reaction-wheel Cubli: a 150 mm cube that balances on an edge and a corner, and
jumps up to those poses by braking its reaction wheels.

## Layout

```
main.tex             the TDD; \input's everything in sections/
sections/            report body, one file per section
references.bib       bibliography (biblatex + biber)
images/              figures consumed by the report  <-- paths are hardcoded in .tex
analysis/            engineering calculation scripts (see analysis/README.md)
electrical/          electrical design notes + schedule generator
docs/                planning notes not part of the report
files/               spreadsheets and LaTeX integration notes
```

## Building the report

The VS Code LaTeX Workshop recipe in `.vscode/settings.json` runs
`pdflatex → biber → pdflatex → pdflatex`. It avoids `latexmk` because MiKTeX
does not ship Perl. Manually:

```
pdflatex main.tex
biber main
pdflatex main.tex
pdflatex main.tex
```

Build artifacts (`.aux`, `.bbl`, `.log`, …) are gitignored; `main.pdf` is
committed so the current report is readable without a TeX install.

## The one coupling to know about

`analysis/PROP_DATA.py` writes `images/mn4006_torque_speed_vs_current.pdf`,
which `sections/05_hardware_design.tex` includes. The figure in the report is
generated from the bench data, not drawn by hand — so if the data changes,
re-run that script and rebuild. Nothing else in `analysis/` touches the report.
