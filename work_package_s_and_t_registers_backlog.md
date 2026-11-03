# VELOOP REWARDS — WORK PACKAGES S & T
## Assumption & Verification Register and Final Implementation Backlog
**Document ID:** VELOOP-DELIV-21-ST  
**Deliverables Covered:** Deliverable 21a (Assumption & Verification Register) & Deliverable 21b (Final Implementation Backlog)  
**Classification:** SIMULATED DATA — CREATED FOR ANALYTICAL TESTING  
**Status Standard:** Confirmed | Proposed | To Be Verified  

---

### 1. Work Package S: Assumption & Verification Register

In strict accordance with **Section 25 (Source & Evidence Discipline)**, analysts must never convert unverified assumptions into facts. Every operational uncertainty or unconfirmed engineering capability is cataloged in the register below with risk ratings and verification owners:

| ID | Unknown / Unverified Item | Why It Matters | Source Checked | Risk Level | Verification Owner | Status |
|---|---|---|---|---|---|---|
| **A-001** | Does the core backend service currently emit real-time event payloads upon task completion or write directly to MySQL? | Required for determining whether the data pipeline needs a CDC connector (Debezium) or can consume from Pub/Sub. | Product Documentation | **High** | Lead Backend Engineer | **To Be Verified** |
| **A-002** | What is the exact expiration window for mobile app session tokens (JWT)? | Defines whether session boundaries should be calculated client-side via foregrounding or synthesized from auth token refresh events. | API Specs | **Medium** | Security / Auth Lead | **To Be Verified** |
| **A-003** | Are ad network postback webhooks (AdMob, Unity) signed with verifiable HMAC SHA-256 signatures? | Crucial for preventing spoofed postback fraud where bots simulate ad completion callbacks to steal rewards. | Partner Documentation | **Critical** | Platform Architect | **To Be Verified** |
| **A-004** | Does the payment gateway (Stripe/PayPal/Cashfree) automatically retry failed payouts or require explicit API re-dispatch? | Dictates whether `withdrawal_reversed` should trigger automated re-queueing or manual ops intervention. | Gateway Developer Docs | **High** | Payments Lead | **To Be Verified** |
| **A-005** | Is there an existing data retention or purging policy enforced on live transactional database tables? | Determines whether analytical history can rely on transactional database dumps or must maintain an independent event lake. | Compliance Policy | **Medium** | Lead DBA / Infrastructure | **To Be Verified** |
| **A-006** | Are user IP addresses currently logged as raw IPv4/IPv6 strings or truncated at the gateway load balancer? | Affects whether geolocation enrichment can happen downstream in dbt or must be resolved at the edge. | Ingestion Gateway Config| **Low** | DevOps / Platform | **To Be Verified** |
| **A-007** | Does the referral engine perform device fingerprinting or MAC address matching before issuing referral bonuses? | Critical for preventing emulator-based referral farming where one user creates multiple accounts on one device. | Fraud Heuristics Specs | **Critical** | Fraud & Risk Lead | **To Be Verified** |

---

### 2. Work Package T: Final Prioritized Implementation Backlog

The **Implementation Backlog** translates all architectural requirements, quality controls, and data model extensions into an actionable development roadmap organized by priority and deployment stage:

| Priority | Requirement Name | Technical Description & Scope | Architectural Reason | Primary Dependency | Team Owner | Target Stage |
|---|---|---|---|---|---|---|
| **Critical** | **Enforce Client Idempotency Keys** | Add UUIDv4 `idempotency_key` to all mutation events (`task_completed`, `reward_credited`) with a 30-min Redis deduplication buffer. | Prevents network retries from double-counting completions and issuing duplicate monetary rewards. | API Gateway | Mobile & Backend Engineering | **Pre-Launch** |
| **Critical** | **Implement Double-Entry Wallet Ledger** | Build `fact_wallet_transactions` table with atomic balance shift verification (`running_balance_after`). | Required for zero-loss financial reconciliation, liability tracking, and fraud auditing (Fixes Gap #1). | Database Schema | Core Backend & DBA | **Pre-Launch** |
| **Critical** | **Implement Withdrawal Finite State Machine** | Build `fact_withdrawals` table tracking states (`Requested -> Under Review -> Processing -> Completed / Rejected / Reversed`). | Core value proposition; required to monitor payout fulfillment SLA and liquidity liabilities (Fixes Gap #2). | Payout Service | Payments Engineering | **Pre-Launch** |
| **Critical** | **Primary Key Database Constraints** | Add strict `PRIMARY KEY` and `UNIQUE` constraints across user IDs and transaction IDs. | Prevents Cartesian fan-out and duplicate user records discovered in `Users_Messy_Audit` (DQI-01). | Database DDL | Lead DBA | **Pre-Launch** |
| **High** | **Relational Referral Attribution Bridge** | Implement `fact_referral_conversions` linking referrer to referee across registration, activation, and conversion. | Prevents paying bonuses for inactive signups; measures true viral coefficient ($K$) (Fixes Gap #3). | Auth & Referral Service | Growth Engineering | **Pre-Launch** |
| **High** | **Telemetry String Sanitization Interceptor** | Add pre-emission SDK middleware enforcing Title Case on feature names and trimming whitespace on status strings. | Eliminates SQL `GROUP BY` fragmentation and silent query filter drops discovered in messy events (DQI-03/04). | Client Telemetry SDK | Mobile & Web Frontend | **Pre-Launch** |
| **High** | **Dynamic PII Masking in Analytics Lake** | Implement BigQuery column-level security or dbt hashing models replacing raw email with SHA-256 hash and domain rollups. | Ensures legal compliance with GDPR and DPDP Act data privacy mandates (DQI-08). | dbt / Warehouse IAM | Data Engineering & InfoSec | **Pre-Launch** |
| **High** | **Task Catalog Monetary Enrichment** | Add numeric `reward_amount` and `reward_unit` columns to `fact_task_activity`. | Enables calculating gross reward issuance and cost-per-completion directly from task events (DQI-07). | Task Engine DB | Product Analytics | **Pre-Launch** |
| **Medium** | **Automated Daily Ledger Reconciliation** | Deploy automated daily SQL test: $\sum \text{Credits} - \sum \text{Debits} == \sum \text{User Balances}$. | Early warning detection for ledger drift, race conditions, or unrecorded database updates. | dbt & Airflow / Cloud Run | Analytics Engineering | **Post-Launch (Day 7)** |
| **Medium** | **Executive & Operational Dashboards** | Deploy Looker Studio / Metabase dashboards across the 7 blueprint specifications. | Replaces manual Excel data manipulation with automated decision cockpits for leadership and operations. | BI Semantic Layer | BI Analyst | **Post-Launch (Day 14)** |
| **Medium** | **Automated Dead-Letter Queue (DLQ) Replay** | Build automated serverless replay function for re-submitting valid DLQ events into ingestion queue. | Prevents event data loss during downstream database maintenance windows. | Cloud Functions / Lambda | Data Platform | **Post-Launch (Day 21)** |
| **Low** | **Machine Learning Bot Detection Pipeline** | Train unsupervised anomaly detection model (Isolation Forest) on inter-tap intervals and session velocities. | Identifies sophisticated autoclickers and human bot farms bypassing basic velocity rules. | Feature Store | Data Science / ML Team | **Post-Launch (Day 60)** |
| **Low** | **Dynamic Currency Exchange Optimization** | Real-time algorithmic adjustment of XP-to-Token exchange rates based on advertiser eCPM fluctuations. | Maximizes platform gross margin while maintaining user earning motivation. | Economy Config Engine | Economy Designer | **Post-Launch (Day 90)** |
