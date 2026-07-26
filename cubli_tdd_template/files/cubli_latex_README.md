# Cubli WBS + Gantt — LaTeX integration

Two ready-to-`\input` files, generated from `cubli_wbs_tasklist.xlsx`. Both were
test-compiled with `pdflatex` (TeX Live) and render correctly.

- `cubli_tasks.tex` — the full task list as `longtable`s, one subsection per workstream
  (Formulation, Control, CAD, Manufacturing, Milestones). Columns: Code, Task, Priority,
  Effort, Dates, Owner (+support), Specification, with the watch-out note under each row in red.
- `cubli_gantt.tex` — a `pgfgantt` chart, day 1 = 23 Jul, day 28 = 19 Aug, grouped and
  colour-coded by workstream with milestone diamonds. Wrapped in a `figure` with a caption
  and `\label{fig:gantt}`.

## Preamble — add these to `main.tex`

```latex
\usepackage{longtable,booktabs,array,xcolor,ragged2e}
\usepackage{pgfgantt}
\newcolumntype{L}[1]{>{\RaggedRight\arraybackslash}p{#1}}
% workstream colours (used by both files)
\definecolor{pfcol}{HTML}{70AD47}
\definecolor{ctcol}{HTML}{2E75B6}
\definecolor{cdcol}{HTML}{BF8F00}
\definecolor{mfcol}{HTML}{C55A11}
\definecolor{mscol}{HTML}{7F7F7F}
\definecolor{p0col}{HTML}{C00000}
```

The colour and `\newcolumntype` definitions are also repeated as comments at the top of each
file, so if you drop them in standalone they still tell you what they need.

## Use in the document

```latex
\section{Project Planning}
\subsection*{Work breakdown}
\input{sections/cubli_tasks.tex}

\subsection*{Schedule}
\input{sections/cubli_gantt.tex}   % floats; reference it with Figure~\ref{fig:gantt}
```

## Page-size note (the one thing likely to need a tweak)

The task tables are wide and the Gantt is very wide. On A4 portrait the Gantt figure is
`\resizebox`d to `\textwidth`, so it will fit but shrink — at 28 days it stays legible.
If it ends up too small for your taste, either:

- put just the Gantt on a landscape page: wrap the `\input` in `\begin{landscape}...\end{landscape}`
  from the `pdflscape` package, **or**
- keep the source deck A4 and let the figure scale (current behaviour).

The `longtable`s break across pages automatically and repeat their header row, so they need no
special handling in portrait.

## Regenerating (if dates or tasks change)

Both files are generated, not hand-written — edit the schedule in the spreadsheet, not here.
The generator reads `cubli_wbs_tasklist.xlsx` (sheet `WBS`, columns A–P) and rewrites both
`.tex` files. If you change a Start/Finish in the sheet, re-run the generator and both the
table dates and the Gantt bar positions move together. Day numbers in the Gantt are computed
as `Start − 23 Jul 2026 + 1`, so the project-start anchor lives in one place.

Tasks with a blank Start/Finish in the sheet (the unscheduled stretch items CT-24, CT-25)
appear in the task tables with `--` for dates and are omitted from the Gantt.
