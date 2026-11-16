"""
VELOOP Rewards - PII Governance, Pseudonymization & Deep Content Scanner (Work Package P)
Technical controls aligned with GDPR (EU 2016/679) & India DPDP Act 2023 Principles.

Important Conceptual Distinction:
--------------------------------
1. PSEUDONYMIZATION (GDPR Art. 4(5) / DPDP Act Sec. 8):
   Processing of personal data such that it can no longer be attributed to a specific data subject
   without the use of additional information (the secret salt/key). Pseudonymized data (e.g. salted hashes,
   masked emails) STILL constitutes personal data under GDPR and DPDP.
2. ANONYMIZATION (GDPR Recital 26):
   Irreversible alteration that permanently removes all direct and indirect identifiers such that
   re-identification is impossible by any reasonable means. Anonymized data is exempt from data protection law.

Disclaimer:
-----------
This module implements TECHNICAL PSEUDONYMIZATION & DATA LEAKAGE CONTROLS. Full legal GDPR/DPDP compliance
additionally requires organizational governance, user consent lifecycles, Data Protection Officer (DPO)
oversight, and formal Data Protection Impact Assessments (DPIA).

Notice: SIMULATED DATA & MODEL — CREATED FOR ANALYTICAL TESTING & ARCHITECTURAL SPECIFICATION
"""

import os
import hashlib
import re
import warnings
from typing import Dict, Any, List, Tuple, Union, Optional

# Regex Patterns for Deep Content Scanning (Detecting raw unmasked PII inside cell text)
PATTERNS = {
    "EMAIL": re.compile(r'\b[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+\b'),
    "INDIAN_MOBILE": re.compile(r'(?:\+?91[\s-]?)?[6789]\d{9}\b'),
    "AADHAAR_NUMBER": re.compile(r'\b[2-9]{1}[0-9]{3}[\s-]?[0-9]{4}[\s-]?[0-9]{4}\b'),
    "INDIAN_PAN": re.compile(r'\b[A-Z]{5}[0-9]{4}[A-Z]{1}\b'),
    "CREDIT_CARD": re.compile(r'\b(?:\d{4}[-\s]?){3}\d{4}\b')
}

FORBIDDEN_COLUMN_PATTERNS = [
    r"^password", r"^pin$", r"^secret", r"^ssn$", r"^aadhaar", r"^credit_card",
    r"^cvv", r"^bank_account_number$", r"^raw_phone", r"^clear_email"
]


def get_hashing_secret() -> str:
    """
    Secure Secret Management:
    Retrieves the hashing salt from environment variables or secure key vault.
    Never relies on hardcoded production secrets in source code.
    """
    secret = os.environ.get("VELOOP_HASHING_SECRET") or os.environ.get("VELOOP_SECRET_SALT")
    if not secret:
        # Development environment fallback with an explicit security warning
        warnings.warn(
            "Security Notice: 'VELOOP_HASHING_SECRET' environment variable is not configured. "
            "Using runtime development fallback salt. Set VELOOP_HASHING_SECRET before deploying to production.",
            RuntimeWarning,
            stacklevel=2
        )
        secret = "dev_runtime_ephemeral_salt_do_not_use_in_prod"
    return secret


def hash_identifier(identifier: str, salt: Optional[str] = None) -> str:
    """
    Produces deterministic 64-char SHA-256 salted hash of a sensitive ID (e.g. user_id or device_id).
    Classified as PSEUDONYMIZATION under GDPR Article 4(5).
    """
    if not identifier:
        return "UNKNOWN_ID"
    active_salt = salt if salt is not None else get_hashing_secret()
    payload = f"{identifier}:{active_salt}".encode('utf-8')
    return hashlib.sha256(payload).hexdigest()


def mask_email_format_preserving(email: str) -> str:
    """
    Format-preserving email pseudonymization:
    Preserves first letter, last letter before '@', and domain.
    E.g.: 'ckarthikreddy190@gmail.com' -> 'c***0@gmail.com'
    """
    if not isinstance(email, str) or '@' not in email:
        return "ANONYMOUS_USER"
        
    local, domain = email.split('@', 1)
    if len(local) <= 2:
        masked_local = local[0] + "***"
    else:
        masked_local = f"{local[0]}***{local[-1]}"
        
    return f"{masked_local}@{domain}"


def mask_phone_number(phone: str) -> str:
    """
    Format-preserving phone pseudonymization:
    Preserves country code and last 3 digits, masking intermediate routing numbers.
    E.g.: '+91 9876543210' -> '+91 98*****210'
    """
    if not isinstance(phone, str) or len(phone) < 7:
        return "MASKED_PHONE"
    clean_digits = re.sub(r'[^\d+]', '', phone)
    if clean_digits.startswith('+91'):
        prefix = "+91 "
        number = clean_digits[3:]
    else:
        prefix = ""
        number = clean_digits

    if len(number) >= 7:
        masked = f"{prefix}{number[:2]}*****{number[-3:]}"
    else:
        masked = f"{prefix}***{number[-2:]}"
    return masked


