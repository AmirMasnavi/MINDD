# Work plan

This is the team's proposed sequence.
Tasks 1 (submitted on 2026-10-04), 2 and 3 are complete. The next task chooses the cut-off after a calibration check
and scores the chosen model once on the test period.
Owners and reviewers are still unassigned, so replace `TBD` when the team allocates work.

## Task 1 sequence

| Step | Work and completion evidence | Depends on | Owner / reviewer | Status |
| --- | --- | --- | --- | --- |
| 0 | Prepare the documentation and the local notebook environment. Verify imports without running analysis. | none | TBD / TBD | Complete on 2026-09-29 |
| 1 | Confirm the official target mapping and its source, the handling of unknown labels, the submission logistics, and the ambiguous preprocessing wording. Record the answers in MEMORY.md. | none | TBD / TBD | The team documented a mapping for EDA. Instructor confirmation is open |
| 2 | Inventory the actual shape, schema and types, timestamp parsing and coverage, identifiers, and field meanings. Record the source fingerprint and investigate differences from the brief. | User asks to implement | TBD / TBD | Complete on 2026-09-29 |
| 3 | Build the target from the stated definition, validate its binary values and missingness, and classify each input by prediction-time availability. | 1, 2 | TBD / TBD | Complete for EDA. The mapping is an assumption |
| 4 | Propose chronological train, validation and test boundaries from the observed coverage and label availability. Reserve the final test period before making adaptive feature or preparation choices. | 2, 3 | TBD / TBD | Complete on 2026-10-02. Burn-in before 2020-04-01, train to 2021-06-30 with purge, validation Q3-2021, test Q4-2021, and 3 expanding-window folds |
| 5 | Audit missingness, duplicates, inconsistencies, numeric ranges and outliers, rare categories and cardinality, and relevant relationships. Investigate each suspected problem before correcting it. | 2, 4 | TBD / TBD | Complete for EDA. The meaning of the flagged fields remains open |
| 6 | Examine temporal changes in volume, prevalence, eligible predictors, and user and post activity. Study cold starts and history availability, and interpret the implications. | 3 to 5 | TBD / TBD | Complete for EDA under the stated mapping |
| 7 | Choose and document the preparation and the retained feature groups. Implement only justified operations, and fit learned transformations on training data. | 5, 6 | TBD / TBD | Complete on 2026-10-02. 29 features in 7 groups, with learned transformations fitted on TRAIN only (§13, ledger) |
| 8 | Write the short report section and the Task 1 synthesis, and cross-check it against the assignment PDF, marking the later ablation as pending. Restart and run the notebook in order, then peer-review both artifacts and submit them. | 7 | TBD / TBD | The notebook is complete and was re-run on 2026-10-02, and the report is rewritten. Teammate review and submission (due 2026-10-04) are pending |

The target mapping in DATASET.md is the team's decision. The dataset's own history columns support it
(`Task1.ipynb`, Section 5.2), so the report states it as a conclusion drawn from the data.

## Task 2 sequence

Task 2 defines the prediction and evaluation setting. It fits no model. The table follows the brief
(`TP1-MINDD2026_27-Task1+Task2.pdf`, pages 4 to 6).

