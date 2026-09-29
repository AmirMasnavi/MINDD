# Project overview

## Purpose

Predict whether an electric-vehicle charging session will end abnormally using
only information available when the session starts. The intended benefit is earlier
monitoring and better maintenance and service decisions.

Target: `is_Abnormal = 1` for abnormal sessions and `0` for normal sessions.
The local CSV currently lacks this column; resolving its definition is the first
data dependency. We must not infer the label mapping from names alone.

## Scope

The supplied four-page brief gives detailed instructions for **Task 1: understand,
audit, and prepare the data**. Its broader project goal includes classification,
critical evaluation, and historical-feature ablation. Detailed later-task briefs,
deadlines, required models, metrics, and report limits have not been supplied.

For now, deliver a justified preparation strategy supported by a notebook and a
concise report section. This setup phase creates documentation and the local
environment only. Start implementation only when the user asks to proceed.

## Approach

1. Resolve the target and define which inputs exist at prediction time.
2. Audit quality, distributions, and change over time before choosing corrections.
3. Design preparation and evaluation to avoid future information leaking into training.
4. Explain each material finding and preparation decision in the report.
5. Later, compare simple baselines and justified classifiers, including comparisons
   with and without charging-post and user history, under a common evaluation design.

The original research dataset is described as 441,077 transactions over two years,
13 stations, and three districts. These are background facts from PDF p. 1,
**not verified dimensions of the supplied educational CSV**.

## What success means

Task 1 is complete when the team can explain the data's main characteristics and
problems, show evidence for preparation decisions, identify eligible feature groups,
state limitations, and explain implications for future models and evaluation.
Plots and cleaning operations count only when they serve an analytical purpose.

Keep one notebook and the small documentation set linked in README.md. Add a report
file when actual evidence exists. Additional scripts, dashboards, models, tracking
services, and documentation folders are unnecessary at this stage.
