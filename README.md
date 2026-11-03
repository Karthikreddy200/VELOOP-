# ⚡ VELOOP REWARDS — PRODUCT ANALYTICS & DATA READINESS PLATFORM
### *Enterprise Product Analytics, Data Quality Assurance & Financial Ledger Architecture*

[![Python](https://img.shields.io/badge/Python-3.11%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.48%2B-FF4B4B.svg)](https://streamlit.io/)
[![Plotly](https://img.shields.io/badge/Plotly-Interactive%20Charts-3F4F75.svg)](https://plotly.com/)
[![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458.svg)](https://pandas.pydata.org/)
[![Status](https://img.shields.io/badge/Deployment-Live%20Ready-success.svg)]()

> **Notice:** `SIMULATED DATA — CREATED FOR ANALYTICAL TESTING`  
> In compliance with Section 34 of the official VELOOP Internship Specification, all analytics, telemetry, and profiles in this repository are derived from simulated testing datasets and do not represent actual proprietary company performance metrics.

---

## 📌 Executive Project Overview

This repository contains the complete analytical architecture, documentation blueprints, data quality audit pipelines, and live interactive web deployment for **VELOOP Rewards Task 01: Product Analytics, Data Readiness & Data Management Blueprint**.

VELOOP is a gamified online rewards ecosystem incorporating micro-tasks, gamification habit loops, multi-currency economies (XP, Gems, Tokens), and external cash-out redemption gateways. This platform models, audits, and visualizes the complete end-to-end data lifecycle required to operate a fraud-resistant rewards application.

---

## 🚀 Live Interactive Deployment (`dashboard_app.py`)

The platform includes a deployed **Streamlit Web Application** featuring 6 specialized exploration views:

| View | Module Name | Focus & Analytical Capabilities |
|---|---|---|
| **View 1** | **📋 Days 1–2: Product Spec & Source Register** | Interactive review of the **15 product modules**, searchable **Source & Verification Register** (26 items classified as Confirmed / Proposed / To Be Verified), Section 6 Fact vs. Assumption tables, and prioritized Engineering Discovery Backlog. |
| **View 2** | **📊 Executive Overview Cockpit** | Macro-level executive dashboard tracking 1,000 acquired users, 35,704 telemetry events, daily active user (DAU) trends, and feature market share. |
| **View 3** | **👥 User Lifecycle & Growth** | Acquisition channel attribution (Organic, Referral, Paid Ads), account lifecycle status breakdown, demographic spreads (ages 18–55), and geographic state distribution. |
| **View 4** | **🎯 Task & Feature Engagement** | Conversion funnel analysis across 9,846 task activities (57.2% Task Completion Rate), duration friction spread (box plot), and 24-hour engagement density heatmaps. |
| **View 5** | **🔍 Data Quality Forensic Audit** | Shift-left data quality engine identifying duplicate primary keys, future dates, and casing anomalies, featuring an **interactive one-click cleaning pipeline** that cleans dirty tables live on screen. |
| **View 6** | **💰 Live Wallet & Payout Simulator** | Interactive demonstration of the proposed **double-entry transaction ledger** (`fact_wallet_transactions`) and **6-stage withdrawal state machine**, verifying atomic running balances and gateway dispatch handshakes. |

---

## 📁 Repository Structure & Work Package Deliverables

```text
├── data/                                             # Raw & audited datasets
│   ├── VELoop_Rewards_Data_01.xlsx                   # User cohort profiles & messy audit logs
│   └── VELOOP_Simulated_User_Behavior_1000.xlsx      # 35k telemetry events, sessions, tasks, daily activity
├── screenshots/                                      # UI screenshots of the deployed dashboard views
├── dashboard_app.py                                  # Live Streamlit Interactive Web Application
│
├── VELOOP_DAY_1_2_SUBMISSION.md                      # Milestone Progress Report: Days 1–2 (Markdown)
├── VELOOP_DAY_1_2_SUBMISSION.html                    # Formatted Milestone Progress Report: Days 1–2 (HTML/PDF)
├── VELOOP_DAYS_1_TO_4_PROGRESS_SUBMISSION.md         # Milestone Progress Report: Days 1–4 (Markdown)
├── VELOOP_DAYS_1_TO_4_PROGRESS_SUBMISSION.html       # Formatted Milestone Progress Report: Days 1–4 (HTML/PDF)
├── VELOOP_TASK01_FINAL_SUBMISSION.html               # Master Consolidated Blueprint (All 21 Deliverables)
│
├── work_package_a_product_data_readiness_audit.md    # WP A: Product Data Readiness & Coverage Matrix
├── work_package_b_user_analytics_spec.md             # WP B: User Identity, Lifecycle & Cohort Analytics
├── work_package_c_earning_reward_analytics.md        # WP C: Earning Mechanics & Anti-Bot Friction
├── work_package_d_wallet_withdrawal_analytics.md     # WP D: Double-Entry Ledger & Withdrawal State Machine
├── work_package_e_referral_engagement_analytics.md   # WP E: Referral Attribution & K-Factor Viral Loops
├── work_package_f_production_event_tracking_plan.md  # WP F: Production Event Tracking Plan (28 Events)
├── work_package_g_data_dictionary.md                 # WP G: Enterprise Data Dictionary (80+ Fields)
├── work_package_h_logical_data_model.md              # WP H: Dimensional Star Schema & ERD DDL
├── work_package_i_kpi_catalogue.md                   # WP I: Master KPI Catalogue (35 KPIs)
├── work_package_j_simulated_data_profiling.md        # WP J: Data Profiling & Statistical Baseline
├── work_package_k_data_quality_audit.md              # WP K: Data Quality Audit & Forensic Issue Log
├── work_package_l_data_quality_control_framework.md  # WP L: Data Quality Control Framework & SLAs
├── work_package_m_analytics_dashboard_blueprint.md   # WP M: Executive & Operational Dashboard Blueprints
├── work_package_n_developer_analytics_handoff.md     # WP N: Developer Handoff & SDK Specs
├── work_package_o_data_pipeline_operating_model.md   # WP O: Data Pipeline Architecture (Bronze/Silver/Gold)
├── work_package_p_privacy_governance.md              # WP P: PII Masking, GDPR & DPDP Act Governance
├── work_package_q_analytics_change_management.md     # WP Q: Analytics Change Management Framework
├── work_package_r_analytics_readiness_assessment.md  # WP R: Organizational Readiness Assessment (82/100)
├── work_package_s_and_t_registers_backlog.md         # WP S & T: Source Register & Implementation Backlog
│
├── requirements.txt                                  # Python dependencies
└── README.md                                         # Project documentation & presentation guide
```

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

### 3. Launch the Live Interactive Dashboard
```bash
streamlit run dashboard_app.py
```
*The app will automatically open in your default browser at `http://localhost:8501`.*

---

## 📑 Days 1–2 Deliverables Summary

* **Product Documentation Review:** Analyzed all 15 operational features across Account Auth, Earning Activities (Watch Ads, Tap & Earn, Mining, Missions), Gamification (Daily Rewards, Streaks, Badges), and Monetary Systems.
* **Source & Verification Register (Deliverable 21a):** Cataloged 26 technical and architectural facts with strict evidence discipline:
  * 🟢 **Confirmed (11):** Verified directly in telemetry and clean tables.
  * 🔵 **Proposed (8):** Recommended architectures (double-entry ledger, withdrawal FSM, idempotency).
  * 🔴 **To Be Verified (7):** Critical technical unknowns requiring engineering confirmation.
* **Evidence Discipline (Section 6 Compliance):** Documented strict boundaries separating confirmed system realities from proposed analytical entities (e.g., Session identifiers, double-entry wallet ledger).
* **Engineering Discovery Backlog:** Structured 10 technical discovery questions for Backend, Security, Payments, and DevOps to resolve key operational unknowns.

---

## 👥 Authors & Acknowledgments

* **Author:** Data Analyst Intern, VELOOP Product Analytics Team  
* **Program:** VELOOP Rewards Data Analyst Internship  
* **Repository:** [https://github.com/Karthikreddy200/VELOOP-.git](https://github.com/Karthikreddy200/VELOOP-.git)
