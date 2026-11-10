"""
VELOOP Rewards - Earning & Reward Economy Engine (Work Package C)
Anti-farming velocity limits, bot-detection heuristics, and token mint-to-burn economics.
"""
from typing import Dict, Any, List, Tuple
import numpy as np

# Operational Thresholds (Work Package C Standard)
MAX_DAILY_REWARDED_ADS = 20
MAX_HOURLY_XP_CAP = 1000
MAX_HUMAN_TAPS_PER_SEC = 10.0
MIN_HUMAN_TAP_VARIANCE_SEC = 0.008  # Micro-variation in milliseconds
MAX_REFERRALS_PER_IP_DAY = 5

def validate_ad_watch_event(user_daily_ad_count: int, ad_duration_sec: float) -> Tuple[bool, str, int]:
    """
    Validates whether an ad watch completion event is eligible for an XP credit.
    Enforces daily cap and minimum viewing duration (e.g. >= 28s for 30s rewarded ad).
    """
    if user_daily_ad_count >= MAX_DAILY_REWARDED_ADS:
        return False, "ERR_DAILY_AD_CAP_EXCEEDED", 0
    if ad_duration_sec < 28.0:
        return False, "ERR_INSUFFICIENT_AD_DURATION", 0
    
    reward_xp = 50
    return True, "SUCCESS", reward_xp

def detect_tap_bot(tap_timestamps_sec: List[float]) -> Tuple[bool, str]:
    """
    Analyzes clickstream tapping intervals for automated bot / autoclicker behavior.
    - Rate Check: Flags if average rate > 10 taps/second.
    - Variance Check: Synthetic autoclickers produce unnaturally fixed intervals (variance ~ 0).
    """
    if len(tap_timestamps_sec) < 5:
        return False, "INSUFFICIENT_DATA"
    
    intervals = np.diff(tap_timestamps_sec)
    
    # 1. Frequency check
    avg_interval = np.mean(intervals)
    if avg_interval < (1.0 / MAX_HUMAN_TAPS_PER_SEC):
        return True, "BOT_DETECTED_SUPERHUMAN_SPEED"
        
    # 2. Timing consistency check (synthetic bots have standard deviation < 8ms)
    std_interval = np.std(intervals)
    if std_interval < MIN_HUMAN_TAP_VARIANCE_SEC:
        return True, "BOT_DETECTED_MECHANICAL_INTERVALS"
        
    return False, "HUMAN_VERIFIED"

def validate_earning_velocity(recent_hourly_xp: int, proposed_reward_xp: int) -> Tuple[bool, str]:
    """Protects against rapid reward-farming spikes by enforcing an hourly XP velocity ceiling."""
    if (recent_hourly_xp + proposed_reward_xp) > MAX_HOURLY_XP_CAP:
        return False, f"ERR_HOURLY_VELOCITY_CAP: Max {MAX_HOURLY_XP_CAP} XP/hour"
    return True, "SUCCESS"

def calculate_token_economy_health(
    total_xp_minted: float,
    total_xp_burned_or_withdrawn: float,
    cash_reserve_usd: float
) -> Dict[str, Any]:
    """
    Computes liquidity and inflation metrics for the VELOOP reward currency.
    - Mint-to-Burn Ratio
    - Economy State (Healthy, Deflationary, Inflationary)
    - Liquidity Coverage Ratio (LCR)
    """
    if total_xp_minted <= 0:
        burn_ratio = 1.0
    else:
        burn_ratio = round(total_xp_burned_or_withdrawn / total_xp_minted, 3)
        
    outstanding_tokens = max(total_xp_minted - total_xp_burned_or_withdrawn, 0)
    outstanding_liability_usd = round(outstanding_tokens / 100.0, 2)
    
    if outstanding_liability_usd <= 0:
        lcr = 2.0
    else:
        lcr = round(cash_reserve_usd / outstanding_liability_usd, 2)
        
    if burn_ratio >= 0.70:
        economy_status = "HEALTHY_CIRCULATION"
    elif burn_ratio >= 0.45:
        economy_status = "MODERATE_INFLATION"
    else:
        economy_status = "CRITICAL_INFLATION_RISK"
        
    return {
        "burn_to_mint_ratio": burn_ratio,
        "outstanding_liability_usd": outstanding_liability_usd,
        "liquidity_coverage_ratio": lcr,
        "is_reserve_adequate": lcr >= 1.20,
        "economy_status": economy_status
    }
