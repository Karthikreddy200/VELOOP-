# VELOOP REWARDS — WORK PACKAGE F
## Production Event Tracking Plan & Engineering Event Catalogue
**Document ID:** VELOOP-DELIV-08  
**Deliverable Covered:** Deliverable 08 (Production Event Tracking Plan)  
**Classification:** SIMULATED DATA — CREATED FOR ANALYTICAL TESTING  
**Status Standard:** Confirmed | Proposed | To Be Verified  

---

### 1. Executive Context & Purpose

The **Production Event Tracking Plan** is the formal technical contract between Product Analytics, Frontend Client Engineers, Backend Service Architects, and Data Engineering. It defines the universal telemetry schema, emission triggers, validation standards, and deduplication rules for the VELOOP platform.

#### Key Engineering Principles:
1. **Idempotent Telemetry Ingestion:** Every event must carry a client-generated or server-generated UUIDv4 `event_id` and `timestamp` to ensure network retries do not cause duplicate counting.
2. **Context Enrichment:** Core attributes (`user_id`, `session_id`, `device`, `platform`, `client_version`) are automatically injected by the base telemetry SDK, eliminating boilerplate in feature code.
3. **Data Integrity & Schema Validation:** Events failing schema validation at the ingestion gateway are routed to a Dead-Letter Queue (DLQ) rather than silently corrupting production tables.

---

### 2. Event Naming Standard & Justification

#### Proposed Standard: `[entity_object]_[action]` (Lowercase snake_case)

After evaluating alternatives (`domain_object_action` vs `object_action`), VELOOP standardizes on the **`[entity_object]_[action]`** convention.

* **Pattern:** `<noun>_<past_tense_verb>` (e.g., `user_registered`, `task_completed`, `reward_credited`, `withdrawal_requested`).
* **Why This Standard Was Selected:**
  1. **Elimination of Redundant Stutter:** Domain-prefixed naming creates unnecessary verbal clutter in telemetry (e.g., `wallet_withdrawal_withdrawal_requested` or `earning_task_task_completed`). Under our standard, the domain is captured cleanly in the `feature_domain` metadata field.
  2. **Direct Alignment with Industry Best Practices:** Conforms to the standard semantic event specifications utilized by Segment, Snowplow, RudderStack, and Google Analytics 4.
  3. **Self-Documenting Code:** Developers can instantly deduce what occurred: the *object* operated on and the *state* reached.

---

### 3. Global Envelope Specification (Standard Event Payload)

Every event emitted into the VELOOP telemetry pipeline wraps its specific properties inside a standardized global envelope:

```json
{
  "event_id": "01HZX87K9W123456789ABCDEFG",
  "event_name": "task_completed",
  "feature_domain": "tasks",
  "timestamp": "2026-11-01T12:00:00.000Z",
  "user_id": "usr_7f8c12e4-6a8b-4b11-9f93-018263549210",
  "session_id": "ses_9921_1791368940",
  "context": {
    "platform": "Android",
    "device_model": "Samsung Galaxy S23",
    "os_version": "Android 14",
    "app_version": "v1.4.2",
    "ip_country": "IN",
    "network_type": "WIFI"
  },
  "properties": {
    "task_id": "TASK0071",
    "task_category": "Advertisement",
    "duration_seconds": 32,
    "client_proof_token": "prf_8829f0a2"
  }
}
```

---

### 4. Master Engineering Event Catalogue (32 Standard Events)

Below is the definitive catalog covering the 7 core domains: Account & Auth, Tasks & Earning, Rewards, Daily & Gamification, Referrals, Wallet, and Withdrawals.

---

#### Domain 1: Account & Authentication

##### Event 01: `user_registered`
* **Trigger:** Backend creates new user row upon successful registration form submission or SSO OAuth callback.
* **Definition:** Marks the creation of a new persistent user account.
* **Core Identifiers:** `user_id` (PK), `event_id` (ULID), `timestamp` (UTC).
* **Feature Domain:** `Account`
* **Source:** Backend Auth Service
* **Required Properties:** `acquisition_source` (String), `registration_method` (`EMAIL`, `GOOGLE`, `APPLE`), `referral_code_used` (String/Nullable).
* **Optional Properties:** `utm_campaign`, `utm_medium`, `utm_source`.
* **Validation:** `user_id` must be non-null and unique; `timestamp` $\le \text{Current Time}$.
* **Business Purpose:** Measures top-of-funnel customer acquisition volume and channel attribution.
* **KPI Dependency:** Total Registrations, Customer Acquisition by Channel, CAC.
* **Status:** Confirmed.

