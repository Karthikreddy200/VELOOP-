-- dbt_project/models/staging/stg_events.sql
-- Silver staging view: Deduplication, casing normalization, and whitespace trimming

WITH source_data AS (
    SELECT 
        event_id,
        user_id,
        session_id,
        event_datetime,
        feature_name,
        event_name,
        event_status,
        device,
        reward_amount_xp
    FROM {{ source('raw_veloop', 'events_messy') }}
),

sanitized_events AS (
    SELECT 
        event_id,
        user_id,
        session_id,
        event_datetime,
        INITCAP(TRIM(feature_name)) AS feature_name,
        LOWER(TRIM(event_name)) AS event_name,
        UPPER(TRIM(event_status)) AS event_status,
        COALESCE(TRIM(device), 'Unknown') AS device,
        COALESCE(reward_amount_xp, 0) AS reward_amount_xp,
        ROW_NUMBER() OVER(PARTITION BY event_id ORDER BY event_datetime ASC) AS rn
    FROM source_data
)

SELECT 
    event_id,
    user_id,
    session_id,
    event_datetime,
    feature_name,
    event_name,
    event_status,
    device,
    reward_amount_xp
FROM sanitized_events
WHERE rn = 1
