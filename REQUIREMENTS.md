# Assignment requirements

Source: [TP1-MINDD2026_27-Task1.pdf](TP1-MINDD2026_27-Task1.pdf), four pages,
MINDD 2026/2027, Project 1. This is a requirements summary, not analysis results.
The PDF takes precedence; team proposals are labelled separately in PLAN.md.

## Required outcomes

| ID | Requirement | Source | Evidence to produce |
| --- | --- | --- | --- |
| R1 | Predict binary `is_Abnormal` at session start, using only information reasonably available then. | p. 1 | Target definition and feature-eligibility rationale |
| R2 | Understand the provided historical variables, assess operational availability, and discuss privacy, generalisation, and cold starts. Reconstruction is not required. | pp. 2–3 | History definitions, assumptions, and limitations |
| R3 | Evaluate historical attributes through feature-group ablation. | p. 3 | Plan now; later compare models with and without history groups |
| R4 | Systematically and critically analyse the data before developing classifiers and define a justified preparation strategy. | p. 3 | Audit findings and preparation decisions |
| R5 | Investigate suspected quality problems before correction; justify retaining, transforming, imputing, grouping, capping, or removing data using evidence and variable meaning. | p. 3 | Decision, evidence, rationale, and impact for each material operation |
| R6 | Use appropriate numerical summaries and figures, interpreting their meaning and modelling implications in the report. | p. 3 | Question-driven summaries and interpreted figures |
| R7 | Investigate temporal changes in session volume, class prevalence, predictors, and user/post activity; explain implications for development and evaluation. | p. 3 | Time-based comparisons and conclusions |
| R8 | End Task 1 with a concise synthesis of key characteristics/problems, evidence for preparation, retained variables/groups, unresolved limitations/assumptions, and implications for models/evaluation. | p. 4 | Closing notebook and report synthesis |
| R9 | Every weekly submission includes the corresponding notebook and a concise report section explaining decisions, evidence, results, and conclusions. The report should not reproduce source code. | p. 4 | Notebook plus reasoned report section |

The PDF suggests, without making an exhaustive checklist: types and meanings,
missingness, duplicates/inconsistencies, temporal coverage, class distribution,
numerical distributions/outliers, categorical cardinality/rare categories,
relationships, and data-quality issues (p. 3). Select relevant investigations and
justify omissions. Quality is assessed through depth, relevance, justification,
and interpretation, rather than the number of plots or operations (p. 4).

## Data and prediction-time constraints

- Identification/location: user, charging post, station location, district.
- Transactions: order creation, energy, charges/payments, start/end/payment times,
  and termination reason. Presence in the CSV does not make a variable eligible.
- Weather: explicitly treat temperature, humidity, and precipitation as estimates
  or forecasts available at session start (p. 2).
- Tariff: `electricity_price` and `tariff_period` apply at session start (p. 2).
- Post/user history: prior completed-session counts, abnormal counts and smoothed
  rates, elapsed time since prior events, and indicators for missing history/new users.
- `user_active_sessions_at_start` represents concurrent account activity separately.
  Earlier-started sessions still active at prediction time were excluded from
  outcome-derived historical attributes. The brief states that histories were
  constructed chronologically to exclude the current and future sessions (p. 3).

## Source ambiguity and local mismatch

1. **Missing target:** the local CSV header contains 47 fields and `end_cause`, but
   no `is_Abnormal`. Obtain the official target field or mapping and handling of
   unknown/missing termination reasons. Do not fabricate labels.
2. **Exact names differ:** PDF `End cause` is CSV `end_cause`; PDF
   `Transaction power/kWh` is CSV `Transaction power/kwh`. Use actual CSV names.
3. **Incomplete sentence:** the final paragraph on p. 3 lists learned preparation
   operations (imputation, scaling, category grouping, outlier thresholds, resampling,
   feature selection, dimensionality reduction) but its sentence is malformed in
   the rendered PDF. Seek clarification. Our separate methodological proposal is
   to fit every learned operation on training data only and document it individually.
4. Due dates, team roles, submission channel, report length, target mapping, and
   detailed later-task requirements are not specified in this supplied brief.
