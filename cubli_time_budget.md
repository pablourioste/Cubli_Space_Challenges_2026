# Cubli — Time Budget and Block Fragmentation Model

Companion to [`SCHEDULE.md`](SCHEDULE.md). This file holds the calendar
arithmetic; `SCHEDULE.md` holds the day-by-day assignments.

Window: **30 July – 20 August 2026**, 22 calendar days, 21 working days
(13 Aug is zero-work).

Every number below is tagged **[given]** (supplied as a hard calendar fact) or
**[derived]** (allocated to satisfy the given constraints). Derived figures are
proposals — change them and the schedule follows.

---

## 1. Baseline envelope

| Segment | Hours | Source |
|---|---|---|
| Pre-trip (30 Jul – 11 Aug) | 88.0 | **[given]** |
| 12 Aug (half day, work stops 13:00) | 3.0 | **[given]** |
| 13 Aug (field trip) | 0.0 | **[given]** |
| Post-trip (14 Aug – 20 Aug) | 46.5 | **[given]** |
| **Total** | **137.5** | **[given]** — sum verified |

## 2. Block-fragmentation classes

Three day classes drive what work is *permissible*, independent of how many
hours the day holds. A task that needs an uninterrupted bench session cannot be
split across two 1.0 h fragments without paying setup/teardown twice.

| Class | Rule | Days |
|---|---|---|
| **HIGH-CONTIGUITY** | Major hardware repetitions, E2/E3 assembly, wheel balancing | Sat 1 Aug, Sat 8 Aug **[given]** |
| **FRAGMENTED** | **NO bench or lab assembly.** Documentation, TDD writing, CAD review, pitch scripting only | Mon 3 Aug, Tue 4 Aug, Fri 7 Aug **[given]** |
| **STANDARD** | Bench work permitted; blocks long enough for a single assembly step | all remaining working days **[derived]** |
| **BLACKOUT** | Zero project work | 12 Aug from 13:00, all 13 Aug, 14 Aug to post-lunch **[given]** |
| **REST** | No hours allocated | Sun 2, 9, 16 Aug **[derived]** |

## 3. Day-by-day allocation

`Hours` = person-hours available that day across the whole team.
`Max block` = longest uninterrupted stretch any one person gets.

### Pre-trip — 88.0 h target

| Date | Day | Hours | Max block | Class | Basis |
|---|---|---|---|---|---|
| 30 Jul | Thu | 8.0 | 3.0 | STANDARD | derived |
| 31 Jul | Fri | 9.0 | 4.0 | STANDARD | derived — critical target day |
| 1 Aug | Sat | 12.0 | 6.0 | HIGH-CONTIGUITY | **given** |
| 2 Aug | Sun | 0.0 | — | REST | derived |
| 3 Aug | Mon | 3.0 | 1.5 | FRAGMENTED | **given** — Preliminary TDD due |
| 4 Aug | Tue | 2.5 | 1.0 | FRAGMENTED | **given** |
| 5 Aug | Wed | 8.0 | 3.0 | STANDARD | derived |
| 6 Aug | Thu | 8.0 | 3.5 | STANDARD | derived |
| 7 Aug | Fri | 3.0 | 1.5 | FRAGMENTED | **given** |
| 8 Aug | Sat | 12.0 | 6.0 | HIGH-CONTIGUITY | **given** |
| 9 Aug | Sun | 0.0 | — | REST | derived |
| 10 Aug | Mon | 8.0 | 3.5 | STANDARD | derived |
| 11 Aug | Tue | 14.5 | 5.0 | STANDARD — **S3 GO/NO-GO EOD** | derived — deliberately loaded |
| **Subtotal** | | **88.0** | | | matches given |

### Trip boundary

| Date | Day | Hours | Max block | Class | Basis |
|---|---|---|---|---|---|
| 12 Aug | Wed | 3.0 | 3.0 | STANDARD until 13:00 | **given** |
| 13 Aug | Thu | 0.0 | — | BLACKOUT | **given** |
| **Subtotal** | | **3.0** | | | matches given |

