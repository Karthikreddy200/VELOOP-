"""
VELOOP Rewards - Multi-Factor Withdrawal Fraud Risk Scoring Engine
Part of Task 01: Product Analytics & Data Readiness Architecture

Computes composite fraud risk scores [0.0 - 1.0] across behavioral,
hardware, velocity, and geolocation signals to determine automated
withdrawal routing: AUTO_APPROVE, MANUAL_REVIEW, or AUTO_REJECT.

Notice: SIMULATED DATA — CREATED FOR ANALYTICAL TESTING
"""

from typing import Dict, Any, Tuple

class FraudRiskScorer:
    """
    Weighted multi-factor heuristic risk scoring model for monetary cashouts.
    """
    WEIGHTS = {
        "account_age": 0.15,
        "withdrawal_velocity_24h": 0.25,
        "device_collision": 0.25,
        "ip_geolocation_hop": 0.15,
        "clickstream_entropy": 0.20
    }

    # Decision Boundaries
    AUTO_APPROVE_THRESHOLD = 0.30
    AUTO_REJECT_THRESHOLD = 0.70

    @classmethod
    def evaluate_withdrawal_risk(cls, features: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluates a withdrawal request and returns a detailed scoring breakdown.
        
        Expected features:
          - account_age_days (float/int)
          - withdrawal_count_24h (int)
          - shared_device_account_count (int)
          - is_ip_country_mismatched (bool)
          - average_tap_micro_jitter_ms (float)
          - task_completion_time_std_dev (float)
        """
        breakdown = {}

        # 1. Account Age Factor (Weight: 15%)
        # Accounts < 3 days = 1.0 risk; 3-7 days = 0.6 risk; 7-30 days = 0.2 risk; >30 days = 0.0 risk
        age_days = features.get("account_age_days", 0)
        if age_days < 3:
            s_age = 1.0
        elif age_days < 7:
            s_age = 0.6
        elif age_days < 30:
            s_age = 0.2
        else:
            s_age = 0.0
        breakdown["account_age_score"] = s_age

        # 2. Withdrawal Velocity 24h Factor (Weight: 25%)
        # > 3 attempts in 24h = 1.0; 2 attempts = 0.5; 1 attempt = 0.0
        velocity = features.get("withdrawal_count_24h", 1)
        if velocity >= 3:
            s_vel = 1.0
        elif velocity == 2:
            s_vel = 0.5
        else:
            s_vel = 0.0
        breakdown["velocity_score"] = s_vel

        # 3. Device Collision Factor (Weight: 25%)
        # Multiple accounts on same device hash: >2 = 1.0; 2 = 0.6; 1 (unique) = 0.0
        device_accounts = features.get("shared_device_account_count", 1)
        if device_accounts >= 3:
            s_dev = 1.0
        elif device_accounts == 2:
            s_dev = 0.6
        else:
            s_dev = 0.0
        breakdown["device_collision_score"] = s_dev

        # 4. Geolocation IP Hop Factor (Weight: 15%)
        is_geo_hop = features.get("is_ip_country_mismatched", False)
        s_geo = 1.0 if is_geo_hop else 0.0
        breakdown["geolocation_score"] = s_geo

        # 5. Clickstream Entropy / Bot Micro-Jitter (Weight: 20%)
        # Robotic timing (<8ms micro-jitter) = 1.0 risk; natural human (>20ms) = 0.0 risk
        jitter = features.get("average_tap_micro_jitter_ms", 25.0)
        if jitter < 8.0:
            s_jitter = 1.0
        elif jitter < 15.0:
            s_jitter = 0.5
        else:
            s_jitter = 0.0
        breakdown["clickstream_entropy_score"] = s_jitter

        # Calculate Composite Weighted Score
        composite_score = (
            cls.WEIGHTS["account_age"] * s_age +
            cls.WEIGHTS["withdrawal_velocity_24h"] * s_vel +
            cls.WEIGHTS["device_collision"] * s_dev +
            cls.WEIGHTS["ip_geolocation_hop"] * s_geo +
            cls.WEIGHTS["clickstream_entropy"] * s_jitter
        )
        composite_score = round(composite_score, 4)

        # Decision Routing
        if composite_score < cls.AUTO_APPROVE_THRESHOLD:
            decision = "AUTO_APPROVE"
            routing_queue = "GATEWAY_DISPATCH_QUEUE"
            action_desc = "Low-risk transaction cleared for automated gateway payout."
        elif composite_score < cls.AUTO_REJECT_THRESHOLD:
            decision = "MANUAL_REVIEW"
            routing_queue = "COMPLIANCE_OPERATIONS_QUEUE"
            action_desc = "Moderate risk signals detected. Forwarded to risk analyst for manual verification."
        else:
            decision = "AUTO_REJECT"
            routing_queue = "SECURITY_LOCKOUT_QUEUE"
            action_desc = "High-confidence fraud heuristics triggered. Withdrawal blocked and account flagged."

        return {
            "composite_risk_score": composite_score,
            "decision": decision,
            "routing_queue": routing_queue,
            "action_description": action_desc,
            "factor_breakdown": breakdown,
            "is_blocked": decision == "AUTO_REJECT"
        }