| Brief item | Where it is answered | Status |
| --- | --- | --- |
| Unit of observation, classes, target from `end_cause`, prediction moment, purpose, meaning of an alert | `Task2.ipynb` Section 3; report Section 4.1 | Complete |
| Classification of every supplied variable into four categories, with justified exclusions | `Task2.ipynb` Section 4 (47 columns: 27 eligible, 1 target only, 7 during or after the session, 12 other reasons); report Section 4.2 | Complete |
| Consequences of false positives and false negatives | `Task2.ipynb` Section 5; report Section 4.3 | Complete |
| Primary, complementary, operational and stability metrics, justified before optimisation | `Task2.ipynb` Section 6; report Section 4.4 | Complete. Primary metric PR-AUC |
| Temporal evaluation strategy and protection of the final test | `Task2.ipynb` Section 7 (four expanding-window folds, purge, test from 2021-10-01 not loaded); report Section 4.5 | Complete |
| Aggregation across temporal folds | `Task2.ipynb` Section 8; report Section 4.6 | Complete |
| No-skill and simple baseline with their expected performance | `Task2.ipynb` Section 9 (B0 and B1); report Section 4.7 | Complete |
| Concise evaluation protocol | `Task2.ipynb` Section 10 and `prepared/task2_protocol.json`; report Section 4.8 | Complete |
| Synthesis (the Task 1 items of the brief, and where the project question stands after Task 2) | report chapter 5, the final chapter, rewritten at each deliverable | Complete |
| Notebook and report section for the submission | `Task2.ipynb`, `docs/TASK2_REPORT.pdf` | Complete on 2026-10-12. Teammate review pending |

## Task 3 sequence

Task 3 runs the feature-group ablation and fits individual and ensemble models under the Task 2 protocol. The table
follows the brief (`TP1-MINDD2026_27-Task1+Task2+Task3.pdf`, pages 6 and 7).

| Brief item | Where it is answered | Status |
| --- | --- | --- |
| Four nested feature sets (context and weather; plus tariff; plus post history; plus user history) | `Task3.ipynb` Sections 3.1 to 3.2; report Section 5.1 | Complete |
| Tariff beyond time of day, post-history contribution, user-history benefit, consistency across periods | `Task3.ipynb` Sections 3.2 to 3.5 (paired differences by fold, bootstrap noise, cold start); report Section 5.1 | Complete. Tariff adds nothing, post history +0.304, user history +0.026 for returning users only |
| Operational or ethical concerns of each feature group | `Task3.ipynb` Section 3.6; report Section 5.1 | Complete |
| Additional leakage-safe features | `Task3.ipynb` Section 3.1 (decision: none added) | Complete |
| At least three individual classifiers of different principles, justified | `Task3.ipynb` Sections 4.1 to 4.4 (logistic regression, Naive Bayes, decision tree; k-NN and SVM left out with reasons; caps checked against Task 1); report Section 5.2 | Complete |
| At least three ensembles of different principles, and why each could improve | `Task3.ipynb` Sections 5.1, 5.2 and 5.4 (random forest, gradient boosting, stacking); report Section 5.3 | Complete |
| Stacking predictions generated without leakage | `Task3.ipynb` Section 5.3 (inner quarters in time order, with assertions); report Section 5.3 | Complete |
| Comparison of all models with the baselines | `Task3.ipynb` Sections 6.1 and 6.2; report Section 5.4 | Complete. Gradient boosting 0.626 against B1 0.511, in all four folds |
| Synthesis | report chapter 6, the final chapter, rewritten for this deliverable | Complete |
| Notebook and report section for the submission | `Task3.ipynb`, `docs/TASK3_REPORT.pdf` | Complete on 2026-10-14. Teammate review pending |

## Notebook structure

The notebook follows §0–§17 (see the README table). For each important result it uses the sequence question, evidence,
interpretation, decision. The notebook holds the authoritative variable dictionary (§2.2) and decision log (§17, saved to
`prepared/decision_log.csv`). `docs/DATASET.md` is a readable summary of the dictionary and must agree with it.

## Task 1 review split (`Task1.ipynb`)

Each of the three members reviews about a third of the notebook. Replace "Student n" with names.

| Reviewer | Sections | Theme | Status |
| --- | --- | --- | --- |
| Student 1 | §0–§6 (intro, setup, load, variables, cleaning, target, missing values) | Understanding and cleaning | Pending |
| Student 2 | §7–§10 (changes over time, leakage, start-time predictors, outliers) | Exploration | Pending |
| Student 3 | §11–§15 (split and sampling, feature engineering and reduction, learned operations, saved files, synthesis) | Preparation and conclusions | Pending |

