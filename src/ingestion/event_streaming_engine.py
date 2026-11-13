"""
VELOOP Rewards - Real-Time Event Streaming & Telemetry Ingestion Engine
Part of Task 01: Product Analytics & Data Readiness Architecture

Models the real-time event ingestion boundary (Kafka / Google Cloud Pub/Sub),
enforcing strict JSON Schema contracts, idempotency deduplication, timestamp drift
guards, and micro-batch buffering for downstream Bronze-to-Silver ETL pipelines.

Notice: SIMULATED DATA — CREATED FOR ANALYTICAL TESTING
"""

import time
import uuid
import hashlib
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Optional, Tuple, Any

# 28 Official VELOOP Production Events (from Work Package F Taxonomy)
VALID_PRODUCTION_EVENTS = {
    # Account & Auth
    "user_registered", "user_logged_in", "kyc_tier_updated", "account_suspended",
    # Earning Mechanics
    "ad_watch_started", "ad_watch_completed", "tap_action_recorded", "mining_session_started",
    "mining_reward_claimed", "spin_wheel_initiated", "spin_wheel_rewarded",
    # Gamification & Habits
    "daily_streak_incremented", "mission_assigned", "mission_completed", "badge_unlocked", "level_up_achieved",
    # Referral Loops (WP E)
    "referral_invite_sent", "referral_link_clicked", "referral_account_created", "referral_milestone_unlocked",
    # Wallet & Financials (WP D)
    "wallet_balance_credited", "wallet_balance_debited", "withdrawal_requested",
    "withdrawal_kyc_validated", "withdrawal_aml_checked", "withdrawal_approved",
    "withdrawal_rejected", "withdrawal_gateway_dispatched"
}

class IngestionValidationError(Exception):
    """Raised when an incoming event violates the telemetry contract."""
    pass

