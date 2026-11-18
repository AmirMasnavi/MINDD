# Work plan

Project 2 asks (statement `TP2-MINDD2026_27-Task1.pdf`, Section 2):

> To what extent can historical charging activity, temporal patterns, and other relevant information be used to
> accurately forecast hourly electric-vehicle charging demand over the next 24 hours, at both network and district
> levels?

Owners and reviewers are still unassigned, so replace `TBD` when the team allocates work.

## Task 1 deliverables

| Deliverable | Content | Owner / reviewer | Status |
| --- | --- | --- | --- |
| `Task1.ipynb` | Checked read, test drop, audit, four hourly series, exploration, formulation, protocol, baseline scores, synthesis | TBD / TBD | Complete on 2026-11-18; runs in under ten seconds, two runs give identical files |
| `prepared/task1_*` | Protocol, series, calendar, audit, predictor catalogue, folds, baseline scores (also by period), results, run information, decision log, ledger, 10 figures | TBD / TBD | Generated on 2026-11-18 |
| `docs/report/main.tex` and `docs/TASK1_REPORT.pdf` | Task 1 chapters and one closing Synthesis chapter | TBD / TBD | Complete on 2026-11-18 (18 pages, main text 12); teammate review pending |

## Decisions fixed before the data work

These come from the Task 1 specification (2026-11-18) and are written into the notebook's decision log when it runs.

- Forecasts are issued once a day at 00:00, with data up to the hour starting at 23:00 of the previous day, for the
  24 hours of the issuance day. Horizon h is clock hour h-1.
- The 24 values come from a direct strategy with one shared model: one row per target hour, inputs known at 00:00
  only, hour of day as an input.
- Evaluation reuses the four Project 1 folds: training from 2020-04-01, validation quarters 2020-Q4, 2021-Q1,
  2021-Q2 and 2021-Q3, test from 2021-10-01, no purge gap.
- The primary score is MASE averaged over the 24 horizons, then over the 4 levels with equal weight, then over the 4
  folds. MAE and RMSE per level are secondary scores.

## Source fingerprints (SHA-256)

| File | Rows | SHA-256 | Status |
| --- | --- | --- | --- |
| `Charging_Data.csv` | 441,077 | `6f3643db401327ec4f4a074109987706e421896869acac26a8ee1a5c6e3b45ee` | Complete copy downloaded again from Moodle on 2026-11-18 (85.6 MB, GBK text, CRLF line ends, 24 columns, three districts, last line complete). The earlier truncated copy must not be used |
