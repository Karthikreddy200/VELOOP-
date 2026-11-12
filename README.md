# ⚡ VELOOP REWARDS — PRODUCT ANALYTICS & DATA READINESS PLATFORM
### *Enterprise Product Analytics, Fraud-Resistant Mechanics & Financial Ledger Architecture*

[![Python](https://img.shields.io/badge/Python-3.11%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.48%2B-FF4B4B.svg)](https://streamlit.io/)
[![Plotly](https://img.shields.io/badge/Plotly-Interactive%20Charts-3F4F75.svg)](https://plotly.com/)
[![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458.svg)](https://pandas.pydata.org/)
[![Tests](https://img.shields.io/badge/Tests-19%2F19%20Passed-brightgreen.svg)]()
[![dbt](https://img.shields.io/badge/dbt-Modular%20Transformations-orange.svg)](https://www.getdbt.com/)
[![Status](https://img.shields.io/badge/Status-Review%20Ready-success.svg)]()

> **Notice:** `SIMULATED DATA — CREATED FOR ANALYTICAL TESTING`  
> In compliance with Section 34 of the official VELOOP Internship Specification, all analytics, telemetry, and user profiles in this repository are derived from simulated testing datasets (1,000 synthetic users, 35k events) and do not represent actual proprietary company performance metrics.

---

## 📌 Executive Project Overview

This repository contains the complete analytical architecture, documentation blueprints, data quality audit pipelines, and live interactive web deployment for **VELOOP Rewards Task 01: Product Analytics, Data Readiness & Data Management Blueprint**.

**VELOOP** is a gamified online rewards ecosystem incorporating micro-tasks, gamification habit loops, multi-currency economies (XP, Gems, Tokens), and external cash-out redemption gateways. This platform models, audits, and visualizes the complete end-to-end data lifecycle required to operate a secure, scalable, and fraud-resistant rewards application.

---

## 🚀 Live Interactive Deployment (`dashboard_app.py`)

The platform features an enterprise-grade **Streamlit Web Application** serving **7 specialized operational views**:

| View | Module Name | Focus & Analytical Capabilities |
|---|---|---|
| **View 1** | **📋 Product Spec & Source Register** | Review of **15 product modules**, searchable **Source & Verification Register** (26 items classified as Confirmed / Proposed / To Be Verified), and prioritized Engineering Discovery Backlog. |
| **View 2** | **📊 Executive Overview Cockpit** | Macro-level executive dashboard tracking 1,000 acquired users, 50.8% DAU/MAU stickiness, $0.48 gross revenue/user, 9,846 task activities, and slice filters. |
| **View 3** | **👥 User Lifecycle & Growth (WP B & E)** | Acquisition attribution, 7-stage deterministic FSM lifecycle, Day 0–30 cohort retention heatmap, and **Tab 5: Referral Conversion Funnel & Viral $K$-Factor Simulator ($K = 0.82$)**. |
| **View 4** | **🎯 Task & Feature Engagement (WP C)** | Conversion funnel across 9,846 task activities, 24h density heatmaps, and **Tab 2: Anti-Farming & Bot Defense Simulator** (clickstream heuristics, superhuman speed detection, token liquidity). |
| **View 5** | **🔍 Data Quality Forensic Audit** | Shift-left data quality engine identifying 11 anomalies across Bronze tables, verifying raw data preservation and automated cleaning pipelines. |
| **View 6** | **💰 Live Wallet & Payout Simulator** | Validated **double-entry transaction ledger** (`Sum(Debits) - Sum(Credits) == 0.0000 USD`) and **4-stage automated withdrawal pipeline** (Balance, KYC, AML velocity, Fraud score). |
| **View 7** | **📑 21 Deliverables Verification Matrix** | Complete compliance matrix cross-referencing all 21 core task deliverables across 7 modules (100% verified and audit-ready). |

---

## 📸 Visual Dashboard Gallery

### 1. Executive Cockpit & North Star Metrics (View 2)
![Executive Cockpit](screenshots/01_executive_cockpit.png)
*Displays platform health, active users, daily activity trends, and acquisition channel breakdowns.*

### 2. Referral Conversion Funnel & Viral $K$-Factor Simulator (View 3 Tab 5)
![Referral Funnel & K-Factor](screenshots/03_referral_viral_growth_wpe.png)
*Work Package E engine modeling the 4-tier funnel (595 invites → 119 installs → 16.8% D30 retention), viral coefficient ($K = 0.82$), and anti-sybil hardware collision checks.*

### 3. Anti-Farming & Bot Defense Simulator (View 4 Tab 2)
![Anti-Farming & Bot Defense](screenshots/05_anti_farming_bot_defense_wpc.png)
*Work Package C security heuristics contrasting human tapping (4.1 taps/s, 28ms jitter) against superhuman autoclickers (>10 taps/s, <8ms jitter), 20-ad daily cap, and $2.0\times$ Liquidity Coverage Ratio.*

### 4. Double-Entry Financial Ledger & Withdrawal Validation (View 6)
![Double-Entry Ledger](screenshots/07_wallet_double_entry_ledger.png)
*Zero-variance accounting reconciliation ($1,428.50 Debits = $1,428.50 Credits) and 4-stage automated withdrawal pipeline.*

### 5. Data Quality Forensic Audit & Anomaly Detection (View 5)
![Data Quality Forensics](screenshots/06_data_quality_audit.png)
*Bronze layer audit isolating 11 data anomalies while preserving raw source tables.*

### 6. 21 Deliverables Verification Matrix & Master Blueprint (View 7)
![21 Deliverables Matrix](screenshots/08_21_deliverables_matrix.png)
*Comprehensive audit matrix verifying 100% completion across all 21 required deliverables.*

---

## 🏗️ Technical Architecture & Key Modules

```text
├── src/
│   ├── analytics/
│   │   ├── referral_attribution.py     # Work Package E: Viral K-factor & Sybil detection
│   │   ├── reward_economy_engine.py    # Work Package C: Anti-farming limits & bot detector
│   │   ├── user_lifecycle_fsm.py       # 7-stage deterministic User Lifecycle FSM
│   │   └── cohort_retention.py         # Day 0-30 survival decay engine
│   └── governance/
│       └── pii_masking.py              # Salted SHA-256 tokenization & GDPR pseudonymization
│
├── dbt_project/                        # Production dbt Transformation Layer
│   ├── models/
│   │   ├── staging/                    # Bronze -> Silver views (stg_users, stg_events)
│   │   └── marts/                      # Silver -> Gold analytical tables (dim_user_lifecycle, etc.)
│   └── dbt_project.yml                 # dbt project definition
│
├── data/                               # Raw & audited Excel datasets (Bronze layer)
├── screenshots/                        # High-resolution dashboard captures
├── tests/
│   └── test_analytics.py               # 19 automated unit tests (100% pass rate)
├── .github/workflows/
│   └── analytics_ci.yml                # Automated CI/CD pipeline
├── dashboard_app.py                    # Streamlit interactive application
├── requirements.txt                    # Project dependencies
└── README.md                           # Documentation & presentation guide
```

---

## 🧪 Automated Testing & CI/CD Pipeline

All analytics modules, financial ledgers, and fraud detection heuristics are covered by automated unit tests:

```bash
python -m unittest tests/test_analytics.py
...................
----------------------------------------------------------------------
Ran 19 tests in 0.003s

OK (19 Passed / 0 Failed / 100% Pass Rate)
```

**Test Coverage Highlights:**
- `test_referral_k_factor_calculation`: Validates viral growth formula ($K = i \times c = 0.82$).
- `test_referral_sybil_fraud_detection`: Blocks multi-accounting on identical device hardware hashes.
- `test_tap_bot_detection`: Identifies superhuman tap frequencies (>10 taps/s) and robotic timing.
- `test_ad_watch_velocity_cap`: Enforces 20-ad daily cap and 28-second active watch minimum.
- `test_withdrawal_valid_transaction`: Asserts zero variance in double-entry financial ledger.
- `test_raw_data_preservation`: Verifies that raw Bronze files remain immutable.

---

## 🛠️ Quick Start & Local Execution

### 1. Clone the Repository
```bash
git clone https://github.com/Karthikreddy200/VELOOP-.git
cd VELOOP-
```

### 2. Install Required Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run Automated Unit Tests
```bash
python -m unittest tests/test_analytics.py
```

### 4. Launch the Live Interactive Dashboard
```bash
streamlit run dashboard_app.py
```
*The application will open in your browser at `http://localhost:8501`.*

---

## 👥 Author & Internship Details

* **Author:** Karthik Reddy (Data Analyst Intern)  
* **Role:** Product Analytics & Data Management  
* **Program:** VELOOP Rewards Internship Program  
* **GitHub Repository:** [https://github.com/Karthikreddy200/VELOOP-](https://github.com/Karthikreddy200/VELOOP-)  
* **LinkedIn:** Connect on [LinkedIn](https://www.linkedin.com)  
