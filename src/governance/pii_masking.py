"""
VELOOP Rewards - PII Masking & Data Governance Module (Work Package P)
Implements GDPR Article 32 and India DPDP Act 2023 compliant pseudonymization,
salted SHA-256 tokenization, subnet truncation, and compliance auditing.
"""
import hashlib
import re
from typing import Dict, Any, List, Tuple

DEFAULT_SALT = "veloop_sec_token_salt_2026"

def hash_identifier(identifier: str, salt: str = DEFAULT_SALT) -> str:
    """Produces deterministic 64-char SHA-256 salted hash of a sensitive ID."""
    if not identifier:
        return "UNKNOWN_ID"
    payload = f"{identifier}:{salt}".encode('utf-8')
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
    Preserves country code and last 3 digits, masking middle 5 digits.
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
    """Truncates last octet of IPv4 addresses for privacy preserving geolocation."""
    if not isinstance(ip_address, str):
        return "0.0.0.0"
    parts = ip_address.split('.')
    if len(parts) == 4:
        return f"{parts[0]}.{parts[1]}.{parts[2]}.0"
    return "MASKED_IP"

def tokenize_device_id(device_id: str, salt: str = DEFAULT_SALT) -> str:
    """Produces irreversible salted token for hardware UUID/IMEI/MAC."""
    if not device_id:
        return "DEV_UNKNOWN"
    return "DEV_TOK_" + hash_identifier(device_id, salt)[:16]

def audit_dataset_pii_compliance(columns: List[str]) -> Dict[str, Any]:
    """
    Audits a list of dataframe columns against GDPR / DPDP forbidden raw fields.
    Returns compliance score and violations.
    """
    forbidden_patterns = [
        r"^password", r"^pin$", r"^secret", r"^ssn$", r"^aadhaar", r"^credit_card",
        r"^cvv", r"^bank_account_number$", r"^raw_phone", r"^clear_email"
    ]
    violations = []
    for col in columns:
        for pat in forbidden_patterns:
            if re.search(pat, col.lower()):
                violations.append({"column": col, "policy_violation": "RAW_CONFIDENTIAL_PII_EXPOSED"})

    is_compliant = len(violations) == 0
    return {
        "is_gdpr_dpdp_compliant": is_compliant,
        "total_columns_audited": len(columns),
        "violations_detected": violations,
        "compliance_rating": "PASS_GRADE_A" if is_compliant else "FAIL_GRADE_F"
    }