def mask_ip_address(ip_address: str) -> str:
    """
    Truncates last octet of IPv4 addresses for privacy-preserving geolocation.
    Reduces geographic accuracy to city/regional subnet, preventing residential identification.
    """
    if not isinstance(ip_address, str):
        return "0.0.0.0"
    parts = ip_address.split('.')
    if len(parts) == 4:
        return f"{parts[0]}.{parts[1]}.{parts[2]}.0"
    return "MASKED_IP"


def tokenize_device_id(device_id: str, salt: Optional[str] = None) -> str:
    """Produces irreversible salted token for hardware UUID/IMEI/MAC."""
    if not device_id:
        return "DEV_UNKNOWN"
    return "DEV_TOK_" + hash_identifier(device_id, salt)[:16]


def scan_content_for_pii(records_or_data: Union[List[Dict[str, Any]], Dict[str, Any]]) -> Dict[str, Any]:
    """
    Deep Content Inspection:
    Scans the actual string contents of cell values across rows and columns to identify
    unmasked emails, phone numbers, Aadhaar numbers, PAN cards, or credit card numbers.
    Detects PII leaks even in innocuously named columns (e.g. 'notes', 'comments', 'metadata').
    """
    if isinstance(records_or_data, dict):
        records = [records_or_data]
    else:
        records = records_or_data

    violations = []
    total_cells_scanned = 0

    for row_idx, row in enumerate(records):
        for col_name, val in row.items():
            if val is None:
                continue
            val_str = str(val).strip()
            total_cells_scanned += 1

            # Check if this cell is already properly masked
            if "***" in val_str or "DEV_TOK_" in val_str or val_str.endswith(".0"):
                continue

            # Run deep regex scans
            for pii_type, regex in PATTERNS.items():
                match = regex.search(val_str)
                if match:
                    violations.append({
                        "row_index": row_idx,
                        "column_name": col_name,
                        "pii_type": pii_type,
                        "matched_snippet": match.group(0)[:4] + "..." + match.group(0)[-2:],
                        "severity": "CRITICAL_PII_LEAKAGE",
                        "recommended_action": f"Apply format-preserving masking to column '{col_name}' prior to ingestion."
                    })

    is_clean = len(violations) == 0
    return {
        "content_scan_passed": is_clean,
        "total_cells_scanned": total_cells_scanned,
        "violations_detected_count": len(violations),
        "violations": violations,
        "classification": "CONTENT_CLEAN" if is_clean else "UNMASKED_PII_FOUND"
    }


def audit_dataset_pii_compliance(
    columns_or_dataset: Union[List[str], List[Dict[str, Any]], Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Dual-layer PII Governance Audit:
    1. Audits schema column names against prohibited raw credential patterns.
    2. If record data is supplied, executes deep content-level regex scanning.
    """
    # 1. Column Name Audit
    if isinstance(columns_or_dataset, list) and columns_or_dataset and isinstance(columns_or_dataset[0], str):
        columns = columns_or_dataset
        content_audit_res = None
    elif isinstance(columns_or_dataset, list) and columns_or_dataset and isinstance(columns_or_dataset[0], dict):
        columns = list(columns_or_dataset[0].keys())
        content_audit_res = scan_content_for_pii(columns_or_dataset)
    elif isinstance(columns_or_dataset, dict):
        columns = list(columns_or_dataset.keys())
        content_audit_res = scan_content_for_pii([columns_or_dataset])
    else:
        columns = []
        content_audit_res = None

    schema_violations = []
    for col in columns:
        for pat in FORBIDDEN_COLUMN_PATTERNS:
            if re.search(pat, col.lower()):
                schema_violations.append({
                    "column": col,
                    "policy_violation": "RAW_CONFIDENTIAL_PII_COLUMN_EXPOSED",
                    "severity": "HIGH"
                })

    is_schema_compliant = len(schema_violations) == 0
    is_content_compliant = content_audit_res["content_scan_passed"] if content_audit_res else True

    overall_passed = is_schema_compliant and is_content_compliant

    return {
        "technical_privacy_controls_verified": overall_passed,
        "schema_audit_passed": is_schema_compliant,
        "content_audit_passed": is_content_compliant,
        "total_columns_audited": len(columns),
        "schema_violations": schema_violations,
        "content_audit_details": content_audit_res,
        "compliance_rating": "PASS_GRADE_A" if overall_passed else "FAIL_GRADE_F",
        "governance_classification": "PSEUDONYMIZED_TELEMETRY" if overall_passed else "NON_COMPLIANT_PII_EXPOSED",
        "disclaimer": "Technical audit verifies automated pseudonymization & leak detection. Full legal compliance requires formal DPIA & DPO sign-off."
    }
