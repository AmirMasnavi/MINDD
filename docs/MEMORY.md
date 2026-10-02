# Project memory

Last updated: 2026-10-02

## Current state

- The single Task 1 notebook is `TP1_Task1_Data_Understanding_and_Preparation.ipynb` (§0–§17). It contains the EDA,
  the derived target, the availability audit, the preparation decisions, the learned transformations (fitted on TRAIN only)
  and the preliminary diagnostics. The only fitted models are untuned diagnostics on training-window folds (§14–§15).
  Validation and test are untouched.
- The CSV has 441,077 rows and 47 original columns. It includes `end_cause` but no `is_Abnormal`. DATASET.md defines all
  original fields and the derived target. `docs/TASK1_REPORT.md` is the only report.
- The notebook runs top to bottom without errors in the local `.venv` (Python 3.12.3, versions pinned in
  `requirements.txt`) and passes all §16 integrity checks.
- The repository root is the local `MINDD/` folder. `origin` is the private GitHub repository
  https://github.com/AmirMasnavi/MINDD. The dataset, the environment and generated outputs are excluded. Team access is
  not configured yet.
- The PDF and CSV are unchanged.
- 2026-10-02: Reviewed all Task 1 files against PDF §4. Every Task 1 requirement has evidence in the notebook and in the
  report. Fixed broken section references (§13.4, §5.3, discretization in §13), a wrong residual-mismatch range in §4.2
  (0.003–0.021%), the month order in §5.1, the period behind the 57.2% order-lag figure (§6.2), the missing §12.1 heading
  and the dangling "see above" in the learned-operations ledger. Added cardinality, post-activity and user-activity
  evidence and a Figure 5 pointer to the report. An unslop pass (phrase, structure and silhouette scanners plus a manual read)
  found no hard AI-writing patterns, and one overstated claim ("irreducible" label ambiguity, §4.4) was softened.
  Re-ran the notebook.

## Decisions

| Date | Decision and reason |
| --- | --- |
| 2026-09-29 | Keep requirements, big picture, plan, memory, shared rules, and setup guide separate, each with one purpose. Use AGENTS.md for this workspace's AI instructions. Skip the duplicate CLAUDE.md and empty reference folders. |
| 2026-09-29 | The user chose to create a local environment. Use the installed Python 3.12 with the notebook and data-exploration dependencies. Defer modelling libraries until needed. |
| 2026-09-29 | Preserve the raw files and the notebook. Record the missing target as a dependency and do not guess a mapping from `end_cause`. |
| 2026-09-29 | Propose chronological evaluation and training-only learned preprocessing. These are methodological choices, not extra requirements quoted from the PDF. |
| 2026-09-29 | Pin the six direct dependencies to tested versions in requirements.txt. Defer a complete transitive lock and the modelling packages to keep setup simple. |
| 2026-09-29 | The user asked to create a GitHub repository with their existing credentials. Created the private AmirMasnavi/MINDD and prepared the planning documents, assignment PDF, empty notebook, and dependency list for version control. No implementation added. |
| 2026-09-29 | Moved the project documentation into docs/ and kept README.md as the entry point. The user asked for Task 1 EDA with slow explanations and a separate dataset guide. |
| 2026-09-29 | For EDA, classify ordinary completion and user-requested stop as normal, and the 13 fault and failure causes as abnormal. This is an explicit team assumption, not a PDF definition. The derived abnormal share is 18.58%. Treating user stops as abnormal would give 53.93%. Record the sensitivity and get instructor confirmation before final modelling claims. |
| 2026-09-29 | The audit found no full-row or user/post/start duplicates. All timestamps parse, and the four missing elapsed-history fields match the no-history flags exactly. Order creation follows the start in 248,588 rows and payment precedes the end in 87,202. Retain these records and investigate their semantics instead of deleting them. |
| 2026-09-29 | EDA found 54,621 zero-energy sessions, 45,563 of them with the assumed abnormal label. Retain them because early faults may deliver no energy. A trailing tab affects one location label in 18,370 rows, and trimming whitespace preserves 13 categories. The median prior 30-day post abnormal rate is 0.122 for normal endings and 0.252 for abnormal endings. This motivates a later history ablation and does not imply causality. |
| 2026-10-02 | (Figures superseded by the pinned-environment re-run: post history −0.195, user history −0.037, cold-start ROC-AUC 0.714 vs 0.845.) Completed §13 (two preprocessing views fitted on TRAIN only, plus the ledger), §14 (class weights keep the ranking but distort probabilities, so no resampling and no SMOTE), §15 (group ablation: removing post history changes PR-AUC by −0.193 and removing user history by −0.035, while the other groups and `post_id` change it by about 0; cold-start users have ROC-AUC 0.716 against 0.846), §16 (artefacts and 8 integrity checks), and §17 (synthesis and decision log). |
| 2026-10-02 | Replaced the unsupported claim that the burn-in exclusion is harmless with an actual check (§15.4: including it changes PR-AUC by +0.0004). The exclusion stays. |
| 2026-10-02 | Added `scipy` and `scikit-learn` (used by the notebook) to `requirements.txt`, and added `prepared/*.csv.gz` to `.gitignore`. |

## Open questions

1. Instructor: confirm or correct the team's `is_Abnormal` mapping, especially whether user-requested stops are normal, and clarify how to handle unknown or missing causes.
2. Instructor: clarify the incomplete preprocessing sentence at the bottom of PDF p. 3.
3. Team: decide whether `post_id` stays in the main feature set or becomes a Task 2 comparison (§15.1 shows no gain).
4. Team and course: confirm the report format and length, the submission channel, the AI-use disclosure, the private data-sharing location, and the repository visibility (must be private). The Task 1 deadline is 2026-10-04.

## Source fingerprints (SHA-256)

- CSV: `f6109dc066162bc770417c39294cdecc7519646c3cfa8c1d95671ea30f0e0a9b`
- PDF: `a0edf5359b7394049ffdb13ea79eea22f707aaf959fb9c46545df0211a05ebda`
- Original notebook: `3d0c78dc6abfa04f1330b3eff4bfa0ca54acd69902df0c4f4d6841e4242ee55f`

## Handoff

Next steps: each member reviews one part of the notebook and report (§1–§6, §7–§12, §13–§17). Then confirm the target
mapping with the instructor and clarify the time and payment semantics if possible.
Proceed to later modelling only when it is requested separately.

Keep future entries short: date, completed work, evidence location, decision
and reason, remaining blocker, next action. Record actual outcomes, not intended work.