##### Event 02: `user_logged_in`
* **Trigger:** Auth service verifies credentials/biometrics and issues an active JWT.
* **Definition:** User initiates an authenticated session.
* **Core Identifiers:** `user_id`, `event_id`, `session_id`, `timestamp`.
* **Feature Domain:** `Account`
* **Source:** Backend Auth Service
* **Required Properties:** `auth_method` (`PASSWORD`, `BIOMETRIC`, `REFRESH_TOKEN`, `SSO`), `is_first_login` (Boolean).
* **Optional Properties:** `failure_attempts_prior` (Integer).
* **Validation:** Valid `session_id` must be generated and returned.
* **Business Purpose:** Core foundation for Daily Active Users (DAU) and session frequency.
* **KPI Dependency:** DAU, WAU, MAU, Login Success Rate.
* **Status:** Confirmed.

##### Event 03: `user_logged_out`
* **Trigger:** User taps "Log Out" or auth token is explicitly revoked.
* **Definition:** User intentionally terminates authenticated state.
* **Core Identifiers:** `user_id`, `event_id`, `session_id`, `timestamp`.
* **Feature Domain:** `Account`
* **Source:** Frontend Client / API Gateway
* **Required Properties:** `logout_reason` (`USER_INITIATED`, `TOKEN_EXPIRED`, `SECURITY_REVOKE`), `session_duration_seconds` (Integer).
* **Optional Properties:** `last_screen_viewed` (String).
* **Validation:** `session_duration_seconds` $\ge 0$.
* **Business Purpose:** Evaluates voluntary app exit points and security revocations.
* **KPI Dependency:** Average Session Duration, Voluntary Churn Signals.
* **Status:** Proposed.

##### Event 04: `onboarding_started`
* **Trigger:** User views first onboarding tutorial card or profile setup screen.
* **Definition:** Inception of the first-time user onboarding journey.
* **Core Identifiers:** `user_id`, `event_id`, `session_id`, `timestamp`.
* **Feature Domain:** `Account`
* **Source:** Frontend Client
* **Required Properties:** `total_steps_in_flow` (Integer), `flow_variant` (String).
* **Optional Properties:** `client_orientation` (String).
* **Validation:** Emitted at most once per `user_id`.
* **Business Purpose:** Denominator for onboarding funnel completion rate.
* **KPI Dependency:** Onboarding Funnel Conversion, Drop-off Rate.
* **Status:** Proposed.

##### Event 05: `onboarding_completed`
* **Trigger:** User finishes final onboarding screen, grants permissions, and lands on home feed.
* **Definition:** Formal conclusion of initial activation setup.
* **Core Identifiers:** `user_id`, `event_id`, `session_id`, `timestamp`.
* **Feature Domain:** `Account`
* **Source:** Frontend Client
* **Required Properties:** `time_to_complete_seconds` (Integer), `steps_completed` (Integer), `push_permission_granted` (Boolean).
* **Optional Properties:** `skipped_steps` (Array of Strings).
* **Validation:** `time_to_complete_seconds` $> 0$; `steps_completed` $\le \text{total\_steps}$.
* **Business Purpose:** Flags account as activation-ready.
* **KPI Dependency:** Onboarding Completion Rate, Day-1 Retention.
* **Status:** Proposed.

---

#### Domain 2: Tasks & Earning Activities

##### Event 06: `task_viewed`
* **Trigger:** Task card rendered in client viewport ($\ge 50\%$ visible for $\ge 1.0\text{s}$).
* **Definition:** User impression on an available earning opportunity.
* **Core Identifiers:** `user_id`, `event_id`, `session_id`, `timestamp`.
* **Feature Domain:** `Tasks`
* **Source:** Frontend Client
* **Required Properties:** `task_id` (String), `task_category` (Enum), `reward_amount` (Decimal), `reward_unit` (Enum).
* **Optional Properties:** `card_position_index` (Integer), `offerwall_provider` (String).
* **Validation:** Valid `task_id` foreign key.
* **Business Purpose:** Measures task visibility, impression volume, and placement effectiveness.
* **KPI Dependency:** Task Impressions, Task CTR.
* **Status:** Confirmed.