Each reviewer first runs Restart & Run All (about 1 minute), then checks that (1) every number in "What we see" matches the
output above it, (2) every decision follows from the evidence shown and names its slide topic, and (3) the text is clear
and claims nothing the data does not show. Agree on the hand-offs together: the target assumption (§5) affects every
abnormal share; the burn-in and split decided in §7.5 are applied in §11; the exclusions in §8 and §10 feed the feature
list in §12.7; and each reviewer checks the synthesis (§15) bullets that cite their sections.

## Task 2 review split (`Task2.ipynb`)

Each of the three members reviews about a third of the notebook (5,785 words of commentary in 50 cells) and the report
sections that go with it. Part 2 holds all nine slide citations, so it goes to Ines, who wrote the first version of
the notebook and has the evaluation slides at hand.

| Reviewer | Notebook sections (cells) | Theme | Report sections | Size | Status |
| --- | --- | --- | --- | --- | --- |
| Manuela | 1 to 5 (cells 0 to 19): setup, data, prediction problem, variable classification, cost of the two errors | What we predict and with which variables | 4.1 to 4.3 | 1,787 words, 5 output tables | Pending |
| Ines | 6 to 8 (cells 20 to 34): metrics, temporal folds, aggregation | How we evaluate | 4.4 to 4.6 | 2,218 words, 2 output tables, 1 figure | Pending |
| Amir | 9 and 10 (cells 35 to 49): baselines, protocol, limitations | The reference results and the final protocol | 4.7, 4.8 and chapter 5 (Synthesis) | 1,780 words, 6 output tables, 1 figure | Pending |

Everyone does the same three checks on their part: every number in the text matches the output above it, every decision
follows from the evidence shown, and the text is clear, sounds like us and claims nothing the data does not show. Run
Restart & Run All once first (a few seconds) to see that it finishes without an error.

Points to look at in each part:

- Manuela. The target wording in Section 3.2 (stated as our decision, with the "about 54%" alternative taken from
  the table). The classification table of Section 4: read the reason of each of the 20 excluded columns and check its
  category, in particular `UserID` and `Order creation time`. The four assumptions after it. In Section 5, whether
  "a missed failure costs more than a false alert" is argued well enough, and the cut-off table (break-even at c = 4.4).
