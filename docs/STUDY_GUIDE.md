# Project 1 study guide (MINDD 2026/27)

Classification of electric-vehicle charging sessions that end abnormally.
Group: Amir Masnavi, Inês Oliveira and Manuela Leite.

English version of `docs/GUIAO_ESTUDO.md` (Portuguese). Both have the same content, sections and numbers.

## How to use this guide

This guide explains the project from scratch. You do not need to know data science to follow it. Every number comes
from the final report (`docs/FINAL_REPORT.pdf`), and next to each one we give the chapter or table it comes from, so
anyone can check it. When we write "Part 4, Section 9", we mean the merged notebook `MINDD_Project1.ipynb`: Part 4 is
Task 4, and Section 9 is the same Section 9 that `Task4.ipynb` had.

Everyone starts with the common core, which takes about 15 minutes to read, and keeps the glossary at hand. Then each
person studies their own part, in under 2 hours:

| Who | Part of the project | Notebook | Report |
| --- | --- | --- | --- |
| Amir | Task 1: understand, audit and prepare the data | Part 1 | Chapters 1 to 3 |
| Inês | Task 2: define the problem and the evaluation; Task 3: ablation and models | Parts 2 and 3 | Chapters 4 and 5 |
| Manuela | Task 4: optimisation, threshold and test; Task 5: final analysis; final model | Parts 4 and 5 | Chapters 6 to 9 |

Each part ends with an "If you only have 30 minutes" list and with likely questions from the instructor, each with a
model answer. The common questions at the end are for everyone. The rehearsal plan, at the very end, explains how to
practise in pairs.

One tip for any spoken answer: start with the decision, give one number that supports it, and say what we did not do
and why. That is how the report is written, and it is what the instructor will look for.

---

## Common core (for everyone)

### The project in one paragraph

An electric-vehicle charging company wants to know, at the moment a charging session starts, whether that session
will end badly: for example because the charging post breaks down, communication fails or the car's battery has a
problem. If it can predict that, it can watch the riskiest posts more closely and send a technician before problems
pile up. The question in the assignment is how far the information available when the session starts (where, when,
the weather, the history of the post and of the user) can predict that abnormal ending. Our short answer is that it
gives a good ranking of the posts that are failing right now, mostly thanks to the recent failure history of the
post, but it cannot see failures that come without warning.

### The data

The file has 441,077 charging sessions and 47 columns, from 31 December 2019 to 31 December 2021, at 92 charging
posts in 13 stations and 3 districts of Jiaxing, China (chapter 1). It is an educational version of a dataset
published by Zhang et al. (2025). The columns fall into groups: identification (user, post), location (station,
district), transaction (energy, costs, start, end and payment times, end cause), weather (temperature, humidity,
precipitation), tariff, and a set of precomputed history columns: how many sessions and how many failures the post or
the user had in the last 1, 7, 30 days, and so on.

### The target

The file did not include the `is_Abnormal` column, only `end_cause`, with 15 values. We decided that a session is
normal when it ends with "Charging ends normally" or "User stops charging" (the user chose to stop). The other 13
causes are faults, so they count as abnormal. With this definition, 18.58% of the sessions are abnormal, about 1
abnormal for every 4.4 normal ones (Table 1.1). We confirmed the definition with the dataset's own history columns: we
recounted the failures with our rule and they match in 100.00% (post) and 99.98% (user) of the rows.

### The five tasks, one line each

1. Task 1: get to know the data, check its quality, see what changes over time, decide what can be used and prepare
   the data.
2. Task 2: define exactly what is predicted and how it is evaluated (metrics, time-based split, baselines), before
   training any model.
3. Task 3: measure which groups of information help (ablation) and train individual models and ensembles.
4. Task 4: tune the best models, choose the final model and the threshold, freeze everything and evaluate once on the
   test period.
5. Task 5: compare the final model with the baseline on the test using every measure the brief asks for, see where it
   fails and explain what it means for the operator.

### The final model and the numbers everyone must know

The final model is a gradient boosting model (many small trees, each correcting the errors of the previous ones) with
depth 6, learning rate 0.1, 200 iterations and at least 100 sessions per leaf, on 27 features (Table 8.2). The
threshold is 0.490: the value that raises an alert on 10% of the development sessions.

| Measure (source) | Final model | B1 (post failure rate over 7 days) | B0 (no skill, random) |
| --- | --- | --- | --- |
| Mean PR-AUC over the 4 development folds (Table 8.1) | 0.626 | 0.511 | 0.181 |
| PR-AUC on the test period (Table 8.1) | 0.532 | 0.381 | 0.178 |
| Alerts on the test with the frozen threshold (Table 7.1) | 7.4% of sessions | | |
| Per 1,000 test sessions (Table 7.1) | 50.3 correct alerts, 24.0 false, 125.6 missed failures | | |

The model beats B1 in every fold, in every district and in every station of the test (chapter 7).

### The frozen-test rule

We kept the last three months (October to December 2021, 80,081 sessions) as the final test and did not touch them
during development. We chose the model, features, hyperparameters and threshold using only the earlier data. We wrote
those choices to a file on 27/10/2026 at 11:40:32, and only then evaluated the test, once. Nothing changed after we
saw the result. Later runs (the Task 4 reproduction, Task 5 and the merged-notebook run) used the same frozen file,
gave the same numbers and were not used to choose anything.

---

## Glossary

