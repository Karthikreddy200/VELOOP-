# VELOOP REWARDS — WORK PACKAGE I
## Master Enterprise KPI Catalogue (35 Standardized KPIs)
**Document ID:** VELOOP-DELIV-11  
**Deliverable Covered:** Deliverable 11 (KPI Catalogue)  
**Classification:** SIMULATED DATA — CREATED FOR ANALYTICAL TESTING  
**Status Standard:** Confirmed | Proposed | To Be Verified  

---

### 1. Governance Principles & Strict Target Discipline

In strict compliance with the **VELOOP Non-Negotiable Integrity Rules**:
* **No fictional company targets are invented** (e.g., prohibiting claims like *"VELOOP should reach 100,000 DAU"* or *"Target withdrawal success is 99%"*).
* Every KPI in this master catalogue is defined with an unambiguous mathematical formula, necessary schema fields, data sources, update cadences, stakeholder accountability, operational interpretations, and analytical boundaries.

The catalogue establishes **35 operational and strategic metrics** organized across 7 core functional pillars:
1. User Lifecycle KPIs (KPIs 01–05)
2. Engagement & Activity KPIs (KPIs 06–11)
3. Reward & Gamification KPIs (KPIs 12–16)
4. Wallet & Ledger KPIs (KPIs 17–21)
5. Withdrawal & Payout KPIs (KPIs 22–27)
6. Referral & Viral Growth KPIs (KPIs 28–31)
7. Support & Customer Operations KPIs (KPIs 32–35)

---

### 2. Domain 1: User Lifecycle KPIs

#### KPI 01: Daily Active Users (DAU)
* **Definition:** The count of unique authenticated users who generate at least one qualifying telemetry interaction event within a 24-hour UTC calendar day.
* **Formula:**  
  $$\text{DAU}_t = \text{COUNT}(\text{DISTINCT } \text{user\_id}) \quad \forall \; \text{event\_datetime} \in [t_{\text{00:00:00}}, t_{\text{23:59:59}}]$$
* **Required Fields:** `fact_feature_events.user_id`, `event_datetime`.
* **Data Source:** `fact_feature_events` (or `fact_daily_user_summary` where `active_flag = 'Yes'`).
* **Frequency:** Daily.
* **Stakeholder:** Executive Leadership, Head of Product.
* **Business Purpose:** Core barometer of platform scale and daily engagement reach.
* **Interpretation:** Sustained day-over-day growth signals healthy product-market fit; sharp contractions highlight outages or app store visibility drops.
* **Limitation:** Does not distinguish between passive single-tap users and highly active multiple-task earners.
* **Status:** Confirmed.

#### KPI 02: Weekly Active Users (WAU)
* **Definition:** The count of unique authenticated users who generated at least one qualifying activity event in the trailing 7 rolling calendar days.
* **Formula:**  
  $$\text{WAU}_t = \text{COUNT}(\text{DISTINCT } \text{user\_id}) \quad \forall \; \text{event\_datetime} \in [t - 6\text{d}, t]$$
* **Required Fields:** `fact_feature_events.user_id`, `event_datetime`.
* **Data Source:** `fact_feature_events`.
* **Frequency:** Weekly (computed daily on a rolling 7-day window).
* **Stakeholder:** Product Management, Growth Team.
* **Business Purpose:** Smooths weekday/weekend volatility to track medium-term user reach.
* **Interpretation:** Upward trend indicates strong weekly habituation across casual earners.
* **Limitation:** Insensitive to mid-week churn if the user was active on Day 1 of the 7-day window.
* **Status:** Confirmed.

#### KPI 03: Monthly Active Users (MAU)
* **Definition:** The count of unique authenticated users who generated at least one qualifying activity event in the trailing 30 rolling calendar days.
* **Formula:**  
  $$\text{MAU}_t = \text{COUNT}(\text{DISTINCT } \text{user\_id}) \quad \forall \; \text{event\_datetime} \in [t - 29\text{d}, t]$$
* **Required Fields:** `fact_feature_events.user_id`, `event_datetime`.
* **Data Source:** `fact_feature_events`.
* **Frequency:** Monthly (rolling 30-day window).
* **Stakeholder:** Board of Directors, Executive Leadership, Marketing.
* **Business Purpose:** High-level platform audience sizing for advertisers and financial stakeholders.
* **Interpretation:** Macro-scale platform health metric.
* **Limitation:** Broad 30-day window can mask acute recent cohort churn.
* **Status:** Confirmed.

