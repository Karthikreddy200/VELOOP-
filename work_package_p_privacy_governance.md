# VELOOP REWARDS — WORK PACKAGE P
## Data Access, Privacy & Governance Policy
**Document ID:** VELOOP-DELIV-18  
**Deliverable Covered:** Deliverable 18 (Privacy & Governance Proposal)  
**Classification:** SIMULATED DATA — CREATED FOR ANALYTICAL TESTING  
**Status Standard:** Confirmed | Proposed | To Be Verified  

---

### 1. Executive Purpose & Governance Charter

Data security, user privacy, and strict role-based data access are non-negotiable foundations for VELOOP Rewards. Because VELOOP manages monetizable tasks, reward liabilities, and real-world cash withdrawals, unmanaged data access creates catastrophic vectors for financial fraud, insider balance manipulation, and regulatory penalties under GDPR and the Digital Personal Data Protection (DPDP) Act.

This document establishes:
1. The **Enterprise Role-Based Access Control (RBAC) Matrix**.
2. Strict **Prohibited & Restricted Data Isolation Standards**.
3. Column-Level **Dynamic Data Masking & Pseudonymization Protocols**.

---

### 2. Role-Based Access Control (RBAC) Matrix

To guarantee **Least-Privilege Access**, data assets across the VELOOP data warehouse and analytical environments are compartmentalized across five formal user personas:

| User Persona / Role | Permitted Data Scope | Prohibited Data Scope | Access Method & Tools | Primary Business Purpose |
|---|---|---|---|---|
| **1. Engineering (Backend / Core)** | Transactional application databases, raw telemetry stream, production logs | Financial payment secrets, raw customer passwords, unmasked payment credentials | Direct read/write to microservice DBs; BigQuery raw logs | Technical event implementation, bug fixes, latency optimization |
| **2. Data Analyst** | Sanitized analytical datasets (`dim_users`, `dim_sessions`, `fact_task_activity`, `fact_wallet_transactions`) | Plaintext PII (raw email, full name, phone number, destination bank account), auth secrets | Read-only access to BigQuery Silver & Gold layers, dbt, Python sandbox | Exploratory data analysis, cohort retention modeling, KPI calculation |
| **3. Product & Operations** | Aggregated data marts, business reporting dashboards, anonymized funnel metrics | Row-level raw transaction payloads, individual user telemetry logs, security risk scores | Looker Studio, Metabase, Tableau, aggregated BI views | Tracking feature adoption, task completion rates, payout SLA turnaround |
| **4. Content & Marketing Team** | Aggregated acquisition channel metrics, campaign conversion summaries, task category CTR | User-level balances, financial ledger transactions, individual withdrawal history | Looker Studio marketing reports, Google Analytics | Optimizing promotional campaigns, partner offerwall placement |
| **5. Intern / External Auditor** | Approved, sanitized simulated datasets, synthetic test beds, masked staging tables | Any live production user data, live wallet transactions, real gateway callbacks | Isolated sandbox project, synthetic CSV/Parquet dumps | Analytical modeling, documentation, data quality testing |

---

### 3. Prohibited & Restricted Data Isolation Standards

In accordance with Section 22 and Section 34 of the VELOOP Data Charter, the following classes of data are **strictly prohibited from entering the analytical data lake**:

```mermaid
flowchart TD
    subgraph Prohibited_Zone ["Prohibited Data (Never Ingested into Analytics)"]
        P1[Raw Passwords & Salt Hashes]
        P2[JWT Secrets & Auth Private Keys]
        P3[Gateway API Keys & Webhook Secrets]
        P4[Plaintext Credit Cards / Bank Account Numbers]
        P5[Government Identity Numbers (SSN/Aadhaar/PAN)]
    end

    subgraph Masked_Restricted_Zone ["Restricted Data (Masked / Tokenized)"]
        M1[User Email -> SHA-256 Hash + Domain Rollup]
        M2[Destination Account -> Gateway Vault Token]
        M3[Device Hardware ID -> Synthetic Device Fingerprint]
        M4[IP Address -> Geo Country / State Rollup]
    end

    subgraph Analytical_Clean_Zone ["Sanitized Analytics Lake (Analyst Access)"]
        A1[Surrogate user_id]
        A2[Aggregated Financial Balances]
        A3[Behavioral Event Streams]
        A4[Task Activity & Funnels]
    end

    Prohibited_Zone x--x|Blocked by Gateway Interceptor| Masked_Restricted_Zone
    Masked_Restricted_Zone -->|Automated dbt Masking| Analytical_Clean_Zone
```

#### Detailed Isolation Rules:
1. **Authentication Secrets & Passwords:** Passwords, bcrypt hashes, and OAuth refresh secrets must reside exclusively in the isolated Auth Provider datastore. They must never be mirrored or synced to data warehouses.
2. **Payment & Banking Credentials:** VELOOP never stores raw bank account numbers, credit card CVVs, or UPI PINs. All disbursements utilize payment gateway vault tokens (e.g. `Stripe Customer ID`, `Cashfree Beneficiary ID`).
3. **Sensitive Anti-Fraud Heuristics:** Raw fraud scoring weights, internal velocity thresholds, and bot trigger rules are maintained in a restricted security microservice. The analytical layer only receives an opaque `risk_tier` (`LOW`, `MEDIUM`, `HIGH`).

---

### 4. Dynamic Column-Level Data Masking Protocol

To eliminate PII exposure while preserving full analytical utility, the following masking transformations are executed during the ingestion into the staging/silver warehouse layers:

| Raw Data Attribute | Masking / Tokenization Algorithm | Stored Analytical Representation | Analytical Value Preserved |
|---|---|---|---|
| `full_name` | Full Redaction / Synthetic Substitution | Excluded from analytical views; surrogate `user_id` used | Eliminates personal identification risk |
| `email` | SHA-256 Hashing + Domain Extraction | `email_hash: "e3b0c44..."`<br/>`email_domain: "gmail.com"` | Preserves demographic analysis (Gmail vs Yahoo) and cross-device deduplication |
| `ip_address` | Geolocation Resolution + Truncation | `geo_country: "IN"`<br/>`geo_state: "Maharashtra"` | Preserves regional segmentation without tracking exact physical coordinates |
| `payment_destination` | SHA-256 Cryptographic Hash | `destination_hash: "8f7a2b..."` | Allows detecting multi-account fraud (same payout account linked to multiple `user_id`s) |
| `device_id` / `imei` | Salted One-Way Hash | `device_fingerprint: "dev_99a8b..."` | Preserves device-sharing fraud detection without hardware serial exposure |

---

### 5. Regulatory Compliance & Data Subject Rights

1. **Right to Erasure (GDPR Art. 17 / DPDP Erasure):**
   * When a user requests account deletion, a tombstone record is flagged in `dim_users` (`account_status = 'Deleted'`).
   * PII attributes in operational databases are permanently purged within 30 days.
   * Analytical transaction ledgers retain the synthetic `user_id` and financial amounts to maintain historical accounting balance sheets without retaining personal identities.
2. **Data Retention Lifecycle:**
   * Raw Bronze telemetry JSONs: 90 days retention in cold object storage, then archived.
   * Silver event facts: 365 days retention for longitudinal trend analysis.
   * Financial ledger facts: 7 years retention to comply with tax and statutory audit laws.
