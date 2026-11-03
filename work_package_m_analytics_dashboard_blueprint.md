# VELOOP REWARDS — WORK PACKAGE M
## Analytics Dashboard Blueprint & Visual Wireframe Specifications
**Document ID:** VELOOP-DELIV-15  
**Deliverable Covered:** Deliverable 15 (Analytics Dashboard Blueprint)  
**Classification:** SIMULATED DATA — CREATED FOR ANALYTICAL TESTING  
**Status Standard:** Confirmed | Proposed | To Be Verified  

---

### 1. Executive Purpose & Design Principles

The **Analytics Dashboard Blueprint** establishes the visual hierarchy, reporting cadence, and decision-support architecture for VELOOP Rewards. It serves executive leadership, product managers, growth marketers, finance controllers, and operations teams.

#### Guiding Principles:
1. **Decision-First Visuals:** Every visual widget directly supports a specific operational or strategic decision rather than displaying vanity data.
2. **Standardized Widget Specification:** Every visual specifies all **10 mandatory attributes**: Metric, Calculation, Source, Visualization Type, Filters, Dimensions, Date Range, Refresh Frequency, Business Question, and Decision Supported.
3. **Responsive Visual Wireframes:** Each dashboard provides structural layout wireframes optimized for modern BI tools (Looker Studio, Tableau, Metabase, Superset).

---

### 2. Dashboard 1: Executive Overview

#### Purpose:
High-level operational cockpit for C-suite and Product Directors tracking macro growth, monetization velocity, and financial liability.

#### Visual Wireframe Layout:
```
+----------------------------------------------------------------------------------------------------+
|  VELOOP REWARDS — EXECUTIVE OVERVIEW COCKPIT                         [ Date Range: Last 30 Days v ]|
+----------------------------------------------------------------------------------------------------+
| [ KPI 1: DAU / MAU ]   | [ KPI 2: Total Active Users ] | [ KPI 3: Gross Issuance ] | [ KPI 4: Net Payouts ]|
|   32.4% (Stickiness)   |    1,000 Total Acquired       |    142,500 XP / 1,425 TOK |   $3,850.00 Settled   |
+------------------------+-------------------------------+---------------------------+-----------------------+
| FEATURE ADOPTION & EVENT VOLUME (Last 30 Days)                 | USER ACQUISITION BY CHANNEL               |
| [==================================] Watch Ads (3.1k)          |   [###] Organic Search (24.4%)            |
| [==============================] Missions (2.7k)                |   [##]  Direct (21.7%)                    |
| [==============================] Streaks (2.7k)                 |   [##]  Social Media (16.0%)              |
| [============================] Mining (2.6k)                   |   [#]   Referral (11.9%)                  |
| [==========================] Daily Reward (2.5k)               |   [#]   WhatsApp / Telegram (15.8%)       |
+----------------------------------------------------------------+-------------------------------------------+
| FINANCIAL LIABILITY & LIQUIDITY DEMAND (Daily Trend)           | RECENT OPERATIONAL HEALTH & SLA           |
| (Line Chart: Daily Issuance Value vs Completed Withdrawals)    | * Gateway Payout Success Rate: 94.2%      |
|   Issuance: ~~~~~~~~~~~~~~~~~~~~~~~~~~                         | * Median Payout SLA: 18.4 Hours           |
|   Settled:  --------------------------                         | * Active Withdrawal Backlog: 24 Requests  |
+----------------------------------------------------------------------------------------------------+
```

#### Detailed Visual Specifications:

##### Visual 1.1: Platform Health & Scale Scorecards
* **Metric:** DAU, MAU, Platform Stickiness ($DAU/MAU$), and Net Circulating Liability.
* **Calculation:** `COUNT(DISTINCT user_id)` over 1-day, 30-days, and $\sum \text{current\_token\_balance}$.
* **Source:** `fact_daily_user_summary` and `dim_users`.
* **Visualization:** Metric KPI Scorecard Cards with trend arrows.
* **Filters:** Country, Platform (Android, iOS, Web).
* **Dimensions:** None (Single-value scalar aggregation).
* **Date Range:** Trailing 30 days vs preceding 30 days.
* **Refresh Frequency:** Hourly.
* **Business Question:** What is the macro scale and health of our active audience today?
* **Decision Supported:** Determines whether to ramp paid acquisition or focus on retention interventions.

