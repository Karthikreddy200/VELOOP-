"""
VELOOP Rewards - Multi-Factor Fraud Risk Engine, Benchmark Validation & Appeal Workflow (Work Package C & D)
Implements:
1. Multi-factor weighted heuristic scoring with domestic mobile carrier ASN dampening.
2. Progressive friction protocol (Challenge / Escalation Hold instead of unilateral account bans).
3. Realistic test benchmarking measuring False-Positive Rate (FPR) and False-Negative Rate (FNR).
4. Formal manual review and appeal workflow tracking.

Notice: SIMULATED DATA & MODEL — CREATED FOR ANALYTICAL TESTING & ARCHITECTURAL SPECIFICATION
"""

from typing import Dict, Any, Tuple, List, Optional
from datetime import datetime, timezone
import uuid

class FraudAppealManager:
    """
    Manages manual compliance reviews and appeals for flagged withdrawal transactions.
    Ensures legitimate users are not permanently frozen without human recourse.
    """
    _appeals_db: Dict[str, Dict[str, Any]] = {}

    @classmethod
    def create_appeal_ticket(
        cls,
        user_id: str,
        transaction_id: str,
        risk_score: float,
        flag_reason: str,
        user_explanation: str = "Automated appeal submission for flagged transaction."
    ) -> Dict[str, Any]:
        """Opens a formal appeal ticket for a held transaction."""
        ticket_id = f"APL-{uuid.uuid4().hex[:8].upper()}"
        now = datetime.now(timezone.utc).isoformat()
        ticket = {
            "ticket_id": ticket_id,
            "user_id": user_id,
            "transaction_id": transaction_id,
            "risk_score": risk_score,
            "flag_reason": flag_reason,
            "user_explanation": user_explanation,
            "status": "PENDING_MANUAL_REVIEW", # PENDING_MANUAL_REVIEW, OVERRULED_APPROVED, UPHELD_REJECTED
            "reviewer_id": None,
            "reviewer_notes": None,
            "created_at": now,
            "updated_at": now
        }
        cls._appeals_db[ticket_id] = ticket
        return ticket

    @classmethod
    def review_appeal_ticket(
        cls,
        ticket_id: str,
        reviewer_id: str,
        decision: str, # "OVERRULE_APPROVE" or "UPHOLD_REJECT"
        reviewer_notes: str
    ) -> Dict[str, Any]:
        """Processes an appeal decision with full audit tracking."""
        if ticket_id not in cls._appeals_db:
            raise KeyError(f"Appeal ticket '{ticket_id}' not found.")
        
        ticket = cls._appeals_db[ticket_id]
        if decision == "OVERRULE_APPROVE":
            ticket["status"] = "OVERRULED_APPROVED"
        elif decision == "UPHOLD_REJECT":
            ticket["status"] = "UPHELD_REJECTED"
        else:
            raise ValueError(f"Invalid decision '{decision}'. Must be 'OVERRULE_APPROVE' or 'UPHOLD_REJECT'.")

        ticket["reviewer_id"] = reviewer_id
        ticket["reviewer_notes"] = reviewer_notes
        ticket["updated_at"] = datetime.now(timezone.utc).isoformat()
        return ticket

    @classmethod
    def get_ticket(cls, ticket_id: str) -> Optional[Dict[str, Any]]:
        return cls._appeals_db.get(ticket_id)

    @classmethod
    def reset(cls):
        """Clears appeal tickets for test isolation."""
        cls._appeals_db.clear()