#### KPI 04: New Registered Users (NRU)
* **Definition:** Count of newly provisioned user accounts successfully created within a reporting period.
* **Formula:**  
  $$\text{NRU}_t = \sum \mathbf{1}_{\{\text{registration\_datetime} \in \text{Period } t\}}$$
* **Required Fields:** `dim_users.user_id`, `registration_datetime`.
* **Data Source:** `dim_users`.
* **Frequency:** Daily, Weekly, Monthly.
* **Stakeholder:** User Acquisition Lead, Performance Marketing.
* **Business Purpose:** Evaluates top-of-funnel customer acquisition pipeline volume.
* **Interpretation:** Spikes indicate effective marketing campaigns or viral referral loops.
* **Limitation:** Raw signups do not reflect actual user activation or retention.
* **Status:** Confirmed.

#### KPI 05: Dormant User Volume & Rate
* **Definition:** Count and percentage of registered accounts with zero activity events for 14 to 29 consecutive days.
* **Formula:**  
  $$\text{Dormant Users}_t = \text{COUNT}(\text{user\_id}) \quad \text{where } (t - \text{last\_login\_datetime}) \in [14\text{d}, 29\text{d}]$$  
  $$\text{Dormancy Rate} = \frac{\text{Dormant Users}_t}{\text{Total Cumulative Registered Users}_t} \times 100$$
* **Required Fields:** `dim_users.user_id`, `last_login_datetime`, `account_status`.
* **Data Source:** `dim_users`.
* **Frequency:** Weekly.
* **Stakeholder:** CRM Lead, Lifecycle Marketing.
* **Business Purpose:** Target population for push notification and email re-engagement campaigns before permanent churn occurs.
* **Interpretation:** Rising dormancy indicates post-onboarding fatigue or lack of fresh earning task inventory.
* **Limitation:** Does not capture uninstalled app clients where push notifications will fail.
* **Status:** Proposed.

---

### 3. Domain 2: Engagement & Activity KPIs

#### KPI 06: Platform Stickiness Ratio (DAU / MAU)
* **Definition:** The ratio of daily active users to monthly active users, expressed as a percentage.
* **Formula:**  
  $$\text{Stickiness (\%)} = \frac{\text{DAU}_t}{\text{MAU}_t} \times 100$$
* **Required Fields:** `DAU`, `MAU`.
* **Data Source:** Derived from `fact_daily_user_summary`.
* **Frequency:** Daily trend.
* **Stakeholder:** Head of Product.
* **Business Purpose:** Quantifies how frequently the monthly active user base returns on an average day.
* **Interpretation:** Ratios between $20\%\text{--}30\%$ indicate steady weekly utility; ratios $> 40\%$ signify strong daily habituation.
* **Limitation:** A surge in new user signups inflates MAU faster than DAU, temporarily depressing the ratio.
* **Status:** Proposed.

#### KPI 07: Feature Penetration Rate
* **Definition:** Percentage of active users who interact with a specific product feature within a defined timeframe.
* **Formula:**  
  $$\text{Penetration}_{\text{feature}} = \frac{\text{COUNT}(\text{DISTINCT } \text{user\_id } | \text{ feature\_name} = f)}{\text{Total DAU in Period}} \times 100$$
* **Required Fields:** `fact_feature_events.user_id`, `feature_name`, `event_datetime`.
* **Data Source:** `fact_feature_events` (or `07_Feature_Usage`).
* **Frequency:** Weekly, Monthly.
* **Stakeholder:** Feature Product Managers.
* **Business Purpose:** Identifies feature discoverability bottlenecks and guides UX real estate allocation.
* **Interpretation:** High engagement features (e.g. Watch Ads at $83.6\%$) represent primary earning hubs; low penetration features (Badges at $67.4\%$) require gamified discovery prompts.
* **Limitation:** Measures any interaction, regardless of whether the user successfully earned a reward.
* **Status:** Confirmed.

#### KPI 08: Average Session Duration (ASD)
* **Definition:** The mean duration in seconds across all closed engagement sessions in a reporting window.
* **Formula:**  
  $$\text{ASD} = \frac{\sum \text{session\_duration\_seconds}}{\text{Total Sessions Count}}$$