##### Visual 1.2: Feature Engagement Distribution
* **Metric:** Total Events Logged per Product Feature.
* **Calculation:** `COUNT(event_id)` grouped by `feature_name`.
* **Source:** `fact_feature_events` (or `07_Feature_Usage`).
* **Visualization:** Horizontal Bar Chart (Sorted descending).
* **Filters:** Platform, User Tenure Cohort.
* **Dimensions:** `feature_name` (15 features).
* **Date Range:** Last 30 Days.
* **Refresh Frequency:** Daily at 01:00 UTC.
* **Business Question:** Which features dominate user engagement time?
* **Decision Supported:** Informs product roadmap priority and feature sunsetting decisions.

##### Visual 1.3: Revenue vs. Liability Issuance Trend
* **Metric:** Gross Reward Issuance vs. Settled Payout Cash Outflow.
* **Calculation:** $\sum \text{Issuance Value}$ vs $\sum \text{Settled Withdrawal Amount}$ by day.
* **Source:** `fact_wallet_transactions` and `fact_withdrawals`.
* **Visualization:** Dual-Axis Line Chart.
* **Filters:** Currency Unit (`TOKENS`, `USD`).
* **Dimensions:** `activity_date` (Daily).
* **Date Range:** Rolling 90 Days.
* **Refresh Frequency:** Daily at 02:00 UTC.
* **Business Question:** Are reward liabilities expanding faster than cash outflow and ad revenue?
* **Decision Supported:** Triggers adjustments to token exchange rates and task reward values.

---

### 3. Dashboard 2: User Lifecycle & Cohort Analytics

#### Purpose:
Monitors customer acquisition channels, onboarding activation, cohort retention, and churn migration.

#### Visual Wireframe Layout:
```
+----------------------------------------------------------------------------------------------------+
|  VELOOP REWARDS — USER LIFECYCLE & COHORTS                           [ Platform: All | Country: All]|
+----------------------------------------------------------------------------------------------------+
| [ New Signups: 1,000 ] | [ Verified Rate: 89.0% ] | [ Onboarded: 89.0% ] | [ 30-Day Churn: 44.0% ] |
+------------------------+--------------------------+----------------------+-------------------------+
| REGISTRATION VOLUME BY ACQUISITION CHANNEL (Weekly Stacked Bar)  | USER GEOGRAPHIC DISTRIBUTION            |
| [ Organic Search | Direct | Social | Referral | WhatsApp ]      | India: 100% (Simulated Baseline)        |
| Week 1: [====|===|==|=|==]                                       | Top States:                             |
| Week 2: [=====|====|===|==|==]                                   | * Maharashtra: 18.2%                    |
| Week 3: [====|===|==|=|==]                                       | * Karnataka: 14.5%                      |
+------------------------------------------------------------------+-----------------------------------------+
| CLASSIC RETENTION COHORT HEATMAP (Day 0 to Day 30)                                                         |
| Cohort Week   | Users | Day 0 | Day 1 | Day 3 | Day 7 | Day 14 | Day 30                                    |
| 2026-W32      | 145   | 100%  | 42%   | 31%   | 24%   | 18%    | 14%                                       |
| 2026-W33      | 168   | 100%  | 45%   | 34%   | 26%   | 19%    | 15%                                       |
| 2026-W34      | 182   | 100%  | 44%   | 32%   | 25%   | --     | --                                        |
+----------------------------------------------------------------------------------------------------+
```

#### Detailed Visual Specifications:

##### Visual 2.1: Retention Cohort Matrix
* **Metric:** N-Day Retention Rate ($D_0, D_1, D_3, D_7, D_{14}, D_{30}$).
* **Calculation:** $\frac{\text{Active Users on Day } N \text{ from Cohort } C}{\text{Total Cohort Size } C} \times 100$.
* **Source:** Joined `dim_users` and `fact_daily_user_summary`.
* **Visualization:** Cohort Retention Heatmap (Color gradient from dark blue to white).
* **Filters:** Acquisition Channel, Primary Device.
* **Dimensions:** Signup Week (Rows) × Elapsed Days (Columns).
* **Date Range:** Last 12 Weeks.
* **Refresh Frequency:** Daily at 02:30 UTC.
* **Business Question:** Does user retention stabilize after Day 7 or decay continuously?
* **Decision Supported:** Identifies whether onboarding improvements successfully flatten the retention curve.