class FraudRiskScorer:
    """
    Weighted multi-factor heuristic risk scoring model with false-positive controls
    and progressive friction escalation.
    """
    WEIGHTS = {
        "account_age": 0.15,
        "withdrawal_velocity_24h": 0.25,
        "device_collision": 0.25,
        "ip_geolocation_hop": 0.15,
        "clickstream_entropy": 0.20
    }

    # Calibrated Decision Boundaries
    AUTO_APPROVE_THRESHOLD = 0.30
    MANUAL_REVIEW_THRESHOLD = 0.70

    # Whitelisted Mobile Carrier ASNs (Dynamic IP Subnet Hops are NOT Fraud)
    DOMESTIC_MOBILE_ASNS = {"AS55836", "AS45609", "AS9829", "AS24560"} # Airtel, Jio, BSNL, Vodafone Idea

    @classmethod
    def evaluate_withdrawal_risk(cls, features: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluates a withdrawal request and returns a detailed scoring breakdown,
        applying false-positive mitigations and progressive friction handling.
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
        if velocity >= 4:
            s_vel = 1.0
        elif velocity >= 2:
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

        # Progressive Friction Protocol (Never freeze users automatically on unverified heuristics)
        if final_score < cls.AUTO_APPROVE_THRESHOLD:
            decision = "AUTO_APPROVE"
            routing_queue = "GATEWAY_DISPATCH_QUEUE"
            friction_action = "NONE_IMMEDIATE_DISPATCH"
            action_desc = "Low-risk transaction cleared for automated gateway payout."
            is_blocked = False
        elif final_score < cls.MANUAL_REVIEW_THRESHOLD:
            decision = "STEP_UP_CHALLENGE"
            routing_queue = "COMPLIANCE_OPERATIONS_QUEUE"
            friction_action = "PROGRESSIVE_CHALLENGE_SMS_OTP"
            action_desc = "Moderate risk signals detected. Dispatched 48h escrow hold and required out-of-band SMS OTP verification."
            is_blocked = True
        else:
            decision = "SECURITY_ESCALATION_HOLD"
            routing_queue = "FRAUD_ESCALATION_REVIEW_QUEUE"
            friction_action = "ESCROW_PAUSE_WITH_APPEAL_TICKET"
            action_desc = "Elevated risk signals detected. Payout paused in escrow for analyst compliance review (not an account ban). In-app appeal ticket generated."
            is_blocked = True

        return {
            "composite_risk_score": final_score,
            "decision": decision,
            "routing_queue": routing_queue,
            "friction_action": friction_action,
            "action_description": action_desc,
            "is_blocked": is_blocked,
            "scoring_breakdown": breakdown
        }

    @classmethod
    def evaluate_model_performance(
        cls,
        benchmark_dataset: List[Dict[str, Any]],
        threshold: float = 0.50
    ) -> Dict[str, Any]:
        """
        Evaluates the fraud scoring engine against an empirical ground-truth benchmark dataset.
        Computes Confusion Matrix, Precision, Recall, False Positive Rate (FPR),
        and False Negative Rate (FNR).
        """
        tp = 0 # Fraud correctly flagged
        fp = 0 # Legitimate incorrectly flagged (False Positive)
        tn = 0 # Legitimate correctly approved
        fn = 0 # Fraud missed (False Negative)

        for case in benchmark_dataset:
            ground_truth_is_fraud = case["is_fraud"]
            eval_res = cls.evaluate_withdrawal_risk(case["features"])
            score = eval_res["composite_risk_score"]
            predicted_fraud = score >= threshold

            if ground_truth_is_fraud and predicted_fraud:
                tp += 1
            elif not ground_truth_is_fraud and predicted_fraud:
                fp += 1
            elif not ground_truth_is_fraud and not predicted_fraud:
                tn += 1
            else:
                fn += 1

        total = len(benchmark_dataset)
        precision = tp / (tp + fp) if (tp + fp) > 0 else 1.0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 1.0
        specificity = tn / (tn + fp) if (tn + fp) > 0 else 1.0
        fpr = fp / (fp + tn) if (fp + tn) > 0 else 0.0
        fnr = fn / (fn + tp) if (fn + tp) > 0 else 0.0
        f1 = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0
        accuracy = (tp + tn) / total if total > 0 else 1.0

        return {
            "total_samples": total,
            "confusion_matrix": {
                "true_positives": tp,
                "false_positives": fp,
                "true_negatives": tn,
                "false_negatives": fn
            },
            "metrics": {
                "accuracy": round(accuracy, 4),
                "precision": round(precision, 4),
                "recall_sensitivity": round(recall, 4),
                "specificity": round(specificity, 4),
                "false_positive_rate": round(fpr, 4),
                "false_negative_rate": round(fnr, 4),
                "f1_score": round(f1, 4)
            },
            "eval_decision_threshold": threshold
        }

    @classmethod
    def get_realistic_benchmark_dataset(cls) -> List[Dict[str, Any]]:
        """
        Returns a curated benchmark set of realistic edge cases representing:
        - Legitimate mobile gamers on cellular network handovers (Should NOT be flagged).
        - Legitimate power users withdrawing frequently with KYC (Should NOT be flagged).
        - Sybil farm multi-accounting bots (Should BE flagged).
        - Autoclicker micro-jitter tap bots (Should BE flagged).
        - Suspicious credential stuffers with IP mismatch (Should BE flagged).
        """
        cases = [
            # 1. Legitimate Mobile User with Dynamic Cellular IP handover
            {
                "case_id": "CASE_LEGIT_01",
                "is_fraud": False,
                "features": {
                    "account_age_days": 45,
                    "withdrawal_count_24h": 1,
                    "shared_device_account_count": 1,
                    "is_ip_country_mismatched": True, # Tower hop
                    "carrier_asn": "AS55836", # Airtel whitelisted
                    "average_tap_micro_jitter_ms": 28.5,
                    "kyc_tier": "TIER_2",
                    "lifetime_completed_tasks": 30
                }
            },
            # 2. Legitimate Established User, 2nd withdrawal
            {
                "case_id": "CASE_LEGIT_02",
                "is_fraud": False,
                "features": {
                    "account_age_days": 60,
                    "withdrawal_count_24h": 2,
                    "shared_device_account_count": 1,
                    "is_ip_country_mismatched": False,
                    "carrier_asn": "AS45609", # Jio
                    "average_tap_micro_jitter_ms": 32.0,
                    "kyc_tier": "TIER_3",
                    "lifetime_completed_tasks": 50
                }
            },
            # 3. Legitimate Rapid Casual Gamer (Natural micro-jitter 22ms)
            {
                "case_id": "CASE_LEGIT_03",
                "is_fraud": False,
                "features": {
                    "account_age_days": 35,
                    "withdrawal_count_24h": 1,
                    "shared_device_account_count": 1,
                    "is_ip_country_mismatched": False,
                    "average_tap_micro_jitter_ms": 22.0,
                    "kyc_tier": "TIER_1",
                    "lifetime_completed_tasks": 15
                }
            },
            # 4. Fraud Case: Sybil Multi-Account Farm on 1 Phone
            {
                "case_id": "CASE_FRAUD_01",
                "is_fraud": True,
                "features": {
                    "account_age_days": 1,
                    "withdrawal_count_24h": 4,
                    "shared_device_account_count": 5,
                    "is_ip_country_mismatched": False,
                    "average_tap_micro_jitter_ms": 1.5, # Autoclicker
                    "kyc_tier": "TIER_0",
                    "lifetime_completed_tasks": 2
                }
            },
            # 5. Fraud Case: International VPN Proxy + Robotic Micro-jitter
            {
                "case_id": "CASE_FRAUD_02",
                "is_fraud": True,
                "features": {
                    "account_age_days": 2,
                    "withdrawal_count_24h": 3,
                    "shared_device_account_count": 3,
                    "is_ip_country_mismatched": True,
                    "carrier_asn": "AS9009", # Unknown foreign hosting ASN
                    "average_tap_micro_jitter_ms": 2.1,
                    "kyc_tier": "TIER_0",
                    "lifetime_completed_tasks": 1
                }
            },
            # 6. Fraud Case: Fast Cash-Out Attack on Compromised Device
            {
                "case_id": "CASE_FRAUD_03",
                "is_fraud": True,
                "features": {
                    "account_age_days": 2,
                    "withdrawal_count_24h": 5,
                    "shared_device_account_count": 4,
                    "is_ip_country_mismatched": True,
                    "carrier_asn": "AS14061", # DigitalOcean datacenter IP
                    "average_tap_micro_jitter_ms": 4.0,
                    "kyc_tier": "TIER_0",
                    "lifetime_completed_tasks": 0
                }
            }
        ]
        return cases
