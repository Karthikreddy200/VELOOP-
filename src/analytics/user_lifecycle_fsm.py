"""
VELOOP Rewards - User Lifecycle Finite State Machine (Work Package B)
Deterministic state machine governing user lifecycle states:
UNREGISTERED -> ONBOARDED -> ACTIVATED -> ENGAGED -> DORMANT -> CHURNED -> RESURRECTED
"""
from datetime import datetime, timezone
from typing import Dict, Any, Tuple

VALID_STATES = {
    'UNREGISTERED',
    'ONBOARDED',
    'ACTIVATED',
    'ENGAGED',
    'DORMANT',
    'CHURNED',
    'RESURRECTED',
    'SUSPENDED'
}

# Permitted state transitions
ALLOWED_TRANSITIONS = {
    'UNREGISTERED': {'ONBOARDED', 'SUSPENDED'},
    'ONBOARDED': {'ACTIVATED', 'DORMANT', 'SUSPENDED'},
    'ACTIVATED': {'ENGAGED', 'DORMANT', 'SUSPENDED'},
    'ENGAGED': {'ENGAGED', 'DORMANT', 'SUSPENDED'},
    'DORMANT': {'ENGAGED', 'CHURNED', 'RESURRECTED', 'SUSPENDED'},
    'CHURNED': {'RESURRECTED', 'SUSPENDED'},
    'RESURRECTED': {'ENGAGED', 'DORMANT', 'CHURNED', 'SUSPENDED'},
    'SUSPENDED': {'ENGAGED', 'DORMANT', 'CHURNED'}  # Only post-compliance clearance
}

def classify_lifecycle_state(
    account_status: str,
    days_since_reg: int,
    days_since_last_active: int,
    completed_task_count: int
) -> str:
    """Classifies a user into their deterministic lifecycle state."""
    if account_status in ['Suspended', 'Banned']:
        return 'SUSPENDED'
    
    if completed_task_count == 0:
        if days_since_reg <= 1:
            return 'ONBOARDED'
        elif days_since_last_active > 14:
            return 'DORMANT'
        else:
            return 'ONBOARDED'
            
    if days_since_last_active <= 7:
        if completed_task_count >= 5:
            return 'ENGAGED'
        else:
            return 'ACTIVATED'
    elif days_since_last_active <= 30:
        return 'DORMANT'
    else:
        return 'CHURNED'

def transition_state(current_state: str, new_state: str) -> Tuple[bool, str]:
    """Validates whether a proposed lifecycle state transition is legal."""
    current_state = current_state.upper()
    new_state = new_state.upper()
    
    if current_state not in VALID_STATES or new_state not in VALID_STATES:
        return False, f"ERR_INVALID_STATE: Unknown state ({current_state} -> {new_state})"
        
    allowed = ALLOWED_TRANSITIONS.get(current_state, set())
    if new_state in allowed:
        return True, "SUCCESS"
    else:
        return False, f"ERR_ILLEGAL_TRANSITION: Cannot jump from {current_state} directly to {new_state}"
