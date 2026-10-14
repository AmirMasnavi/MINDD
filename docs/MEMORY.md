# Project memory

Last updated: 2026-10-14

## Current state

- Task 3 (feature-group ablation, individual and ensemble models) is complete in `Task3.ipynb` (Sections 1 to 7). It
  reads `prepared/task2_protocol.json` unchanged and writes `prepared/task3_results.json`, `prepared/task3_fold_metrics.csv`,
  `prepared/task3_decision_log.csv` and three figures to `prepared/figures_task3/`. The report for Tasks 1 to 3 is
  `docs/TASK3_REPORT.pdf`: chapter 5 is Task 3 and chapter 6 is the final Synthesis. Selected set: 27 features (the 29 of
  Task 2 without `post_id` and `tariff_period`). Best model: gradient boosting (depth 6, learning rate 0.1, 200
  iterations), mean PR-AUC 0.626 against 0.511 for B1, above B1 in all four folds.
- Task 2 (prediction and evaluation setting) is complete in `Task2.ipynb` (Sections 1 to 10). It fits no model. It
  writes the evaluation protocol to `prepared/task2_protocol.json`, the decision log to
  `prepared/task2_decision_log.csv` and two figures to `prepared/figures_task2/`. The report for both tasks is
  `docs/TASK2_REPORT.pdf`, built from `docs/report/main.tex`. Chapters 1 to 3 are Task 1, chapter 4 is Task 2 and chapter 5
  is the final Synthesis, which is rewritten at each deliverable.
- The protocol: 29 features in 7 groups from 27 of the 47 columns; primary metric PR-AUC read with the abnormal share;
  ROC-AUC, Brier score and log-loss as complementary metrics; alerts per 1,000 sessions at budgets of 5%, 10% and 20%;
  four expanding-window folds (validation quarters 2020-Q4 to 2021-Q3) with a purge; test from 2021-10-01 not loaded;
  models ranked by the unweighted mean of the fold PR-AUC; baselines B0 (no skill) and B1 (7-day post failure rate,
  mean PR-AUC 0.511 against 0.181).
- The submitted Task 1 notebook is `Task1.ipynb`. The extended reference notebook is
  `TP1_Task1_Data_Understanding_and_Preparation.ipynb` (§0–§17). It contains the EDA,
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
| 2026-10-05 | The target mapping is stated as the team's decision, supported by the dataset's own history columns (about 100% agreement). Reports and notebooks no longer say that it waits for the instructor. |
| 2026-10-09 | First version of `Task2.ipynb` committed (`eb92ca6`): problem definition, classification of the 47 columns, metrics, four expanding-window folds, aggregation rule and baselines B0 and B1. |
| 2026-10-12 | Rewrote the commentary of `Task2.ipynb` in the same voice as `Task1.ipynb` (no fixed labels, "Section x.y" for references) and kept every methodological decision. Re-ran it in the pinned `.venv`: all four result tables are identical to the first version. Three figures in the commentary were corrected against the output (user stops would give about 54% abnormal in the development data; 12% of the development sessions are from new users; the reading of the fold 4 precision-recall curve). |
| 2026-10-12 | The 7-day window of baseline B1 comes from the Task 1 ranking, whose training period overlaps the validation quarters of folds 1 to 3. Recorded as a limitation in the notebook and the report; B1 fits nothing, so the effect should be small. |
| 2026-10-12 | Added chapter 5 (Task 2) to the report and saved it as `docs/TASK2_REPORT.pdf`. The validation quarter of Task 1 is fold 4 of Task 2, and the report now says so. Sentences that promised model fitting "for Task 2" now say "the modelling task". |
| 2026-10-12 | Ran the unslop skill (`theclaymethod/unslop` 2.3.0, rewrite flow, `crisp` preset) over the commentary of `Task1.ipynb` and `Task2.ipynb` and over the whole report. It confirmed and repaired 6 sentences: 3 in `Task2.ipynb` (cells 12, 28 and 37) and 3 in report Sections 5.2, 5.5 and 5.7. They were one "not a matter of taste" framing (in both files), two empty framing sentences, and "equals" / "exactly as the theory says" for B0 where the quoted numbers only come close (in both files). `Task1.ipynb` and report chapters 1 to 4 had no confirmed finding and were not edited. Protected with a reason: "the real capacity is unknown" (the only hard scanner hit, a literal use, in the metric table of the notebook and of the report) and "robust to outliers" in `Task1.ipynb`. Scanner figures before and after: hard phrase hits 0 / 1 / 1 for Task 1 / Task 2 / report, unchanged; opener unique ratio 0.421 / 0.391 / 0.488 before and 0.421 / 0.385 / 0.482 after; average sentence length 23.9 / 21.7 / 17.1 before and 23.9 / 21.8 / 17.1 after. The soft structure and silhouette flags remain, and the skill treats them as advisory. `Task2.ipynb` was re-run (result tables identical) and the report rebuilt (18 pages). |
| 2026-10-12 | Restructured the report around one final chapter. The chapter "Synthesis of Task 1" was removed, the Task 2 chapter is now chapter 4, and chapter 5, "Synthesis", closes the report and is rewritten at each deliverable. It is built around the project question and has four paragraphs: what the data allow (the Task 1 items of the brief, with their numbers), where the answer stands (protocol fixed, B1 at a mean PR-AUC of 0.511 against 0.181), the assumptions and limits of both tasks in one place, and one sentence on the modelling task. The limitations paragraph left the "Evaluation protocol" section. The earlier entries of this date name the Task 2 chapter by its old number: Sections 5.x are now 4.x. Two layout changes in `main.tex`: the bibliography follows the Synthesis on the same page, and chapter headings use the `needspace` package so a heading and its contents entry stay on the same page (the contents listed the Synthesis one page early before this). The report is still 18 pages. |

