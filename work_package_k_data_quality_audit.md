# VELOOP REWARDS — WORK PACKAGE K
## Data Quality Audit & Anomaly Issue Register
**Document ID:** VELOOP-DELIV-13  
**Deliverable Covered:** Deliverable 13 (Data Quality Audit Report)  
**Classification:** SIMULATED DATA — CREATED FOR ANALYTICAL TESTING  
**Status Standard:** Confirmed | Proposed | To Be Verified  

---

### 1. Executive Summary & Audit Methodology

The **Data Quality Audit** evaluates intentional and systemic data quality flaws present in the supplied simulated working pack:
* `Users_Messy_Audit` (1,008 records in `VELoop_Rewards_Data_01.xlsx`)
* `10_Event_Data_Quality_Audit` (35,714 records in `VELOOP_Simulated_User_Behavior_1000.xlsx`)

By cross-referencing these sheets against their sanitized counterparts (`Users_1000_Clean` and `03_Feature_Events`), automated scripts extracted exact record counts, affected columns, detection algorithms, and architectural root causes for each defect.

---

### 2. Comprehensive Data Quality Issue Register

The table below catalogs every identified data defect using VELOOP's standard audit template:

| Issue ID | Dataset | Affected Field | Issue Type | Records Affected | Severity | Detection Logic | Likely Root Cause | Correction Action | Prevention Standard | Owner Team | Status |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **DQI-01** | `Users_Messy_Audit` | `user_id` | Duplicate Primary Key | 16 rows (8 pairs) | **Critical** | `df['user_id'].duplicated(keep=False)` | Retry storm or missing unique constraint on database insert | Deduplicate rows keeping latest updated record | Enforce `PRIMARY KEY (user_id)` constraint in PostgreSQL / BigQuery | Backend Auth | Resolved |
| **DQI-02** | `10_Event_Data_Quality_Audit` | `event_id` | Duplicate Event Key | 20 rows (10 pairs) | **Critical** | `df['event_id'].duplicated(keep=False)` | Mobile client offline queue flush resending event payload | Deduplicate on `event_id` taking earliest timestamp | Ingest with idempotency buffer; reject duplicate event UUIDs | Data Engineering | Resolved |
| **DQI-03** | `10_Event_Data_Quality_Audit` | `feature_name` | Inconsistent Casing | 5 records | **High** | `feature_name.str.islower()` | Frontend developers hardcoding string literals instead of using shared enum | Normalize strings via `INITCAP()` / mapping dict | Enforce strict schema validation and string enums at API gateway | Frontend Mobile/Web | Resolved |
| **DQI-04** | `10_Event_Data_Quality_Audit` | `event_status` | Trailing Whitespace & Casing | 4 records | **High** | `apply(lambda x: x != x.strip() or x.islower())` | Manual data patch or unvalidated client string submission (`'success '`) | Apply `TRIM(INITCAP(event_status))` during ingestion | Pre-serialization string sanitation interceptor in SDK | Client SDK | Resolved |
| **DQI-05** | `Users_Messy_Audit` | `registration_datetime` | Unexpected Null & Broken Chronology | 1 record (`VLUSR000023`) | **Critical** | `registration_datetime.isnull() & last_login.notnull()` | Race condition in social login OAuth provisioning | Backfill from first session timestamp (`2026-06-29`) | Make `registration_datetime` `NOT NULL DEFAULT CURRENT_TIMESTAMP` | Backend Auth | Resolved |
| **DQI-06** | `Users_Messy_Audit` | `active_days` vs `lifetime_sessions` | Impossible State Transition | 1 record (`VLUSR000023`) | **Medium** | `active_days == 0 & lifetime_sessions > 0` | Aggregator job failed to increment `active_days` on initial session | Recompute `active_days` from `fact_daily_user_summary` | Unit test aggregation pipeline logic on zero-boundary cases | Analytics Engineering | Resolved |
| **DQI-07** | `05_Task_Activity` | `reward_amount`, `reward_unit` | Complete Column Omission | 9,846 records (100%) | **Critical** | `reward_amount not in df.columns` | Analytical schema omitted monetary fields, logging only boolean `reward_status` | Join with `dim_tasks` catalog to enrich expected reward amounts | Enforce analytical event contract before deploying task pipeline | Product Analytics | Proposed |
| **DQI-08** | `Users_1000_Clean` | `full_name`, `email` | Privacy / PII Exposure | 1,000 records (100%) | **High** | Regex scan for plain-text emails (`@proton.me`, `@gmail.com`) | Legacy analytics dump copying raw production user table | Mask names; hash emails with SHA-256; store domain rollups | Implement dynamic column-level masking (BigQuery Policy Tags) | InfoSec / Governance | Proposed |

