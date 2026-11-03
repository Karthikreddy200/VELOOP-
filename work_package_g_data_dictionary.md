# VELOOP REWARDS — WORK PACKAGE G
## Enterprise Data Dictionary (85 Standardized Fields)
**Document ID:** VELOOP-DELIV-09  
**Deliverable Covered:** Deliverable 09 (VELOOP Data Dictionary)  
**Classification:** SIMULATED DATA — CREATED FOR ANALYTICAL TESTING  
**Status Standard:** Confirmed | Proposed | To Be Verified  

---

### 1. Architectural Overview & Governance

This **Enterprise Data Dictionary** establishes the formal schema contract for the analytical data warehouse of VELOOP Rewards. It covers **85 standardized, meaningful fields** across 9 core entities:

1. `dim_users` (User Dimension — 18 fields)
2. `dim_sessions` (Session Dimension — 10 fields)
3. `fact_feature_events` (Telemetry Event Log — 11 fields)
4. `dim_tasks` (Task Catalog Dimension — 8 fields)
5. `fact_task_activity` (Task Execution Fact — 11 fields)
6. `fact_wallet_transactions` (Double-Entry Ledger Fact — 10 fields)
7. `fact_withdrawals` (Withdrawal Settlement Fact — 11 fields)
8. `fact_referral_conversions` (Referral Attribution Fact — 8 fields)
9. `fact_daily_user_summary` (Aggregated Daily Engagement Fact — 8 fields)

#### Sensitivity Tiers:
* **Public:** Non-sensitive operational codes, public task metadata, and system enumerations.
* **Internal:** Non-PII behavioral telemetry, aggregated engagement metrics, and operational timestamps accessible to analysts.
* **Restricted:** Highly sensitive security tokens, anti-fraud risk scores, device hashes, and financial settlement data requiring restricted IAM role access.

---

### 2. Entity 1: `dim_users` (User Account Dimension)

| Field Name | Data Type | Definition | Example | Required? | Allowed Values | Validation Rule | Source Engine | Sensitivity | Analytical Use | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| `user_id` | String | Permanent immutable global user identifier | `usr_9a8b7c6d5e` | Yes | Alphanumeric UUIDv4 | Unique PK; non-null; regex `^usr_[a-zA-Z0-9_\-]+$` | Auth Service | Internal | Global join key across all facts | Confirmed |
| `registration_datetime` | Timestamp | UTC timestamp of initial account creation | `2026-06-10 07:14:00` | Yes | Valid ISO 8601 UTC | $\le \text{Current Time}$ | Auth Service | Internal | Cohort retention baselines (D1, D7, D30) | Confirmed |
| `registration_channel` | String | High-level marketing acquisition channel | `Organic Search` | Yes | `Organic Search`, `Direct`, `Social Media`, `Referral`, `WhatsApp`, `Telegram`, `Other` | Whitelist enum | Client / SDK | Internal | Acquisition channel CAC & ROI | Confirmed |
| `referral_source_detail` | String | Granular context for referral origin | `Friend/Family` | No | `Friend/Family`, `Influencer`, `Community`, `Paid Affiliate` | Nullable if non-referral | Client / SDK | Internal | Sub-channel viral segmentation | Confirmed |
| `referral_code` | String | Unique referral code assigned to user | `VL850800` | Yes | Alphanumeric (6-10 chars) | Unique; non-null; uppercase | Referral Engine | Internal | Advocate tracking and code distribution | Confirmed |
| `primary_platform` | String | Most frequent operating system platform | `Android` | Yes | `Android`, `iOS`, `Web` | Whitelist enum | Client SDK | Internal | Platform health and feature parity analysis | Confirmed |
| `primary_device_category` | String | Physical hardware form factor | `Mobile` | Yes | `Mobile`, `Tablet`, `Desktop` | Whitelist enum | Client User-Agent| Internal | Hardware segmentation and UI optimization | Confirmed |
| `account_status` | String | Current lifecycle and operational state | `Active` | Yes | `Active`, `Inactive`, `Suspended`, `Pending Verification` | Whitelist enum | Account Service | Internal | User churn, dormancy, and ban analysis | Confirmed |
| `email_verification_status`| String | Verification state of user's email | `Verified` | Yes | `Verified`, `Unverified`, `Bounced` | Whitelist enum | Auth Service | Internal | Bot detection and trust scoring | Confirmed |
| `onboarding_status` | String | Progression status through initial onboarding | `Completed` | Yes | `Not Started`, `In Progress`, `Completed`, `Skipped` | Whitelist enum | Onboarding Service| Internal | Activation funnel drop-off analysis | Confirmed |
| `last_login_datetime` | Timestamp | Most recent successful login timestamp | `2026-08-11 10:14:00` | No | Valid ISO 8601 UTC | $\ge \text{registration\_datetime}$ | Auth Service | Internal | Recency calculation and dormancy trigger | Confirmed |
| `lifetime_sessions_count` | Integer | Total cumulative sessions started | `42` | Yes | Non-negative integer | $\ge 0$ | Session Rollup | Internal | Lifetime user engagement depth | Confirmed |
| `lifetime_active_days` | Integer | Cumulative unique days with qualified activity | `18` | Yes | Non-negative integer | $\le \text{days\_since\_registration}$ | Daily Rollup | Internal | User habituation and L-ness scoring | Confirmed |
| `current_xp_balance` | Integer | Cumulative gamification experience points | `2450` | Yes | Non-negative integer | $\ge 0$ | Wallet Ledger | Internal | Gamification tier and level progression | Confirmed |
| `current_token_balance` | Decimal | Redeemable monetary token balance | `12.5000` | Yes | Non-negative Decimal(18,4) | $\ge 0.0000$ | Wallet Ledger | Internal | Outstanding redemption liability | Proposed |
| `days_since_registration` | Decimal | Elapsed time in fractional days since signup | `45.8` | Yes | Non-negative Float | $\ge 0.0$ | Derived Field | Internal | Lifecycle aging and tenure cohorting | Confirmed |
| `is_active_7d_flag` | Boolean | Qualified activity event within trailing 7 days | `true` | Yes | `true`, `false` | Boolean | Derived Rollup | Internal | Weekly Active Users (WAU) reporting | Confirmed |
| `is_active_30d_flag` | Boolean | Qualified activity event within trailing 30 days| `true` | Yes | `true`, `false` | Boolean | Derived Rollup | Internal | Monthly Active Users (MAU) reporting | Confirmed |

