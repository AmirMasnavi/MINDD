# Project memory

Last updated: 2026-11-18

## Current state

| Date | Entry |
| --- | --- |
| 2026-11-18 | The repository was split into `project1/` (closed) and `project2/`, each with its own README, requirements and documents; both use the root `.venv`. The `Charging_Data.csv` in `project2/` is a truncated download (254,171 rows, Tongxiang and Nanhu only, last row cut at 2020-01-16 15:01), so data work waits for a complete re-download. Spec `specs/008-p2-task1-forecasting-framework` fixes Task 1: daily issuance at 00:00, direct strategy with one shared model, the four Project 1 folds, MASE averaged over horizons, levels and folds as the primary score. The truncated copy shows the file format: GBK text (read as `gb18030`), with a tab at the end of every timestamp. Facts from the development period of the Project 1 file, to be recomputed on the new download: the autocorrelation of network hourly demand is 0.848 at lag 24 against 0.821 at lag 168; the in-sample seasonal naive MAE is 7.12 sessions per hour with m = 24 against 7.66 with m = 168. |
| 2026-11-18 | Setup done before the data arrives (tasks T001 to T004, T006, T009, T034): `requirements.txt`, PLAN, MEMORY, the report skeleton (builds, 7 pages) and the notebook skeleton with the holiday calendar (30 holiday days and 6 adjusted working days in 2020, 31 and 7 in 2021; all assertions pass in a scratch run). The prose went through unslop (rewrite flow, crisp preset) and the humanizer. Scanner figures before and after: notebook markdown 0 hard hits, opener unique ratio 0.875, average sentence 33.3 words before and 30.9 after (one 63-word sentence split); this file's entry 0 hard hits, average sentence 39.0 before and 32.4 after (the format facts were attributed to the truncated copy, not the Project 1 file); PLAN 0 hard hits, no edit (its 53.2-word average comes from bullet lines the scanner joins). Blocker: the complete `Charging_Data.csv` (task T005). |

Keep future entries short: date, completed work, evidence location, decision
and reason, remaining blocker, next action. Record actual outcomes, not intended work.