| Term | What it means | Example in our project |
| --- | --- | --- |
| Dataset | The data as a table, where each row is a case and each column a characteristic | Each row is a charging session |
| Feature (predictor) | A column the model uses to predict | Start hour, temperature, the post's failure rate |
| Target | What we want to predict | `is_Abnormal`: 1 if the session ends badly, 0 if it ends well |
| Positive / negative class | The two values of the target. The positive one is what we look for | Positive: abnormal session. Negative: normal session |
| Leakage | Using information that would not be available at prediction time. It gives falsely good results | Energy delivered is only known at the end, so it cannot predict the end |
| Class imbalance | One class is much rarer than the other | 18.6% abnormal against 81.4% normal |
| Missing values | Empty cells (NaN) | "Hours since the post's last failure" is empty if the post never failed |
| Outlier | A value far from the others. It can be an error or a real case | An account with more than 500 sessions (a fleet) |
| IQR | Interquartile range, the "Tukey fences" rule for spotting outliers | Used in Part 1, Section 10.1 |
| Isolation Forest | A method that looks for rare cases using several columns at once | The sessions it flagged were 60% abnormal |
| Encoding | Turning categories into numbers | Districts A, B, C become 0, 1, 2, or three 0/1 columns (one-hot) |
| Scaling | Putting columns on a similar scale | Mean 0 and standard deviation 1 for logistic regression |
| Log transform | Taking the logarithm to "shrink" very large values | `log1p` on counts with long tails |
| VIF | Measures how much a variable is explained by the others. Above 10 means redundancy | The user's 180- and 730-day windows reach 65.4 |
| PCA | Combines correlated variables into a few components | Tested and not used |
| Temporal split | Train on the past and evaluate on the future, instead of shuffling at random | Training until June 2021, test October to December 2021 |
| Burn-in | An initial period that is not used | Until 31/03/2020, because the history columns were still incomplete |
| Fold | One train/validation split. Evaluating on several folds shows how stable a model is | We used 4 folds, one per quarter |
| Expanding window | Each fold trains on everything before its validation quarter, so training keeps growing | Fold 1 trains on 6 months, fold 4 on 15 |
| Purge gap | Removing from training the sessions whose outcome is only known after the boundary | 27 to 39 sessions per fold |
| Baseline | A simple reference. A model is only worth it if it beats the baseline | B0 random, B1 post failure rate over 7 days |
| Precision | Of the alerts raised, how many were real failures | 0.677 on the test: 68 of every 100 alerts are real |
| Recall | Of the failures that happened, how many we caught | 0.286 on the test: we caught 29 of every 100 failures |
| F1 | Harmonic mean of precision and recall | 0.402 on the test |
| PR-AUC | Area under the precision-recall curve. Summarises the ranking quality over all thresholds. Its "random" value is the share of positives | 0.532 on the test against 0.178 at random |
| ROC-AUC | Probability that an abnormal session gets a higher score than a normal one. 0.5 is random | 0.794 on the test |
| Lift | How many times the PR-AUC is above random | 3.03 on the test |
| Balanced accuracy | Mean of the recall of the two classes. 0.5 is random | 0.628 on the test |
| MCC | Correlation between prediction and reality, from −1 to 1. 0 is random | 0.373 on the test |
| Threshold (cut-off) | The score above which an alert is raised | 0.490 |
| Alert rate | Share of sessions with an alert | 10% on development, 7.4% on the test |
| Alert budget | How many alerts the team can handle, as a share of sessions | We tested 5%, 10% and 20% |
| Overfitting | The model memorises the training data and fails on new data | A depth-16 tree with leaves of 50 sessions |
| Hyperparameter | A setting chosen before training | Tree depth, learning rate |
| Ensemble | Combining several models | Random forest, gradient boosting, stacking |
| Bagging / random forest | Many trees trained on different samples; their average lowers the variance | 200 trees |
| Boosting | Trees in sequence, each correcting the errors of the previous ones, which lowers the bias | Our final model |
| Stacking | A meta-model learns how to combine the predictions of other models | Logistic regression on top of LR, Naive Bayes and a tree |
| Calibration | Whether the score can be read as a probability | A score of 0.74 corresponds to about 74% real failures |
| Brier score | Mean error of the probabilities. Lower is better | 0.103 on development |
| Permutation importance | Shuffle a column and measure how much the model gets worse | Shuffling the post history removes 0.366 of PR-AUC |
| Partial dependence | How the average score changes when one variable changes | The score rises sharply when the post's 1-day rate passes 0.3 |
| Drift | The data change over time | The abnormal share goes from 26.3% to 13.7% and then to 22.9% |
| Cold start | There is no history for a new case | New users: the model has less information about them |
| Ablation | Removing or adding groups of variables to measure what each one is worth | Sets S1 to S4 in Task 3 |
| Bootstrap | Resampling with replacement to estimate uncertainty | Standard error of the PR-AUC of 0.004 to 0.006 |
| McNemar | A test that compares two classifiers on the same sessions | The model alone is right 4,283 times, B1 alone 2,223 |

---

## Amir's part: Task 1, understand, audit and prepare the data

Part 1 of the notebook, chapters 1 to 3 of the report.

This part answers two questions: can we trust the data, and what can we use to predict? Everything the other tasks
do rests on the decisions made here.

### Step by step

#### Sections 2 to 4: load, describe and clean

We read the file and looked at each column: type, meaning and when it is known. Then we ran the quality checks of
Table 2.1. We found extra tabs at the end of some dates and in 18,370 location values, and stripped them on load.
There are no repeated rows. There are 17 pairs where the same account starts on two posts in the same second; these
are fleet accounts, so they stayed. There are no negative values and no sessions that end before they start.
Durations stop at 23.99 hours, which looks like a system limit. There are 54,621 sessions with zero energy, but energy
is an end-of-session column, so we do not use it anyway. Overall the data are in good condition, and before
correcting anything we checked whether it really was an error.

#### Section 5: build the target

This is the most important decision of the task, explained in the common core. We decided that "User stops charging"
counts as normal, because the user chose to stop. The evidence is that, with this rule, the dataset's history columns
match in 100.00% and 99.98% of the rows. With the alternative (only "Charging ends normally" is normal) they match in
0.26% and 35.85%, and the abnormal share would rise to 53.93% (Table 1.1). We also noticed that the failure rates are
already smoothed, (failures + 1) / (sessions + 5), so a post with no history gets 0.2. There are 9,058 normal
sessions (2.5%) that delivered no energy, almost always users who stopped after a minute. They stayed normal, because
removing them would require the energy, which is only known at the end.

#### Section 6: missing values

They only appear in 4 "time since the last session or failure" columns, and every empty cell matches its "no history"
flag. Empty means "this never happened", not "we don't know". We decided not to delete rows or fill in the mean. For
the trees we leave the empty cell, because the model can handle it. For logistic regression we fill in the training
maximum, reading "never happened" as "happened a long time ago", and keep the flag.

#### Section 7: changes over time

The data are not stable (Figure 2.3). Volume drops to 1,391 sessions in February 2020, probably because of COVID-19,
and reaches 25 to 28 thousand a month in autumn 2021. The abnormal share falls from 26.3% to 13.7% and rises again to
22.9%. The type of fault changes too: connection faults add 7.1 points to the abnormal share in the first quarter of
2020 and only 1 to 2 points from the third quarter on. At the start of the file the history is still incomplete, so
31% of the January 2020 sessions look like new users, against 9 to 15% later. One thing is stable: each post's
failure share is similar in 2020 and 2021 (Spearman 0.81), which is why post history works. From this we decided to
split the data by time and not at random. A random split would mix different periods and give results that are too
optimistic.

#### Section 8: leakage, or what is known at the start

Seven columns only exist after the session: energy, electricity cost, service charge, amount, actual payment, end
time and payment time. On their own they separate the classes with a ROC-AUC of 0.82 to 0.85, better than any
start-time variable (the best has 0.77), and that is exactly why they are dangerous: they describe the outcome, they
do not predict it (Figure 2.1). Abnormal sessions are short and deliver little energy. We excluded them all. The order
creation time was the hard case: it appears after the start in 56% of the sessions, sometimes 16 hours later, and its
link to the outcome is weak (AUC 0.59). Since we cannot be sure it exists at prediction time, we excluded it too.
Weather has only one value per district and day; we followed the brief and treat it as a forecast known at the start.

#### Section 9: exploring the predictors (training period only)

We measured relationships on the training period only, so that validation and test do not influence our choices.
Location matters mostly at post level: districts go from 14.6% to 24.1% abnormal, stations from about 8% to 38% and
posts from 4.1% to 60.9%. The 10 worst posts produce 24.1% of the failures with only 10.2% of the sessions. Hour and
weekday move things little (14.7% to 20.5% and 17.0% to 18.9%) and weather has weak effects. History is the strongest
signal (Figure 2.2): splitting the post's 7-day failure rate into deciles, the abnormal share goes from about 4% in
the lowest decile to about 60% in the highest. A post that failed recently tends to fail again. User history also
helps, but less (AUC 0.69 to 0.70 against 0.75 to 0.77 for the post). Users are very unequal: 45% of the 34,294
training accounts have a single session, but the most active 1% of accounts make 34% of the sessions. New users fail a
little more often (20.2% against 17.5%).

#### Section 10: outliers