---

### 3. Detailed Forensic Analysis of Primary Defects

#### 1. Issue DQI-01: Duplicate User Records in `Users_Messy_Audit`
* **Affected IDs:** `VLUSR000095`, `VLUSR000217`, `VLUSR000272`, `VLUSR000335`, `VLUSR000409`, `VLUSR000779`, `VLUSR000803`, `VLUSR000813`.
* **Impact:** In downstream reporting, joining against a non-unique `user_id` causes exponential Cartesian product fan-out, inflating session counts, transaction volumes, and financial liabilities.
* **Remediation SQL:**
  ```sql
  WITH ranked_users AS (
    SELECT *,
           ROW_NUMBER() OVER(PARTITION BY user_id ORDER BY last_login_datetime DESC NULLS LAST) as rn
    FROM staging_users_messy
  )
  SELECT * EXCEPT(rn)
  FROM ranked_users
  WHERE rn = 1;
  ```

#### 2. Issue DQI-03: Inconsistent Feature Casing in Telemetry
* **Affected Values:** `'missions'` (1), `'daily reward'` (1), `'wallet'` (1), `'leaderboard'` (1), `'watch ads'` (1).
* **Impact:** A simple query `SELECT feature_name, COUNT(*) FROM events GROUP BY 1` splits Missions into two separate rows (`Missions: 2780` and `missions: 1`), breaking executive dashboard charts unless manual cleaning is applied.
* **Remediation Transformation:**
  ```sql
  SELECT
    event_id,
    user_id,
    session_id,
    event_datetime,
    CASE 
      WHEN LOWER(TRIM(feature_name)) = 'missions' THEN 'Missions'
      WHEN LOWER(TRIM(feature_name)) = 'daily reward' THEN 'Daily Reward'
      WHEN LOWER(TRIM(feature_name)) = 'wallet' THEN 'Wallet'
      WHEN LOWER(TRIM(feature_name)) = 'leaderboard' THEN 'Leaderboard'
      WHEN LOWER(TRIM(feature_name)) = 'watch ads' THEN 'Watch Ads'
      ELSE INITCAP(TRIM(feature_name))
    END AS feature_name
  FROM raw_feature_events;
  ```

#### 3. Issue DQI-04: Trailing Whitespace in `event_status`
* **Affected Value:** `'success '` (4 occurrences).
* **Impact:** String filters like `WHERE event_status = 'Success'` evaluate to `FALSE` for these 4 records, silently dropping user completions from conversion rate calculations.
* **Remediation:**
  ```sql
  UPDATE raw_feature_events
  SET event_status = 'Success'
  WHERE LOWER(TRIM(event_status)) = 'success';
  ```

#### 4. Issue DQI-05: Corrupted Registration Date (`VLUSR000023`)
* **Forensic Evidence:** Record has `registration_datetime: NaN`, but `last_login_datetime: 2026-06-29 14:52:00`, `lifetime_sessions: 9`, and `days_since_registration: 77.6`.
* **Chronological Deduction:** Subtracting 77.6 days from the audit snapshot confirms account creation occurred on approximately `2026-04-12`.
* **Fix:** Impute missing registration timestamp from the user's earliest recorded session timestamp.