* **Required Fields:** `dim_sessions.session_duration_seconds`, `session_status = 'Closed'`.
* **Data Source:** `dim_sessions`.
* **Frequency:** Daily, Weekly.
* **Stakeholder:** UX/UI Design Team, Product Analyst.
* **Business Purpose:** Measures user attention depth and time-spent on platform.
* **Interpretation:** In micro-earning apps, sessions that are too short ($< 15\text{s}$) indicate bounces; moderate sessions ($3\text{--}8\text{ mins}$) indicate multi-task completion.
* **Limitation:** Distorted by abandoned sessions left open in background tabs before timeout.
* **Status:** Confirmed.

#### KPI 09: Task Start Volume
* **Definition:** Total gross count of task executions initiated by users.
* **Formula:**  
  $$\text{Task Starts} = \sum \mathbf{1}_{\{\text{event\_name} = \text{'task\_started'}\}}$$
* **Required Fields:** `fact_task_activity.activity_id`, `task_started_at`.
* **Data Source:** `fact_task_activity`.
* **Frequency:** Daily.
* **Stakeholder:** Operations / Offerwall Manager.
* **Business Purpose:** Measures top-of-funnel earning intent and demand for task inventory.
* **Interpretation:** Divergence between task starts and ad inventory indicates partner API exhaustion.
* **Limitation:** Does not reflect whether tasks were successfully completed.
* **Status:** Confirmed.

#### KPI 10: Task Completion Rate (TCR)
* **Definition:** The percentage of initiated task attempts that reach successful completion.
* **Formula:**  
  $$\text{TCR (\%)} = \frac{\sum \mathbf{1}_{\{\text{task\_status} = \text{'Completed'}\}}}{\sum \mathbf{1}_{\{\text{task\_status} \in ('\text{Completed}', '\text{Abandoned}', '\text{Failed}')\}}} \times 100$$
* **Required Fields:** `fact_task_activity.task_status`.
* **Data Source:** `fact_task_activity`.
* **Frequency:** Daily, sliced by `task_category`.
* **Stakeholder:** Offerwall Operations Lead, Product Analyst.
* **Business Purpose:** Identifies task friction, technical bugs, or excessive task difficulty.
* **Interpretation:** A low completion rate on surveys indicates demographic screener disqualifications; low completion on video ads signals video player buffering or crashes.
* **Limitation:** In-flight pending tasks must be excluded from the denominator.
* **Status:** Confirmed.

#### KPI 11: Repeat Task User Ratio (Habitual Earner Ratio)
* **Definition:** The proportion of active users who complete $\ge 3$ distinct tasks within a 7-day period.
* **Formula:**  
  $$\text{Habitual Earner Ratio (\%)} = \frac{\text{COUNT}(\text{DISTINCT } \text{user\_id } | \text{ Completed Tasks} \ge 3)}{\text{Total WAU}} \times 100$$
* **Required Fields:** `fact_task_activity.user_id`, `task_status = 'Completed'`, `task_completed_at`.
* **Data Source:** `fact_task_activity`.
* **Frequency:** Weekly.
* **Stakeholder:** Product Retention Lead.
* **Business Purpose:** Isolates high-value habitual earners from casual single-task visitors.
* **Interpretation:** Higher ratios correlate strongly with 30-day retention and lifetime value (LTV).
* **Limitation:** Does not weigh the economic value of tasks completed (e.g. 3 micro-taps vs 3 high-paying app installs).
* **Status:** Proposed.

---

### 4. Domain 3: Reward & Gamification KPIs

#### KPI 12: Gross Reward Issuance Volume
* **Definition:** Total monetary and gamified value awarded to users across all features, segmented by currency unit.
* **Formula:**  
  $$\text{Gross Issuance}_{\text{unit}} = \sum (\text{amount} \times \mathbf{1}_{\{\text{transaction\_type} = \text{'REWARD\_CREDIT'}\}})$$
* **Required Fields:** `fact_wallet_transactions.amount`, `currency_unit`, `transaction_type`.
* **Data Source:** `fact_wallet_transactions`.
* **Frequency:** Daily, Monthly.
* **Stakeholder:** Head of Finance, Economy Designer.
* **Business Purpose:** Monitors total platform liability generation and inflation rate across XP, Gems, and Tokens.
* **Interpretation:** Rapid acceleration without corresponding ad revenue growth signals an unsustainable reward economy or bot exploitation.
* **Limitation:** Expresses gross issuance; does not net out reversals or clawbacks.
* **Status:** Proposed.