First we applied the IQR rule, which showed long tails in counts and times (skewness 3 to 9). Then we looked at the
extreme cases one by one: posts idle for more than 14 days (39% failures when they come back), 21 accounts with more
than 500 sessions and two storm days. Finally we ran Isolation Forest, and the sessions it flagged were 60% abnormal.
The extremes are real and informative, so we removed no row. For linear models we apply `log1p`, which shrinks the
tails without deleting anything.

#### Section 11: time-based split

We left out the burn-in (until 31/03/2020, 14,017 sessions), because the history was incomplete and the fault mix of
that period no longer exists. The rest was split by date (Table 3.1): training from April 2020 to June 2021 (271,182
sessions, 17.8% abnormal), validation from July to September 2021 (75,769, 21.1%) and test from October to December
2021 (80,081, 17.6%). We purged 28 training sessions that ended after the boundary, because their outcome would only
be known later. This split showed two things. First, 39.9% of the validation sessions and 61.3% of the test sessions
come from accounts never seen in training, so `user_id` cannot be a feature. Second, every validation and test post
was already in training, so we cannot test a new post.

#### Section 12: features and reduction

We kept 29 features in 7 groups: calendar (hour and weekday), tariff, location (post, station, district), weather
(temperature, humidity, precipitation and a new `rain_flag`), post history (8), user history (10) and concurrency (1).
We removed redundant columns (Table 3.2): the electricity price, which the tariff fixes, six failure counts that are
exact functions of other columns, two flags that are always 0 after the burn-in, and one repeated flag. Some features
are highly correlated: the user windows reach a VIF of 65.4, because the 180- and 730-day windows hold almost the same
sessions. Trees and regularised models cope with that. For plain linear models we built a reduced set, 19 of the 23
numeric variables, with a maximum VIF of 8.6. We also tested PCA: it needs 11 of 23 components to keep 90% of the
variance, and the first component hardly separates the classes (AUC 0.51). It compresses little and mixes post and
user information, so we did not use it.

#### Section 13: learned operations and imbalance

We prepared two versions of the data. The tree version keeps the raw values, the empty cells and the category codes.
The linear version applies `log1p` to 8 columns, fills the empty cells with the training maximum, scales, encodes hour
and weekday with sine and cosine (because they are circular: hour 23 is close to hour 0) and one-hot encodes the post
and the tariff, which gives 126 columns. Everything that learns something from the data (means, deviations, category
lists, fill values) is learned on the training period only (Table 3.3). To show why this matters: if we learned from
all periods, the fill value for "days since the user's last failure" would move from 543 to 702 days, which is future
information leaking into training. As for the imbalance (1 to 4.4), we neither resampled nor used class weights. The
models learn the real proportion and are judged with metrics that it does not fool. We also did not use SMOTE, because
it would invent impossible sessions, such as half a flag or a mix of two posts.

#### Sections 14 and 15: files and synthesis

The notebook saves the prepared data, the feature groups, the decision log and the ledger of learned operations, and
ends with the synthesis the brief asks for. In the report, that synthesis is part of chapter 9.

### If you only have 30 minutes

- The target comes from `end_cause`: 13 fault causes are abnormal, and "user stops" is normal. That gives 18.58%
  abnormal and matches the dataset's history in about 100% of the rows.
- Seven end-of-session columns plus `end_cause` are leakage. The order time was also dropped, because its timing is
  uncertain.
- Weather is treated as a forecast, as the brief says.
- We removed no row: there are no true duplicates, empty cells mean "never happened" and the extremes are real.
- The data change over time (volume, abnormal share, fault type), so the split is by time, with a burn-in and a purge.
- The strongest signal is the post's recent failure history: from 4% to 60% abnormal between the lowest and highest
  decile.
- 29 features in 7 groups remain. PCA was tested and rejected. High VIF only appears in the user windows.
- Everything that learns from the data is learned on the training period only (example: 543 against 702 days).
- No resampling and no SMOTE: the models learn the real proportion.
- `user_id` cannot be a feature, because 61.3% of the test sessions come from new accounts.

### Leads into

Task 2 uses the 29 features, the time split and the "learn on training only" rule to build the folds and the
protocol. Task 3 uses the two versions of the data, one for trees and one for linear models.

### Likely questions on Task 1

1. **How did you define the target, and why is "User stops charging" normal?**
   It is normal because stopping is the user's choice, not a fault. The other 13 causes are equipment, communication
   or vehicle faults. We tested this definition by recounting the failures in the dataset's history, and it matches in
   100.00% (post) and 99.98% (user) of the rows; the alternative only matches 0.26%. See chapter 1.1.

2. **Why didn't you remove any rows?**
   Because we investigated each problem before acting and none was an error. There are no true duplicates (the 17
   pairs are fleet accounts), empty cells mean "never happened" and the extremes are real situations, such as posts
   idle for a long time or fleet accounts. The sessions Isolation Forest flagged as unusual were 60% abnormal, so
   deleting them would delete the signal. See Table 2.1.

3. **How did you handle missing values?**
   Empty cells only appear in 4 "time since the last session or failure" columns, and each one matches the "no
   history" flag. For the trees we left them, because the model sends them to the right side of each split. In the
   linear version we filled in the training maximum and kept the flag. We did not use the mean, because "never
   happened" is not an average value. See Section 3.3.

4. **How did you check there is no leakage?**
   We classified each column by the moment it becomes known. The seven end-of-session columns have a ROC-AUC of 0.82
   to 0.85, above anything known at the start (0.77), because they describe the outcome. They were all removed, and so
   was the order time, which appears after the start in 56% of cases. Also, everything that learns from the data is
   learned on the training period only. See Section 2.1.

5. **What changes over time did you find, and what do they mean for evaluation?**
   Volume, the abnormal share (26.3%, then 13.7%, then 22.9%) and the fault type change. So we cannot shuffle the data:
   we always evaluate on the future relative to training, and we read every PR-AUC next to the abnormal share of its
   period. See Section 2.4.

6. **Why did you leave out the first three months?**
   At the start of the file the history is still filling up: 31% of the January 2020 sessions look like new users,
   against 9 to 15% later. Also, the connection faults of that period almost disappeared later. Those months would
   teach the model a pattern that no longer exists. See Section 3.1.

7. **What is the purge and why is it needed?**
   A session's outcome is only known when it ends, up to 24 hours later. A session that starts before the training
   boundary and ends after it has an outcome "from the future". We removed those 28 sessions from training so that
   outcome does not enter the model. See Section 3.1.

8. **Why didn't you use PCA?**
   We tested it: it needs 11 of 23 components to keep 90% of the variance, and the first component hardly separates the
   classes (AUC 0.51). It compressed little, mixed post and user history, and would make the model harder to explain.
   See Section 3.2.

9. **Why didn't you balance the classes with SMOTE or undersampling?**
   The imbalance is moderate (1 to 4.4), and we evaluate with PR-AUC and alerts per 1,000 sessions, which the majority
   class does not fool. SMOTE would create impossible sessions, such as half a flag. If we had resampled, it would only
   be inside the training window of each fold, so validation and test keep the real proportion. See Section 3.3.

10. **Can weather really be used at the start?**
    There is only one value per district and day, so it is not the exact weather of the session. The brief tells us to
    treat it as a forecast known at the start, which is what we did. We listed this as a limitation. In any case, the
    model barely uses it (importance below 0.002). See Sections 2.1 and 6.6.