---

### 3. Entity 2: `dim_sessions` (Session Dimension)

| Field Name | Data Type | Definition | Example | Required? | Allowed Values | Validation Rule | Source Engine | Sensitivity | Analytical Use | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| `session_id` | String | Unique identifier for a continuous engagement window | `SESS0000001` | Yes | Alphanumeric (prefix `SESS`) | Unique PK; non-null | Frontend SDK | Internal | Primary key of session dimension | Confirmed |
| `user_id` | String | Identifier of user initiating the session | `usr_9a8b7c6d5e` | Yes | Valid `user_id` | Foreign key to `dim_users` | Auth Session | Internal | Links sessions to persistent user identity | Confirmed |
| `session_start` | Timestamp | Timestamp when app entered foreground / session initiated | `2026-08-11 10:30:01` | Yes | Valid ISO 8601 UTC | $\le \text{Current Time}$ | Client Clock | Internal | Hourly / daily usage trend analysis | Confirmed |
| `session_end` | Timestamp | Timestamp when app backgrounded or timeout reached | `2026-08-11 10:30:46` | Yes | Valid ISO 8601 UTC | $\ge \text{session\_start}$ | Client Clock | Internal | Session boundary definition | Confirmed |
| `session_duration_seconds` | Integer | Elapsed engagement duration in seconds | `45` | Yes | Non-negative integer | $\ge 0$ | Derived ($\text{end} - \text{start}$) | Internal | Session length and time-spent KPIs | Confirmed |
| `device` | String | Operating system platform of the session | `Android` | Yes | `Android`, `iOS`, `Web` | Whitelist enum | Client User-Agent| Internal | Cross-platform session performance | Confirmed |
| `platform` | String | Application environment | `App` | Yes | `App`, `Mobile Web`, `Desktop Web` | Whitelist enum | Client User-Agent| Internal | Web vs native app engagement comparison | Confirmed |
| `entry_point` | String | First screen or feature viewed in session | `Daily Reward` | Yes | Feature name enum | Whitelist enum | Navigation Stack| Internal | Ingress channel and feature entry analysis | Confirmed |
| `exit_feature` | String | Final screen or feature viewed before termination | `Watch Ads` | Yes | Feature name enum | Whitelist enum | Navigation Stack| Internal | Egress bottleneck and bounce analysis | Confirmed |
| `events_in_session` | Integer | Total number of telemetry events logged | `14` | Yes | Positive integer | $\ge 1$ | Event Counter | Internal | Session interaction density | Confirmed |