##### Event 07: `task_opened`
* **Trigger:** User taps a task card to inspect details and instructions.
* **Definition:** User inspects task modal / details sheet.
* **Core Identifiers:** `user_id`, `event_id`, `session_id`, `timestamp`.
* **Feature Domain:** `Tasks`
* **Source:** Frontend Client
* **Required Properties:** `task_id` (String), `task_category` (Enum), `estimated_duration_sec` (Integer).
* **Optional Properties:** `referring_screen` (String).
* **Validation:** Must follow a prior `task_viewed` in session.
* **Business Purpose:** Measures user interest and evaluation intent.
* **KPI Dependency:** Task Open Rate, Modal Bounce Rate.
* **Status:** Confirmed.

##### Event 08: `task_started`
* **Trigger:** User taps "Start Task" / begins video playback / launches external link.
* **Definition:** Formal initiation of task execution.
* **Core Identifiers:** `user_id`, `event_id`, `session_id`, `timestamp`.
* **Feature Domain:** `Tasks`
* **Source:** Frontend Client / Gateway
* **Required Properties:** `task_id` (String), `activity_id` (String: PK of task attempt), `task_category` (Enum).
* **Optional Properties:** `sub_id_tracking_hash` (String).
* **Validation:** Unique `activity_id` generated.
* **Business Purpose:** Denominator for task completion rate; tracks task intent.
* **KPI Dependency:** Task Starts, Start-to-Completion Conversion.
* **Status:** Confirmed.

##### Event 09: `task_completed`
* **Trigger:** User completes task criteria on client (finishes video, completes survey questions).
* **Definition:** Client reports conclusion of the required action.
* **Core Identifiers:** `user_id`, `event_id`, `session_id`, `timestamp`.
* **Feature Domain:** `Tasks`
* **Source:** Frontend Client
* **Required Properties:** `task_id` (String), `activity_id` (String), `task_duration_seconds` (Integer), `client_proof_token` (String).
* **Optional Properties:** `survey_score` (Integer), `video_seconds_watched` (Integer).
* **Validation:** `task_duration_seconds` $\ge$ minimum task threshold.
* **Business Purpose:** Measures client completion velocity and productivity.
* **KPI Dependency:** Task Completion Rate, Mean Completion Time.
* **Status:** Confirmed.

##### Event 10: `task_failed`
* **Trigger:** Task execution fails due to timeout, user exit, bot block, or third-party error.
* **Definition:** Unsuccessful termination of a task attempt.
* **Core Identifiers:** `user_id`, `event_id`, `session_id`, `timestamp`.
* **Feature Domain:** `Tasks`
* **Source:** Frontend Client / Backend Rules
* **Required Properties:** `task_id` (String), `activity_id` (String), `failure_category` (`USER_ABANDON`, `PARTNER_ERROR`, `VALIDATION_REJECT`, `SYSTEM_FAULT`), `failure_code` (Enum).
* **Optional Properties:** `error_message` (String), `time_elapsed_seconds` (Integer).
* **Validation:** Valid whitelisted `failure_code`.
* **Business Purpose:** Root-cause troubleshooting for task friction and technical failures.
* **KPI Dependency:** Task Failure Rate, Abandonment Distribution.
* **Status:** Confirmed.

---

#### Domain 3: Rewards & Ledger Accounting

##### Event 11: `reward_credited`
* **Trigger:** Wallet ledger commits double-entry balance increment.
* **Definition:** Monetary/gamified reward unit posted to user's wallet.
* **Core Identifiers:** `user_id`, `event_id`, `timestamp`.
* **Feature Domain:** `Rewards`
* **Source:** Backend Wallet Service
* **Required Properties:** `transaction_id` (PK), `amount` (Decimal), `currency_unit` (`XP`, `GEMS`, `TOKENS`), `source_feature` (Enum), `reference_id` (`activity_id`).
* **Optional Properties:** `new_running_balance` (Decimal).
* **Validation:** `amount` $> 0.0000$; `transaction_id` unique and idempotent.
* **Business Purpose:** Tracks platform reward issuance liabilities.
* **KPI Dependency:** Daily Reward Issuance Volume, Cost of Rewards, XP Velocity.
* **Status:** Confirmed.