---

## Inês's part: Task 2 (problem and evaluation) and Task 3 (ablation and models)

Parts 2 and 3 of the notebook, chapters 4 and 5 of the report.

Task 2 sets the rules of the game before playing: what is predicted, with which variables, how it is measured and
what it is compared with. Task 3 plays by those rules: it measures which information helps and trains the first
models.

### Task 2 step by step (Part 2)

#### Section 3: the problem

The unit is one charging session. The positive class is an abnormal ending. The prediction is made once, at the start
of the session, using only what is known at that moment. We designed the use as preventive monitoring and
maintenance priority: the sessions that are starting, and through them the posts, are ranked by risk, and the
operator, who has limited capacity, looks at the riskiest first. An alert means "this session, on this post, has a
higher risk of ending badly". It is not a diagnosis and it does not say which fault will happen. In the development
period (April 2020 to September 2021) there are 346,979 sessions, 18.5% abnormal.

#### Section 4: which variables can be used

We placed each of the 47 columns in one of the brief's four categories (Table 4.1): 27 eligible, 1 only to build the
target (`end_cause`), 7 generated during or after the session, and 12 excluded for another reason (`UserID`, the order
time and 10 redundant columns). The notebook checks in code that every column appears exactly once. `UserID` is
excluded because 35% to 46% of each fold's validation sessions come from accounts not in the training window: the
model would only memorise accounts and would identify people. User history is the legitimate substitute. `post_id` is
also an identifier, but the post is known at the start, so it stayed at this stage (Task 3 later removed it).

#### Section 5: the cost of the two errors

A false positive is an alert on a session that ends well; a false negative is a failure that passes without an alert.
Per event, the false negative is worse: an alert leads to a cheap action (watch or inspect), while an unseen failure
leaves a broken post in service, and failures come in clusters on the same post. But the number of false alerts is
limited by the technicians' capacity, and a huge list of alerts is useless. We do not know the cost ratio
c = cost(FN) / cost(FP). With calibrated probabilities, the best threshold would be 1/(1+c): 0.50 for c = 1, 0.33 for
c = 2 and 0.17 for c = 5. Since fixing a threshold at this stage would be arbitrary, we chose metrics that judge the
ranking and report results for three alert budgets: 5%, 10% and 20% of the sessions.

#### Section 6: metrics

The primary metric is PR-AUC (Table 4.2). It measures how precise the alerts stay as we catch more failures, and it
ignores the true negatives, which are the majority. Its limitation is that its random value is the abnormal share,
which changes between periods, so we always read it next to that share, or as a lift. The complementary metrics are
ROC-AUC, which does not depend on the abnormal share and can therefore be compared across periods, and the Brier score
and log-loss, which measure the quality of the probabilities. The operational ones are precision, recall and correct,
false and missed alerts per 1,000 sessions, for each budget. For stability we look at the value in each fold, the
standard deviation, the worst fold, the trend and the folds won. We do not use accuracy, because always predicting
"normal" is right in 79% to 84% of each fold's sessions and catches no failure. F1 only appears once there is a
threshold.

#### Section 7: temporal evaluation

We split the development period into four expanding-window folds, one per quarter (Table 4.3). Fold 1 trains until
30/09/2020 (111,470 sessions) and validates on Oct–Dec 2020 (60,364). Fold 4 trains until 30/06/2021 (271,182) and
validates on Jul–Sep 2021 (75,769). The boundaries are calendar quarters, fixed before seeing any result. A quarter is
large enough for a stable estimate (each has at least 6,600 abnormal sessions) and short enough to show changes. Four
folds are a compromise: an earlier fold would train on less than six months, and monthly folds would give 12 small,
noisy estimates. The folds have different sizes, and the first ones train on less data and without a full winter, so
we expect them to be a bit pessimistic. In each fold, the 27 to 39 sessions still running at the boundary are purged,
and all preprocessing is fitted again inside that fold's training window. The test is removed right after reading the
file, and we only count its rows.

#### Section 8: aggregating the folds

We rank models by the simple mean of the four fold PR-AUCs, so each period counts once. We also report the mean
weighted by the number of sessions and the pooled value (all predictions together), which is what we use to choose the
threshold. Since the abnormal share changes between folds, we do not compare folds with each other, but we do compare
two models within the same fold: paired differences and number of folds won. We do not claim statistical
significance, because with four folds the smallest possible p-value of an exact Wilcoxon test is 0.125, even if one
model wins every fold.

#### Section 9: baselines

B0 is chance: random scores. Its PR-AUC is each fold's abnormal share (mean 0.181). B1 uses one dataset column as its
score, the post's failure rate over the last 7 days, and learns nothing. It is already strong: mean PR-AUC 0.511,
ROC-AUC 0.772, worst fold 0.456 in fold 2 (Table 4.4). With a 5% budget, 74% of its alerts are real failures, but it
only catches 21% of the failures (Table 4.5). A model is only worth its complexity if it catches more failures than
B1 with the same budget.

#### Section 10: protocol

Table 4.6 summarises everything, and the notebook saves it to `prepared/task2_protocol.json`. The later tasks read
that file and use exactly the same features, folds and metrics.

### Task 3 step by step (Part 3)

#### Section 3: feature-group ablation

We compared the four sets the brief asks for, always with the same reference model, an untuned gradient boosting.
That way the differences come from the information and not from tuning. We treat differences below 0.005 as
negligible; a bootstrap gives a standard error of 0.004 to 0.006 for one PR-AUC, which sets the scale of that
tolerance. Results (Table 5.1):

| Set | Features | Mean PR-AUC | Gain |
| --- | --- | --- | --- |
| S1 context and weather | 9 | 0.290 | |
| S2 + tariff | 10 | 0.290 | +0.0006 |
| S3 + post history | 18 | 0.584 | +0.294, in all 4 folds |
| S4 + user history | 29 | 0.615 | +0.031, in all 4 folds |
| Selected (S4 without `post_id` and tariff) | 27 | 0.626 | |
| Selected without user history | 16 | 0.599 | |