---

### 4. Entity 3: `fact_feature_events` (Telemetry Event Log)

| Field Name | Data Type | Definition | Example | Required? | Allowed Values | Validation Rule | Source Engine | Sensitivity | Analytical Use | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| `event_id` | String | Atomic point-in-time telemetry event identifier | `EVT00000001` | Yes | Alphanumeric ULID | Unique PK; non-null | Client / Gateway | Internal | Idempotent event deduplication | Confirmed |
| `user_id` | String | User triggering the interaction | `usr_9a8b7c6d5e` | Yes | Valid `user_id` | Foreign key to `dim_users` | Auth Session | Internal | Event attribution to user | Confirmed |
| `session_id` | String | Session context in which event occurred | `SESS0000001` | Yes | Valid `session_id` | Foreign key to `dim_sessions` | Client Session | Internal | Event sessionization and journey mapping | Confirmed |
| `event_datetime` | Timestamp | Precise UTC time of occurrence | `2026-08-11 10:30:03` | Yes | Valid ISO 8601 UTC | Sub-millisecond precision | Client Clock | Internal | Chronological event sequencing | Confirmed |
| `feature_name` | String | Standardized functional product module | `Missions` | Yes | Whitelist of 15 features | Lowercase / Standard Case | Navigation Router| Internal | Feature-level aggregation and reporting | Confirmed |
| `event_name` | String | Standardized action name (`object_action`) | `mission_viewed` | Yes | Whitelist of 32 events | Snake_case regex | Client SDK | Internal | Granular user behavior analysis | Confirmed |
| `event_status` | String | Immediate client outcome of event | `Success` | Yes | `Success`, `Failed`, `Pending`, `Abandoned` | Whitelist enum | Client Logic | Internal | Client-side feature error rate | Confirmed |
| `sequence_number` | Integer | Monotonically increasing counter within session | `3` | Yes | Positive integer | $\ge 1$ | Client Counter | Internal | Funnel step sequencing and drop-off analysis | Confirmed |
| `reward_related_flag` | Boolean | Indicates whether event triggers reward logic | `true` | Yes | `true`, `false` | Boolean | Telemetry Router | Internal | Filters events for reward funnel analysis | Confirmed |
| `xp_related_flag` | Boolean | Indicates whether event contributes to XP | `true` | Yes | `true`, `false` | Boolean | Telemetry Router | Internal | Filters events for level progression | Confirmed |
| `idempotency_key` | String | Unique hash to prevent duplicate network retries | `idemp_8f7b2c9a` | Yes | UUIDv4 or SHA-256 | Unique per client action | Client SDK | Restricted | Guarantees zero duplicate event insertion | Proposed |

---

### 5. Entity 4: `dim_tasks` (Task Catalog Dimension)

| Field Name | Data Type | Definition | Example | Required? | Allowed Values | Validation Rule | Source Engine | Sensitivity | Analytical Use | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| `task_id` | String | Unique identifier of a task definition | `TASK0071` | Yes | Alphanumeric | Unique PK; non-null | Task Catalog | Public | Joins task execution to catalog rules | Confirmed |
| `task_title` | String | User-facing display title | `Watch 30s Sponsored Video` | Yes | Text (max 150 chars) | Non-empty | CMS / Catalog | Public | Content and task inventory auditing | Proposed |
| `task_category` | String | Functional category of task | `Advertisement` | Yes | `Advertisement`, `App Task`, `Survey`, `CAPTCHA`, `Social Activity`, `Game`, `Mission`, `Promotional Task` | Whitelist enum | Task Catalog | Public | Category performance and revenue mix | Confirmed |
| `base_reward_amount` | Decimal | Base promised reward payout | `50.0000` | Yes | Decimal $\ge 0.0000$ | Non-negative | Economy Config | Internal | Expected cost-per-completion modeling | Proposed |
| `base_reward_unit` | String | Currency unit awarded | `XP` | Yes | `XP`, `GEMS`, `TOKENS` | Whitelist enum | Economy Config | Internal | Reward liability type classification | Proposed |
| `partner_network` | String | Third-party offerwall or ad vendor | `AdMob` | Yes | `AdMob`, `Unity`, `BitLabs`, `CPALead`, `Internal` | Whitelist enum | Partner Service | Internal | Partner performance and fill-rate auditing | Proposed |
| `cooldown_period_minutes`| Integer| Minimum minutes user must wait before repeating | `60` | Yes | Non-negative integer | $\ge 0$ | Task Rules | Internal | Rate-limiting and fraud abuse controls | Proposed |
| `is_active_flag` | Boolean | Availability state of task in active catalog | `true` | Yes | `true`, `false` | Boolean | Task Catalog | Internal | Active inventory tracking | Proposed |