#### KPI 13: Reward Credit Transaction Count
* **Definition:** The count of discrete successful reward ledger transactions executed.
* **Formula:**  
  $$\text{Reward Transactions} = \sum \mathbf{1}_{\{\text{transaction\_type} = \text{'REWARD\_CREDIT'}\}}$$
* **Required Fields:** `fact_wallet_transactions.transaction_id`, `transaction_type`.
* **Data Source:** `fact_wallet_transactions`.
* **Frequency:** Daily.
* **Stakeholder:** Backend Engineering Lead, Wallet Team.
* **Business Purpose:** Measures database write throughput and reward event frequency.
* **Interpretation:** Benchmark for ledger database capacity planning and concurrency stress.
* **Limitation:** Does not reflect the monetary size of transactions.
* **Status:** Proposed.

#### KPI 14: Reward Reversal Rate
* **Definition:** Percentage of issued rewards that are subsequently clawed back or reversed due to fraud or partner chargebacks.
* **Formula:**  
  $$\text{Reversal Rate (\%)} = \frac{\sum (\text{amount} \times \mathbf{1}_{\{\text{transaction\_type} = \text{'REVERSAL'}\}})}{\sum (\text{amount} \times \mathbf{1}_{\{\text{transaction\_type} = \text{'REWARD\_CREDIT'}\}})} \times 100$$
* **Required Fields:** `fact_wallet_transactions.amount`, `transaction_type`.
* **Data Source:** `fact_wallet_transactions`.
* **Frequency:** Weekly, Monthly.
* **Stakeholder:** Fraud & Risk Team, Offerwall Partnerships.
* **Business Purpose:** Identifies toxic partner networks and fraudulent user rings.
* **Interpretation:** Reversal rates $> 5\%$ on an affiliate network warrant immediate contract renegotiation or source pause.
* **Limitation:** Partner clawbacks lag by up to 30 days, creating a delayed reporting signal.
* **Status:** Proposed.

#### KPI 15: Reward Activity Distribution by Feature
* **Definition:** Percentage share of total rewards distributed across each contributing feature.
* **Formula:**  
  $$\text{Share}_{\text{feature}} = \frac{\text{Issuance}_{\text{feature}}}{\text{Total Gross Issuance}} \times 100$$
* **Required Fields:** `fact_wallet_transactions.amount`, `source_module`.
* **Data Source:** `fact_wallet_transactions`.
* **Frequency:** Monthly.
* **Stakeholder:** Game Economy Designer, Product Lead.
* **Business Purpose:** Monitors reliance on specific earning mechanics (e.g. AdMob vs Surveys vs Streaks).
* **Interpretation:** Over-reliance on passive mining rewards indicates risk if ad revenue shifts.
* **Limitation:** Compares nominal token/XP amounts; currency exchange rates must be normalized.
* **Status:** Proposed.

#### KPI 16: Average Reward Velocity per Active User
* **Definition:** The mean reward units earned per active user per day.
* **Formula:**  
  $$\text{Reward Velocity} = \frac{\text{Total Daily Issuance Volume}}{\text{DAU}_t}$$
* **Required Fields:** `fact_wallet_transactions.amount`, `fact_daily_user_summary.user_id`.
* **Data Source:** Joined `fact_wallet_transactions` and `fact_daily_user_summary`.
* **Frequency:** Daily trend.
* **Stakeholder:** Economy Designer.
* **Business Purpose:** Tracks user progression speed towards minimum withdrawal thresholds.
* **Interpretation:** If velocity is too low, time-to-cash-out is excessive, causing user churn; if too high, platform burn rate escalates.
* **Limitation:** Heavily skewed by extreme power earners; should be paired with median velocity.
* **Status:** Proposed.

---

### 5. Domain 4: Wallet & Ledger KPIs

#### KPI 17: Total Wallet Transaction Volume
* **Definition:** Gross count and absolute volume of all ledger mutations (Credits, Debits, Exchanges, Adjustments).
* **Formula:**  
  $$\text{Ledger Turnover} = \sum |\text{amount}| \quad \forall \; \text{fact\_wallet\_transactions}$$
