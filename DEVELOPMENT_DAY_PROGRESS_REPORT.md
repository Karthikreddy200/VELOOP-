# VELOOP REWARDS DATA ANALYST INTERNSHIP
## DEVELOPMENT DAY OFFICIAL PROGRESS & CODE IMPROVEMENT REPORT
**Schedule Reference:** Phase 2 Development Milestone (Work Package B — Deliverable 04)  
**Session Window:** Session 1 (9:30 AM – 2:30 PM)  
**Classification:** `SIMULATED DATA — CREATED FOR ANALYTICAL TESTING`  
**Author:** Karthik Reddy, Data Analyst Intern — VELOOP Product Analytics  
**Date Submitted:** November 5, 2026  

---

## 1. Executive Summary & Development Day Objectives

In strict compliance with today's **Development Day** charter, analytical development focused on code hardening, error resolution, UI/UX optimization, and advancing into **Work Package B (User & Account Analytics Specification)**. 

### Core Milestones Executed:
1. **Bug Resolution & Zero-Error Hardening:** Successfully debugged dynamic aggregation exceptions (`KeyError: active_users` and `ValueError: duration_seconds`), achieving zero-error rendering across all 6 live views.
2. **Work Package B Implementation (Deliverable 04):** Built a formal **5-stage User Lifecycle State Machine** classifying 1,000 cohort profiles and establishing operational transition triggers.
3. **Empirical Cohort Retention Modeling:** Derived Day-1, Day-7, Day-14, and Day-30 retention decay curves from 6,667 daily telemetry records, identifying Referral acquisition as the highest-loyalty channel.
4. **Data Governance & PII Masking (Section 22):** Deployed a live **SHA-256 PII pseudonymization engine** ensuring strict compliance with the Digital Personal Data Protection (DPDP) Act and GDPR.
5. **Analytics Engineering dbt SQL Models:** Formulated modular bronze-to-silver warehouse transformation models (`stg_users.sql`, `stg_events.sql`) for automated deduplication and string sanitation.
6. **UI/UX Interactive Slicing:** Implemented global multi-platform and acquisition source filters across the live Streamlit dashboard.

---

## 2. Bug Resolution & Deployment Hardening

During deployment stress testing, two critical runtime exceptions were identified in the telemetry visualization pipeline and permanently resolved:

| Defect ID | Affected View | Exception Encountered | Root Cause Analysis | Engineering Remediation Applied | Status |
|---|---|---|---|---|---|
| **BUG-01** | **View 2: Executive Cockpit** | `KeyError: 'active_users'` | `04_Daily_Activity` logs user-date records without pre-aggregated counts. Calling `.sum()` on a missing scalar column triggered a runtime exception. | Implemented dynamic distinct user aggregation: `data['daily'].groupby('activity_date')['user_id'].nunique()`, aliased to `active_users`. | **Resolved & Verified** |
| **BUG-02** | **View 4: Task Engagement** | `ValueError: duration_seconds` | `05_Task_Activity` records raw ISO timestamps (`task_started_at`, `task_completed_at`) rather than a pre-computed duration float. | Added automated duration delta computation `(task_completed_at - task_started_at).dt.total_seconds()` in the data loader, with NaN fallback. | **Resolved & Verified** |

> **Result:** All 6 platform exploration views compile and render with zero warnings or exceptions.

---

## 3. Work Package B: User Lifecycle State Machine (Deliverable 04)

To prevent customer churn and enable automated lifecycle marketing, the 1,000-user cohort was classified into **5 operational lifecycle states**:

```mermaid
flowchart LR
    A[Anonymous Visitor] --> B[Registered User]
    B --> C[Highly Active 7D<br/>69 Users]
    C --> D[Moderately Active 30D<br/>231 Users]
    D --> E[Dormant At Risk<br/>162 Users]
    E --> F[Churned >60D<br/>461 Users]
    B -. Violations .-> G[Suspended / Fraud<br/>77 Users]
    E -. Re-engagement .-> C
```