| 2026-10-14 | Reworked the first version of `Task3.ipynb` (commit `cb75870`) in place. The `.venv` pointed at a removed `/usr/bin/python3.12`, so it was recreated with Python 3.12.3 (pyenv) and the pins of `requirements.txt`; the first version had run on Python 3.11.9. Compared with the first version, no fold PR-AUC, ROC-AUC or Brier score changed at three decimals. The mean PR-AUC of the logistic regression now rounds to 0.593 instead of 0.592 (no caps, see the next entry), two Naive Bayes log-losses moved by 0.0004, and some alert counts of the random forest, Naive Bayes, logistic regression and stacking moved in the third decimal. Two clean runs in a row give identical metrics to three decimals (about 3 minutes each). Naive Bayes was not reproducible: `KBinsDiscretizer` draws a random sample of 200,000 rows for its quantiles, so fold 4 changed between runs. The bins now use every training row (`subsample=None`). The test rows are now dropped right after the CSV is read, before the target is built (they used to be dropped after it). |
| 2026-10-14 | Task 3 decisions. The first version capped the logged inputs and the active-session count of the logistic regression at the 0.1% / 99.9% training quantiles, which contradicts the Task 1 decision not to cap. With and without caps the mean PR-AUC differs by -0.0001 (0.5925 against 0.5924), so the Task 1 preparation is kept (notebook Section 4.4) and the logistic regression is now 0.593. The trees keep the Task 1 category codes for station and district, justified against the slide that advises against an arbitrary order (13 stations and 3 districts; gradient boosting reads them as categories). No new feature is added. The commentary now cites the course slides in `../T` for each technique, and the bold run-in labels were removed. Four numbers of the first version were corrected (+0.072 to +0.073, +0.078 to +0.077, +0.121 to +0.120, 40–76k to 42–76k validation sessions). |
| 2026-10-14 | Report: added chapter 5 "Individual and Ensemble Models" (ablation, individual models, ensembles, comparison and alerts, with three figures) and rewrote chapter 6, the Synthesis, around the project question with the Task 3 results and all the limitations of Tasks 1 to 3. Added a Task 3 paragraph to the abstract and updated the cover and the forward references. The report has 24 pages and is saved as `docs/TASK3_REPORT.pdf`. Ran the unslop skill (`theclaymethod/unslop` 2.3.0, rewrite flow, `crisp` preset) over the changed commentary of `Task3.ipynb`, chapter 5, the Synthesis, the new abstract paragraph, and the new text of README, PLAN and MEMORY. Hard phrase hits: 0 everywhere. It confirmed and repaired 4 sentences: 2 in the notebook ("if it clearly helps" and "The caps change nothing that matters", in Section 4.4) and 2 signpost sentences in the Synthesis ("The models of Chapter 5 show how much more..." and "These results rest on assumptions and have limits"). Protected with a reason: "by far the largest contribution" and "in practice" (both measured). The docs text had no finding. The preservation check passed (429 of 429 constraints in the notebook, 122 of 122 in the report). Opener unique ratio and average sentence length: first version of the notebook 0.464 / 31.2; reworked notebook 0.411 / 27.6 before and after; report text 0.485 / 23.2 before and 0.463 / 23.5 after. The soft structure and silhouette flags remain and are advisory. |
| 2026-10-14 | The professor asked for more references. The report now cites 16 sources across chapters 1 to 6: the assignment brief, the dataset paper, the four MINDD slide decks (Rodrigues: Introduction to Data Science, Data Preparation, Evaluation of Machine Learning Models, Foundational Models for Supervised Classification) and the evaluation lab notebook, grey literature (scikit-learn 1.9.1 User Guide, Regulation (EU) 2016/679 Article 5, Hyndman and Athanasopoulos' online *Forecasting: Principles and Practice*, section 5.10) and six papers (Pedregosa 2011, Saito and Rehmsmeier 2015, Brier 1950, Breiman 2001, Friedman 2001, Wolpert 1992). Every source was checked online (Crossref, jmlr.org, otexts.com, scikit-learn.org, EUR-Lex) or from the PDF cover before it was cited, every entry is cited and every citation has an entry. The bibliography now starts on its own page after the Synthesis and does not count as content: 19 content pages (13 in the Task 2 report), 26 pages in total. No number changed. Unslop on the cited sentences: 0 hard hits; one confirmed finding repaired (a loose paraphrase of the evaluation slides replaced by their "golden rule"); one citation of the lab moved from the formula $t^* = 1/(1+c)$, which the lab does not state, to the sentence on choosing the cut-off from costs. |

## Open questions

1. Closed on 2026-10-05: the `is_Abnormal` mapping is the team's decision (see Decisions). No confirmation is awaited.
2. Instructor: clarify the incomplete preprocessing sentence at the bottom of PDF p. 3.
3. Closed on 2026-10-14: `post_id` is dropped. Removing it raised the mean PR-AUC by +0.0057, in all four folds (`Task3.ipynb` Section 3.4).
4. Team and course: confirm the report format and length, the submission channel, the AI-use disclosure, the private data-sharing location, and the repository visibility (must be private). The Task 1 deadline is 2026-10-04.

5. Team: `Task2.ipynb` cites "the slides" nine times for evaluation concepts (PR curve, holdout and K-fold, the golden rule, evaluating on the initial distribution, Wilcoxon, McNemar, model complexity). The author of the first version should confirm them against the evaluation deck.
6. Next task: the cost ratio between a missed failure and a false alert, and the alert capacity, are unknown. The budgets of 5%, 10% and 20% are assumptions, and the threshold, chosen after a calibration check, needs a stated assumption.

## Source fingerprints (SHA-256)

- CSV: `f6109dc066162bc770417c39294cdecc7519646c3cfa8c1d95671ea30f0e0a9b`
- PDF (Task 1 brief): `a0edf5359b7394049ffdb13ea79eea22f707aaf959fb9c46545df0211a05ebda`
- PDF (Task 1 and Task 2 brief): `e3a3e16aa97e96558dca298edf6492679d6a07c311ffb158a1a7ae7dccb350a1`
- PDF (Task 1 to Task 3 brief): `4cb2e5d9e806fde28c2c1560df8c290276bcc7655ee0c40ab4c80609d5c37213`
- Original notebook: `3d0c78dc6abfa04f1330b3eff4bfa0ca54acd69902df0c4f4d6841e4242ee55f`

## Handoff

Next steps: the author of the first version of `Task3.ipynb` reviews the reworked notebook and chapters 5 and 6 of the
report. Then submit Task 3 (notebook and `docs/TASK3_REPORT.pdf`). The next task reads `prepared/task3_results.json` and
`prepared/task2_protocol.json` unchanged, checks calibration, chooses the threshold and scores the test period once.

Keep future entries short: date, completed work, evidence location, decision
and reason, remaining blocker, next action. Record actual outcomes, not intended work.