* **Required Fields:** `fact_wallet_transactions.amount`, `transaction_timestamp`.
* **Data Source:** `fact_wallet_transactions`.
* **Frequency:** Daily.
* **Stakeholder:** Wallet Engineering, Internal Audit.
* **Business Purpose:** Measures total transactional velocity and system throughput.
* **Interpretation:** Core input for ledger database scalability and latency monitoring.
* **Limitation:** Combines positive credits and negative debits.
* **Status:** Proposed.

#### KPI 18: Net Token Liability (System Balance)
* **Definition:** The cumulative sum of all unredeemed, circulating tokens and XP held in user wallets across the platform.
* **Formula:**  
  $$\text{Circulating Liability} = \sum_{\text{users}} \text{current\_token\_balance}$$
* **Required Fields:** `dim_users.current_token_balance`, `current_xp_balance`.
* **Data Source:** `dim_users` (or snapshot sum of `running_balance_after`).
* **Frequency:** Daily at 00:00 UTC.
* **Stakeholder:** Chief Financial Officer (CFO), Treasury.
* **Business Purpose:** Quantifies total outstanding financial obligation owed to users.
* **Interpretation:** Critical for treasury pre-funding; ensures liquid bank reserves match outstanding token liabilities.
* **Limitation:** Includes tokens held by dormant/abandoned accounts that may never be redeemed (breakage).
* **Status:** Proposed.

#### KPI 19: Internal Currency Exchange Volume
* **Definition:** Total gross volume of secondary currency (XP / Gems) converted into primary redeemable Tokens within the Exchange Center.
* **Formula:**  
  $$\text{Exchange Volume} = \sum (\text{amount} \times \mathbf{1}_{\{\text{transaction\_type} = \text{'EXCHANGE\_CONVERSION'}\}})$$
* **Required Fields:** `fact_wallet_transactions.amount`, `source_module = 'EXCHANGE'`.
* **Data Source:** `fact_wallet_transactions`.
* **Frequency:** Weekly, Monthly.
* **Stakeholder:** Product Manager (Monetization).
* **Business Purpose:** Measures user progression from gamified status (XP) to monetary cash-out intent (Tokens).
* **Interpretation:** Surges in exchange volume precede spikes in withdrawal requests.
* **Limitation:** Does not reflect external fiat cash flow until a withdrawal is requested.
* **Status:** Proposed.

#### KPI 20: Ledger Reversal & Adjustment Rate
* **Definition:** The frequency of administrative corrections and clawback transactions relative to total completed transactions.
* **Formula:**  
  $$\text{Adjustment Rate (\%)} = \frac{\sum \mathbf{1}_{\{\text{transaction\_type} \in ('\text{REVERSAL}', '\text{ADMIN\_ADJUSTMENT}')\}}}{\sum \mathbf{1}_{\{\text{All Transactions}\}}} \times 100$$
* **Required Fields:** `fact_wallet_transactions.transaction_type`.
* **Data Source:** `fact_wallet_transactions`.
* **Frequency:** Monthly.
* **Stakeholder:** Finance Controller, Lead Data Engineer.
* **Business Purpose:** Detects operational errors, customer support over-rides, and ledger drift.
* **Interpretation:** Rates $> 1.0\%$ signal systemic backend synchronization flaws or excessive manual customer support interventions.
* **Limitation:** Combines automated fraud clawbacks with manual human error corrections.
* **Status:** Proposed.

#### KPI 21: Active Wallet Check Frequency
* **Definition:** Mean number of times active users navigate to the wallet screen per active day.
* **Formula:**  
  $$\text{Wallet Views per User} = \frac{\sum \mathbf{1}_{\{\text{event\_name} = \text{'wallet\_viewed'}\}}}{\text{DAU}_t}$$
* **Required Fields:** `fact_feature_events.event_name`, `fact_feature_events.user_id`.
* **Data Source:** `fact_feature_events`.
* **Frequency:** Weekly.
* **Stakeholder:** UX Designer, Product Lead.
* **Business Purpose:** Gauges user financial consciousness and anticipation of cash-out.
* **Interpretation:** Simulated data indicates high curiosity (2,172 wallet views across 810 users, averaging 2.68 views/user).
* **Limitation:** Viewing a wallet does not imply the user possesses a redeemable balance.
* **Status:** Confirmed.

---

### 6. Domain 5: Withdrawal & Payout KPIs

