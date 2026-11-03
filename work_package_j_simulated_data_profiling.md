# VELOOP REWARDS — WORK PACKAGE J
## Simulated Data Profiling & Structural Integrity Report
**Document ID:** VELOOP-DELIV-12  
**Deliverable Covered:** Deliverable 12 (Simulated Data Profiling Report)  
**Classification:** SIMULATED DATA — CREATED FOR ANALYTICAL TESTING  
**Status Standard:** Confirmed | Proposed | To Be Verified  

---

### 1. Executive Context & Objective

Now that the architectural blueprint, data dictionary, and KPI catalogue have been established, this work package executes empirical analysis against the actual simulated datasets provided in the VELOOP working pack:
* Workbook 1: `VELoop_Rewards_Data_01.xlsx` (5 sheets)
* Workbook 2: `VELOOP_Simulated_User_Behavior_1000.xlsx` (10 sheets)

This evaluation encompasses three rigorous tests:
1. **J1. Comprehensive Dataset Profiling:** Row counts, columns, date ranges, null counts, duplicate keys, status distributions, and numeric ranges.
2. **J2. Referential Integrity & Relationship Testing:** Testing foreign key linkages across `user_id` and `session_id` to detect orphan records.
3. **J3. KPI Feasibility & Calculability Test:** Evaluating whether the proposed 35 KPIs can actually be computed from the supplied dataset, pinpointing missing columns and structural requirements.

---

### 2. J1. Comprehensive Dataset Profiling Summary

Automated profiling executed across all 15 workbook tabs produced the following empirical baseline:

| Workbook | Sheet Name | Records (Rows) | Columns | Date Range Covered | Unique IDs | Duplicate Keys | Missing Values | Core Categories / Statuses |
|---|---|---|---|---|---|---|---|---|
| **File 1** | `Users_1000_Clean` | 1,000 | 27 | 2026-04-01 to 2026-09-17 | 1,000 `user_id` | 0 | 953 (881 referral detail, 72 last login) | `Active` (352), `Inactive` (440), `Suspended` (98), `Pending Verification` (110) |
| **File 1** | `Users_Messy_Audit` | 1,008 | 28 | 2026-04-01 to 2026-09-17 | 1,000 `user_id` | **8 duplicate IDs** | 966 | Same statuses + 8 duplicated rows |
| **File 1** | `Data_Dictionary` | 25 | 5 | N/A (Static metadata) | 25 fields | 0 | 0 | String, Integer, Decimal, Datetime, Boolean |
| **File 2** | `01_Users_1000` | 1,000 | 16 | 2026-04-01 to 2026-09-15 | 1,000 `user_id` | 0 | 846 (referral detail) | Matches File 1 clean cohort |
| **File 2** | `02_Sessions` | 7,913 | 12 | 2026-04-02 to 2026-09-15 | 7,913 `session_id` | 0 | 466 (exit feature) | Duration: 20s min, 470s max, 45s median |
| **File 2** | `03_Feature_Events` | 35,704 | 13 | 2026-04-02 to 2026-09-15 | 35,704 `event_id` | 0 | 0 | 15 distinct features, 35 discrete event names |
| **File 2** | `04_Daily_Activity` | 6,667 | 17 | 2026-04-02 to 2026-09-15 | 6,667 user-days | 0 | 0 | Sessions: 1 to 10; Completed tasks: 0 to 38 |
| **File 2** | `05_Task_Activity` | 9,846 | 12 | 2026-04-02 to 2026-09-15 | 9,846 `activity_id`| 0 | 10,494 (completion time, failure reason) | `Completed` (5,627), `Abandoned` (2,051), `Failed` (1,520), `Pending` (648) |
| **File 2** | `06_Milestones` | 4,799 | 6 | 2026-04-02 to 2026-09-15 | 4,799 milestone unlocks| 0 | 40 (source event) | 12 milestone types (First task, D7 streak, etc.) |
| **File 2** | `07_Feature_Usage` | 15 | 7 | Aggregated summary | 15 features | 0 | 0 | Watch Ads (3,126 events), Missions (2,780), Streaks (2,734) |
| **File 2** | `10_Event_Data_Quality_Audit` | 35,714 | 13 | 2026-04-02 to 2026-09-15 | 35,704 `event_id` | **10 duplicate IDs**| 0 | Contains dirty casing (`missions`, `daily reward`) & trailing space (`'success '`) |

---

### 3. J2. Referential Integrity & Relationship Tests

We evaluated foreign key referential integrity across the sheets using automated join scripts:

