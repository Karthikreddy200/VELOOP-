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
from src.analytics.referral_attribution import (
    calculate_k_factor,
    compute_referral_conversion_funnel,
    detect_referral_sybil_fraud
)
from src.governance.pii_masking import (
    hash_identifier,
    mask_email_format_preserving,
    mask_phone_number,
    mask_ip_address,
    tokenize_device_id,
    audit_dataset_pii_compliance
)
from src.ingestion.event_streaming_engine import (
    EventSchemaValidator,
    EventStreamBuffer,
    generate_sample_telemetry_event
)
from src.analytics.fraud_risk_scorer import FraudRiskScorer
from src.analytics.persistent_ledger import (
    record_persistent_transaction,
    fetch_persisted_ledger,
    compute_persisted_account_balances
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
    # WORK PACKAGE E: REFERRAL & VIRAL GROWTH TESTS
    # ==========================================
    def test_referral_k_factor_calculation(self):
        # 100 users, 250 invites sent, 80 converted -> i = 2.5, c = 0.32 -> K = 0.8
        res = calculate_k_factor(total_active_users=100, total_invites_sent=250, converted_referees=80)
        self.assertEqual(res['invites_per_user'], 2.5)
        self.assertEqual(res['conversion_rate_pct'], 32.0)
        self.assertEqual(res['k_factor'], 0.8)
        self.assertEqual(res['viral_status'], "HEALTHY_ORGANIC_AMPLIFICATION")

    def test_referral_funnel_stages(self):
        funnel = compute_referral_conversion_funnel(cohort_size=119)
        self.assertEqual(len(funnel), 4)
        self.assertEqual(funnel[0]['stage'], "1. Invites Sent")
        self.assertEqual(funnel[1]['count'], 119)
        self.assertEqual(funnel[3]['conversion_pct'], 16.8)

    def test_referral_sybil_fraud_detection(self):
        # 1. Device collision
        is_fraud, msg = detect_referral_sybil_fraud(
            referrer_device_id="DEV_IMEI_12345",
            referee_device_id="DEV_IMEI_12345",
            referrer_ip="103.21.4.10",
            referee_ip="103.21.4.15"
        )
        self.assertTrue(is_fraud)
        self.assertTrue("FRAUD_HARDWARE_COLLISION" in msg)

        # 2. Clean referral
        is_fraud, msg = detect_referral_sybil_fraud(
            referrer_device_id="DEV_IMEI_11111",
            referee_device_id="DEV_IMEI_22222",
            referrer_ip="103.21.4.10",
            referee_ip="49.36.12.50"
        )
        self.assertFalse(is_fraud)
        self.assertEqual(msg, "CLEAN_REFERRAL_VERIFIED")

    # ==========================================
    # DATA LAKE IMMUTABILITY TEST
    # ==========================================
    def test_raw_data_preservation(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        data_path = os.path.join(base_dir, "data", "VELoop_Rewards_Data_01.xlsx")
        self.assertTrue(os.path.exists(data_path), "Raw data source file must be preserved in data/ directory")
        self.assertGreater(os.path.getsize(data_path), 1000, "Raw data file must remain intact and non-empty")

    # ==========================================
    # REAL-TIME EVENT STREAMING & INGESTION TESTS
    # ==========================================
    def test_streaming_valid_event_ingestion(self):
        buffer = EventStreamBuffer(batch_size=10)
        event = generate_sample_telemetry_event(
            user_id="USR-9901",
            event_name="ad_watch_completed",
            payload={"reward_xp": 50, "duration_seconds": 29.0}
        )
        success, msg = buffer.ingest(event)
        self.assertTrue(success)
        self.assertEqual(msg, "INGESTED_SUCCESS")
        self.assertEqual(buffer.ingested_count, 1)

    def test_streaming_schema_rejection_invalid_event_name(self):
        buffer = EventStreamBuffer(batch_size=10)
        event = generate_sample_telemetry_event(user_id="USR-9901", event_name="invalid_custom_event_action")
        success, msg = buffer.ingest(event)
        self.assertFalse(success)
        self.assertTrue("SCHEMA_REJECTED" in msg)
        self.assertEqual(len(buffer.dead_letter_queue), 1)

    def test_streaming_idempotency_deduplication(self):
        buffer = EventStreamBuffer(batch_size=10)
        event = generate_sample_telemetry_event(user_id="USR-9901", event_name="daily_streak_incremented")
        success1, _ = buffer.ingest(event)
        success2, msg2 = buffer.ingest(event)  # Identical idempotency key
        self.assertTrue(success1)
        self.assertFalse(success2)
        self.assertEqual(msg2, "DUPLICATE_IDEMPOTENCY_KEY_REJECTED")

    def test_streaming_future_timestamp_drift_rejection(self):
        from datetime import datetime, timezone, timedelta
        buffer = EventStreamBuffer(batch_size=10)
        future_ts = (datetime.now(timezone.utc) + timedelta(minutes=15)).isoformat()
        event = generate_sample_telemetry_event(user_id="USR-9901", event_name="spin_wheel_initiated")
        event["event_timestamp"] = future_ts
        success, msg = buffer.ingest(event)
        self.assertFalse(success)
        self.assertTrue("Future drift" in msg)

    # ==========================================
    # MULTI-FACTOR FRAUD RISK SCORING TESTS
    # ==========================================
    def test_fraud_risk_scorer_auto_approve(self):
        features = {
            "account_age_days": 45,
            "withdrawal_count_24h": 1,
            "shared_device_account_count": 1,
            "is_ip_country_mismatched": False,
            "average_tap_micro_jitter_ms": 28.5
        }
        res = FraudRiskScorer.evaluate_withdrawal_risk(features)
        self.assertEqual(res["decision"], "AUTO_APPROVE")
        self.assertLess(res["composite_risk_score"], 0.30)
        self.assertFalse(res["is_blocked"])

    def test_fraud_risk_scorer_manual_review(self):
        features = {
            "account_age_days": 5,                 # Moderate risk (0.6) -> 0.09
            "withdrawal_count_24h": 2,             # Moderate velocity (0.5) -> 0.125
            "shared_device_account_count": 1,      # Unique device (0.0) -> 0.0
            "is_ip_country_mismatched": False,
            "average_tap_micro_jitter_ms": 12.0    # Borderline jitter (0.5) -> 0.10
        }                                          # Total score = 0.315 (between 0.30 and 0.70)
        res = FraudRiskScorer.evaluate_withdrawal_risk(features)
        self.assertEqual(res["decision"], "MANUAL_REVIEW")
        self.assertGreaterEqual(res["composite_risk_score"], 0.30)
        self.assertLess(res["composite_risk_score"], 0.70)
        self.assertEqual(res["routing_queue"], "COMPLIANCE_OPERATIONS_QUEUE")

    def test_fraud_risk_scorer_auto_reject(self):
        features = {
            "account_age_days": 1,                 # High risk (1.0)
            "withdrawal_count_24h": 4,             # High velocity (1.0)
            "shared_device_account_count": 5,      # Multi-account farm (1.0)
            "is_ip_country_mismatched": True,      # Geo hop (1.0)
            "average_tap_micro_jitter_ms": 1.2     # Autoclicker bot (1.0)
        }
        res = FraudRiskScorer.evaluate_withdrawal_risk(features)
        self.assertEqual(res["decision"], "AUTO_REJECT")
        self.assertGreaterEqual(res["composite_risk_score"], 0.70)
        self.assertTrue(res["is_blocked"])
        self.assertEqual(res["routing_queue"], "SECURITY_LOCKOUT_QUEUE")

    # ==========================================
    # PERSISTENT FINANCIAL LEDGER & PII GOVERNANCE TESTS
    # ==========================================
    def test_persistent_ledger_commit_and_fetch(self):
        tx_id = "tx_test_persist_001"
        success = record_persistent_transaction(
            transaction_id=tx_id,
            user_id="USR-8801",
            event_type="REWARD_EARNED",
            direction="CREDIT",
            currency_unit="XP",
            gross_amount=100.0,
            equivalent_usd=1.00,
            running_balance_after=250.0,
            debit_account="1010_CASH_AND_AD_RECEIVABLES",
            credit_account="2010_USER_WALLET_LIABILITY",
            variance=0.0000
        )
        self.assertTrue(success)
        records = fetch_persisted_ledger(limit=10)
        found = any(r["transaction_id"] == tx_id for r in records)
        self.assertTrue(found, "Persisted transaction must exist in SQLite database")

    def test_persistent_ledger_reconciliation_zero_variance(self):
        stats = compute_persisted_account_balances()
        self.assertIn("is_balanced", stats)
        self.assertTrue(stats["is_balanced"], "Double-entry cumulative variance must be 0.0000 USD")
        self.assertEqual(stats["cumulative_variance_usd"], 0.0)

    def test_pii_phone_masking(self):
        masked1 = mask_phone_number("+91 9876543210")
        self.assertTrue(masked1.startswith("+91 98*****"))
        self.assertTrue(masked1.endswith("210"))
        
        token = tokenize_device_id("IMEI_864209048123456")
        self.assertTrue(token.startswith("DEV_TOK_"))
        self.assertEqual(len(token), 24)

    def test_pii_dataset_compliance_audit(self):
        # 1. Clean analytical columns
        clean_cols = ["user_id", "masked_email", "masked_phone", "account_status", "xp_balance"]
        res = audit_dataset_pii_compliance(clean_cols)
        self.assertTrue(res["is_gdpr_dpdp_compliant"])
        self.assertEqual(res["compliance_rating"], "PASS_GRADE_A")

        # 2. Leaked raw confidential columns
        dirty_cols = ["user_id", "raw_phone", "password", "aadhaar"]
        res_dirty = audit_dataset_pii_compliance(dirty_cols)
        self.assertFalse(res_dirty["is_gdpr_dpdp_compliant"])
        self.assertEqual(res_dirty["compliance_rating"], "FAIL_GRADE_F")
        self.assertEqual(len(res_dirty["violations_detected"]), 3)


if __name__ == '__main__':
    unittest.main()