#### KPI 22: Gross Withdrawal Request Volume & Count
* **Definition:** Total gross fiat value and discrete count of payout requests submitted within a reporting period.
* **Formula:**  
  $$\text{Withdrawal Count} = \sum \mathbf{1}_{\{\text{fact\_withdrawals}\}}, \quad \text{Gross Volume} = \sum \text{requested\_amount}$$
* **Required Fields:** `fact_withdrawals.withdrawal_id`, `requested_amount`, `requested_timestamp`.
* **Data Source:** `fact_withdrawals`.
* **Frequency:** Daily, Weekly.
* **Stakeholder:** Treasury, Operations Manager.
* **Business Purpose:** Tracks gross outflow demand and cash burn trajectory.
* **Interpretation:** Early warning metric for treasury liquidity management.
* **Limitation:** Unsettled requests do not represent finalized cash deductions.
* **Status:** Proposed.

#### KPI 23: Completed Withdrawal Settlement Volume
* **Definition:** Total finalized fiat cash disbursed and settled into user external payment accounts.
* **Formula:**  
  $$\text{Settled Volume} = \sum (\text{requested\_amount} \times \mathbf{1}_{\{\text{withdrawal\_status} = \text{'COMPLETED'}\}})$$
* **Required Fields:** `fact_withdrawals.requested_amount`, `withdrawal_status = 'COMPLETED'`.
* **Data Source:** `fact_withdrawals` joined with gateway bank settlement logs.
* **Frequency:** Daily, Monthly.
* **Stakeholder:** Chief Financial Officer (CFO).
* **Business Purpose:** Primary cash-out figure for accounting financial statements.
* **Interpretation:** Reflects true fulfilled value delivered to users.
* **Limitation:** Excludes gateway processing transaction fees.
* **Status:** Proposed.

#### KPI 24: End-to-End Payout SLA (Processing Duration)
* **Definition:** Elapsed time in hours from user request submission to gateway settlement confirmation.
* **Formula:**  
  $$\text{SLA Latency} = \text{settlement\_timestamp} - \text{requested\_timestamp}$$  
  $$\text{Median SLA} = \text{Median}(\text{SLA Latency}), \quad P_{95}\text{ SLA} = \text{Percentile}_{95}(\text{SLA Latency})$$
* **Required Fields:** `requested_timestamp`, `settlement_timestamp`, `withdrawal_status = 'COMPLETED'`.
* **Data Source:** `fact_withdrawals`.
* **Frequency:** Weekly.
* **Stakeholder:** Head of Customer Operations, Product Lead.
* **Business Purpose:** Monitors adherence to published user payout guarantees (e.g. 24–48 hour SLA).
* **Interpretation:** Divergence between median and $P_{95}$ indicates a heavy operational tail of stuck manual reviews.
* **Limitation:** Banking holidays artificially inflate latency for ACH and wire transfers.
* **Status:** Proposed.

#### KPI 25: Withdrawal Completion (Fulfillment) Rate
* **Definition:** Percentage of submitted withdrawal requests that successfully conclude in settled payout.
* **Formula:**  
  $$\text{Fulfillment Rate (\%)} = \frac{\sum \mathbf{1}_{\{\text{status} = \text{'COMPLETED'}\}}}{\sum \mathbf{1}_{\{\text{status} \in ('\text{COMPLETED}', '\text{REJECTED}', '\text{REVERSED}')\}}} \times 100$$
* **Required Fields:** `fact_withdrawals.withdrawal_status`.
* **Data Source:** `fact_withdrawals`.
* **Frequency:** Weekly, Monthly.
* **Stakeholder:** Executive Leadership.
* **Business Purpose:** Core brand trust and operational reliability metric.
* **Interpretation:** Low fulfillment destroys user ratings and triggers viral churn.
* **Limitation:** In-flight pending requests must be excluded from denominator.
* **Status:** Proposed.

#### KPI 26: Withdrawal Rejection Rate
* **Definition:** Percentage of withdrawal requests blocked by automated risk rules or compliance reviewers prior to gateway dispatch.
* **Formula:**  
  $$\text{Rejection Rate (\%)} = \frac{\sum \mathbf{1}_{\{\text{status} = \text{'REJECTED'}\}}}{\text{Total Resolved Requests}} \times 100$$