##### Visual 2.2: User Lifecycle State Migration
* **Metric:** Distribution of Users across Lifecycle States (`Active`, `Dormant`, `Churned`, `Suspended`).
* **Calculation:** `COUNT(user_id)` grouped by `account_status`.
* **Source:** `dim_users`.
* **Visualization:** 100% Stacked Area Chart over time.
* **Filters:** Channel, Platform.
* **Dimensions:** Snapshot Date (Weekly).
* **Date Range:** Trailing 6 Months.
* **Refresh Frequency:** Weekly.
* **Business Question:** What proportion of the historical user base has become permanently dormant?
* **Decision Supported:** Directs budget allocation toward re-engagement push campaigns vs new acquisition.

---

### 4. Dashboard 3: Task & Feature Engagement Intelligence

#### Purpose:
Granular visibility into micro-earning activities, task completion funnels, and failure modes across offerwalls.

#### Visual Wireframe Layout:
```
+----------------------------------------------------------------------------------------------------+
|  VELOOP REWARDS — ENGAGEMENT & TASK INTELLIGENCE                     [ Category: All Categories v ]|
+----------------------------------------------------------------------------------------------------+
| [ Total Starts: 9,846 ] | [ Completed: 5,627 ] | [ Overall TCR: 57.1% ] | [ Mean Velocity: 3.2m ]  |
+-------------------------+----------------------+------------------------+--------------------------+
| TASK CONVERSION FUNNEL (Viewed -> Opened -> Started -> Completed)                                  |
| 1. Task Viewed:    [========================================] 100% (14,200)                         |
| 2. Task Opened:    [============================] 72% (10,224)                                      |
| 3. Task Started:   [======================] 56% (7,950)                                             |
| 4. Task Completed: [================] 39% (5,627)                                                   |
+----------------------------------------------------------------------------------------------------+
| COMPLETION RATE (TCR) BY CATEGORY (%)      | ROOT CAUSE FAILURE BREAKDOWN                          |
| Advertisement:    [================] 68%   | [====] Validation Failed (732 records)                |
| App Task:         [============] 52%       | [====] Task Unavailable (722 records)                 |
| Survey:           [==========] 44%         | [====] Timeout (710 records)                          |
| CAPTCHA:          [==================] 76% | [====] Incomplete Action (706 records)                |
| Game:             [==============] 58%     | [====] User Exited Early (701 records)                |
+----------------------------------------------------------------------------------------------------+
```

#### Detailed Visual Specifications:

##### Visual 3.1: Task Conversion Funnel
* **Metric:** Task Drop-Off Funnel Conversion ($CTR, SCR, TCR$).
* **Calculation:** Step-by-step conversion percentages across the 4 stages.
* **Source:** `fact_feature_events` and `fact_task_activity`.
* **Visualization:** Horizontal Funnel Chart.
* **Filters:** `task_category`, Device Platform.
* **Dimensions:** Funnel Step.
* **Date Range:** Last 30 Days.
* **Refresh Frequency:** Daily at 01:00 UTC.
* **Business Question:** At which point in the earning flow do users experience the greatest drop-off?
* **Decision Supported:** Optimizes task card presentation and streamlines external redirect handoffs.

##### Visual 3.2: Failure Taxonomy Distribution
* **Metric:** Count of Failed / Abandoned Task Attempts by Error Code.
* **Calculation:** `COUNT(activity_id)` grouped by `failure_reason`.
* **Source:** `fact_task_activity` (where `task_status IN ('Failed', 'Abandoned')`).
* **Visualization:** Donut Chart / Sorted Bar Chart.
* **Filters:** `task_category`, Partner Network.
* **Dimensions:** `failure_reason`.
* **Date Range:** Last 14 Days.
* **Refresh Frequency:** Daily.
* **Business Question:** Are tasks failing due to user abandonment or partner API technical errors?
* **Decision Supported:** Pauses under-performing survey routers with excessive screenout rates.

---

### 5. Dashboard 4: Rewards & Gamification Economics

#### Purpose:
Monitors gamification progression, daily streak habits, badge minting, and reward distribution equity.

