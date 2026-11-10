"""
VELOOP Rewards - PII Masking & Data Governance Module (Work Package P)
Implements GDPR Article 32 and India DPDP Act 2023 compliant pseudonymization.
"""
import hashlib
import re

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

def mask_ip_address(ip_address: str) -> str:
    """Truncates last octet of IPv4 addresses for privacy preserving geolocation."""
    if not isinstance(ip_address, str):
        return "0.0.0.0"
    parts = ip_address.split('.')
    if len(parts) == 4:
        return f"{parts[0]}.{parts[1]}.{parts[2]}.0"
    return "MASKED_IP"