* **Required Fields:** `fact_withdrawals.withdrawal_status`.
* **Data Source:** `fact_withdrawals`.
* **Frequency:** Weekly.
* **Stakeholder:** Fraud & Risk Team, Compliance Officer.
* **Business Purpose:** Measures bot attack mitigation and monitors false-positive friction.
* **Interpretation:** High rejection indicates coordinated fraud attempts or overly strict heuristics.
* **Limitation:** Does not confirm guilt without manual case audit.
* **Status:** Proposed.

#### KPI 27: Post-Dispatch Payout Reversal Rate
* **Definition:** Percentage of payouts dispatched to gateways that bounce or fail due to external banking issues.
* **Formula:**  
  $$\text{Payout Reversal Rate (\%)} = \frac{\sum \mathbf{1}_{\{\text{status} = \text{'REVERSED'}\}}}{\sum \mathbf{1}_{\{\text{status} \in ('\text{COMPLETED}', '\text{REVERSED}')\}}} \times 100$$
* **Required Fields:** `fact_withdrawals.withdrawal_status`.
* **Data Source:** `fact_withdrawals`.
* **Frequency:** Weekly, Monthly.
* **Stakeholder:** Payments Engineering Lead.
* **Business Purpose:** Detects invalid user payment inputs (wrong UPI ID, closed PayPal account) and gateway outages.
* **Interpretation:** Spikes on a specific payment rail indicate provider technical degradation.
* **Limitation:** Webhook bounce signals can lag by several days.
* **Status:** Proposed.

---

### 7. Domain 6: Referral & Viral Growth KPIs

#### KPI 28: Referral Link Creation & Share Volume
* **Definition:** Total gross count of referral links generated and shared across social channels.
* **Formula:**  
  $$\text{Share Volume} = \sum \mathbf{1}_{\{\text{event\_name} = \text{'referral\_shared'}\}}$$
* **Required Fields:** `fact_feature_events.event_name`, `timestamp`.
* **Data Source:** `fact_feature_events`.
* **Frequency:** Daily.
* **Stakeholder:** Growth Marketing Lead.
* **Business Purpose:** Measures top-of-funnel advocacy and organic distribution effort.
* **Interpretation:** Simulated data reveals 834 shares across 811 users, demonstrating strong organic sharing intent.
* **Limitation:** Does not guarantee external clicks or app downloads.
* **Status:** Confirmed.

#### KPI 29: Referral Registration Conversion Rate
* **Definition:** Percentage of shared referral invitations that result in a successfully registered user account.
* **Formula:**  
  $$\text{Reg Conversion Rate (\%)} = \frac{\text{Total Referral Registrations}}{\text{Total Referral Shares}} \times 100$$
* **Required Fields:** `fact_referral_conversions.registration_timestamp`, `fact_feature_events.event_name = 'referral_shared'`.
* **Data Source:** Joined `fact_feature_events` and `fact_referral_conversions`.
* **Frequency:** Weekly.
* **Stakeholder:** Growth Lead.
* **Business Purpose:** Measures landing page conversion efficiency and invite copy resonance.
* **Interpretation:** Low conversion suggests landing page friction or broken deep links.
* **Limitation:** Dark social sharing (direct copy-paste) complicates exact denominator tracking.
* **Status:** Proposed.

#### KPI 30: Referee Activation Rate (RAR)
* **Definition:** Percentage of referred registered users who complete at least one qualified monetizable task within 14 days of signup.
* **Formula:**  
  $$\text{RAR (\%)} = \frac{\sum \mathbf{1}_{\{\text{activation\_timestamp is not null}\}}}{\sum \mathbf{1}_{\{\text{registration\_timestamp is not null}\}}} \times 100$$
* **Required Fields:** `fact_referral_conversions.activation_timestamp`, `registration_timestamp`.
* **Data Source:** `fact_referral_conversions`.
* **Frequency:** Weekly cohort.
* **Stakeholder:** Lifecycle Marketer, Growth Product Manager.
* **Business Purpose:** Core quality filter distinguishing valuable users from referral bonus hunters.
* **Interpretation:** Crucial gate before distributing advocate bonuses.
* **Limitation:** Requires a 14-day maturation window to mature each weekly cohort.
* **Status:** Proposed.

