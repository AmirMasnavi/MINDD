# Work plan

This is the team's proposed sequence. Requirement IDs refer to REQUIREMENTS.md.
Task 1 has started. Owners and reviewers remain unassigned; replace
`—` when the team allocates work. No deadlines have been invented.

## Task 1 sequence

| Step | Work and completion evidence | Depends on | Owner / reviewer | Status |
| --- | --- | --- | --- | --- |
| 0 | Prepare documentation and local notebook environment; verify imports without running analysis. | — | — / — | Complete — 2026-09-29 |
| 1 | Confirm official target mapping/source, unknown-label handling, submission logistics, and ambiguous preprocessing wording. Record answers in MEMORY.md. | — | — / — | Team mapping documented for EDA; instructor confirmation open |
| 2 | Inventory actual shape, schema/types, timestamp parsing/coverage, identifiers, and field meanings. Record the source fingerprint and investigate differences from the brief. | User asks to implement | — / — | Complete — 2026-09-29 |
| 3 | Build the target from the stated definition, validate binary values/missingness, and classify each input by prediction-time availability. | 1, 2 | — / — | Complete for EDA; mapping is an assumption |
| 4 | Propose chronological train/validation/test boundaries using observed coverage and label availability; reserve the final test period before adaptive feature/preparation choices. | 2, 3 | — / — | Calendar proposal recorded; cutoff check belongs to modelling |
| 5 | Audit missingness, duplicates, inconsistencies, numeric ranges/outliers, rare categories/cardinality, and relevant relationships. Investigate each suspected problem before correction. | 2, 4 | — / — | Complete for EDA; semantics of flagged fields remain open |
| 6 | Examine temporal changes in volume, prevalence, eligible predictors, and user/post activity; study cold starts and history availability. Interpret implications. | 3–5 | — / — | Complete for EDA under stated mapping |
| 7 | Choose and document preparation and retained feature groups; implement only justified operations, fitting learned transformations on training data. | 5, 6 | — / — | Strategy documented; only target derived, no learned operation needed for EDA |
| 8 | Write the concise report section and Task 1 synthesis; cross-check R1–R9, marking later ablation as pending. Restart and run the notebook in order, then peer-review and submit both artifacts. | 7 | — / — | Notebook and draft report complete; teammate review pending |

Task 1 EDA uses the explicit target assumption in DATASET.md. Instructor
confirmation remains necessary before final modelling claims. Team review and
submission logistics remain open.

## Notebook outline to add when implementation starts

1. Objective, source, scope, assumptions, environment, and reproducibility settings.
2. Data inventory and schema/meaning table.
3. Target definition and prediction-time feature audit.
4. Evaluation boundaries and data-access policy.
5. Data-quality investigation and evidence.
6. Exploratory and temporal analysis, including history and cold starts.
7. Preparation decisions and final feature groups.
8. Task 1 synthesis, limitations, and next steps.

For each important result, use: **question → evidence → interpretation → decision**.
Keep the field dictionary and decision table in the notebook rather than maintaining
duplicate standalone documents. A decision row needs the variable/group, issue,
evidence location, action or retention, rationale, and where any parameters are fitted.

## Proposed feature policy (to validate, not an analysis result)

| Group | Initial treatment and questions |
| --- | --- |
| Start context | Consider start-time calendar features, location, district, weather, and tariff. Check parsing, missingness, and real availability. |
| Order creation time | Use only after confirming its relationship to session start and availability at that instant. |
| Post history | Consider provided `post_*` features; understand windows, smoothing, units, and no-history indicators. |
| User history/activity | Consider `user_*` features and `is_new_user`; check meaning, cold starts, privacy, and operational access. |
| Raw user/post identifiers | Retain for audit/grouping. Decide predictive use separately based on cardinality, privacy, memorisation, and unseen-entity performance. |
| Post-session information | Exclude `end_cause`, `End Time`, `Payment time`, final energy, costs, and payments from predictors, including derived features. They may support target construction or auditing only where justified. |

Do not drop suspicious extremes or duplicates automatically. First determine whether
they are errors, repeated records, or valid sessions. Do not interpret absent history
as ordinary missing data without checking the associated flags and definitions.

## Evaluation and preparation safeguards (team proposal)

- Prefer a chronological evaluation that reflects predicting future sessions; choose
  dates after inventory rather than assuming a split ratio.
- Keep labels from sessions not yet completed at a training cutoff out of that
  training set. End timestamps can support this audit without becoming predictors.
- Basic schema/quality/coverage checks may inspect the supplied data; clearly mark
  any whole-period descriptive summaries. Use training data for adaptive exploration
  and choices, validation for comparison, and the held-out test only for final evaluation.
- Fit imputers, scalers, category grouping, thresholds, selection, and any resampling
  inside the training partition/fold. Apply fitted transformations unchanged to
  validation/test data. Resample training data only, if evidence justifies it.
- Keep the supplied chronological histories. Do not rebuild them unless needed.
  Later-period histories can contain outcomes of sessions completed before that
  prediction, including earlier evaluation-period sessions, if simulating continuously
  updated production history. State that evaluation assumption explicitly.
- Plan unseen-category handling and report cold-start/unseen-user or post behaviour
  where sample sizes permit. Fix random seeds for stochastic steps when implemented.

## Later project stages — provisional until later briefs arrive

1. Reconcile the next brief with REQUIREMENTS.md before adding scope.
2. Establish a simple baseline and a small justified set of classifiers using the
   same partitions and appropriate preprocessing.
3. Choose metrics from class balance and the cost of missed abnormalities versus
   false alarms. Candidate measures include precision, recall, PR-AUC, and a confusion
   matrix; thresholds and hyperparameters must be chosen without test feedback.
4. Compare start context alone, context + post history, context + user history,
   and context + both. Keep identifier policy, splits, metric definitions, and tuning
   effort consistent so feature-group ablation is interpretable (R3).
5. Evaluate the chosen approach once on the held-out test, investigate limitations
   and subgroup/time behaviour, and finish the report with privacy, generalisation,
   cold-start, operational assumptions, and reproducibility details.

## Submission check

- [ ] Target definition is official and the feature audit enforces prediction-time availability.
- [ ] Quality and temporal findings have evidence and modelling implications.
- [ ] Every material preparation choice is justified; learned steps use training data only.
- [ ] Retained groups, unresolved assumptions, and future evaluation implications are explicit.
- [ ] Notebook runs top-to-bottom with the documented environment and relative paths.
- [ ] Report explains decisions/results without copying code; teammate has reviewed both files.
- [ ] Current deadline, file format, and submission channel are confirmed.
