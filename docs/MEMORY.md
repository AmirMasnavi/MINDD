# Project memory

Last updated: 2026-09-29

## Current state

- User subsequently authorised Task 1 EDA and requested a teaching-style notebook
  based on the supplied PL_Aula2.ipynb example. The example was used for structure,
  not for its regression instructions.
- PDF read in full (four pages); the malformed p. 3 sentence was also visually checked.
- Task 1 notebook now contains and executes the EDA, a derived target, explanations,
  plots, a feature-availability audit, and preparation decisions. No classifier was fitted.
- CSV has 441,077 rows and 47 original columns, including `end_cause` but no
  `is_Abnormal`. DATASET.md defines all original fields and the derived target.
- `main.ipynb` now has Python 3.12 metadata and saved aggregate outputs.
- `data/` and `models/` already existed and were empty.
- Private GitHub repository created at https://github.com/AmirMasnavi/MINDD using
  the user's existing GitHub CLI login. Local `Project/` is the repository root;
  `origin` points to that repository. Dataset, environment, and generated outputs
  are excluded. Team access has not been configured.
- Local `.venv` created with Python 3.12.0. All six direct dependency imports and
  the dependency compatibility check passed; the Python kernel was found inside
  this environment. Tested versions are recorded in requirements.txt.
- PDF and CSV remain unchanged; the notebook was intentionally updated and run.

## Decisions

| Date | Decision and reason |
| --- | --- |
| 2026-09-29 | Keep requirements, big picture, plan, memory, shared rules, and setup guide separate, each with one purpose. Use AGENTS.md for this workspace's AI instructions; skip duplicate CLAUDE.md and empty reference folders. |
| 2026-09-29 | User chose creation of a local environment. Use installed Python 3.12 with notebook/data exploration dependencies; defer modelling libraries until needed. |
| 2026-09-29 | Preserve raw files and the notebook. Record missing target as a dependency; do not guess a mapping from `end_cause`. |
| 2026-09-29 | Propose chronological evaluation and training-only learned preprocessing; these are methodological choices, not additional quoted PDF requirements. |
| 2026-09-29 | Pin the six direct dependencies to tested versions in requirements.txt; defer a complete transitive lock and modelling packages to avoid unnecessary setup complexity. |
| 2026-09-29 | User requested GitHub repository creation with their existing credentials. Created private AmirMasnavi/MINDD and prepared the planning documents, assignment PDF, empty notebook, and dependency list for version control. No implementation added. |
| 2026-09-29 | Moved project documentation into docs/, leaving README.md as the entry point. The user asked for Task 1 EDA with slow explanations and a separate dataset guide. |
| 2026-09-29 | For EDA, classify ordinary completion and user-requested stop as normal; classify the 13 fault/failure causes as abnormal. This is an explicit team assumption, not a PDF definition. The derived abnormal share is 18.58%; treating user stops as abnormal would yield 53.93%. Record sensitivity and seek instructor confirmation before final modelling claims. |
| 2026-09-29 | Audit found no full-row or user/post/start duplicates; all timestamps parse; four missing elapsed-history fields match no-history flags exactly. Order creation follows start in 248,588 rows and payment precedes end in 87,202; retain records and investigate semantics rather than delete them. |
| 2026-09-29 | EDA found 54,621 zero-energy sessions, including 45,563 with the assumed abnormal label; retain because early faults may deliver no energy. A trailing tab affects one location label in 18,370 rows; whitespace trimming preserves 13 categories. Median prior 30-day post abnormal rate is 0.122 for normal endings and 0.252 for abnormal endings, motivating later history ablation without claiming causality. |

## Open questions

1. Instructor: confirm or correct the team's `is_Abnormal` mapping, especially whether user-requested stops are normal, and clarify unknown/missing cause handling.
2. Instructor: clarify the incomplete preprocessing sentence at the bottom of PDF p. 3.
3. Team/course: confirm deadlines, report format/length, submission channel, later briefs,
   teammate names, step owners/reviewers, private data sharing location, and repository access.

## Source fingerprints (SHA-256)

- CSV: `f6109dc066162bc770417c39294cdecc7519646c3cfa8c1d95671ea30f0e0a9b`
- PDF: `a0edf5359b7394049ffdb13ea79eea22f707aaf959fb9c46545df0211a05ebda`
- Original notebook: `3d0c78dc6abfa04f1330b3eff4bfa0ca54acd69902df0c4f4d6841e4242ee55f`

## Handoff

Next: ask a teammate to review the notebook and draft report, confirm the target
mapping with the instructor, clarify the time/payment semantics if possible, and
then proceed to later modelling only when separately requested.

Future entries should be short: date, completed work, evidence location, decision
and reason, remaining blocker, next action. Record actual outcomes, not intended work.