These give the answers to the brief's questions. The tariff adds nothing beyond the hour, because the tariff period is
a function of the start hour and the model can rebuild it. Post history is by far the most useful group: it raises
PR-AUC from 0.290 to 0.584, with gains of +0.249 to +0.360 in each quarter, and with it the model is already above B1
in every fold. User history helps less (+0.031), always in the same direction, but the gain shrinks from +0.044 in
fold 1 to +0.018 in fold 4. For returning users PR-AUC rises from 0.609 to 0.640; for new accounts (about 13% of the
sessions) it barely changes. The order of the sets is the same in every fold, so the effect is consistent over time,
although the size of the gains varies. Then we removed `post_id` (PR-AUC rises +0.0107 in all four folds, which shows
the post's identity adds nothing once the history is there) and the tariff (+0.0003). We ended with 27 features.

There are also operational and ethical concerns. Post history needs a live record of finished sessions, which always
lags. If alerts lead to maintenance, failures may drop and the history may change. User history is a behaviour profile
tied to an account: a driver who used a broken post may get a higher score and be "blamed" for an equipment fault. We
kept it because it improves the ranking, but only to rank sessions internally, never to make a decision about a
driver. The model without user history (0.599) is the privacy alternative.

#### Section 4: individual models

The brief asks for at least three principles. We chose three families from the slides (Table 5.2). Logistic
regression is linear: the failure rate rises smoothly with the post history, and the model outputs probabilities. It
needs log and scaling and suffers from correlated variables, which the penalty controls. Naive Bayes is probabilistic,
has few parameters and a different bias, but assumes the variables are independent given the class, which the 1-, 7-
and 30-day windows violate. The decision tree makes successive splits on thresholds, which is the shape of the
relationships seen in Task 1, and needs no scaling; in return it is unstable and overfits, so we tuned the depth and
the minimum leaf size. We left out kNN, which needs a distance between counts, rates and categories and would compare
each validation session with up to 271,000 training sessions, and the kernel SVM, whose time grows between the square
and the cube of the number of sessions and which gives no probabilities. Both would force us to use a sample and throw
away the history that holds the signal. Results: tree 0.597, logistic regression 0.593 and Naive Bayes 0.525. Naive
Bayes ranks reasonably (ROC-AUC 0.814), but its probabilities are worse than a constant (Brier 0.172 against 0.148),
which is consistent with the violated independence. The tree and logistic regression reach almost the same value
despite being so different, which suggests the limit is in the available information, not in the model.

#### Section 5: ensembles

We chose one ensemble per idea. The random forest does bagging: averaging 200 trees trained on different samples
lowers the variance of an unstable tree. Gradient boosting does boosting: small trees in sequence, each correcting the
errors of the previous ones, lower the bias. Stacking combines logistic regression, Naive Bayes and the tree with a
logistic regression on top, which learns how much to trust each one. We did not use equal-weight voting, because one
of the models is much weaker. The brief warns that stacking must not leak. So we built the meta-model's predictions in
time order: inside each fold's training window, each quarter is predicted by models trained only on sessions that
started and ended before it (Figure 5.2). All three ensembles beat their components in every fold: the random forest
is +0.025 above the tree and boosting +0.028.

#### Section 6: comparison and alerts

Final ranking (Table 5.3): gradient boosting 0.626, random forest 0.622, stacking 0.610, tree 0.597, logistic
regression 0.593, Naive Bayes 0.525, B1 0.511 and B0 0.181. Boosting and the random forest are within the tolerance.
We prefer boosting because it wins three folds and is much faster to retrain. It beats B1 in every fold, by +0.103 to
+0.120 (+0.115 on average). In alerts (Table 5.4), with a 5% budget, 88% of boosting's alerts are real failures,
against 74% for B1, but the model still misses 136 of about 180 failures per 1,000 sessions.

### If you only have 30 minutes

- The prediction is a risk alert at the start of the session, for monitoring and maintenance, not a diagnosis.
- 47 columns: 27 eligible, 1 target, 7 end-of-session and 12 excluded for another reason. `UserID` is excluded because
  the model would memorise accounts and identify people.
- A false negative is worse per event, but technician capacity limits false alerts. So we evaluate the ranking and use
  budgets of 5%, 10% and 20%.
- PR-AUC is the primary metric and is always read with the abnormal share (chance). Accuracy is useless: always
  predicting "normal" is already right 79% to 84% of the time.
- Four expanding-window folds, one per quarter, with a purge. The test stays closed.
- Models are ranked by the simple mean of the folds and compared fold by fold. No significance with 4 folds (minimum
  Wilcoxon 0.125).
- B0 = 0.181 and B1 = 0.511. B1 is already strong.
- Ablation: tariff adds nothing, post history adds +0.294 and user history +0.031. 27 features remain (no `post_id`,
  no tariff).
- Three individual models (logistic regression, Naive Bayes, tree) and three ensembles (random forest, boosting,
  time-ordered stacking). kNN and SVM were left out for scale reasons.
- Winner: gradient boosting at 0.626, +0.115 above B1 and better in all 4 folds.

### Leads into

Task 4 tunes boosting, the random forest and the tree with the same folds and tolerance rule, and chooses the
threshold with the 10% budget defined here. Task 2's B1 is Task 5's baseline.

### Likely questions on Tasks 2 and 3

1. **Why did you use PR-AUC and not accuracy?**
   The abnormal class is the minority (about 18%), so always predicting "normal" already gives 79% to 84% accuracy
   without catching a single failure. PR-AUC measures how precise the alerts stay as we catch more failures, and it
   ignores the true negatives. Its limitation is that it depends on the abnormal share, so we always read it with that
   share or as a lift. See Section 4.4.

2. **Why didn't you use random K-fold?**
   The data change over time and the model will be used on future sessions. With random folds, the model would train
   on sessions from after the ones it is evaluated on and would see the future, which gives over-optimistic results.
   We used four expanding-window folds where training always comes before validation. See Section 4.5.

3. **What is the purge between training and validation?**
   A session's outcome only exists once it ends. The 27 to 39 sessions per fold that started before the boundary and
   ended after it are removed from training, so no outcome "from the future" enters the model. See Section 4.5.

4. **Why is B1 a good baseline?**
   Because it is what an operator could do today without any model: look at the posts that failed in the last week.
   It learns nothing, it is known at the start of the session, and it was the strongest signal in Task 1. It already
   reaches 0.511 PR-AUC against 0.181 by chance, so beating B1 is a serious requirement. See Section 4.7.

5. **Does the tariff add information beyond the hour?**
   No. Adding it changes PR-AUC by +0.0006, and the per-fold differences (−0.0033 to +0.0038) all stay within the 0.005
   tolerance. The tariff period is set by the start hour, so a model that already has the hour can rebuild it. See
   Section 5.1.

6. **How much is user history worth, and what problems does it raise?**
   It adds +0.031 PR-AUC in every fold, mostly for returning users (from 0.609 to 0.640), and the gain shrinks over
   time. It is a behaviour profile of a person, so we only use it to rank sessions internally and never to make a
   decision about a driver. The model without it (0.599) is the privacy alternative. See Section 5.1.

7. **Why didn't you use kNN or SVM?**
   The brief asks for three principles and we used linear, probabilistic and tree. kNN would need a distance between
   counts, rates and categories and would compare each validation session with up to 271,000 training sessions. The
   kernel SVM grows between the square and the cube of the number of sessions and gives no probabilities. Both would
   force us to use a sample and lose the history that holds the signal. See Section 5.2.

8. **How did you avoid leakage in the stacking?**
   We did not use random cross-validation to produce the meta-model's predictions. Inside each fold's training window,
   each quarter was predicted by models trained only on sessions that started and ended before it. Then the meta-model
   learned from those predictions, and assertions in the code check the dates of every fit. See Section 5.3.

9. **Why is Naive Bayes the worst?**
   It assumes the variables are independent given the class, but the 1-, 7- and 30-day windows partly count the same
   failures. It ranks reasonably (ROC-AUC 0.814), but its probabilities are overconfident: its Brier score is 0.172,
   worse than the constant's 0.148. See Section 5.2.

10. **Why can ensembles improve on individual models?**
    The random forest averages many trees on different samples, which cancels out a single tree's instability.
    Boosting corrects errors step by step, which lowers the bias of small trees. Stacking combines models that make
    different mistakes. On our data, all of them were above their components in every fold. See Section 5.3.

---

## Manuela's part: Task 4, Task 5 and the final model

Parts 4 and 5 of the notebook, chapters 6 to 9 of the report.

Task 4 turns the best model into an alert system: it tunes it, chooses the threshold, freezes everything and only then
opens the test. Task 5 studies that frozen model on the test: against the baseline, over time, by group, in its errors
and in the operator's daily work. Chapter 8 brings the final choices together and chapter 9 answers the project
question.

### Task 4 step by step (Part 4)

#### Sections 2 to 4: which models to tune and how

We tuned three models: gradient boosting, the random forest and the decision tree. They are the two best ensembles
and the best individual model of Task 3, and they cover three principles (boosting, bagging and a single tree).
Boosting and the random forest were 0.003 apart, within the tolerance, so both needed tuning before choosing. We left
out stacking (0.015 behind and very costly to tune), logistic regression (both penalties already gave the same result)
and Naive Bayes (its only setting does not touch the independence problem). Each model was searched on an explicit
grid (Table 6.1): 39, 13 and 41 configurations, 37 minutes in total. Each configuration was trained on each fold's
training window and evaluated on the following quarter, so the search respects time and never sees the test. The
objective is the simple mean of the 4 fold PR-AUCs. The choice rule, among configurations within 0.005 of the best, is
to keep the simplest. When the choice landed on the edge of a grid, we widened that grid once. We used grid search
because it lets us state the search space and procedure exactly, as the brief asks.

#### Section 5: optimised against initial

We only adopted a new configuration if it beat the Task 3 one by more than 0.005 on average (meaningful gain) and in
at least 3 of the 4 folds (stable). None passed (Table 6.2). For boosting, the search's choice is −0.002 and wins 1
fold; for the random forest, +0.001 in 4 folds; for the tree, +0.002 in 3 folds. The results are flat: 31 of the 39
boosting configurations are within 0.005 of the best. The search confirmed the Task 3 configurations, which were
already on the plateau. The final model is Task 3's gradient boosting (depth 6, learning rate 0.1, 200 iterations,
minimum leaf 100). Since it was 0.003 from the random forest, we applied the tie-break set before the search, the
better worst fold: 0.575 against 0.567. It is also about four times faster to train.