---

### 6. Entity 5: `fact_task_activity` (Task Execution Fact)

| Field Name | Data Type | Definition | Example | Required? | Allowed Values | Validation Rule | Source Engine | Sensitivity | Analytical Use | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| `activity_id` | String | Unique identifier for a task attempt | `ACT0000001` | Yes | Alphanumeric (prefix `ACT`) | Unique PK; non-null | Task Engine | Internal | Primary key of task activity fact | Confirmed |
| `user_id` | String | User attempting the task | `usr_9a8b7c6d5e` | Yes | Valid `user_id` | Foreign key to `dim_users` | Auth Session | Internal | Task completion tracking per user | Confirmed |
| `task_id` | String | Specific task attempted | `TASK0071` | Yes | Valid `task_id` | Foreign key to `dim_tasks` | Task Catalog | Internal | Task-level conversion analytics | Confirmed |
| `session_id` | String | Session context of task execution | `SESS0000001` | Yes | Valid `session_id` | Foreign key to `dim_sessions` | Client Session | Internal | Session-level task density | Confirmed |
| `task_viewed_at` | Timestamp | Time when task card was presented | `2026-08-05 19:36:29` | Yes | Valid ISO 8601 UTC | Valid timestamp | Client SDK | Internal | Task consideration window calculation | Confirmed |
| `task_started_at` | Timestamp | Time when task action began | `2026-08-05 19:38:50` | Yes | Valid ISO 8601 UTC | $\ge \text{task\_viewed\_at}$ | Client SDK | Internal | Start conversion baseline | Confirmed |
| `task_completed_at` | Timestamp | Time when user finished required action | `2026-08-05 19:40:15` | No | Valid ISO 8601 UTC | Nullable; $\ge \text{task\_started\_at}$ | Client SDK | Internal | Task velocity and duration | Confirmed |
| `task_status` | String | Terminal attempt state | `Completed` | Yes | `Completed`, `Abandoned`, `Failed`, `Pending` | Whitelist enum | Task Engine | Internal | Task completion and drop-off analysis | Confirmed |
| `failure_reason` | String | Root cause code for non-completion | `Validation failed`| No | Standard failure taxonomy | Whitelist enum | Rules Engine | Internal | Failure mode breakdown | Confirmed |
| `validation_status` | String | Server verification outcome | `Passed` | Yes | `Pending`, `Passed`, `Failed` | Whitelist enum | Rules Engine | Internal | Bot detection and quality control | Proposed |
| `reward_status` | String | Settlement state of associated reward | `Credited` | Yes | `Credited`, `Not Credited`, `Pending` | Whitelist enum | Wallet Ledger | Internal | Financial reconciliation with ledger | Confirmed |

---

### 7. Entity 6: `fact_wallet_transactions` (Double-Entry Ledger Fact)

