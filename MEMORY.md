# Project memory

Last updated: 2026-09-29

## Current state

- Planning/setup only; user explicitly requested no implementation yet.
- PDF read in full (four pages); the malformed p. 3 sentence was also visually checked.
- CSV inspection was limited to its header and file metadata/fingerprint. No row
  counts, distributions, quality findings, or model results have been computed.
- CSV has 47 columns, including `end_cause`, but lacks `is_Abnormal`.
- `main.ipynb` has one empty Markdown cell and one empty code cell. Its Python 3
  kernel label conflicts with Python 2.7.6 language metadata; notebook left unchanged.
- `data/` and `models/` already existed and were empty.
- Private GitHub repository created at https://github.com/AmirMasnavi/MINDD using
  the user's existing GitHub CLI login. Local `Project/` is the repository root;
  `origin` points to that repository. Dataset, environment, and generated outputs
  are excluded. Team access has not been configured.
- Local `.venv` created with Python 3.12.0. All six direct dependency imports and
  the dependency compatibility check passed; the Python kernel was found inside
  this environment. Tested versions are recorded in requirements.txt.
- Documentation links were checked. SHA-256 checks confirmed the PDF, CSV, and
  notebook are unchanged. No analysis or notebook cells were executed.

## Decisions

| Date | Decision and reason |
| --- | --- |
| 2026-09-29 | Keep requirements, big picture, plan, memory, shared rules, and setup guide separate, each with one purpose. Use AGENTS.md for this workspace's AI instructions; skip duplicate CLAUDE.md and empty reference folders. |
| 2026-09-29 | User chose creation of a local environment. Use installed Python 3.12 with notebook/data exploration dependencies; defer modelling libraries until needed. |
| 2026-09-29 | Preserve raw files and the notebook. Record missing target as a dependency; do not guess a mapping from `end_cause`. |
| 2026-09-29 | Propose chronological evaluation and training-only learned preprocessing; these are methodological choices, not additional quoted PDF requirements. |
| 2026-09-29 | Pin the six direct dependencies to tested versions in requirements.txt; defer a complete transitive lock and modelling packages to avoid unnecessary setup complexity. |
| 2026-09-29 | User requested GitHub repository creation with their existing credentials. Created private AmirMasnavi/MINDD and prepared the planning documents, assignment PDF, empty notebook, and dependency list for version control. No implementation added. |

## Open questions

1. Instructor: supply `is_Abnormal` or the official mapping from `end_cause`, including unknown/missing values.
2. Instructor: clarify the incomplete preprocessing sentence at the bottom of PDF p. 3.
3. Team/course: confirm deadlines, report format/length, submission channel, later briefs,
   teammate names, step owners/reviewers, private data sharing location, and repository access.

## Source fingerprints (SHA-256)

- CSV: `f6109dc066162bc770417c39294cdecc7519646c3cfa8c1d95671ea30f0e0a9b`
- PDF: `a0edf5359b7394049ffdb13ea79eea22f707aaf959fb9c46545df0211a05ebda`
- Original notebook: `3d0c78dc6abfa04f1330b3eff4bfa0ca54acd69902df0c4f4d6841e4242ee55f`

## Handoff

Next: confirm the target definition and allocate PLAN.md steps. After the user asks
to begin implementation, start with the notebook's inventory and feature audit;
target-independent checks can proceed while label clarification is pending.

Future entries should be short: date, completed work, evidence location, decision
and reason, remaining blocker, next action. Record actual outcomes, not intended work.