#### Visual Wireframe Layout:
```
+----------------------------------------------------------------------------------------------------+
|  VELOOP REWARDS — GAMIFICATION & REWARD ECONOMICS                    [ Timeframe: Last 30 Days v ] |
+----------------------------------------------------------------------------------------------------+
| [ XP Distributed: 342,000 ] | [ Badges Minted: 954 ] | [ Active Streaks: 832 ] | [ Level Ups: 1,266 ]|
+-----------------------------+------------------------+-------------------------+---------------------+
| STREAK HABIT DISTRIBUTION (Day 1 through Day 30)             | REWARD ISSUANCE BY FEATURE          |
| D1:  [==============================] 832 users               | Watch Ads:      [==============] 32% |
| D3:  [====================] 512 users                        | Daily Reward:   [============] 24%  |
| D7:  [==============] 376 users                              | Missions:       [==========] 18%    |
| D14: [========] 194 users                                    | Mining:         [========] 14%      |
| D30: [===] 68 users                                          | Spin Wheel:     [=====] 12%         |
+--------------------------------------------------------------+-------------------------------------+
| SPIN THE WHEEL PRIZE DISTRIBUTION (%)                        | REWARD REVERSALS & CLAWBACKS        |
| 10 XP Prize:   [====================] 42%                    | Total Reversed: 4,200 XP            |
| 50 XP Prize:   [============] 28%                            | Reversal Rate: 1.2%                 |
| 1 Token:       [======] 14%                                  | Primary Reason: Survey Fraud (64%)  |
| Nothing:       [=======] 16%                                 |                                     |
+----------------------------------------------------------------------------------------------------+
```

#### Detailed Visual Specifications:

##### Visual 4.1: Streak Habit Curve & Attrition
* **Metric:** Unique Users maintaining an unbroken streak at each Day-N milestone.
* **Calculation:** `COUNT(DISTINCT user_id)` grouped by `streak_day_count`.
* **Source:** `fact_daily_user_summary` and `fact_feature_events` (`streak_updated`).
* **Visualization:** Bar Chart / Step Line.
* **Filters:** User Acquisition Cohort, Platform.
* **Dimensions:** `streak_day_count` (1 to 30).
* **Date Range:** Trailing 30 Days.
* **Refresh Frequency:** Daily at 02:00 UTC.
* **Business Question:** What is the critical inflection day where user streak discipline collapses?
* **Decision Supported:** Calibrates push notification reminders and streak-freeze perks at Day 3 and Day 7.

##### Visual 4.2: Reward Issuance Breakdown by Module
* **Metric:** Proportion of Total Rewards Issued by Module.
* **Calculation:** $\frac{\sum \text{amount}_{\text{module}}}{\sum \text{total\_amount}} \times 100$.
* **Source:** `fact_wallet_transactions` (where `transaction_type = 'REWARD_CREDIT'`).
* **Visualization:** Treemap / Donut Chart.
* **Filters:** Currency Unit (`XP`, `TOKENS`).
* **Dimensions:** `source_module`.
* **Date Range:** Last 30 Days.
* **Refresh Frequency:** Daily.
* **Business Question:** Is the platform over-dependent on a single earning feature?
* **Decision Supported:** Rebalances reward multipliers across under-utilized gamification features.

---

### 6. Dashboard 5: Wallet & Transaction Ledger Operations

#### Purpose:
Real-time financial surveillance for internal audit, treasury management, and double-entry reconciliation.

#### Visual Wireframe Layout:
```
+----------------------------------------------------------------------------------------------------+
|  VELOOP REWARDS — WALLET & LEDGER OPERATIONS                         [ Currency: All Units v ]     |
+----------------------------------------------------------------------------------------------------+
| [ Total Ledger TX: 12,450 ] | [ Total Credits: 450k ] | [ Redemptions: 110k ] | [ Ledger Drift: 0.00 ]|
+-----------------------------+-------------------------+-----------------------+----------------------+
| DAILY LEDGER MUTATIONS (Credits vs Debits Stacked)          | TRANSACTION TYPE DISTRIBUTION        |
| Credits (+): [===|===|===|===|===|===|===]                  | REWARD_CREDIT:        [=======] 65%  |
| Debits  (-): [==|==|==|==|==|==|==]                         | REDEMPTION:           [====] 22%     |
| Net Shift:   ~~~~~~~~~~~~~~~~~~~~~~~~~                      | EXCHANGE_CONVERSION:  [==] 10%       |
|                                                             | REVERSAL:             [*] 2%         |
|                                                             | ADMIN_ADJUSTMENT:     [*] 1%         |
+-------------------------------------------------------------+--------------------------------------+
| DOUBLE-ENTRY RECONCILIATION AUDIT LOG (Real-Time Integrity)                                        |
| Date       | Computed Ledger Delta | Dim Users Balance Delta | Variance (Drift) | Status           |
| 2026-09-15 | +12,450.0000 TOK      | +12,450.0000 TOK        | 0.0000 TOK       | [ PASS ]         |
| 2026-09-14 | +11,820.0000 TOK      | +11,820.0000 TOK        | 0.0000 TOK       | [ PASS ]         |
+----------------------------------------------------------------------------------------------------+
```