### Post-trip — 46.5 h target

| Date | Day | Hours | Max block | Class | Basis |
|---|---|---|---|---|---|
| 14 Aug | Fri | 4.5 | 3.0 | STANDARD, post-lunch start | derived |
| 15 Aug | Sat | 10.0 | 5.0 | STANDARD | derived |
| 16 Aug | Sun | 0.0 | — | REST | derived |
| 17 Aug | Mon | 8.0 | 3.5 | STANDARD | derived |
| 18 Aug | Tue | 8.0 | 3.0 | STANDARD — rehearsal 1 | derived |
| 19 Aug | Wed | 8.0 | 3.0 | STANDARD — dress rehearsal | derived |
| 20 Aug | Thu | 8.0 | 4.0 | PRESENTATION | derived |
| **Subtotal** | | **46.5** | | | matches given |

**Grand total: 137.5 h.**

## 4. Consequences of the fragmentation rules

Four scheduling facts fall directly out of the constraints above. They are not
preferences.

**4.1 — 3–4 Aug and 7 Aug remove 8.5 h of bench capacity.**
Those three days hold 8.5 h, but none of it can touch the bench. Any hardware
task that would naturally have landed there must move to 1 Aug, 5–6 Aug or
8 Aug. This is why the two Saturdays carry the assembly load.

**4.2 — The two Saturdays are the only 6.0 h blocks in the project.**
Wheel balancing, three-axis assembly and the 48 A first-battery power-on each
need one long uninterrupted session. There are exactly two such sessions
available, on 1 Aug and 8 Aug. Losing either has no in-window recovery.

**4.3 — Moving S3 Go/No-Go to 11 Aug EOD compresses, it does not shift.**
The gate was 13 Aug, which is now zero-work. Pulling it to 11 Aug removes
2 days of integration and debug from the pre-gate run. 11 Aug is loaded to
14.5 h to partly absorb this; the remainder is paid for in scope, per §4.4.

**4.4 — The brake / jump-up chain is the sacrificial item.**
This is the standing decision already recorded in `electrical/schedule.yaml`
(issue I-4) and it is unchanged here: brake work yields to balance work without
discussion on the day. Post-trip, 14–17 Aug is the only window for both
jump-up work and pitch preparation, and pitch preparation has a fixed external
date on 20 Aug. If they collide, the jump-up is cut.

## 5. Sequencing constraint on Nasia

Nasia's 3D CAD, frame and enclosure work is **strictly downstream** of Andrea
and Deyan's sizing and inertia outputs. Frame geometry cannot be frozen ahead
of the inertia tensor and mass budget. The schedule therefore orders:

```
Andrea & Deyan: sizing + inertia + control budget
        |
        v
Nasia: frame geometry -> enclosure -> print-ready package
        |
        v
Suvanna: mechanical testbench + 1-DoF verification
```

A slip in the sizing chain propagates to Nasia the same day. Nasia's fallback,
on any day the upstream numbers are late, is CAD review and tolerance work on
already-frozen geometry — never speculative re-modelling against unconfirmed
numbers.

## 6. Open items that affect this budget

Carried from `electrical/schedule.yaml`; unresolved at time of writing.

| # | Item | Affects |
|---|---|---|
| Q-2 | Does a 470–1000 µF ≥50 V bulk capacitor exist / is it ordered? | First battery power-on, 8 Aug |
| Q-8 | Design wheel speed — 733 rad/s or 628 rad/s? | Spin-up target and brake energy, 17 Aug |
| — | Is `files/cubli_wbs_tasklist.xlsx` live or superseded? | Whether a third schedule source needs syncing |
| — | Are the 8.0 h STANDARD-day figures real, or should they be measured? | All derived rows in §3 |
