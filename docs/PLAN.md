# Work plan

This is the team's proposed sequence.
Task 1 is complete apart from team review, instructor confirmation of the target and submission (due 2026-10-04).
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

Task 1 EDA uses the target assumption stated in DATASET.md. The team needs instructor
confirmation before making final modelling claims. Team review and
submission logistics remain open.

## Notebook structure

The notebook follows §0–§17 (see the README table). For each important result it uses the sequence question, evidence,
interpretation, decision. The notebook holds the authoritative variable dictionary (§2.2) and decision log (§17, saved to
`prepared/decision_log.csv`). `docs/DATASET.md` is a readable summary of the dictionary and must agree with it.

## Task 1 review split (`TP1_Task1_Merged.ipynb`)

Each of the three members reviews about a third of the merged notebook. Replace "Student n" with names.

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

## Later project stages (provisional until later briefs arrive)

1. Reconcile the next brief with this plan before adding scope.
2. Establish a simple baseline and a small justified set of classifiers using the
   same partitions and appropriate preprocessing.
3. Choose metrics from class balance and the cost of missed abnormalities versus
   false alarms. Candidate measures include precision, recall, PR-AUC, and a confusion
   matrix; thresholds and hyperparameters must be chosen without test feedback.
4. Compare start context alone, context plus post history, context plus user history,
   and context plus both. Keep identifier policy, splits, metric definitions, and tuning
   effort consistent so the feature-group ablation is interpretable.
5. Evaluate the chosen approach once on the held-out test, investigate limitations
   and subgroup and time behaviour, and finish the report with privacy, generalisation,
   cold-start, operational assumptions, and reproducibility details.

## Submission check

- [ ] Target definition is official (instructor confirmation pending). The feature audit enforces prediction-time availability (§6).
- [x] Quality and temporal findings have evidence and modelling implications.
- [x] Every material preparation choice is justified; learned steps use training data only.
- [x] Retained groups, unresolved assumptions, and future evaluation implications are explicit.
- [x] Notebook runs top-to-bottom with the documented environment and relative paths.
- [ ] Report explains decisions/results without copying code (done); teammate has reviewed both files (pending).
- [ ] Current deadline, file format, and submission channel are confirmed.