#### Detailed Visual Specifications:

##### Visual 5.1: Double-Entry Ledger Reconciliation Monitor
* **Metric:** System Ledger Drift ($\Delta = \text{Ledger Balance} - \text{User Dimension Balance}$).
* **Calculation:** $|\sum (\text{Credits} - \text{Debits}) - \sum \text{current\_token\_balance}|$.
* **Source:** `fact_wallet_transactions` joined with `dim_users`.
* **Visualization:** Real-Time Audit Table with status badge indicators (`PASS` / `FAIL`).
* **Filters:** Currency Unit (`XP`, `TOKENS`).
* **Dimensions:** Reconciliation Date.
* **Date Range:** Last 30 Days.
* **Refresh Frequency:** Hourly.
* **Business Question:** Does any mathematical variance exist between ledger history and account balances?
* **Decision Supported:** Automatically triggers an emergency circuit-breaker if variance $> 0.0001$.

##### Visual 5.2: Internal Currency Exchange Velocity
* **Metric:** Total XP Debited and Tokens Credited via Exchange Center.
* **Calculation:** $\sum \text{amount}$ grouped by exchange direction.
* **Source:** `fact_wallet_transactions` (where `source_module = 'EXCHANGE'`).
* **Visualization:** Grouped Bar Chart.
* **Filters:** Platform.
* **Dimensions:** Date (Weekly).
* **Date Range:** Last 90 Days.
* **Refresh Frequency:** Daily at 02:00 UTC.
* **Business Question:** Are users actively converting casual XP into redeemable payout tokens?
* **Decision Supported:** Anticipates upcoming cash-out liquidity requirements.

---

### 7. Dashboard 6: Withdrawal & Payout Operations

#### Purpose:
Operational command center for payout dispatch, gateway SLA monitoring, and anti-fraud review.

#### Visual Wireframe Layout:
```
+----------------------------------------------------------------------------------------------------+
|  VELOOP REWARDS — WITHDRAWAL & PAYOUT OPERATIONS                     [ Gateway: All Gateways v ]   |
+----------------------------------------------------------------------------------------------------+
| [ Pending Queue: 24 Req ] | [ Settled Vol: $3,850 ] | [ Fulfillment: 94.2% ] | [ Median SLA: 18.4h ] |
+---------------------------+-------------------------+------------------------+---------------------+
| WITHDRAWAL LIFECYCLE QUEUE STATUS (Active Pipeline)          | PAYOUT METHOD DISTRIBUTION ($)       |
| 1. Requested:     [====] 12 requests                         | PayPal:         [==============] 48% |
| 2. Under Review:  [==] 8 requests                            | Bank Transfer:  [==========] 26%    |
| 3. Processing:    [=] 4 requests                             | UPI:            [======] 16%        |
| 4. Completed:     [==============================] 310 settled | Crypto USDT:    [===] 10%           |
+--------------------------------------------------------------+-------------------------------------+
| SLA LATENCY TREND (Median vs 95th Percentile Hours)          | REJECTION ROOT CAUSE DISTRIBUTION   |
| Median SLA: ------ (Target: < 24h)                           | [====] Multi-Account Ring (42%)     |
| P95 SLA:    ~~~~~~ (Warning: > 48h)                          | [===]  Invalid Beneficiary (28%)    |
|                                                              | [==]   Suspicious XP Velocity (18%) |
|                                                              | [=]    KYC Documentation (12%)      |
+----------------------------------------------------------------------------------------------------+
```

#### Detailed Visual Specifications:

##### Visual 6.1: Payout SLA Latency Distribution
* **Metric:** Median and 95th Percentile Processing Duration (Hours).
* **Calculation:** $\text{Percentile}_{50}(\text{settlement\_time} - \text{requested\_time})$ and $\text{Percentile}_{95}(\dots)$.
* **Source:** `fact_withdrawals` (where `status = 'COMPLETED'`).
* **Visualization:** Time-Series Area Chart with SLA Threshold Bands.
* **Filters:** Payout Method, Gateway.
* **Dimensions:** Settlement Date (Daily).
* **Date Range:** Last 30 Days.
* **Refresh Frequency:** Daily.
* **Business Question:** Is the company meeting its published 24-hour payout turnaround promise?
* **Decision Supported:** Flags bottlenecks in compliance reviews or external gateway delays.