##### Event 12: `reward_pending`
* **Trigger:** Task completion approved but reward placed in escrow hold pending partner clearance.
* **Definition:** Temporary escrow hold on high-value reward disbursement.
* **Core Identifiers:** `user_id`, `event_id`, `timestamp`.
* **Feature Domain:** `Rewards`
* **Source:** Backend Wallet Service
* **Required Properties:** `escrow_id` (String), `amount` (Decimal), `currency_unit` (Enum), `hold_reason` (`HIGH_VALUE_AUDIT`, `PARTNER_S2S_CLEARANCE`), `expected_release_at` (Timestamp).
* **Optional Properties:** `partner_reference_id` (String).
* **Validation:** `expected_release_at` $>$ current timestamp.
* **Business Purpose:** Manages outstanding pending liabilities and escrow exposure.
* **KPI Dependency:** Outstanding Escrow Volume, Pending Settlement Time.
* **Status:** Proposed.

##### Event 13: `reward_reversed`
* **Trigger:** Fraud detection or partner clawback reverses previously credited reward.
* **Definition:** Compensating debit ledger transaction clawing back ill-gotten rewards.
* **Core Identifiers:** `user_id`, `event_id`, `timestamp`.
* **Feature Domain:** `Rewards`
* **Source:** Backend Wallet Service
* **Required Properties:** `reversal_tx_id` (PK), `orig_transaction_id` (FK), `amount_reversed` (Decimal), `reversal_reason` (Enum).
* **Optional Properties:** `investigation_ticket_id` (String).
* **Validation:** `orig_transaction_id` must exist in `fact_wallet_transactions`.
* **Business Purpose:** Audits anti-fraud clawbacks and revenue loss recovery.
* **KPI Dependency:** Reward Reversal Rate, Clawback Volume.
* **Status:** Proposed.

---

#### Domain 4: Daily Habits & Gamification

##### Event 14: `daily_reward_claimed`
* **Trigger:** User taps "Claim" on calendar day reward modal.
* **Definition:** Claiming the recurring calendar day reward.
* **Core Identifiers:** `user_id`, `event_id`, `session_id`, `timestamp`.
* **Feature Domain:** `Daily Reward`
* **Source:** Backend API
* **Required Properties:** `calendar_day_number` (Integer: 1–30), `streak_day_count` (Integer), `reward_amount` (Decimal), `reward_unit` (Enum).
* **Optional Properties:** `multiplier_applied` (Decimal).
* **Validation:** Claim allowed at most once per calendar date (UTC).
* **Business Purpose:** Measures habitual day-over-day return behavior.
* **KPI Dependency:** Daily Claim Rate, Day-N Retention.
* **Status:** Confirmed.

##### Event 15: `streak_updated`
* **Trigger:** Daily evaluation cron increments or breaks a user's active login streak.
* **Definition:** State transition in user streak counter.
* **Core Identifiers:** `user_id`, `event_id`, `timestamp`.
* **Feature Domain:** `Streak Rewards`
* **Source:** Backend Cron Worker
* **Required Properties:** `current_streak_length` (Integer), `previous_streak_length` (Integer), `streak_status` (`EXTENDED`, `BROKEN`, `RESTORED`).
* **Optional Properties:** `streak_freeze_used` (Boolean).
* **Validation:** If `BROKEN`, `current_streak_length` resets to 0 or 1.
* **Business Purpose:** Evaluates streak habit curves and churn inflection points.
* **KPI Dependency:** Active Streak Distribution, Streak Break Churn Rate.
* **Status:** Confirmed.

##### Event 16: `mission_started`
* **Trigger:** User elects to participate in a structured multi-part mission challenge.
* **Definition:** Activation of a goal-oriented quest.
* **Core Identifiers:** `user_id`, `event_id`, `session_id`, `timestamp`.
* **Feature Domain:** `Missions`
* **Source:** Frontend Client / API
* **Required Properties:** `mission_id` (String), `mission_type` (`DAILY`, `WEEKLY`, `SPECIAL`), `required_task_count` (Integer).
* **Optional Properties:** `time_limit_hours` (Integer).
* **Validation:** Valid active `mission_id`.
* **Business Purpose:** Tracks participation in complex goal structures.
* **KPI Dependency:** Mission Adoption Rate.
* **Status:** Confirmed.

