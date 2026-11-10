import unittest
import hashlib
import os
import sys

# Add src to python path for modular import
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.analytics.user_lifecycle_fsm import classify_lifecycle_state, transition_state
from src.analytics.reward_economy_engine import (
    validate_ad_watch_event,
    detect_tap_bot,
    validate_earning_velocity,
    calculate_token_economy_health
)
from src.governance.pii_masking import (
    hash_identifier,
    mask_email_format_preserving,
    mask_ip_address
)

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

    # ==========================================
    # WORK PACKAGE B: USER LIFECYCLE FSM TESTS
    # ==========================================
    def test_lifecycle_engaged(self):
        state = classify_lifecycle_state('Active', days_since_reg=10, days_since_last_active=2, completed_task_count=8)
        self.assertEqual(state, 'ENGAGED')

    def test_lifecycle_activated(self):
        state = classify_lifecycle_state('Active', days_since_reg=5, days_since_last_active=1, completed_task_count=2)
        self.assertEqual(state, 'ACTIVATED')

    def test_lifecycle_dormant_at_risk(self):
        state = classify_lifecycle_state('Active', days_since_reg=25, days_since_last_active=18, completed_task_count=3)
        self.assertEqual(state, 'DORMANT')

    def test_lifecycle_churned(self):
        state = classify_lifecycle_state('Active', days_since_reg=90, days_since_last_active=45, completed_task_count=1)
        self.assertEqual(state, 'CHURNED')

    def test_lifecycle_suspended_precedence(self):
        state = classify_lifecycle_state('Suspended', days_since_reg=5, days_since_last_active=1, completed_task_count=10)
        self.assertEqual(state, 'SUSPENDED')

    def test_fsm_valid_and_illegal_transitions(self):
        # Legal transition: ONBOARDED -> ACTIVATED
        valid, msg = transition_state('ONBOARDED', 'ACTIVATED')
        self.assertTrue(valid)
        self.assertEqual(msg, "SUCCESS")

        # Illegal leap: UNREGISTERED -> ENGAGED (prohibited)
        valid, msg = transition_state('UNREGISTERED', 'ENGAGED')
        self.assertFalse(valid)
        self.assertTrue("ERR_ILLEGAL_TRANSITION" in msg)

    # ==========================================
    # WORK PACKAGE P: PII GOVERNANCE TESTS
    # ==========================================
    def test_pii_email_masking(self):
        masked = mask_email_format_preserving("ckarthikreddy190@gmail.com")
        self.assertEqual(masked, "c***0@gmail.com")
        self.assertTrue(masked.endswith("@gmail.com"))

    def test_pii_salted_hash_determinism(self):
        h1 = hash_identifier("USR_001")
        h2 = hash_identifier("USR_001")
        self.assertEqual(h1, h2)
        self.assertEqual(len(h1), 64)

    def test_pii_ip_masking(self):
        ip = mask_ip_address("192.168.1.155")
        self.assertEqual(ip, "192.168.1.0")

    # ==========================================
    # WORK PACKAGE D: WALLET & WITHDRAWAL TESTS
    # ==========================================
    def test_withdrawal_valid_transaction(self):
        valid, status, fee, net = validate_withdrawal('Active', 25.0, 10.0)
        self.assertTrue(valid)
        self.assertEqual(status, "SUCCESS")
        self.assertEqual(fee, 0.20)
        self.assertEqual(net, 9.80)
        self.assertAlmostEqual(fee + net, 10.0, places=4)

    def test_withdrawal_guards_and_thresholds(self):
        # 1. Suspended account guard
        v, s, _, _ = validate_withdrawal('Suspended', 50.0, 10.0)
        self.assertFalse(v)
        self.assertEqual(s, "ERR_ACCOUNT_SUSPENDED")

        # 2. Below minimum threshold ($5.00)
        v, s, _, _ = validate_withdrawal('Active', 50.0, 3.0)
        self.assertFalse(v)
        self.assertEqual(s, "ERR_BELOW_MIN_THRESHOLD")

        # 3. Insufficient balance guard
        v, s, _, _ = validate_withdrawal('Active', 10.0, 20.0)
        self.assertFalse(v)
        self.assertEqual(s, "ERR_INSUFFICIENT_FUNDS")

    # ==========================================
    # WORK PACKAGE C: REWARD ECONOMY & BOT TESTS
    # ==========================================
    def test_ad_watch_velocity_cap(self):
        # User within daily limit (<20)
        valid, msg, xp = validate_ad_watch_event(user_daily_ad_count=5, ad_duration_sec=30.0)
        self.assertTrue(valid)
        self.assertEqual(xp, 50)

        # User at or above cap (>=20)
        valid, msg, xp = validate_ad_watch_event(user_daily_ad_count=20, ad_duration_sec=30.0)
        self.assertFalse(valid)
        self.assertEqual(msg, "ERR_DAILY_AD_CAP_EXCEEDED")

        # Incomplete view (<28s)
        valid, msg, xp = validate_ad_watch_event(user_daily_ad_count=2, ad_duration_sec=15.0)
        self.assertFalse(valid)
        self.assertEqual(msg, "ERR_INSUFFICIENT_AD_DURATION")

    def test_tap_bot_detection(self):
        # Human taps: ~4 taps/sec with natural human micro-jitter variance
        human_timestamps = [0.0, 0.26, 0.51, 0.79, 1.05, 1.33, 1.60]
        is_bot, reason = detect_tap_bot(human_timestamps)
        self.assertFalse(is_bot)
        self.assertEqual(reason, "HUMAN_VERIFIED")

        # Superhuman autoclicker: 50 taps/sec (interval = 0.02s)
        bot_fast_timestamps = [i * 0.02 for i in range(10)]
        is_bot, reason = detect_tap_bot(bot_fast_timestamps)
        self.assertTrue(is_bot)
        self.assertEqual(reason, "BOT_DETECTED_SUPERHUMAN_SPEED")

        # Robot clicker with mechanical zero variance: exactly 0.12s every tap
        bot_robotic_timestamps = [i * 0.12 for i in range(10)]
        is_bot, reason = detect_tap_bot(bot_robotic_timestamps)
        self.assertTrue(is_bot)
        self.assertEqual(reason, "BOT_DETECTED_MECHANICAL_INTERVALS")

    def test_earning_hourly_velocity_cap(self):
        # Under limit: 600 + 100 = 700 <= 1000
        valid, msg = validate_earning_velocity(recent_hourly_xp=600, proposed_reward_xp=100)
        self.assertTrue(valid)

        # Exceeds limit: 950 + 200 = 1150 > 1000
        valid, msg = validate_earning_velocity(recent_hourly_xp=950, proposed_reward_xp=200)
        self.assertFalse(valid)
        self.assertTrue("ERR_HOURLY_VELOCITY_CAP" in msg)

    def test_token_economy_health_metrics(self):
        # Healthy circulation: 10,000 minted, 7,500 burned (75% burn ratio), $50 reserve against $25 liability
        health = calculate_token_economy_health(
            total_xp_minted=10000,
            total_xp_burned_or_withdrawn=7500,
            cash_reserve_usd=50.0
        )
        self.assertEqual(health['burn_to_mint_ratio'], 0.75)
        self.assertEqual(health['outstanding_liability_usd'], 25.0)
        self.assertEqual(health['liquidity_coverage_ratio'], 2.0)
        self.assertTrue(health['is_reserve_adequate'])
        self.assertEqual(health['economy_status'], "HEALTHY_CIRCULATION")

    # ==========================================
    # DATA LAKE IMMUTABILITY TEST
    # ==========================================
    def test_raw_data_preservation(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        data_path = os.path.join(base_dir, "data", "VELoop_Rewards_Data_01.xlsx")
        self.assertTrue(os.path.exists(data_path), "Raw data source file must be preserved in data/ directory")
        self.assertGreater(os.path.getsize(data_path), 1000, "Raw data file must remain intact and non-empty")


if __name__ == '__main__':
    unittest.main()