| Field Name | Data Type | Definition | Example | Required? | Allowed Values | Validation Rule | Source Engine | Sensitivity | Analytical Use | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| `transaction_id` | String | Unique immutable ledger entry identifier | `tx_wall_9901` | Yes | Alphanumeric UUID | Unique PK; non-null | Wallet Core | Restricted | Primary key for financial reconciliation | Proposed |
| `user_id` | String | Account holder experiencing balance shift | `usr_9a8b7c6d5e` | Yes | Valid `user_id` | Foreign key to `dim_users` | Auth Session | Internal | User-level monetary accounting | Confirmed |
| `transaction_timestamp` | Timestamp | Exact UTC commit time of database transaction | `2026-08-05 19:40:16` | Yes | Valid ISO 8601 UTC | $\le \text{Current Time}$ | Database Clock | Internal | Financial timeline auditing | Proposed |
| `transaction_type` | String | Functional classification of transaction | `REWARD_CREDIT` | Yes | `REWARD_CREDIT`, `REDEMPTION`, `EXCHANGE_CONVERSION`, `REVERSAL`, `ADMIN_ADJUSTMENT` | Whitelist enum | Wallet Core | Internal | Cash flow and liability breakdown | Proposed |
| `amount` | Decimal | Quantified balance mutation value | `50.0000` | Yes | Decimal(18,4) $> 0.0000$ | Strict positive | Ledger Engine | Restricted | Ledger magnitude calculation | Proposed |
| `currency_unit` | String | Currency unit being shifted | `XP` | Yes | `XP`, `GEMS`, `TOKENS`, `FIAT_USD` | Whitelist enum | Ledger Engine | Internal | Currency-specific ledger balancing | Proposed |
| `balance_direction` | String | Shift direction | `CREDIT` | Yes | `CREDIT` (+), `DEBIT` (-) | Whitelist enum | Ledger Engine | Internal | Double-entry balance calculation | Proposed |
| `running_balance_after` | Decimal | Account balance immediately after commit | `2450.0000` | Yes | Decimal(18,4) $\ge 0.0000$ | Must equal previous $\pm$ amount | Ledger Engine | Restricted | Point-in-time balance reconstruction | Proposed |
| `source_module` | String | Product area that generated the mutation | `WATCH_ADS` | Yes | `WATCH_ADS`, `SURVEY`, `SPIN`, `WITHDRAWAL`, `REFERRAL`, `EXCHANGE` | Whitelist enum | Routing Service | Internal | Revenue attribution by product feature | Proposed |
| `reference_id` | String | Originating business entity ID | `ACT0000001` | Yes | Traceable foreign key | Foreign key to origin table | Origin Service | Internal | Audit cross-referencing across facts | Proposed |

---

### 8. Entity 7: `fact_withdrawals` (Withdrawal Settlement Fact)

| Field Name | Data Type | Definition | Example | Required? | Allowed Values | Validation Rule | Source Engine | Sensitivity | Analytical Use | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| `withdrawal_id` | String | Unique identifier of withdrawal request | `WD_8812001` | Yes | Alphanumeric (prefix `WD_`) | Unique PK; non-null | Payout Service | Restricted | Primary key for payout lifecycle tracking | Proposed |
| `user_id` | String | User requesting cash-out | `usr_9a8b7c6d5e` | Yes | Valid `user_id` | Foreign key to `dim_users` | Auth Session | Internal | User withdrawal history and frequency | Confirmed |
| `requested_amount` | Decimal | Gross cash-out amount requested | `10.00` | Yes | Decimal(10,2) $\ge 5.00$ | Minimum cash-out rule | Client Payload | Restricted | Liquidity liability calculation | Proposed |
| `payout_currency` | String | Fiat target currency | `USD` | Yes | `USD`, `INR`, `EUR`, `GBP` | Whitelist enum | Client Payload | Internal | FX exposure and regional payout split | Proposed |
| `tokens_debited` | Decimal | Number of platform tokens debited from wallet | `100.0000` | Yes | Decimal(18,4) $> 0.0000$ | Matches redemption rate | Wallet Ledger | Internal | Token redemption velocity | Proposed |
| `payout_method` | String | Beneficiary payment rail | `PAYPAL` | Yes | `PAYPAL`, `BANK_TRANSFER`, `UPI`, `CRYPTO_USDT`, `GIFT_CARD` | Whitelist enum | Client Payload | Internal | Payment method popularity and routing | Proposed |
| `payout_gateway` | String | Third-party processor handling disbursement | `Stripe` | Yes | `Stripe`, `PayPal`, `Cashfree`, `Direct RPC` | Whitelist enum | Gateway Router | Internal | Vendor SLA and fee reconciliation | Proposed |
| `withdrawal_status` | String | Current lifecycle state | `COMPLETED` | Yes | `REQUESTED`, `UNDER_REVIEW`, `PROCESSING`, `COMPLETED`, `REJECTED`, `REVERSED` | Whitelist enum | State Machine | Internal | Payout funnel conversion and drop-off | Proposed |
| `requested_timestamp` | Timestamp | Time user submitted cash-out request | `2026-08-10 14:22:10` | Yes | Valid ISO 8601 UTC | Valid timestamp | Client Gateway | Internal | SLA start timestamp | Proposed |
| `settlement_timestamp` | Timestamp | Time gateway confirmed final settlement | `2026-08-11 09:15:30` | No | Valid ISO 8601 UTC | Nullable; $\ge \text{requested\_time}$ | Gateway Webhook | Internal | SLA completion latency calculation | Proposed |
| `rejection_reason_code` | String | Formal code if payout rejected or reversed | `FRAUD_SUSPICION` | No | Standard rejection codes | Whitelist enum | Risk / Ops | Restricted | Anti-fraud and rejection analytics | Proposed |

