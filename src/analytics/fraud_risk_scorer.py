"""
VELOOP Rewards - Multi-Factor Withdrawal Fraud Risk Scoring & False-Positive Mitigation Engine
Part of Task 01: Product Analytics & Data Readiness Architecture

Computes composite fraud risk scores [0.0 - 1.0] across behavioral,
hardware, velocity, and geolocation signals, incorporating false-positive
dampeners, KYC trust discounts, and progressive friction handling.

Notice: SIMULATED DATA — CREATED FOR ANALYTICAL TESTING
"""

from typing import Dict, Any, Tuple, List

class FraudRiskScorer:
    """
    Weighted multi-factor heuristic risk scoring model with false-positive controls.
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

    # Whitelisted Mobile Carrier ASNs (Dynamic IP Subnet Hops are NOT Fraud)
    DOMESTIC_MOBILE_ASNS = {"AS55836", "AS45609", "AS9829", "AS24560"} # Airtel, Jio, BSNL, Vodafone Idea

    @classmethod
    def evaluate_withdrawal_risk(cls, features: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluates a withdrawal request and returns a detailed scoring breakdown,
        applying false-positive mitigations and trust discounts.
        """
        breakdown = {}

        # 1. Account Age Factor (Weight: 15%)
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
        velocity = features.get("withdrawal_count_24h", 1)
        if velocity >= 3:
            s_vel = 1.0
        elif velocity == 2:
            s_vel = 0.5
        else:
            s_vel = 0.0
        breakdown["velocity_score"] = s_vel

        # 3. Device Collision Factor (Weight: 25%)
        device_accounts = features.get("shared_device_account_count", 1)
        if device_accounts >= 3:
            s_dev = 1.0
        elif device_accounts == 2:
            s_dev = 0.6
        else:
            s_dev = 0.0
        breakdown["device_collision_score"] = s_dev

        # 4. Geolocation IP Hop Factor (Weight: 15%)
        # False Positive Mitigation: Whitelist domestic cellular dynamic IP rotation
        is_geo_hop = features.get("is_ip_country_mismatched", False)
        asn = features.get("carrier_asn", "")
        is_domestic_cellular = asn in cls.DOMESTIC_MOBILE_ASNS
        
        if is_geo_hop and not is_domestic_cellular:
            s_geo = 1.0
        elif is_geo_hop and is_domestic_cellular:
            s_geo = 0.2  # Dampened: likely mobile carrier tower handover, not international proxy
            breakdown["geo_hop_mitigation"] = "CELLULAR_DYNAMIC_IP_DAMPENED"
        else:
            s_geo = 0.0
        breakdown["geolocation_score"] = s_geo

        # 5. Clickstream Entropy / Bot Micro-Jitter (Weight: 20%)
        # Robotic timing (<8ms micro-jitter) = 1.0 risk; natural human (>15ms) = 0.0 risk
        jitter = features.get("average_tap_micro_jitter_ms", 25.0)
        if jitter < 8.0:
            s_jitter = 1.0
        elif jitter < 15.0:
            s_jitter = 0.5
        else:
            s_jitter = 0.0
        breakdown["clickstream_entropy_score"] = s_jitter

        # Base Weighted Composite Score
        composite_score = (
            cls.WEIGHTS["account_age"] * s_age +
            cls.WEIGHTS["withdrawal_velocity_24h"] * s_vel +
            cls.WEIGHTS["device_collision"] * s_dev +
            cls.WEIGHTS["ip_geolocation_hop"] * s_geo +
            cls.WEIGHTS["clickstream_entropy"] * s_jitter
        )

        # 6. Trust Discount Factors (False Positive Dampener for Legitimate Users)
        trust_discount = 0.0
        kyc_tier = features.get("kyc_tier", "TIER_0")
        if kyc_tier in ["TIER_2", "TIER_3"]:
            trust_discount += 0.10  # Aadhaar/PAN verified users get 10% risk discount
            breakdown["kyc_trust_discount"] = -0.10

        completed_tasks = features.get("lifetime_completed_tasks", 0)
        if completed_tasks > 25:
            trust_discount += 0.05  # Long-standing active contributor discount
            breakdown["tenure_trust_discount"] = -0.05

        final_score = max(0.0, min(1.0, composite_score - trust_discount))
        final_score = round(final_score, 4)

        # Decision Routing & Progressive Friction Protocol
        if final_score < cls.AUTO_APPROVE_THRESHOLD:
            decision = "AUTO_APPROVE"
            routing_queue = "GATEWAY_DISPATCH_QUEUE"
            friction_action = "NONE_IMMEDIATE_DISPATCH"
            action_desc = "Low-risk transaction cleared for automated gateway payout."
        elif final_score < cls.AUTO_REJECT_THRESHOLD:
            decision = "MANUAL_REVIEW"
            routing_queue = "COMPLIANCE_OPERATIONS_QUEUE"
            friction_action = "PROGRESSIVE_CHALLENGE_SMS_OTP"
            action_desc = "Moderate risk signals detected. Dispatched 48h escrow hold and required out-of-band SMS OTP verification."
        else:
            decision = "AUTO_REJECT"
            routing_queue = "SECURITY_LOCKOUT_QUEUE"
            friction_action = "ACCOUNT_FREEZE_WITH_APPEAL_LINK"
            action_desc = "High-confidence fraud heuristics triggered. Withdrawal blocked; automated user appeal ticket opened."

        return {
            "composite_risk_score": final_score,
            "raw_composite_score": round(composite_score, 4),
            "decision": decision,
            "routing_queue": routing_queue,
            "friction_action": friction_action,
            "action_description": action_desc,
            "factor_breakdown": breakdown,
            "is_blocked": decision == "AUTO_REJECT"
        }