```mermaid
flowchart TD
    U[dim_users: 1,000 Unique IDs]
    
    U -->|1:N Join Check| S[Sessions: 7,913 rows<br/>Orphans: 0 (100% Valid)]
    U -->|1:N Join Check| E[Feature Events: 35,704 rows<br/>Orphans: 0 (100% Valid)]
    U -->|1:N Join Check| D[Daily Activity: 6,667 rows<br/>Orphans: 0 (100% Valid)]
    U -->|1:N Join Check| T[Task Activity: 9,846 rows<br/>Orphans: 0 (100% Valid)]
    U -->|1:N Join Check| M[Milestones: 4,799 rows<br/>Orphans: 0 (100% Valid)]

    S -->|1:N Join Check| E2[Events to Sessions<br/>Orphans: 0 (100% Valid)]
    S -->|1:N Join Check| T2[Tasks to Sessions<br/>Orphans: 0 (100% Valid)]
```

#### Test Results:
1. **User Identity Consistency:**
   * Exact match of 1,000 `user_id` keys between `Users_1000_Clean` (File 1) and `01_Users_1000` (File 2). Overlap is $100\%$.
2. **Orphan Records in Event Tables:**
   * `Sessions.user_id` $\rightarrow$ `Users.user_id`: **0 orphan records** (All 7,913 sessions belong to valid users).
   * `Feature_Events.user_id` $\rightarrow$ `Users.user_id`: **0 orphan records** (All 35,704 events map to valid users).
   * `Task_Activity.user_id` $\rightarrow$ `Users.user_id`: **0 orphan records** (All 9,846 task records map to valid users).
   * `Daily_Activity.user_id` $\rightarrow$ `Users.user_id`: **0 orphan records**.
   * `Milestones.user_id` $\rightarrow$ `Users.user_id`: **0 orphan records**.
3. **Session Referential Integrity:**
   * `Feature_Events.session_id` $\rightarrow$ `Sessions.session_id`: **0 orphan records**.
   * `Task_Activity.session_id` $\rightarrow$ `Sessions.session_id`: **0 orphan records**.

> [!NOTE]
> **Integrity Finding:**
> Within the existing tables of the simulated user behavior dataset, **relational referential integrity is pristine (0 orphans)**. The data generation model maintained perfect foreign key consistency across user and session boundaries.

---

### 4. J3. KPI Calculability & Feasibility Test

We tested a representative sample of our 35 proposed KPIs against the actual fields present in the supplied workbooks to determine feasibility:

| KPI ID & Name | Calculable from Supplied Data? | Feasibility Assessment & Missing Data Audit |
|---|---|---|
| **KPI 01: Daily Active Users (DAU)** | **YES** | Can be calculated directly by aggregating `COUNT(DISTINCT user_id)` grouped by date from `03_Feature_Events` or filtering `active_flag = 'Yes'` on `04_Daily_Activity`. |
| **KPI 06: Platform Stickiness ($DAU/MAU$)** | **YES** | Calculable by computing 1-day vs 30-day rolling unique active users from `04_Daily_Activity`. |
| **KPI 07: Feature Penetration Rate** | **YES** | Calculable using `07_Feature_Usage` (`unique_users / total_users`). |
| **KPI 08: Average Session Duration (ASD)** | **YES** | Calculable directly using `02_Sessions.session_duration_seconds` (mean = $45.0\text{s}$). |
| **KPI 10: Task Completion Rate (TCR)** | **YES** | Calculable from `05_Task_Activity` ($\frac{5627 \text{ Completed}}{9846 \text{ Total}} = 57.15\%$). |
| **KPI 12: Gross Reward Issuance Volume** | **PARTIAL / NO** | **Missing Data:** In `05_Task_Activity`, there is a `reward_status` column ('Credited', 'Not Credited', 'Pending') but **no numeric `reward_amount` or `reward_unit` column**. XP balance exists only as a static lifetime snapshot in `Users_1000_Clean`. |
| **KPI 17: Total Wallet Transaction Volume** | **NO** | **Missing Data:** No wallet ledger table exists in the simulated dataset. `wallet_viewed` is logged as a UI click event, but transaction ledger records do not exist. |
| **KPI 22: Gross Withdrawal Volume & Count** | **NO** | **Missing Data:** The simulated dataset contains **zero withdrawal request records** (`fact_withdrawals` does not exist). |
| **KPI 24: End-to-End Payout SLA Duration** | **NO** | **Missing Data:** No withdrawal timestamps or gateway settlement logs exist in the supplied sheets. |
| **KPI 30: Referee Activation Rate (RAR)** | **PARTIAL** | **Missing Data:** `Users_1000_Clean` tracks `referral_code` and `referral_source_detail`, but there is no relational referrer-to-referee bridge linking which specific user referred whom. |

#### Conclusion of Feasibility Test:
While **User Lifecycle and Engagement KPIs** are $100\%$ calculable from the supplied simulated dataset, **Monetary, Ledger, and Withdrawal KPIs require the implementation of our proposed production tables (`fact_wallet_transactions`, `fact_withdrawals`, and `fact_referral_conversions`)**.
