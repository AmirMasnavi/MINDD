# Dataset guide

This explains the supplied `Charging_Data_educational.csv`, based on the assignment
and the checks in [main.ipynb](../main.ipynb). It is an educational adaptation of
the China EV Charging Dataset cited in the assignment. The local file has 441,077
rows and 47 original columns, covering session starts from 31 December 2019 to
31 December 2021. Each row appears to represent one charging transaction. No full
row or `(UserID, Charging Post ID, Start Time)` duplicate was found.

## Reading the outcome

The original CSV has no `is_Abnormal` column. The notebook creates it **in memory**
from `end_cause`, under this explicit project assumption:

| Label | Termination reasons | Reasoning |
| --- | --- | --- |
| 0 — normal | `Charging ends normally`; `User stops charging` | A user-requested stop is treated as an intentional end, not an equipment or vehicle fault. |
| 1 — abnormal | The other 13 recorded causes, all containing “fault” or “failure” | These describe equipment, vehicle, connection, communication, or power failures. |

This is a team definition, **not a mapping stated in the PDF**. It yields 81,934
abnormal sessions (18.58%) and 359,143 normal sessions (81.42%). If “User stops
charging” were instead counted abnormal, the abnormal share would be 53.93%.
That sensitivity is large, so the team should seek an instructor definition before
using this label for final model claims. New or missing cause values should stop the
mapping for review, rather than silently becoming abnormal. `end_cause` and the
derived label are outcomes, never predictors at session start.

One `Location Information` category carries a trailing tab in 18,370 rows.
Removing surrounding whitespace leaves the same 13 categories and is a justified
cleanup for future encoding. The original CSV remains unchanged.

## Original field dictionary

Names below match the CSV exactly. `1D`, `7D`, `30D`, `180D`, and `730D` mean
lookback windows of that many days. A “previous completed” outcome excludes
earlier-started sessions still active at prediction time, according to PDF p. 3.
Smoothed rates are provided; the smoothing formula is not specified in the PDF,
so do not assume each equals abnormal count divided by session count.

| CSV field | Meaning and timing |
| --- | --- |
| `UserID` | Account identifier; available for lookup, sensitive/high-cardinality. |
| `Charging Post ID` | Charging-post identifier; available for lookup. |
| `Location Information` | Station location; known at start. |
| `District Name` | District of station; known at start. |
| `Order creation time` | Recorded order creation timestamp; theoretically before start, but ordering conflicts in many rows. |
| `Transaction power/kwh` | Energy for the completed transaction; unavailable at start. CSV spelling uses lowercase `kwh`. |
| `Electricity cost/Yuan` | Final electricity charge; unavailable at start. |
| `Service charge/Yuan` | Final service charge; unavailable at start. |
| `Transaction Amount/Yuan` | Listed final total; equals electricity plus service charges in this CSV. |
| `Actual Payment/Yuan` | Final amount paid; can differ from listed total. |
| `Start Time` | Charging start timestamp and prediction-time anchor. |
| `End Time` | Charging end timestamp; unavailable at start. |
| `Payment time` | Recorded payment timestamp; unavailable at start. |
| `Temperature(℃)` | Weather estimate/forecast at start, as instructed by the PDF. |
| `Relative Humidity(%)` | Weather estimate/forecast at start. |
| `Precipitation(mm)` | Weather estimate/forecast at start. |
| `end_cause` | Termination reason; outcome known after the session. |
| `electricity_price` | Electricity price applicable at session start. |
| `tariff_period` | Start-time tariff interval. |
| `post_previous_sessions_1D` | Completed sessions at this post in prior 1 day. |
| `post_previous_abnormal_1D` | Completed abnormal sessions at this post in prior 1 day. |
| `post_previous_abnormal_rate_1D` | Provided smoothed prior abnormal rate for this post and window. |
| `post_previous_sessions_7D` | Completed sessions at this post in prior 7 days. |
| `post_previous_abnormal_7D` | Completed abnormal sessions at this post in prior 7 days. |
| `post_previous_abnormal_rate_7D` | Provided smoothed prior abnormal rate for this post and window. |
| `post_previous_sessions_30D` | Completed sessions at this post in prior 30 days. |
| `post_previous_abnormal_30D` | Completed abnormal sessions at this post in prior 30 days. |
| `post_previous_abnormal_rate_30D` | Provided smoothed prior abnormal rate for this post and window. |
| `post_hours_since_previous_completed_session` | Hours since the post's last completed session; blank when none exists. |
| `post_no_previous_completed_session` | Flag for no previous completed session at the post. |
| `post_hours_since_previous_completed_abnormal` | Hours since last completed abnormal session at this post; blank when none exists. |
| `post_no_previous_completed_abnormal` | Flag for no previous completed abnormal session at the post. |
| `is_new_user` | Provided new-user indicator; check its exact operational meaning before deployment. |
| `user_previous_sessions_30D` | Completed sessions for this account in prior 30 days. |
| `user_previous_abnormal_30D` | Completed abnormal sessions for this account in prior 30 days. |
| `user_previous_abnormal_rate_30D` | Provided smoothed prior abnormal rate for this account and window. |
| `user_previous_sessions_180D` | Completed sessions for this account in prior 180 days. |
| `user_previous_abnormal_180D` | Completed abnormal sessions for this account in prior 180 days. |
| `user_previous_abnormal_rate_180D` | Provided smoothed prior abnormal rate for this account and window. |
| `user_previous_sessions_730D` | Completed sessions for this account in prior 730 days. |
| `user_previous_abnormal_730D` | Completed abnormal sessions for this account in prior 730 days. |
| `user_previous_abnormal_rate_730D` | Provided smoothed prior abnormal rate for this account and window. |
| `user_days_since_previous_completed_session` | Days since account's last completed session; blank when none exists. |
| `user_no_previous_completed_session` | Flag for no previous completed session for the account. |
| `user_days_since_previous_completed_abnormal` | Days since account's last completed abnormal session; blank when none exists. |
| `user_no_previous_completed_abnormal` | Flag for no previous completed abnormal session for the account. |
| `user_active_sessions_at_start` | Number of other sessions on the same account active at current start time; no unfinished outcome is used. |

## How to use this guide

Use the notebook for measurements and justification, this page for definitions,
and [REQUIREMENTS.md](REQUIREMENTS.md) for what the assignment actually demands.
An original field's presence in the CSV does not make it suitable for prediction.
The prediction-time grouping and current preparation decisions are in the notebook.
Do not share raw user-level examples in reports or screenshots.