#### Section 6: the threshold

A score only becomes an alert once there is a threshold. Of the brief's criteria, we used the alert-rate constraint:
the threshold raises an alert on 10% of the sessions, so the operator inspects about 100 in every 1,000. We did not use
a cost function because we do not have the real costs, and we would have had to invent a ratio. We did not maximise
F1 either, because it gives precision and recall the same weight without an operational reason, nor did we impose a
minimum recall, which would leave the workload open. The alert budget is the one quantity an operator can set
directly. The threshold was computed on the pooled out-of-fold predictions: each of the 235,472 validation sessions was
scored by the model trained on its own fold's training window. The 90th percentile of these scores is 0.490. Table 6.3
compares it with the default threshold, 0.50: on development they are almost the same (alerts 9.7% against 10.0%,
precision 0.747 against 0.740, recall 0.395 against 0.403, F1 0.517 against 0.522). This happens because this model's
scores are close to probabilities, and about 10% of the sessions have a risk above 0.5. F1 would peak near 0.3, but
there the model would flag far more than 10% of the sessions. For the operator, 10% means 74.0 real failures and 26.0
false alerts in every 100 inspections, while 109.8 of 183.8 failures per 1,000 sessions go without an alert. Read as a
probability, 0.490 is like saying a missed failure costs about the same as a useless inspection (ratio 1.04).

#### Section 7: calibration

The threshold only uses the score as a ranking, but an operator may read it as a risk, so we checked. The Brier score
is 0.103, against 0.150 for a constant. In ten bands, the mean score and the real failure share differ by at most
0.015, and in the top band, where the alerts are, 0.738 predicted matches 0.740 observed. We did not add calibration,
because a calibration that keeps the order of the scores would flag exactly the same 10% of the sessions.

#### Sections 8 and 9: freeze and evaluate the test once

We wrote the model, the 27 features and the threshold to `prepared/task4_frozen.json` on 27/10/2026 at 11:40:32,
before reading the test. Then we trained the model on all 346,931 development sessions whose outcome was known before
1/10/2021 and evaluated the test (80,081 sessions, 17.6% abnormal) once (Table 6.4). The model has PR-AUC 0.532, three
times chance and +0.152 above B1 (0.381); B0 has 0.178. The margin over B1 is larger than on development, but the
absolute value falls 0.128 below fold 4 (0.660), about 27 standard errors, so it is a real change in that quarter and
not noise. B1 falls even more. With the threshold unchanged, the model flags 7.4% of the sessions instead of 10%, with
precision 0.677 and recall 0.286. We reported this as it came out and changed nothing.

#### Section 10: what the model uses

We measured permutation importance: shuffle the columns of one group and see how much PR-AUC drops, on the validation
quarters. Post history dominates (drops 0.366), user history comes next (0.097, and its role shrinks from 0.108 in
fold 1 to 0.067 in fold 4), location costs 0.012, and calendar, concurrency and weather less than 0.002 each (Figure
6.3). The most important single variable is the post's failure rate over the last day (0.196). The order matches Task
3's ablation, although the sizes differ, because the two methods answer different questions: permutation measures how
much this model uses a group, and ablation measures what is lost when the model is retrained without it. There are
three limits. Correlated variables share importance between them. The method measures use, not cause. And it describes
the model on validation, before the change seen on the test.

#### Sections 11 to 13

Conclusions, saved files and, in Section 13, the final comparison table and model description that appear in chapter 8.

### Task 5 step by step (Part 5)

#### Section 2: choosing the final model and the baseline

The choice uses development results only. Only the random forest (0.622) is within 0.005 of boosting (0.626), so the
decision comes from stability and cost: boosting has the better worst fold (0.575 against 0.567), less variation
across folds (0.038 against 0.042) and a fit about four times cheaper (3.3 s against 12.4 s per fold, Section 6.2).
Interpretability does not separate them, because both are tree ensembles, and the most readable model, the tree, is
0.028 behind, more than five times the tolerance. For the operator the choice changes nothing in daily work, because
the same 10% threshold turns either ranking into alerts. The baseline is B1: known at the start, it learns nothing and
it is what an operator could use today.

#### Sections 3 and 4: refit and test

We trained the model again on all the development data with the decisions fixed and scored the test with the same
frozen file. The Task 4 numbers came back exactly the same. Everything after that is descriptive: it uses the test
labels to describe the frozen model and changes no choice.

#### Section 5: the final model against the baseline

Table 7.1 has every measure the brief asks for. B1 also needs a threshold, so we gave it the same criterion as the
model (10% on development, which gives 0.393). Since the two thresholds give different numbers of alerts on the test,
the table also shows B1 and B0 with the same number of alerts as the model:

| Measure | Final model | B1 (threshold 0.393) | B1 (same alerts) | B0 (same alerts) |
| --- | --- | --- | --- | --- |
| PR-AUC | 0.532 | 0.381 | 0.381 | 0.178 |
| Precision / recall | 0.677 / 0.286 | 0.504 / 0.225 | 0.509 / 0.215 | 0.180 / 0.076 |
| F1 | 0.402 | 0.311 | 0.302 | 0.107 |
| Balanced accuracy / MCC | 0.628 / 0.373 | 0.589 / 0.251 | 0.585 / 0.248 | 0.501 / 0.003 |
| Alerts | 7.4% | 7.8% | 7.4% | 7.4% |
| Correct / false / missed per 1,000 | 50.3 / 24.0 / 125.6 | 39.5 / 38.9 / 136.4 | 37.8 / 36.4 / 138.1 | 13.4 / 60.9 / 162.5 |