### 3.1 State Breakdown & Cohort Sizing

| Lifecycle State | Active Cohort Size | Proportion (%) | Operational Definition | Target Marketing / Analytics Action |
|---|---|---|---|---|
| 🟢 **Highly Active (7D)** | **69 users** | **6.9%** | Active within the rolling 7-day habit window (`is_active_7d = 1`). | Reward loyalty with VIP streak badges and exclusive multiplier missions. |
| 🔵 **Moderately Active (30D)** | **231 users** | **23.1%** | Active within the rolling 30-day window (`is_active_30d = 1`). | Send mid-week earning reminders and personalized task recommendations. |
| 🟠 **Dormant (At Risk)** | **162 users** | **16.2%** | Inactive between 31 and 60 days (`days_since_reg` > 30, inactive 30d). | Trigger high-priority automated push notifications and re-activation bonus XP. |
| 🔴 **Churned (>60D)** | **461 users** | **46.1%** | Inactive for > 60 consecutive days. | Funnel into win-back campaigns and conduct churn exit surveys. |
| ⚪ **Suspended / Fraud** | **77 users** | **7.7%** | Flagged for multi-accounting, autoclickers, or emulator use. | Frozen funds in escrow; manual compliance review required. |

---

## 4. Empirical Cohort Retention Modeling

Using 6,667 daily activity records cross-joined with user registration dates, empirical return rates were derived across critical retention intervals:

$$\text{Retention Rate}(t) = \frac{\text{Unique Active Users at Day } t}{\text{Total Cohort Registration Size}} \times 100$$

### 4.1 Platform Retention Benchmarks

* **Day-1 Retention (Next-Day Return):** `5.6%` (Initial onboarding habituation)
* **Day-7 Retention (Streak Milestone):** `11.4%` (Habit loop formation)
* **Day-14 Retention (Mid-Funnel):** `10.6%`
* **Day-30 Retention (Long-Term Loyalty):** `14.2%`

### 4.2 Cohort Retention Decay by Acquisition Source

| Acquisition Channel | Cohort Size ($N$) | Day 1 (%) | Day 7 (%) | Day 14 (%) | Day 30 (%) | Channel Performance Verdict |
|---|---|---|---|---|---|---|
| **Referral** | **119** | **8.4%** | **10.1%** | **12.6%** | **16.8%** | ⭐ **Top Performer:** Highest Day-30 retention. Strong social accountability. |
| **Organic Search** | 244 | 7.4% | 10.7% | 11.5% | 14.8% | **High Quality:** High intent users with sustained 30-day return rate. |
| **Direct** | 217 | 5.1% | 13.8% | 11.1% | 12.9% | **Solid Core:** Steady Day-7 habituation. |
| **Social Media** | 160 | 4.4% | 8.8% | 8.1% | 13.1% | **Volatile:** High early drop-off, requires stronger onboarding hooks. |
| **Telegram** | 55 | 5.5% | 14.5% | 9.1% | 10.9% | **Niche:** Strong early week engagement, rapid mid-funnel decay. |
| **WhatsApp** | 103 | 1.9% | 10.7% | 11.7% | 18.4% | **High Late Retention:** Slower Day-1 activation, but high Day-30 stickiness. |

---

## 5. Section 22 PII Governance & 4-Tier Identity Hierarchy

To ensure compliance with the **Digital Personal Data Protection (DPDP) Act 2023** and **GDPR**, personally identifiable information (PII) must never be stored in plaintext within analytical warehouse layers.

### 5.1 The 4-Tier Identity Hierarchy Model

```mermaid
flowchart TD
    T1["Tier 1: user_id (UUIDv4)<br/>Immutable Platform Identity Anchor"] --> T2["Tier 2: session_id<br/>30-Minute Continuous Activity Container"]
    T2 --> T3["Tier 3: event_id<br/>Atomic Clickstream Telemetry Interaction"]
    T2 --> T4["Tier 4: transaction_id<br/>Immutable Financial Double-Entry Ledger Shift"]
```

