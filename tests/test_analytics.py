import unittest
import hashlib
import re
import os

def classify_lifecycle(account_status, is_active_7d, is_active_30d, days_since_registration):
    if account_status in ['Suspended', 'Banned']:
        return 'Suspended'
    if is_active_7d in ['Yes', 1]:
        return 'Highly Active (7D)'
    elif is_active_30d in ['Yes', 1]:
        return 'Moderately Active (30D)'
    elif days_since_registration > 60:
        return 'Churned (>60D)'
    else:
        return 'Dormant (At Risk)'

def mask_email(email):
    if not isinstance(email, str) or '@' not in email:
        return "UNKNOWN_USER"
    user, domain = email.split('@', 1)
    if len(user) <= 2:
        masked_user = user[0] + "***"
    else:
        masked_user = user[0] + "***" + user[-1]
    return f"{masked_user}@{domain}"

def salted_hash_id(identifier, salt="veloop_salt_2026"):
    return hashlib.sha256(f"{identifier}:{salt}".encode('utf-8')).hexdigest()

def validate_withdrawal(user_status, available_usd, requested_usd, min_threshold=5.0, fee_pct=0.02):
    if user_status in ['Suspended', 'Banned']:
        return False, "ERR_ACCOUNT_SUSPENDED", 0.0, 0.0
    if requested_usd < min_threshold:
        return False, "ERR_BELOW_MIN_THRESHOLD", 0.0, 0.0
    if requested_usd > available_usd:
        return False, "ERR_INSUFFICIENT_FUNDS", 0.0, 0.0
    
    fee = round(requested_usd * fee_pct, 2)
    net_payout = round(requested_usd - fee, 2)
    return True, "SUCCESS", fee, net_payout


class TestVELOOPAnalyticsEngine(unittest.TestCase):

    def test_lifecycle_highly_active(self):
        state = classify_lifecycle('Active', 1, 1, 10)
        self.assertEqual(state, 'Highly Active (7D)')

    def test_lifecycle_moderately_active(self):
        state = classify_lifecycle('Active', 0, 1, 20)
        self.assertEqual(state, 'Moderately Active (30D)')

    def test_lifecycle_dormant_at_risk(self):
        state = classify_lifecycle('Active', 0, 0, 45)
        self.assertEqual(state, 'Dormant (At Risk)')

    def test_lifecycle_churned(self):
        state = classify_lifecycle('Active', 0, 0, 75)
        self.assertEqual(state, 'Churned (>60D)')

    def test_lifecycle_suspended_precedence(self):
        state = classify_lifecycle('Suspended', 1, 1, 5)
        self.assertEqual(state, 'Suspended')

    def test_pii_email_masking(self):
        masked = mask_email("ckarthikreddy190@gmail.com")
        self.assertEqual(masked, "c***0@gmail.com")
        self.assertTrue(masked.endswith("@gmail.com"))

    def test_pii_salted_hash_determinism(self):
        h1 = salted_hash_id("USR_001")
        h2 = salted_hash_id("USR_001")
        self.assertEqual(h1, h2)
        self.assertEqual(len(h1), 64)

    def test_withdrawal_valid_transaction(self):
        valid, status, fee, net = validate_withdrawal('Active', 25.0, 10.0)
        self.assertTrue(valid)
        self.assertEqual(status, "SUCCESS")
        self.assertEqual(fee, 0.20)
        self.assertEqual(net, 9.80)
        self.assertAlmostEqual(fee + net, 10.0, places=4)

    def test_withdrawal_guards_and_thresholds(self):
        # 1. Suspended account
        v, s, _, _ = validate_withdrawal('Suspended', 50.0, 10.0)
        self.assertFalse(v)
        self.assertEqual(s, "ERR_ACCOUNT_SUSPENDED")

        # 2. Below minimum threshold ($5.00)
        v, s, _, _ = validate_withdrawal('Active', 50.0, 3.0)
        self.assertFalse(v)
        self.assertEqual(s, "ERR_BELOW_MIN_THRESHOLD")

        # 3. Insufficient balance
        v, s, _, _ = validate_withdrawal('Active', 10.0, 20.0)
        self.assertFalse(v)
        self.assertEqual(s, "ERR_INSUFFICIENT_FUNDS")

    def test_raw_data_preservation(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        data_path = os.path.join(base_dir, "data", "VELoop_Rewards_Data_01.xlsx")
        self.assertTrue(os.path.exists(data_path), "Raw data source file must be preserved in data/ directory")
        self.assertGreater(os.path.getsize(data_path), 1000, "Raw data file must remain intact and non-empty")


if __name__ == '__main__':
    unittest.main()