##### Event 17: `mission_completed`
* **Trigger:** All prerequisite tasks within mission verified by rules engine.
* **Definition:** Successful fulfillment of a mission.
* **Core Identifiers:** `user_id`, `event_id`, `session_id`, `timestamp`.
* **Feature Domain:** `Missions`
* **Source:** Backend Rules Engine
* **Required Properties:** `mission_id` (String), `duration_hours` (Decimal), `xp_bonus_awarded` (Integer), `badge_unlocked_id` (String/Nullable).
* **Optional Properties:** `all_tasks_completed` (Array of Strings).
* **Validation:** `duration_hours` $\le \text{time\_limit\_hours}$.
* **Business Purpose:** Evaluates quest progression and milestone reward velocity.
* **KPI Dependency:** Mission Completion Rate.
* **Status:** Confirmed.

##### Event 18: `badge_earned`
* **Trigger:** User reaches cumulative achievement criterion.
* **Definition:** Permanent cosmetic or status badge minted.
* **Core Identifiers:** `user_id`, `event_id`, `timestamp`.
* **Feature Domain:** `Badges`
* **Source:** Backend Gamification Engine
* **Required Properties:** `badge_id` (String), `badge_tier` (`BRONZE`, `SILVER`, `GOLD`, `PLATINUM`), `criteria_code` (String).
* **Optional Properties:** `share_cta_clicked` (Boolean).
* **Validation:** Unique per `badge_id` per `user_id`.
* **Business Purpose:** Measures gamified progression and vanity status engagement.
* **KPI Dependency:** Badge Minting Velocity, Status Cohort Retention.
* **Status:** Confirmed.

##### Event 19: `spin_started`
* **Trigger:** User pulls lever / taps spin button on lucky wheel.
* **Definition:** Initiation of RNG prize wheel spin.
* **Core Identifiers:** `user_id`, `event_id`, `session_id`, `timestamp`.
* **Feature Domain:** `Spin the Wheel`
* **Source:** Frontend Client
* **Required Properties:** `spin_cost_type` (`FREE_DAILY`, `AD_SPONSORED`, `TOKEN_PAID`), `wheel_theme` (String).
* **Optional Properties:** `tokens_deducted` (Decimal).
* **Validation:** User must have qualifying spin balance.
* **Business Purpose:** Tracks micro-gaming participation.
* **KPI Dependency:** Daily Spin Volume.
* **Status:** Confirmed.

##### Event 20: `spin_completed`
* **Trigger:** Server RNG determines prize slice and wheel animation halts.
* **Definition:** Resolution of spin outcome and prize allocation.
* **Core Identifiers:** `user_id`, `event_id`, `session_id`, `timestamp`.
* **Feature Domain:** `Spin the Wheel`
* **Source:** Backend RNG Engine
* **Required Properties:** `spin_id` (String), `prize_tier` (String), `prize_type` (`XP`, `GEMS`, `TOKENS`, `NOTHING`), `reward_value` (Decimal).
* **Optional Properties:** `rng_seed_hash` (String).
* **Validation:** Prize value matches published payout probabilities.
* **Business Purpose:** Monitors gamification economy liability and prize distribution fairness.
* **KPI Dependency:** Spin Payout Volume, Return-to-Player (RTP) Rate.
* **Status:** Confirmed.

---

#### Domain 5: Referral Funnel

##### Event 21: `referral_created`
* **Trigger:** User accesses referral screen; system provisions personal referral code.
* **Definition:** Referral identity generation.
* **Core Identifiers:** `user_id` (Referrer), `event_id`, `session_id`, `timestamp`.
* **Feature Domain:** `Referral`
* **Source:** Backend Referral Service
* **Required Properties:** `referral_code` (String), `campaign_tier` (String).
* **Optional Properties:** `custom_vanity_code` (String/Nullable).
* **Validation:** Code must be unique globally.
* **Business Purpose:** Tracks user intent to become an advocate.
* **KPI Dependency:** Active Referrer Base.
* **Status:** Confirmed.

##### Event 22: `referral_registered`
* **Trigger:** New referee signs up attaching a valid referral code.
* **Definition:** Top-of-funnel link created between referrer and referee.
* **Core Identifiers:** `user_id` (Referee), `event_id`, `timestamp`.
* **Feature Domain:** `Referral`
* **Source:** Backend Auth Service
* **Required Properties:** `referral_id` (PK), `referrer_user_id` (FK), `referral_code_used` (String), `channel` (Enum).
* **Optional Properties:** `utm_source` (String).
* **Validation:** `referrer_user_id` $\ne \text{user\_id}$ (anti-self-referral check).
* **Business Purpose:** Measures viral signup volume.
* **KPI Dependency:** Referral Signups, Invitation Conversion Rate.
* **Status:** Proposed.

