# VELOOP REWARDS — DATA ANALYST INTERNSHIP
## MILESTONE 1 PROGRESS REPORT: DAYS 1–4
### Product Documentation Review, Source Register, Data Audit & Coverage Matrix

**Intern Name:** Data Analyst Intern  
**Internship Schedule Window:** Days 1–4 (Phase 1 Baseline)  
**Deliverables Covered:**  
* **Days 1–2:** Product Documentation Review & Source & Verification Register  
* **Days 3–4:** Work Package A (Product Data Audit, Data Coverage Matrix & Top 10 Analytics Gaps)  
**Classification:** SIMULATED DATA — CREATED FOR ANALYTICAL TESTING  
**Status Standards Enforced:** Confirmed | Proposed | To Be Verified  

---

## 1. Executive Summary: Days 1–4 Progress

During the first 4 days of the internship, the analytical foundation for VELOOP Rewards was established:
1. **Days 1–2 (Product Discovery & Evidence Discipline):** Reviewed all available product documentation across the 15 simulated product modules. Established the **Source & Verification Register**, tagging all data points as `Confirmed`, `Proposed`, or `To Be Verified` to guarantee no assumption is silently converted into fact.
2. **Days 3–4 (Work Package A — Product Data Readiness Audit):** Mapped user journeys vs system actions across all 15 features, built the **Comprehensive Data Coverage Matrix**, and identified the **Top 10 Mission-Critical Analytics Gaps** that currently block production launch.

---

## 2. Days 1–2: Source & Verification Register

In accordance with Section 6 of the assignment charter, the analyst must maintain strict evidence discipline. The register below documents where every product fact originated and its current verification status:

| Item ID | Product Fact / Information Found | Source Where Found | Source Type | Date Checked | Status | Notes & Limitations |
|---|---|---|---|---|---|---|
| **SVR-01** | VELOOP features 15 functional earning & engagement modules (*Watch Ads, Missions, Daily Reward, Streak Rewards, Mining, Spin, Referrals, etc.*) | `03_Feature_Events` & `07_Feature_Usage` in simulated workbook | Simulated Dataset | 2026-11-01 | **Confirmed** | Features exist in simulated telemetry; production release parity requires engineering confirmation. |
| **SVR-02** | User accounts have statuses: `Active`, `Inactive`, `Suspended`, `Pending Verification` | `Users_1000_Clean` sheet | Simulated Dataset | 2026-11-01 | **Confirmed** | Observed in 1,000 clean user records. |
| **SVR-03** | Telemetry logs 35,704 clickstream events across 35 discrete action event names | `03_Feature_Events` sheet | Simulated Dataset | 2026-11-01 | **Confirmed** | Validated via Python profiling scripts. |
| **SVR-04** | A stable `user_id` anchors user profiles across web and mobile platforms | `01_Users_1000` & `Users_1000_Clean` | Simulated Dataset | 2026-11-01 | **Confirmed** | Formatted as `VLUSR000001` in simulation; proposed UUIDv4 for production. |
| **SVR-05** | Telemetry events contain a `session_id` (`SESS0000001`) | `02_Sessions` & `03_Feature_Events` | Simulated Dataset | 2026-11-01 | **Confirmed** | Verified 7,913 session instances. |
| **SVR-06** | A dedicated double-entry wallet transaction ledger table exists in the current system | Simulated behavior workbook | Simulated Dataset | 2026-11-01 | **Proposed (GAP)** | **Fact:** No ledger table exists in the data. `wallet_viewed` is only a UI click. A transaction model is proposed. |
| **SVR-07** | A normalized withdrawal lifecycle table exists tracking external cash-outs | Simulated behavior workbook | Simulated Dataset | 2026-11-01 | **Proposed (GAP)** | **Fact:** Zero withdrawal records exist in the provided dataset. Dedicated table is proposed. |
| **SVR-08** | Client SDK automatically attaches idempotency keys to network requests | Telemetry event schema | Technical Spec | 2026-11-01 | **To Be Verified** | Telemetry lacks client UUIDs. Requires verification with mobile engineering. |
| **SVR-09** | Third-party ad networks provide verifiable cryptographic postbacks upon video completion | Partner Offerwall Architecture | Product Docs | 2026-11-01 | **To Be Verified** | Required to prevent bot callback spoofing. |

---

## 3. Days 3–4: Work Package A — Product Data Readiness Audit

### 3.1 A1. Product Area Mapping (15 Functional Modules)

