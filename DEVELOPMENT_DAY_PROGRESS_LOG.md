# VELOOP REWARDS DATA ANALYST INTERNSHIP
## DEVELOPMENT DAY PROGRESS & CODE IMPROVEMENT LOG
**Date:** November 5, 2026  
**Intern Name:** Karthik Reddy  
**Role:** Data Analyst Intern — VELOOP Product Analytics  
**Classification:** `SIMULATED DATA — CREATED FOR ANALYTICAL TESTING`  
**Focus Milestone:** Transition into Work Package B (User Lifecycle, Cohort Analytics & Data Governance)  

---

### 1. Executive Summary of Today's Improvements
In accordance with the **Development Day** charter, today's development focused on enhancing project functionality, code quality, and advancing into scheduled **Work Package B (User Analytics & Cohort Retention Specification)**.

---

### 2. Detailed Technical Upgrades Implemented

#### A. Interactive Slice Filters (UI/UX Improvement)
* **What was added:** Global interactive filters added to the dashboard sidebar allowing dynamic slicing by:
  * **Platform:** `All`, `Android`, `iOS`, `Web`
  * **Acquisition Source:** `All`, `Direct`, `Organic Search`, `Referral`, `Social Media`, `Telegram`, `WhatsApp`
* **Impact:** Enables stakeholders to drill down into platform-specific performance and cohort quality without writing custom SQL.

#### B. Work Package B: User Lifecycle State Machine (Deliverable 04)
* **What was added:** Engineered an automated classification engine categorizing users into 5 distinct lifecycle states:
  * 🟢 **Highly Active (7D):** 69 users (active within the rolling 7-day habit window)
  * 🔵 **Moderately Active (30D):** 231 users (monthly active users)
  * 🟠 **Dormant (At Risk):** 162 users (inactive between 31 and 60 days, requiring re-engagement push notifications)
  * 🔴 **Churned (>60D):** 461 users (long-term inactive cohort)
  * ⚪ **Suspended:** 77 users (compliance/risk held accounts)
* **Impact:** Provides product managers with an operational state transition matrix to trigger targeted CRM campaigns.

#### C. Cohort Retention Modeling & Decay Curves
* **What was added:** Calculated empirical user return rates across registration cohorts from 6,667 daily activity records:
  * **Day 1 Retention:** `5.6%`
  * **Day 7 Retention:** `11.4%` (streak milestone)
  * **Day 14 Retention:** `10.6%`
  * **Day 30 Retention:** `14.2%` (long-term loyalty)
* **Key Analytical Finding:** Users acquired via **Referrals exhibited the highest Day-30 retention (16.8%)**, outperforming Paid Direct and Organic Search.

#### D. Section 22 PII Governance & 4-Tier Identity Hierarchy
* **What was added:** Integrated an interactive **PII Masking Engine** supporting live switching between:
  * **Raw PII Mode (Restricted Admin):** Plaintext names and emails.
  * **SHA-256 Masked Mode (Analytics Lake):** Pseudonymized hashes (`c54edcba...@gmail.com`) preserving domain suffixes for email deliverability analytics.
* **Impact:** Guarantees strict compliance with the **DPDP Act (India)** and **GDPR (EU)**.

#### E. Production SQL dbt Transformation Models (Analytics Engineering)
* **What was added:** Formulated modular dbt SQL transformation models in View 5:
  * `stg_users.sql`: Automated primary key deduplication via window functions (`ROW_NUMBER()`) and future registration date correction.
  * `stg_events.sql`: Pre-emission string trimming and Title Case normalization (`INITCAP(TRIM(feature_name))`).

---

### 3. Verification & Deployment Status
* **Local Web URL:** `http://localhost:8501` (Active, zero runtime errors)
* **Repository:** `https://github.com/Karthikreddy200/VELOOP-.git`
* **Attendance:** Session 1 Marked