##### Visual 6.2: Rejection Reason Breakdown
* **Metric:** Count and Volume of Rejected Withdrawals by Cause Code.
* **Calculation:** `COUNT(withdrawal_id)` grouped by `rejection_reason_code`.
* **Source:** `fact_withdrawals` (where `status = 'REJECTED'`).
* **Visualization:** Horizontal Bar Chart.
* **Filters:** Amount Tier ($< \$10, \$10\text{--}\$50, > \$50$).
* **Dimensions:** `rejection_reason_code`.
* **Date Range:** Last 30 Days.
* **Refresh Frequency:** Daily.
* **Business Question:** What are the primary triggers blocking user payouts?
* **Decision Supported:** Guides improvements in payout form validation and anti-fraud heuristics.

---

### 8. Dashboard 7: Referral & Growth Funnel Analytics

#### Purpose:
Tracks viral growth, ambassador performance, referee activation, and customer acquisition efficiency.

#### Visual Wireframe Layout:
```
+----------------------------------------------------------------------------------------------------+
|  VELOOP REWARDS — REFERRAL & VIRAL GROWTH ENGINE                     [ Channel: All Channels v ]   |
+----------------------------------------------------------------------------------------------------+
| [ Shares: 834 ] | [ Referee Signups: 119 ] | [ Activated: 78 ] | [ Converted: 62 ] | [ K-Factor: 0.12 ]|
+-----------------+--------------------------+-------------------+-------------------+-------------------+
| 4-STAGE REFERRAL CONVERSION FUNNEL                                                                 |
| 1. Referral Shared:     [========================================] 834 shares                      |
| 2. Referee Registered:  [======] 14.3% (119 users acquired)                                         |
| 3. Referee Activated:   [====] 9.4% (78 completed >= 1 task)                                       |
| 4. Referral Converted:  [===] 7.4% (62 bonuses paid)                                               |
+----------------------------------------------------------------------------------------------------+
| SHARING CHANNEL RESIDUAL EFFICIENCY        | TOP ADVOCATE LEADERBOARD (Qualified Referees)         |
| WhatsApp:       [==============] 45%      | 1. VLUSR000142: 18 Activated Referees (2,400 XP)       |
| Telegram:       [==========] 28%           | 2. VLUSR000881: 14 Activated Referees (1,850 XP)       |
| Direct Copy:    [======] 16%               | 3. VLUSR000419: 11 Activated Referees (1,400 XP)       |
| Social Media:   [====] 11%                 | 4. VLUSR000072: 9 Activated Referees (1,150 XP)        |
+----------------------------------------------------------------------------------------------------+
```

#### Detailed Visual Specifications:

##### Visual 7.1: 4-Stage Referral Funnel
* **Metric:** Step-by-Step Conversion across the Referral Funnel.
* **Calculation:** Counts and percentages across `Shared`, `Registered`, `Activated`, and `Converted`.
* **Source:** `fact_referral_conversions` joined with `fact_feature_events`.
* **Visualization:** Stepped Funnel Chart.
* **Filters:** Sharing Channel, Referrer Cohort.
* **Dimensions:** Referral Lifecycle Stage.
* **Date Range:** Last 60 Days.
* **Refresh Frequency:** Daily at 02:00 UTC.
* **Business Question:** Where is viral acquisition leaking—at the signup stage or the first task activation stage?
* **Decision Supported:** Informs onboarding prompts for newly referred users to drive first task completion.

##### Visual 7.2: Sharing Channel Conversion Efficiency
* **Metric:** Conversion Rate from Share to Activated User by Channel.
* **Calculation:** $\frac{\text{Activated Referees}_{\text{channel}}}{\text{Total Shares}_{\text{channel}}} \times 100$.
* **Source:** `fact_referral_conversions`.
* **Visualization:** Grouped Column Chart.
* **Filters:** Platform.
* **Dimensions:** `sharing_channel`.
* **Date Range:** Last 30 Days.
* **Refresh Frequency:** Weekly.
* **Business Question:** Which social messaging channels deliver the highest quality active users?
* **Decision Supported:** Re-orders share CTA buttons in the client UI to prioritize high-converting channels.