The model beats B1 on every measure. With the same number of alerts, it gives 12.4 more correct alerts and 12.4 fewer
false ones per 1,000 sessions. The PR-AUC gain is 0.152, with a 95% bootstrap interval from 0.145 to 0.158, and in the
McNemar test the model alone is right on 4,283 sessions, against 2,223 for B1. Because sessions of the same post and
day are not independent, these numbers show the size of the gain, not an exact p-value. Balanced accuracy and MCC are
well above chance but moderate, because the high specificity (0.971) hides a low recall.

#### Section 6: over time

The test looks much worse than development (0.532 against 0.635 pooled and 0.660 in fold 4), but most of the drop is
arithmetic. PR-AUC rises with the abnormal share, which was 21.1% in fold 4 and is 17.6% on the test. Applying fold
4's lift to the test share, we would expect 0.550, so 87% of the drop comes from the share and 13% from a lower lift.
The ranking did weaken a little, as ROC-AUC shows, since it does not depend on the share: 0.794 on the test against
0.825 to 0.844 in the folds. By month the model gets 0.553, 0.483 and 0.551, with no downward trend within the quarter
(Figure 7.2).

#### Section 7: by group

The model is above B1 in all three districts (gains of 0.144 to 0.189) and in the 12 stations of the test (0.083 to
0.269). Tongxiang, with 47.9% of the sessions and only 12.0% abnormal, has the lowest PR-AUC (0.474). Alerts follow the
posts that fail most: the nine posts with the most alerts get 46.4% of them. The weakest group is new users (12.9% of
the test), with PR-AUC 0.394 against 0.551 for returning users and recall 0.146 against 0.307. The model gives them
fewer alerts because it has no history for them. This is the cold-start problem.

#### Section 8: where the model fails

On the test there are 4,026 true positives, 1,921 false positives, 10,062 false negatives and 64,072 true negatives.
False positives look like true positives, and missed failures look like normal sessions. For both kinds of alert, the
median session starts about a minute and a half after an abnormal session at the same post; for missed failures, 6.9
hours after. Sessions that start less than 6 hours after a failure at the post (38.3% of the test) hold 91.7% of the
false alerts and have recall 0.445. After 6 hours, recall drops to 0.02 to 0.05, and those quiet periods hold 52.9% of
the missed failures (Figure 7.3). We used `end_cause` only to describe the errors, never as a predictor: recall goes
from 0.19 for control-loop failures to 0.50 for DC switching failures. In short, the model reacts to a post that is
failing now and does not see failures that come without warning.

#### Section 9: interpretation

We repeated permutation importance on the test and the order holds: post history removes 0.271, user history 0.114,
location 0.009 and the rest less than 0.001. We also used partial dependence, which is not in the slides and which we
used as a "model-based" version of Task 1's decile curves: the average score rises sharply when the post's 1-day rate
passes 0.3. Both methods describe how the model uses its inputs, not what causes failures, and they split importance
between correlated windows.

#### Section 10: the threshold in practice

On an average test day, the threshold gives 65 alerts out of 870 sessions, 21 of them false, and 109 abnormal sessions
go without an alert. The alerts come from about 20 posts a day, so the number of inspections is smaller than the
number of alerts, but it ranges from 18 to 210 alerts a day, following the failures. If a false alert costs 1 and a
missed failure costs c, the model is cheaper than raising no alerts when c > 0.48 and cheaper than alerting on
everything when c < 6.4, so it is useful over a wide range of costs. We also described what other budgets (5%, 10%,
20%) would give, but only as description: the 0.490 threshold stayed and no threshold came from there.

### Chapter 8: the final model and reproducibility

Table 8.1 brings together every model evaluated on the four quarters, with the baselines. Only three rows have a test
value (final model, B1, B0), because the test was used once. Table 8.2 describes what is needed to rebuild the model.
Data: development from 1/4/2020 to 30/9/2021 in four folds with a purge, final training on 346,931 sessions, test
from October to December 2021. Preprocessing: ordinal codes for location and district learned on training, everything
else unchanged, no imputation, no resampling and no weights. Features: 27 (post history 8, user 10, weather 4,
calendar 2, location 2, concurrency 1). Hyperparameters: the boosting ones above, seed 42. Threshold: 0.490.
Calibration: none. The reproducibility statement (Section 8.3) explains how to repeat everything: Python 3.12.3, the
versions pinned in `requirements.txt`, the CSV with its SHA-256, seed 42 and the notebook run from start to finish. It
also says the reproduction runs scored the test again with the same frozen file, gave the same numbers and were not
used to choose anything.

### Chapter 9: the synthesis

It answers the project question: the information at the start of a session supports a useful ranking of the posts
that are failing now, mostly thanks to post history, but it does not see failures without warning, and the strength
of the signal changes over time. The limitations include daily weather treated as a forecast, new posts left untested,
the privacy of user history, optimistic development scores, a test of a single quarter, unknown costs and the 13
causes merged together. There are three recommendations: ask the operator for the real costs and daily capacity
before changing the threshold (always on development data), retrain the model regularly and monitor the ranking, and
add data the file does not have, such as post maintenance records or telemetry, to catch failures after quiet
periods.

### If you only have 30 minutes

- We tuned three models (boosting, random forest, tree) with grid search on the same 4 folds. No tuning gained more
  than 0.005 in a stable way, so the Task 3 configuration stayed.
- The final model is gradient boosting (depth 6, lr 0.1, 200 iterations, leaf 100), with 27 features. It beat the
  random forest on the better worst fold (0.575 against 0.567).
- The 0.490 threshold raises alerts on 10% of development sessions, chosen on the out-of-fold predictions. Almost equal
  to 0.50, because the scores are well calibrated (Brier 0.103).
- Frozen on 27/10 at 11:40:32. The test was evaluated once: 0.532 against 0.381 (B1) and 0.178 (B0).
- On the test: 7.4% alerts, precision 0.677, recall 0.286, F1 0.402, balanced accuracy 0.628, MCC 0.373. Per 1,000
  sessions: 50.3 correct alerts, 24.0 false and 125.6 missed failures.
- The drop from development is 87% arithmetic (fewer abnormal sessions on the test). ROC-AUC shows a small real loss
  (0.794 against 0.825 to 0.844).
- Above B1 in every district and station. The weakest group is new users (recall 0.146).
- Errors: the model catches failures right after another failure at the post and misses those that come after quiet
  periods (52.9% of the missed failures).
- Post history dominates the importance. Permutation measures use, not cause.
- Useful for failure costs between 0.48 and 6.4 times the cost of a false alert. Recommendations: real costs, regular
  retraining, maintenance data.

### Leads into

This part uses everything that came before: the features and the "learn on training only" rule from Task 1, the
folds, metrics and B1 from Task 2, and the winner and tolerance from Task 3.

### Likely questions on Tasks 4 and 5

1. **Why was no tuned configuration kept?**
   We only accepted a new configuration if it gained more than 0.005 on average and in at least 3 of the 4 folds. None
   passed: tuned boosting was −0.002, the random forest +0.001 and the tree +0.002. The results are flat (31 of the 39
   boosting configurations are within 0.005 of the best), so Task 3 was already on the plateau. See Section 6.2.