- Ines. Confirm the nine slide citations against the evaluation deck: three in Section 6 (performance depends on
  class distribution and costs, PR curve for rare positives, ROC-AUC optimistic under imbalance), two in Section 7.1
  (holdout and K-fold, the golden rule), one in Section 7.3 (evaluate on the initial distribution) and three in
  Section 8 (Wilcoxon test, a more complex model is not necessarily better, McNemar's test). Then the metric table
  (each "why" and "limitation", and whether alert budgets of 5%, 10% and 20% are reasonable), the fold table against
  its commentary, the reasons for quarters and for four folds, and the ranking rule of Section 8.
- Amir. The caveat on the 7-day window of baseline B1 (Section 9 and the limitations). The per-fold, aggregated
  and operational results against their tables. The reading of the precision-recall curves against the figure (fold 4
  falls below 0.8 at a recall of about 0.07 and is the highest curve beyond about 0.4). The protocol table of
  Section 10 against `prepared/task2_protocol.json`, and the limitations list. In the report, Tables 4.4 and 4.5
  against the notebook, and the Synthesis.

Do not edit the notebook in parallel: three edited copies of one `.ipynb` cannot be merged cleanly. Each reviewer writes
the proposed changes as comments with the cell number (in the pull request or a shared list), and one person applies
them all at the end, re-runs the notebook and rebuilds the report. A change in one part can touch another: the fold
numbers of Section 7 are quoted in Sections 5 and 9, and the notebook wording of Sections 4 and 9 is repeated in report
Sections 4.2 and 4.7.

## Initial feature policy (proposed before the analysis; the outcome is in notebook §11.3)

| Group | Initial treatment and questions |
| --- | --- |
| Start context | Consider start-time calendar features, location, district, weather, and tariff. Check parsing, missingness, and actual availability. |
| Order creation time | Use only after confirming its relationship to session start and its availability at that instant. |
| Post history | Consider the provided `post_*` features. Understand the windows, smoothing, units, and no-history indicators. |
| User history/activity | Consider `user_*` features and `is_new_user`. Check their meaning, cold starts, privacy, and operational access. |
| Raw user/post identifiers | Retain for audit and grouping. Decide predictive use separately, based on cardinality, privacy, memorisation, and unseen-entity performance. |
| Post-session information | Exclude `end_cause`, `End Time`, `Payment time`, final energy, costs, and payments from predictors, including derived features. They may support target construction or auditing only where justified. |

Do not drop suspicious extremes or duplicates automatically. First determine whether
they are errors, repeated records, or valid sessions. Do not interpret absent history
as ordinary missing data without checking the associated flags and definitions.

## Evaluation and preparation safeguards (team proposal)

- Prefer a chronological evaluation that simulates predicting future sessions. Choose
  dates after the inventory instead of assuming a split ratio.
- Keep labels from sessions not yet completed at a training cutoff out of that
  training set. End timestamps can support this audit without becoming predictors.
- Basic schema, quality and coverage checks may inspect all of the supplied data. Mark
  any whole-period descriptive summary clearly. Use training data for adaptive exploration
  and choices, validation for comparison, and the held-out test only for final evaluation.
- Fit imputers, scalers, category grouping, thresholds, selection, and any resampling
  inside the training partition or fold. Apply the fitted transformations unchanged to
  validation and test data. Resample training data only, and only if the evidence justifies it.
- Keep the supplied chronological histories and rebuild them only if needed.
  If you simulate a production history that updates continuously, later-period histories
  can contain outcomes of sessions completed before the prediction, including earlier
  evaluation-period sessions. State that evaluation assumption explicitly.
- Plan how to handle unseen categories, and report cold-start behaviour for unseen users
  or posts where sample sizes permit. Fix random seeds for stochastic steps when implemented.

## Later project stages (after Task 3; provisional until the next brief arrives)

1. Reconcile the next brief with this plan before adding scope.
2. Done in Task 3: classifiers and ensembles on the four folds of Task 2, the feature-group ablation, and the
   hyperparameters (`prepared/task3_results.json`).
3. Check the calibration of the chosen model and choose the decision threshold without test feedback. The threshold is
   chosen on the pooled out-of-fold predictions, from the alert budget or the cost ratio, and then frozen.
4. Evaluate the chosen approach once on the held-out test, investigate limitations and subgroup and time behaviour,
   and finish the report with privacy, generalisation, cold-start, operational assumptions and reproducibility details.

## Submission check

- [x] Target definition is stated as the team's decision with its evidence. The feature audit enforces prediction-time availability.
- [x] Quality and temporal findings have evidence and modelling implications.
- [x] Every material preparation choice is justified; learned steps use training data only.
- [x] Retained groups, unresolved assumptions, and future evaluation implications are explicit.
- [x] Notebook runs top-to-bottom with the documented environment and relative paths.
- [ ] Report explains decisions/results without copying code (done); teammate has reviewed both files (pending).
- [ ] Current deadline, file format, and submission channel are confirmed.
- [x] Task 2: every brief item has a notebook section and a report section (table above), and the report numbers match the notebook output.
- [ ] Task 2: the author of the first notebook version has reviewed the rewritten commentary and confirmed the slide citations.
- [x] Task 3: every brief item has a notebook section and a report section (table above), and the report numbers match the notebook output.
- [ ] Task 3: the author of the first notebook version has reviewed the reworked notebook and report chapter 5.