| Product Area | Feature / Module | User Action | System Outcome | Data Required | Business Question Addressed | Status |
|---|---|---|---|---|---|---|
| **Account** | Registration | User submits signup form / SSO | Account provisioned; verification dispatched | `user_id`, `reg_datetime`, `channel`, `platform` | Which marketing channels yield active accounts? | Confirmed |
| **Account** | Login | Submits credentials / biometrics | Session token generated; JWT issued | `user_id`, `session_id`, `login_datetime` | What is our true DAU vs background refresh hits? | Confirmed |
| **Earning** | Watch Ads | Taps ad card; watches 30s video | Ad impression verified; reward credited | `user_id`, `ad_unit_id`, `duration_sec`, `reward_id` | Which ad networks deliver completed views vs high abandonment? | Confirmed |
| **Earning** | Tap & Earn | Taps interactive screen canvas | Tap counter incremented; anti-bot checked | `user_id`, `tap_count`, `duration_ms`, `multiplier` | What is the average session fatigue point for micro-tapping? | Confirmed |
| **Earning** | Mining Rewards | Initiates mining session timer | Cloud timer started; yield accumulated | `user_id`, `start_time`, `yield_rate`, `end_time` | Does passive earning drive sustained retention? | Confirmed |
| **Earning** | Missions | Starts multi-step quest | Progress tracked; validation verified | `user_id`, `mission_id`, `criteria_met`, `xp_awarded` | Do structured missions improve Day-7 retention cohorts? | Confirmed |
| **Earning** | Follow & Earn | Taps external social follow link | S2S verification pinged; reward unlocked | `user_id`, `platform_name`, `target_account`, `status` | What is the conversion efficiency of social tasks? | Confirmed |
| **Gamification**| Spin the Wheel | Taps spin button | RNG algorithm assigns prize tier | `user_id`, `spin_id`, `prize_tier`, `reward_value` | Does daily wheel spinning stimulate core task adoption? | Confirmed |
| **Gamification**| Daily Rewards | Claims calendar day reward | Day counter incremented; streak evaluated | `user_id`, `calendar_day`, `streak_day_count`, `reward` | What percentage of users maintain unbroken 7-day habits? | Confirmed |
| **Gamification**| Streak Rewards | Completes daily task to save streak | Streak milestone unlocked; multiplier applied | `user_id`, `current_streak`, `is_broken_flag` | At what streak length does user drop-off peak? | Confirmed |
| **Gamification**| Badges & Levels | Accumulates XP progression | Level incremented; cosmetic badge minted | `user_id`, `level_number`, `badge_id`, `total_xp` | Does status progression correlate with lower churn? | Confirmed |
| **Gamification**| Leaderboard | Views global/regional rank | Leaderboard rank served | `user_id`, `rank_position`, `cohort_id` | Does competitive ranking drive re-engagement? | Confirmed |
| **Security** | CAPTCHA | Solves puzzle challenge | Solution evaluated server-side | `user_id`, `challenge_id`, `latency_ms`, `passed_flag` | What is our true bot incidence rate across task attempts? | Confirmed |
| **Monetary** | Wallet | Views balance & transaction log | Balance served from ledger | `user_id`, `xp_balance`, `token_balance` | How often do users check balances prior to cash-out? | Confirmed |
| **Monetary** | Withdrawals | Submits cash-out to gateway | Hold placed; payout dispatched | `user_id`, `withdrawal_id`, `amount`, `method`, `status` | What is our payout completion rate and SLA turnaround? | Proposed |
| **Growth** | Referrals | Shares code / friend joins | Attribution link created; bonus unlocked | `referrer_id`, `referee_id`, `code`, `status` | What is our viral coefficient ($K$) and referee activation rate? | Confirmed |

---

### 3.2 A2. User Action Flows vs. System Outcomes

Every feature was decomposed into discrete client actions and server validation gates:
* **Task Earning Lifecycle:**
  $$\text{Task Viewed} \longrightarrow \text{Task Opened} \longrightarrow \text{Task Started} \longrightarrow \text{Task Completed} \longrightarrow \text{Validation Passed} \longrightarrow \text{Reward Credited}$$
* **Withdrawal Lifecycle:**
  $$\text{Withdrawal Requested} \longrightarrow \text{Under Review} \longrightarrow \text{Processing} \longrightarrow \text{Completed / Rejected}$$

---

### 3.3 A3. Distinguishing User Events, System Events, and Business Outcomes

To prevent conflating client clicks with financial consequences:
1. **User Event (Client):** `task_completed`, `withdrawal_requested` (Untrusted client telemetry).
2. **System Event (Server):** `task_validation_passed`, `reward_credited`, `withdrawal_completed` (Atomic backend ledger mutations).
3. **Business Outcome (Macro):** Day-30 Retention Rate, Net Token Liability, Customer Acquisition Cost (Derived analytics).

---

### 3.4 A4. Comprehensive Data Coverage Matrix

