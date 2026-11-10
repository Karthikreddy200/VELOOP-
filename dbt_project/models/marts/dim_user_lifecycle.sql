-- dbt_project/models/marts/dim_user_lifecycle.sql
-- Gold dimensional model: User lifecycle state classification & engagement metrics

WITH users AS (
    SELECT * FROM {{ ref('stg_users') }}
),

user_activity AS (
    SELECT 
        user_id,
        MAX(event_datetime) AS last_active_at,
        COUNT(DISTINCT event_id) AS total_events,
        COUNT(DISTINCT DATE(event_datetime)) AS active_days_count,
        SUM(reward_amount_xp) AS total_xp_earned
    FROM {{ ref('stg_events') }}
    GROUP BY user_id
)

SELECT 
    u.user_id,
    u.masked_email_hash,
    u.email_domain,
    u.account_status,
    u.cleaned_registration_datetime AS registration_at,
    u.platform,
    u.acquisition_source,
    u.cleaned_xp_balance AS current_xp_balance,
    COALESCE(a.total_events, 0) AS total_events,
    COALESCE(a.active_days_count, 0) AS active_days_count,
    COALESCE(a.total_xp_earned, 0) AS total_xp_earned,
    a.last_active_at,
    DATEDIFF('day', u.cleaned_registration_datetime, CURRENT_DATE()) AS tenure_days,
    DATEDIFF('day', a.last_active_at, CURRENT_DATE()) AS days_since_last_active,
    -- Deterministic FSM classification logic
    CASE 
        WHEN u.account_status IN ('Suspended', 'Banned') THEN 'SUSPENDED'
        WHEN DATEDIFF('day', a.last_active_at, CURRENT_DATE()) <= 7 THEN 'HIGHLY_ACTIVE_7D'
        WHEN DATEDIFF('day', a.last_active_at, CURRENT_DATE()) <= 30 THEN 'MODERATELY_ACTIVE_30D'
        WHEN DATEDIFF('day', u.cleaned_registration_datetime, CURRENT_DATE()) > 60 THEN 'CHURNED'
        ELSE 'DORMANT_AT_RISK'
    END AS lifecycle_state
FROM users u
LEFT JOIN user_activity a ON u.user_id = a.user_id