##### Event 23: `referral_activated`
* **Trigger:** Referee completes first qualifying monetizable task ($\ge 10\text{ XP}$).
* **Definition:** Referee reaches active earner status.
* **Core Identifiers:** `user_id` (Referee), `event_id`, `timestamp`.
* **Feature Domain:** `Referral`
* **Source:** Backend Rules Engine
* **Required Properties:** `referral_id` (FK), `referrer_user_id` (FK), `qualifying_activity_id` (String), `hours_since_signup` (Decimal).
* **Optional Properties:** `device_risk_score` (Decimal).
* **Validation:** Must occur within 14 days of signup.
* **Business Purpose:** Evaluates referee quality and activation speed.
* **KPI Dependency:** Referral Activation Rate ($RAR$).
* **Status:** Proposed.

##### Event 24: `referral_converted`
* **Trigger:** Referral engine clears anti-fraud checks and unlocks referral bonus.
* **Definition:** Both parties receive monetary referral bonus.
* **Core Identifiers:** `user_id` (Referrer), `event_id`, `timestamp`.
* **Feature Domain:** `Referral`
* **Source:** Backend Referral Service
* **Required Properties:** `referral_id` (FK), `referee_user_id` (FK), `referrer_bonus_amount` (Decimal), `bonus_transaction_id` (String).
* **Optional Properties:** `referee_bonus_amount` (Decimal).
* **Validation:** Ledger credit confirmed.
* **Business Purpose:** Measures true paid viral customer acquisition.
* **KPI Dependency:** Referral Conversion Rate, Viral Coefficient ($K$).
* **Status:** Proposed.

---

#### Domain 6: Wallet Operations

##### Event 25: `wallet_transaction_created`
* **Trigger:** User or system initiates balance mutation request.
* **Definition:** Inception of ledger entry in `PENDING` state.
* **Core Identifiers:** `user_id`, `event_id`, `timestamp`.
* **Feature Domain:** `Wallet`
* **Source:** Backend Wallet Service
* **Required Properties:** `transaction_id` (PK), `transaction_type` (Enum), `amount` (Decimal), `currency_unit` (Enum), `direction` (`CREDIT`/`DEBIT`).
* **Optional Properties:** `external_reference_id` (String).
* **Validation:** Debit amount cannot exceed available verified balance.
* **Business Purpose:** Records balance reservation and prevents double-spending.
* **KPI Dependency:** Transaction Velocity.
* **Status:** Proposed.

##### Event 26: `wallet_transaction_completed`
* **Trigger:** Database commits transaction and updates persistent user balance.
* **Definition:** Terminal successful ledger commitment.
* **Core Identifiers:** `user_id`, `event_id`, `timestamp`.
* **Feature Domain:** `Wallet`
* **Source:** Backend Wallet Service
* **Required Properties:** `transaction_id` (FK), `settled_amount` (Decimal), `currency_unit` (Enum), `running_balance_after` (Decimal).
* **Optional Properties:** `commit_latency_ms` (Integer).
* **Validation:** `running_balance_after` equals previous balance adjusted by settled amount.
* **Business Purpose:** Financial audit trail and ledger verification.
* **KPI Dependency:** Total Ledger Volume, System Liability.
* **Status:** Proposed.

##### Event 27: `wallet_transaction_reversed`
* **Trigger:** Compensating transaction created to void a prior transaction.
* **Definition:** Rollback of balance shift due to dispute or fraud.
* **Core Identifiers:** `user_id`, `event_id`, `timestamp`.
* **Feature Domain:** `Wallet`
* **Source:** Backend Wallet Service
* **Required Properties:** `reversal_tx_id` (PK), `original_transaction_id` (FK), `amount_reversed` (Decimal), `reversal_reason` (String).
* **Optional Properties:** `admin_user_id` (String).
* **Validation:** `original_transaction_id` must be in `COMPLETED` status.
* **Business Purpose:** Ledger reconciliation and fraud recovery.
* **KPI Dependency:** Net Ledger Drift, Reversal Volume.
* **Status:** Proposed.

---