#### KPI 31: Viral Coefficient ($K$-Factor)
* **Definition:** The number of newly activated users generated by each existing active user.
* **Formula:**  
  $$K = i \times c$$  
  $$\text{where } i = \frac{\text{Total Invites Sent}}{\text{Active Users}}, \quad c = \frac{\text{Activated Referees}}{\text{Total Invites Sent}}$$
* **Required Fields:** `fact_feature_events`, `fact_referral_conversions`.
* **Data Source:** Derived growth model.
* **Frequency:** Monthly.
* **Stakeholder:** Head of Growth, Executive Leadership.
* **Business Purpose:** Evaluates whether viral growth is self-sustaining ($K > 1.0$) or requires paid marketing ($K < 1.0$).
* **Interpretation:** If $K = 0.25$, for every 100 acquired users, 25 additional users join organically through referrals.
* **Limitation:** High $K$-factor with low Day-30 retention will still result in platform contraction.
* **Status:** Proposed.

---

### 8. Domain 7: Support & Operations KPIs

#### KPI 32: Support Request Volume
* **Definition:** Total count of discrete customer service tickets submitted by users.
* **Formula:**  
  $$\text{Ticket Volume} = \sum \mathbf{1}_{\{\text{event\_name} = \text{'support\_ticket_created'}\}}$$
* **Required Fields:** `ticket_id`, `created_at`.
* **Data Source:** Support Helpdesk API / Telemetry.
* **Frequency:** Daily, Weekly.
* **Stakeholder:** Head of Customer Support.
* **Business Purpose:** Measures platform friction, bug incidence, and support team workload.
* **Interpretation:** Spikes following app updates indicate release regressions or gateway payment outages.
* **Limitation:** Many frustrated users churn silently without opening tickets.
* **Status:** Proposed.

#### KPI 33: Ticket Distribution by Product Issue Category
* **Definition:** Percentage breakdown of support requests split across functional categories (Payout Issues, Task Verification, Account Access, Bugs).
* **Formula:**  
  $$\text{Share}_{\text{category}} = \frac{\text{Tickets}_{\text{category}}}{\text{Total Resolved Tickets}} \times 100$$
* **Required Fields:** `ticket_id`, `issue_category`.
* **Data Source:** Support Helpdesk API.
* **Frequency:** Monthly.
* **Stakeholder:** Product Operations, Quality Assurance (QA).
* **Business Purpose:** Highlights which product features generate the greatest operational drag and user confusion.
* **Interpretation:** Over $50\%$ in withdrawal categories signals urgent need for transparent in-app payout status tracking.
* **Limitation:** Relies on accurate categorization by support agents.
* **Status:** Proposed.

#### KPI 34: Help Center Self-Service Resolution Rate
* **Definition:** Percentage of users who view FAQ articles and exit without opening a formal support ticket within 2 hours.
* **Formula:**  
  $$\text{Self-Service Rate (\%)} = \frac{\text{FAQ Visitors who do NOT open a ticket}}{\text{Total Unique FAQ Article Visitors}} \times 100$$
* **Required Fields:** `fact_feature_events.feature_name = 'Help Center'`, `ticket_id`.
* **Data Source:** Joined `fact_feature_events` and support tickets.
* **Frequency:** Monthly.
* **Stakeholder:** Customer Operations Lead, Technical Writer.
* **Business Purpose:** Measures the efficacy of documentation in resolving user issues autonomously.
* **Interpretation:** Higher rates lower support overhead costs and improve user autonomy.
* **Limitation:** A user may read an unhelpful FAQ and abandon the app entirely in disgust rather than submit a ticket.
* **Status:** Proposed.

#### KPI 35: Mean Time to Resolution (MTTR)
* **Definition:** Average elapsed time in hours from ticket submission to verified ticket resolution.
* **Formula:**  
  $$\text{MTTR} = \frac{\sum (\text{resolved\_timestamp} - \text{created\_timestamp})}{\text{Total Resolved Tickets}}$$
* **Required Fields:** `ticket_id`, `created_timestamp`, `resolved_timestamp`.
* **Data Source:** Support Helpdesk API.
* **Frequency:** Weekly, Monthly.
* **Stakeholder:** Customer Support Lead.
* **Business Purpose:** Operational efficiency and user satisfaction (CSAT) benchmark.
* **Interpretation:** Extended MTTR on payment disputes severely damages brand reputation.
* **Limitation:** Complex fraud investigations inflate the metric average; median MTTR should be reported concurrently.
* **Status:** Proposed.