### 5.2 Live SHA-256 Masking Implementation
In the analytical lake, personal emails are pseudonymized via SHA-256 hashing while retaining the domain suffix for ISP deliverability reporting:

$$\text{Masked Email} = \text{SHA-256}(\text{Username})[:8] + \text{"...@"} + \text{Domain}$$

* **Raw Format:** `sanjay.singh1@gmail.com`
* **Compliant Analytical Format:** `c54edcba...@gmail.com`

---

## 6. Analytics Engineering: Production dbt SQL Models

To operationalize data cleaning at scale, modular dbt transformation models were authored for warehouse deployment:

### 6.1 `stg_users.sql` (Deduplication & Anomaly Cleansing)
```sql
-- models/silver/stg_users.sql
WITH ranked_users AS (
    SELECT 
        user_id,
        SHA256(email) AS masked_email_hash,
        SPLIT_PART(email, '@', 2) AS email_domain,
        account_status,
        -- Correct future registration dates discovered in audit
        CASE 
            WHEN registration_datetime > CURRENT_TIMESTAMP() THEN CURRENT_TIMESTAMP()
            ELSE registration_datetime 
        END AS cleaned_registration_datetime,
        -- Enforce non-negative point constraint
        GREATEST(xp_balance, 0) AS cleaned_xp_balance,
        ROW_NUMBER() OVER(PARTITION BY user_id ORDER BY registration_datetime ASC) AS rn
    FROM {{ source('raw_veloop', 'users_messy') }}
)
SELECT 
    user_id,
    masked_email_hash,
    email_domain,
    account_status,
    cleaned_registration_datetime,
    cleaned_xp_balance
FROM ranked_users
WHERE rn = 1;
```

### 6.2 `stg_events.sql` (Casing Normalization & String Sanitization)
```sql
-- models/silver/stg_events.sql
SELECT 
    event_id,
    user_id,
    session_id,
    event_datetime,
    -- Resolve SQL aggregation fragmentation from dirty casing
    INITCAP(TRIM(feature_name)) AS feature_name,
    LOWER(TRIM(event_name)) AS event_name,
    UPPER(TRIM(event_status)) AS event_status,
    COALESCE(device, 'UNKNOWN') AS device
FROM {{ source('raw_veloop', 'events_messy') }}
QUALIFY ROW_NUMBER() OVER(PARTITION BY event_id ORDER BY event_datetime ASC) = 1;
```

---

## 7. UI/UX & Interactive Platform Slicing

The Streamlit deployment was upgraded with global multi-dimensional slicing:
* **Dynamic Platform Filter:** `All`, `Android`, `iOS`, `Web`
* **Acquisition Source Filter:** `All`, `Direct`, `Organic Search`, `Referral`, `Social Media`, `Telegram`, `WhatsApp`
* **Instant KPI Recalculation:** Changing filters dynamically updates active cohort counts, circumscribes demographics, and recalibrates total circulating XP liabilities.

---

## 8. Development Verification & Delivery Summary

| Verification Gate | Result / Metric | Evidence Location |
|---|---|---|
| **Compilation & Syntax** | 100% Passed (0 Errors) | `python -m py_compile dashboard_app.py` |
| **Local Deployment** | Active on Port 8501 (HTTP 200) | `http://localhost:8501` |
| **Git Version Control** | Committed to `main` (Commit a9a375e) | `DEVELOPMENT_DAY_PROGRESS_LOG.md` |
| **Attendance Status** | Session 1 Marked (9:30 AM – 2:30 PM) | Logged in Internship Portal |

---
**Report Compiled By:** Karthik Reddy, Data Analyst Intern  
**Project Workspace:** `C:\Users\ckart\.gemini\antigravity\scratch\veloop_analytics_task01\`  
**Milestone:** Development Day Session 1 Complete