#### Domain 7: Withdrawals & Payouts

##### Event 28: `withdrawal_requested`
* **Trigger:** User submits withdrawal form; balance debited to escrow hold.
* **Definition:** User requests payout to real-world payment instrument.
* **Core Identifiers:** `user_id`, `event_id`, `session_id`, `timestamp`.
* **Feature Domain:** `Withdrawals`
* **Source:** Frontend Client / Gateway
* **Required Properties:** `withdrawal_id` (PK), `requested_amount` (Decimal), `currency` (String), `payout_method` (Enum), `tokens_debited` (Decimal).
* **Optional Properties:** `user_balance_at_request` (Decimal).
* **Validation:** `requested_amount` $\ge$ minimum cash-out threshold ($5.00).
* **Business Purpose:** Measures user cash-out intent and liquidity demand.
* **KPI Dependency:** Total Withdrawal Requests, Gross Requested Volume.
* **Status:** Proposed.

##### Event 29: `withdrawal_processing`
* **Trigger:** Risk checks pass; payout payload dispatched to third-party payment gateway.
* **Definition:** Payout handoff to external financial institution.
* **Core Identifiers:** `user_id`, `event_id`, `timestamp`.
* **Feature Domain:** `Withdrawals`
* **Source:** Backend Payout Router
* **Required Properties:** `withdrawal_id` (FK), `payout_gateway` (`STRIPE`, `PAYPAL`, `CASHFREE`), `gateway_reference_id` (String).
* **Optional Properties:** `risk_review_duration_minutes` (Decimal).
* **Validation:** Valid gateway transaction submission token.
* **Business Purpose:** Benchmarks external gateway latency.
* **KPI Dependency:** Gateway In-Flight Queue, Gateway Handshake SLA.
* **Status:** Proposed.

##### Event 30: `withdrawal_completed`
* **Trigger:** Payment processor webhook confirms successful fund settlement.
* **Definition:** Payout successfully settled into user's external account.
* **Core Identifiers:** `user_id`, `event_id`, `timestamp`.
* **Feature Domain:** `Withdrawals`
* **Source:** Backend Webhook Consumer
* **Required Properties:** `withdrawal_id` (FK), `settlement_amount` (Decimal), `processing_fee` (Decimal), `total_sla_duration_hours` (Decimal).
* **Optional Properties:** `gateway_transfer_receipt_url` (String).
* **Validation:** Webhook cryptographic signature validated.
* **Business Purpose:** Measures net fulfilled cash outflow and user satisfaction.
* **KPI Dependency:** Completed Withdrawals, Median SLA Latency.
* **Status:** Proposed.

##### Event 31: `withdrawal_rejected`
* **Trigger:** Automated risk rules or manual compliance review rejects payout.
* **Definition:** Payout blocked prior to settlement; escrow hold refunded to wallet.
* **Core Identifiers:** `user_id`, `event_id`, `timestamp`.
* **Feature Domain:** `Withdrawals`
* **Source:** Backend Risk Service / Ops Dashboard
* **Required Properties:** `withdrawal_id` (FK), `rejection_code` (`SUSPICIOUS_XP`, `DUPLICATE_PAYOUT_DESTINATION`, `KYC_FAILED`), `refund_transaction_id` (String).
* **Optional Properties:** `compliance_notes` (String).
* **Validation:** Compensating ledger refund transaction executed.
* **Business Purpose:** Monitors anti-fraud barrier effectiveness.
* **KPI Dependency:** Withdrawal Rejection Rate.
* **Status:** Proposed.

##### Event 32: `withdrawal_reversed`
* **Trigger:** Post-dispatch banking failure (e.g. invalid account, beneficiary bank reject).
* **Definition:** External payment bounced back after dispatch.
* **Core Identifiers:** `user_id`, `event_id`, `timestamp`.
* **Feature Domain:** `Withdrawals`
* **Source:** Backend Webhook Consumer
* **Required Properties:** `withdrawal_id` (FK), `bank_error_code` (String), `refund_transaction_id` (String), `gateway_reversal_fee` (Decimal).
* **Optional Properties:** `bank_reversal_timestamp` (Timestamp).
* **Validation:** Compensating ledger refund credit executed.
* **Business Purpose:** Identifies payout gateway unreliability and user payment credential errors.
* **KPI Dependency:** Payout Reversal Rate.
* **Status:** Proposed.