| Product Area | User Action | System Action | Business Outcome | Data Required | Proposed Event Name | Source | Business Question | Status | Priority |
|---|---|---|---|---|---|---|---|---|---|
| **Account** | Signs up | Creates DB record | New Registered User | `user_id`, `reg_datetime`, `channel` | `user_registered` | Backend Auth | What is our customer acquisition volume? | Confirmed | Critical |
| **Account** | Logs in | Issues JWT session | Active Session / DAU | `user_id`, `session_id`, `timestamp` | `user_logged_in` | Backend Auth | What is our true DAU count? | Confirmed | Critical |
| **Tasks** | Opens task | Displays task modal | Task Consideration | `user_id`, `task_id`, `category` | `task_opened` | Frontend SDK | Which task types attract highest interest? | Confirmed | High |
| **Tasks** | Starts task | Sets in-progress state | Earning Intent | `user_id`, `task_id`, `started_at` | `task_started` | Frontend SDK | What is the open-to-start conversion rate? | Confirmed | Critical |
| **Tasks** | Completes task | Receives client proof | Completion Velocity | `user_id`, `task_id`, `duration_sec` | `task_completed` | Frontend SDK | What is our baseline task completion rate? | Confirmed | Critical |
| **Validation** | N/A (Auto) | Evaluates rules/fraud | Fraud Prevention | `task_id`, `user_id`, `risk_score` | `task_validation_passed` | Backend Rules | What is our genuine completion rate? | Proposed | Critical |
| **Rewards** | N/A (Auto) | Writes ledger credit | Liability Issuance | `tx_id`, `user_id`, `amount`, `unit` | `reward_credited` | Backend Wallet | What is our daily reward issuance liability? | Confirmed | Critical |
| **Gamification**| Claims streak | Increments counter | Habit Formation | `user_id`, `streak_day`, `reward` | `daily_reward_claimed` | Backend API | What percentage of users maintain 7-day streaks? | Confirmed | High |
| **Withdrawals** | Submits payout | Places escrow hold | Liquidity Demand | `withdrawal_id`, `user_id`, `amount` | `withdrawal_requested` | Backend Wallet | What is our gross cash-out demand? | Proposed | Critical |
| **Withdrawals** | Webhook callback| Confirms settlement | Fulfilled Settlement | `withdrawal_id`, `settlement_time` | `withdrawal_completed` | Gateway Webhook | What is our net payout success rate? | Proposed | Critical |
| **Referrals** | Shares link | Generates deep link | Organic Reach | `user_id`, `code`, `channel` | `referral_shared` | Frontend SDK | Which social channels generate highest shares? | Confirmed | High |
| **Referrals** | Referee earns | Unlocks bonus | Qualified Acquisition | `referral_id`, `referrer_id`, `bonus` | `referral_converted` | Backend Wallet | What is our Cost Per Qualified Referee? | Proposed | Critical |

---

### 3.5 Top 10 Critical Analytics Gaps Identified

Based on cross-referencing simulated data against production requirements, 10 mission-critical gaps were identified:
1. **Absence of a Double-Entry Transaction Ledger Table (Critical):** Wallet activity exists only as a UI click. Impossible to audit balances or track monetary liabilities.
2. **Absence of a Normalized Withdrawal Lifecycle Entity (Critical):** Zero cash-out data exists in the current system, blinding management to payout fulfillment.
3. **Severed Referral Attribution Linkage (Critical):** Users have referral codes, but no relational link ties referrer to referee across registration and activation.
4. **Missing Task Validation & Bot Telemetry (Critical):** No system validation events exist to distinguish genuine users from autoclickers.
5. **Lack of Event Idempotency Keys (High):** Raw events lack client UUIDs, making the platform vulnerable to duplicate reward counting on network retries.
6. **Inconsistent Feature Casing in Telemetry (High):** Mixed casing (`missions` vs `Missions`) fragments SQL aggregations.
7. **Granular Onboarding Funnel Missing (High):** Onboarding is tracked as a static boolean; intermediate step drop-offs are invisible.
8. **Conflation of "Activity Occurred" with "Reward Credited" (High):** Task completion is erroneously assumed to equal immediate wallet credit.
9. **Raw PII Storage in Analytical Layer (High):** Plaintext emails and names stored in user tables violate GDPR/DPDP privacy mandates.
10. **Missing Session Timeout Instrumentation (Medium):** Sessions lack background/foreground heartbeat pings.

---

## 4. Summary & Preview of Days 5–6

* **Days 1–4 Status:** 100% Complete & Documented.
* **Days 5–6 Target:** **Work Package B (User & Account Analytics Specification)**:
  * Formalizing user lifecycle state transitions (`Anonymous -> Registered -> Active -> Dormant -> Churned`).
  * Specifying the 4-tier Identity Hierarchy (`user_id`, `session_id`, `event_id`, `transaction_id`).
  * Standardizing 25 analytical user fields with strict PII masking protocols.