class EventSchemaValidator:
    """
    Validates event payload contracts, timestamp drift tolerance,
    and official event taxonomy naming.
    """
    MAX_FUTURE_DRIFT_SECONDS = 300   # Max 5 minutes future drift allowed
    MAX_PAST_DRIFT_SECONDS = 604800 # Max 7 days historical drift allowed

    @classmethod
    def validate_event(cls, event: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        """
        Validates event structure and constraints.
        Returns: (is_valid, error_message)
        """
        required_keys = {"event_id", "user_id", "event_name", "event_timestamp", "payload", "idempotency_key"}
        missing_keys = required_keys - set(event.keys())
        if missing_keys:
            return False, f"Missing mandatory contract fields: {missing_keys}"

        # Event Name Taxonomy Check
        event_name = event["event_name"]
        if event_name not in VALID_PRODUCTION_EVENTS:
            return False, f"Invalid event_name '{event_name}'. Must conform to 28 official VELOOP production events."

        # User ID check
        if not event["user_id"] or not isinstance(event["user_id"], str):
            return False, "user_id must be a non-empty string"

        # Timestamp Drift Verification
        ts_val = event["event_timestamp"]
        try:
            if isinstance(ts_val, (int, float)):
                event_dt = datetime.fromtimestamp(ts_val, tz=timezone.utc)
            elif isinstance(ts_val, str):
                event_dt = datetime.fromisoformat(ts_val.replace("Z", "+00:00"))
            else:
                return False, "event_timestamp must be an ISO8601 string or Unix timestamp"
        except Exception as e:
            return False, f"Malformed event_timestamp format: {e}"

        now = datetime.now(timezone.utc)
        drift = (event_dt - now).total_seconds()

        if drift > cls.MAX_FUTURE_DRIFT_SECONDS:
            return False, f"Timestamp rejected: Future drift of {drift:.1f}s exceeds {cls.MAX_FUTURE_DRIFT_SECONDS}s ceiling"

        if drift < -cls.MAX_PAST_DRIFT_SECONDS:
            return False, f"Timestamp rejected: Event timestamp older than {cls.MAX_PAST_DRIFT_SECONDS}s (7 days)"

        # Payload dictionary check
        if not isinstance(event["payload"], dict):
            return False, "payload must be a valid JSON dictionary"

        return True, None


class EventStreamBuffer:
    """
    In-memory partition buffer simulating Kafka / PubSub topic consumer
    with idempotency deduplication and micro-batching.
    """
    def __init__(self, batch_size: int = 100, deduplication_window: int = 10000):
        self.batch_size = batch_size
        self.seen_idempotency_keys = set()
        self.dedup_queue: List[str] = []
        self.max_dedup_size = deduplication_window
        self.active_buffer: List[Dict[str, Any]] = []
        self.dead_letter_queue: List[Dict[str, Any]] = []
        self.ingested_count = 0
        self.rejected_count = 0
        self.latencies_ms: List[float] = []

    def ingest(self, event: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Ingests a single event into the stream buffer.
        Enforces schema validation and deduplication.
        """
        start_time = time.perf_counter()

        # Idempotency check
        idem_key = event.get("idempotency_key")
        if not idem_key:
            idem_key = hashlib.sha256(f"{event.get('user_id')}_{event.get('event_name')}_{event.get('event_timestamp')}".encode()).hexdigest()
            event["idempotency_key"] = idem_key

        if idem_key in self.seen_idempotency_keys:
            self.rejected_count += 1
            return False, "DUPLICATE_IDEMPOTENCY_KEY_REJECTED"

        # Schema Validation
        is_valid, err_msg = EventSchemaValidator.validate_event(event)
        latency = (time.perf_counter() - start_time) * 1000.0
        self.latencies_ms.append(latency)

        if not is_valid:
            self.rejected_count += 1
            self.dead_letter_queue.append({"event": event, "reason": err_msg, "rejected_at": datetime.now(timezone.utc).isoformat()})
            return False, f"SCHEMA_REJECTED: {err_msg}"

        # Register key
        self.seen_idempotency_keys.add(idem_key)
        self.dedup_queue.append(idem_key)
        if len(self.dedup_queue) > self.max_dedup_size:
            oldest_key = self.dedup_queue.pop(0)
            self.seen_idempotency_keys.discard(oldest_key)

        self.active_buffer.append(event)
        self.ingested_count += 1
        return True, "INGESTED_SUCCESS"

    def flush_micro_batch(self) -> List[Dict[str, Any]]:
        """
        Flushes up to batch_size records to downstream Silver layer.
        """
        batch = self.active_buffer[:self.batch_size]
        self.active_buffer = self.active_buffer[self.batch_size:]
        return batch

    def get_metrics(self) -> Dict[str, Any]:
        """
        Returns streaming ingestion health indicators.
        """
        p50 = 0.0
        p95 = 0.0
        if self.latencies_ms:
            sorted_lat = sorted(self.latencies_ms)
            p50 = sorted_lat[int(len(sorted_lat) * 0.50)]
            p95 = sorted_lat[int(len(sorted_lat) * 0.95)]

        return {
            "ingested_count": self.ingested_count,
            "rejected_count": self.rejected_count,
            "buffer_depth": len(self.active_buffer),
            "dead_letter_depth": len(self.dead_letter_queue),
            "p50_latency_ms": round(p50, 2),
            "p95_latency_ms": round(p95, 2),
            "rejection_rate_pct": round((self.rejected_count / max(1, self.ingested_count + self.rejected_count)) * 100, 2)
        }


def generate_sample_telemetry_event(
    user_id: str = "USR-10042",
    event_name: str = "ad_watch_completed",
    payload: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Generates a synthetically valid telemetry event conforming to the contract.
    """
    if payload is None:
        payload = {"ad_id": "AD-8842", "reward_xp": 50, "duration_seconds": 29.5}

    event_id = str(uuid.uuid4())
    ts = datetime.now(timezone.utc).isoformat()
    idem_key = hashlib.sha256(f"{user_id}_{event_name}_{event_id}".encode()).hexdigest()

    return {
        "event_id": event_id,
        "user_id": user_id,
        "event_name": event_name,
        "event_timestamp": ts,
        "payload": payload,
        "idempotency_key": idem_key
    }
