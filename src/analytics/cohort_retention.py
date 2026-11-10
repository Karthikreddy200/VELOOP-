"""
VELOOP Rewards - Cohort Retention & Survival Decay Engine (Work Package B)
Computes empirical cohort retention matrices and survival decay functions across Days 0–30.
"""
from typing import List, Dict, Any
import pandas as pd
import numpy as np

def compute_cohort_retention(
    registrations: pd.DataFrame,
    activity_events: pd.DataFrame
) -> pd.DataFrame:
    """
    Computes cohort retention matrix across Day 0, Day 1, Day 7, Day 14, and Day 30.
    
    registrations schema: user_id, registration_date
    activity_events schema: user_id, activity_date
    """
    df_reg = registrations.copy()
    df_act = activity_events.copy()
    
    df_reg['registration_date'] = pd.to_datetime(df_reg['registration_date'])
    df_act['activity_date'] = pd.to_datetime(df_act['activity_date'])
    
    # Merge activity with registration to compute tenure day offset
    merged = pd.merge(df_act, df_reg, on='user_id', how='inner')
    merged['day_offset'] = (merged['activity_date'] - merged['registration_date']).dt.days
    
    # Restrict to active tenure within Day 0 to 30
    valid_events = merged[(merged['day_offset'] >= 0) & (merged['day_offset'] <= 30)]
    
    # Assign cohort week
    df_reg['cohort_week'] = df_reg['registration_date'].dt.to_period('W').astype(str)
    valid_events = pd.merge(valid_events, df_reg[['user_id', 'cohort_week']], on=['user_id', 'cohort_week'], how='inner')
    
    cohort_sizes = df_reg.groupby('cohort_week')['user_id'].nunique().rename('cohort_size')
    
    # Day milestones
    milestones = [0, 1, 7, 14, 30]
    retention_dict = {}
    
    for m in milestones:
        # Active on milestone day m (or within +/- 1 day window for m > 1)
        if m == 0:
            active_m = valid_events[valid_events['day_offset'] == 0]
        else:
            active_m = valid_events[(valid_events['day_offset'] >= m - 1) & (valid_events['day_offset'] <= m + 1)]
            
        retained = active_m.groupby('cohort_week')['user_id'].nunique()
        retention_dict[f'Day_{m}_pct'] = (retained / cohort_sizes * 100.0).round(2).fillna(0.0)
        
    retention_df = pd.DataFrame(retention_dict).join(cohort_sizes)
    retention_df['Day_0_pct'] = 100.0  # Normalized onboarding baseline
    return retention_df.reset_index()

def calculate_survival_decay(retention_rates: List[float]) -> Dict[str, float]:
    """
    Fits an exponential decay curve to empirical retention points: R(t) = R_0 * e^(-k * t)
    Returns decay rate k and projected Day-60 retention.
    """
    if not retention_rates or len(retention_rates) < 2:
        return {'decay_rate_k': 0.05, 'projected_day_60_pct': 5.0}
        
    # Baseline retention at t=1 vs t=30
    r0 = max(retention_rates[0], 1.0)
    r_last = max(retention_rates[-1], 0.1)
    t = 30.0
    
    # k = -ln(R_t / R_0) / t
    k = -np.log(r_last / r0) / t
    projected_d60 = round(float(r0 * np.exp(-k * 60.0)), 2)
    
    return {
        'decay_rate_k': round(float(k), 4),
        'projected_day_60_pct': max(projected_d60, 0.5)
    }