---

### 9. Entity 8: `fact_referral_conversions` (Referral Attribution Fact)

| Field Name | Data Type | Definition | Example | Required? | Allowed Values | Validation Rule | Source Engine | Sensitivity | Analytical Use | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| `referral_id` | String | Unique identifier of referral relationship | `REF_440129` | Yes | Alphanumeric (prefix `REF_`) | Unique PK; non-null | Referral Engine | Internal | Primary key for referral attribution | Proposed |
| `referrer_user_id` | String | User sharing the invitation | `usr_9a8b7c6d5e` | Yes | Valid `user_id` | Foreign key to `dim_users` | Auth Session | Internal | Advocate identification and leaderboard | Confirmed |
| `referee_user_id` | String | Newly acquired user | `usr_1122334455` | Yes | Valid `user_id` | Foreign key to `dim_users`; $\ne \text{referrer}$ | Auth Service | Internal | Acquired user tracking | Proposed |
| `referral_code_used` | String | Code entered during onboarding | `VL850800` | Yes | Alphanumeric | Matches valid code | Auth Payload | Internal | Code-level marketing performance | Confirmed |
| `registration_timestamp`| Timestamp | Time referee created account | `2026-07-01 12:00:00` | Yes | Valid ISO 8601 UTC | Valid timestamp | Auth Database | Internal | Top-of-funnel referral conversion | Proposed |
| `activation_timestamp` | Timestamp | Time referee completed 1st monetizable task | `2026-07-01 12:45:20` | No | Valid ISO 8601 UTC | Nullable; $\ge \text{reg\_time}$ | Task Service | Internal | Referee activation speed and rate | Proposed |
| `conversion_timestamp` | Timestamp | Time referral bonus was posted to wallet | `2026-07-01 13:00:00` | No | Valid ISO 8601 UTC | Nullable; $\ge \text{act\_time}$ | Referral Engine | Internal | Paid viral acquisition efficiency | Proposed |
| `referral_status` | String | Current funnel status | `CONVERTED` | Yes | `REGISTERED`, `ACTIVATED`, `CONVERTED`, `EXPIRED`, `FRAUD_DISQUALIFIED` | Whitelist enum | Referral Engine | Internal | Funnel drop-off and fraud monitoring | Proposed |

---

### 10. Entity 9: `fact_daily_user_summary` (Aggregated Daily Fact)

| Field Name | Data Type | Definition | Example | Required? | Allowed Values | Validation Rule | Source Engine | Sensitivity | Analytical Use | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| `daily_summary_id` | String | Unique compound key for user-date record | `DS_usr99_20260811` | Yes | Compound string | Unique PK; `user_id` + `date` | Aggregation Pipeline | Internal | Fast analytical query performance | Proposed |
| `user_id` | String | Subject user identifier | `usr_9a8b7c6d5e` | Yes | Valid `user_id` | Foreign key to `dim_users` | Aggregation Pipeline | Internal | Rollup link to user profile | Confirmed |
| `activity_date` | Date | Calendar date of aggregated activity | `2026-08-11` | Yes | Valid Date (YYYY-MM-DD) | $\le \text{Current Date}$ | Calendar Clock | Internal | Daily time-series partitioning key | Confirmed |
| `session_count` | Integer | Total sessions initiated on date | `3` | Yes | Integer $\ge 0$ | Non-negative | Derived Rollup | Internal | Daily session frequency | Confirmed |
| `total_duration_minutes`| Decimal | Total engaged minutes across all sessions | `34.5` | Yes | Decimal $\ge 0.0$ | Non-negative | Derived Rollup | Internal | Daily time-spent per active user | Confirmed |
| `completed_tasks_count` | Integer | Total rewarded tasks completed on date | `4` | Yes | Integer $\ge 0$ | Non-negative | Derived Rollup | Internal | Daily task productivity | Confirmed |
| `streak_day_count` | Integer | Current consecutive active day streak | `7` | Yes | Integer $\ge 0$ | Non-negative | Gamification Engine | Internal | Daily streak monitoring | Confirmed |
| `active_flag` | String | Indicates qualifying active status | `Yes` | Yes | `Yes`, `No` | Whitelist enum | Derived Rollup | Internal | Quick filtering for DAU calculations | Confirmed |