2. **Why does the threshold come from a 10% budget and not from maximum F1?**
   F1 gives precision and recall the same weight without an operational reason, and its maximum, near 0.3, would flag
   far more than 10% of the sessions. The budget is the quantity the operator controls: how many inspections they can
   do. 10% is the middle of the protocol's three budgets and the last one where the extra alerts are more often right
   than wrong. See Section 6.3.

3. **Why is 0.490 almost equal to 0.50?**
   Because the model's scores are close to probabilities (Brier 0.103, deviations up to 0.015) and about 10% of the
   sessions have a risk above 0.5. It is a coincidence of this model, not a property of 0.50. See Sections 6.3 and 6.4.

4. **Did you need to calibrate the model?**
   We checked and no. In the top band, where the alerts are, the mean score is 0.738 and the real share 0.740. Also, a
   calibration that keeps the order would flag the same 10% of sessions, so it would not change the alerts. See
   Section 6.4.

5. **Why is the test PR-AUC lower than on development?**
   Mostly because the test has fewer abnormal sessions (17.6% against 21.1% in fold 4), and PR-AUC rises with that
   share. With fold 4's lift we expected 0.550, so 87% of the drop comes from that. ROC-AUC, which does not depend on
   the share, shows a small real loss (0.794 against 0.825 to 0.844). See Section 7.3.

6. **Can you guarantee the test was used only once, if you scored it again?**
   The official evaluation is the one on 27/10, done after freezing the choices to the file. The later runs used the
   same frozen file unchanged, gave exactly the same numbers, are disclosed in the reproducibility statement and were
   not used to choose anything. What the brief forbids is changing models, features, hyperparameters or thresholds
   after seeing the test, and that did not happen. See Sections 6.5 and 8.3.

7. **Which failures does the model miss, and why?**
   Those that come after a quiet period at the post. After 6 hours with no failure, recall drops to 0.02 to 0.05, and
   those periods hold 52.9% of the missed failures. The model relies on the post's recent history, and without a
   recent failure there is no warning. It also does worse with new users (recall 0.146). See Sections 7.3 and 7.4.

8. **What can permutation importance tell you, and what can't it?**
   It tells how much this model uses each group of variables: post history dominates. It does not tell what causes the
   failures, and correlated variables share importance, so a single window looks less important than it is. That is
   why we shuffled whole groups. See Sections 6.6 and 7.5.

9. **Is the model useful for an operator?**
   Yes, as a ranking of the posts that are failing now. On an average day it gives 65 alerts out of 870 sessions, 21 of
   them false, from about 20 posts. It is cheaper than raising no alerts or alerting on everything for failure costs
   between 0.48 and 6.4 times that of a false alert. It is not a complete detector: it lets 109 failures a day through.
   See Section 7.6.

10. **Why did you choose gradient boosting and not the random forest, if they are tied?**
    They were within the tolerance (0.626 against 0.622), so we applied the tie-break set in advance: the better worst
    fold (0.575 against 0.567). Boosting also varies less across folds and trains about four times faster, which makes
    regular retraining easier. See Sections 6.2 and 7.1.

---

## Common questions (everyone must be able to answer)

1. **What is the project question, and what is your answer, in two sentences?**
   The question is how far the information available at the start of a session can predict that it will end badly.
   Our answer is that it supports a useful ranking of the posts that are failing now (PR-AUC 0.532 on the test, against
   0.381 for the best simple rule), but it does not detect failures that come without warning in the post's history.
   See chapter 9.

2. **Why do you only use information from the start of the session?**
   Because the prediction is made when the session starts, and the brief only allows what is known at that moment. The
   end-of-session columns (energy, costs, end time) separate the classes very well (ROC-AUC 0.82 to 0.85), but only
   because they describe the outcome; using them would be leakage and the results would be false. See Section 2.1.

3. **Why did you split the data by time and not at random?**
   Because volume, abnormal share and fault type change over the two years, and because the model will be used on
   future sessions. At random, the model would see the future during training and look better than it is. See
   Sections 2.4 and 4.5.

4. **Why is PR-AUC the primary metric?**
   Because failures are the minority (about 18%) and what matters is that the alerts at the top of the list are real
   failures. PR-AUC measures exactly that and ignores the true negatives. Its random value is the abnormal share, so we
   always read it next to that share. See Section 4.4.

5. **Which model won and by how much?**
   Gradient boosting with 27 features. On development it gets 0.626 against 0.511 for B1 (+0.115, better in all four
   folds). On the test it gets 0.532 against 0.381 (+0.152), and it beats B1 in every district and station. See
   Table 8.1.

6. **How did you make sure the test was used only once?**
   We removed the test right after reading the file, in every task. We chose everything with the four development
   folds, wrote the choices to a file on 27/10 at 11:40:32, and only then evaluated the test. Nothing changed after
   that. The reproduction runs used the same file and gave the same numbers. See Sections 6.5 and 8.3.

7. **Why did you submit a single notebook?**
   The brief asks for complete and reproducible notebook(s), and the instructor's message mentions "notebook and
   report". We joined the five tasks in order into one notebook, without changing any code cell, and ran it from
   start to finish in a new environment. The test numbers stayed the same as on 27/10. See Section 8.3.

8. **What are the main limitations?**
   Weather is daily and was treated as a forecast. We could not test new posts, because every test post was already in
   training. The test is a single quarter. The real error costs and the operator's capacity are not in the data, so
   the 10% budget is our choice. The 13 fault causes are merged, and the model detects some much worse than others.
   See chapter 9.

9. **What do you recommend to improve it?**
   Ask the operator for the real costs and daily capacity before changing the threshold, and always do it on
   development data. Retrain the model regularly and monitor the ranking, because ROC-AUC dropped on the test. Add
   data the file does not have, such as post maintenance records or telemetry, to catch failures after quiet periods.
   See chapter 9.

10. **What about a new post with no history?**
    We could not evaluate it, because every validation and test post was already in training. We expect the model to
    do worse, as it does with new users (recall 0.146 against 0.307), because the main signal is the post's history.
    It is a stated limitation. See Sections 3.1 and 7.3.

11. **Why didn't you use a neural network or another more advanced model?**
    The brief values a small, well-justified comparison more than many algorithms, and the methods come from the
    course slides. Also, logistic regression (0.593) and the tree (0.597) reach almost the same value while being very
    different, and tuning did not help. That suggests the limit is the available information, not model complexity.
    See Sections 5.2 and 6.2.

12. **What would you do with more time?**
    The same as we recommend: get real costs and capacity, test the model on more quarters and, if possible, on new
    posts, and separate the fault causes to see whether some types are easier to predict on their own. All without
    touching the current test. See chapter 9.

---

## Rehearsal plan (30 minutes, in pairs)

1. Each person reads someone else's common core aloud in 5 minutes, and the other corrects anything wrong.
2. For 10 minutes, person A asks 10 questions from person B's part (picked at random, mixing B's questions with the
   common ones). B answers without notes. A checks against the model answer and points out what was missing.
3. Swap roles for another 10 minutes.
4. In the last 5 minutes, each person writes down the questions they hesitated on and rereads that part of the guide.

The goal is to answer at least 8 of 10 questions from your own part and 7 of 10 common ones correctly. If a question
is about someone else's part, the model answer says where to read.
