-- dbt_project/models/staging/stg_users.sql
-- Silver staging view: Deduplication, PII SHA-256 pseudonymization, and boundary checks

WITH source_data AS (
    SELECT 
        user_id,
        email,
        phone_number,
        account_status,
        registration_datetime,
        xp_balance,
        referred_by,
        platform,
        acquisition_source
    FROM {{ source('raw_veloop', 'users_messy') }}
),

ranked_users AS (
    SELECT 
        user_id,
        SHA256(CONCAT(email, ':veloop_salt_2026')) AS masked_email_hash,
        SPLIT_PART(email, '@', 2) AS email_domain,
        account_status,
        -- Cap future dates at current UTC timestamp
        CASE 
            WHEN registration_datetime > CURRENT_TIMESTAMP() THEN CURRENT_TIMESTAMP()
            ELSE registration_datetime 
        END AS cleaned_registration_datetime,
        -- Non-negative XP boundary clamp
        GREATEST(xp_balance, 0) AS cleaned_xp_balance,
        referred_by,
        COALESCE(platform, 'Unknown') AS platform,
        COALESCE(acquisition_source, 'Organic') AS acquisition_source,
        ROW_NUMBER() OVER(PARTITION BY user_id ORDER BY registration_datetime ASC) AS rn
    FROM source_data
)

SELECT 
    user_id,
    masked_email_hash,
    email_domain,
    account_status,
    cleaned_registration_datetime,
    cleaned_xp_balance,
    referred_by,
    platform,
    acquisition_source
FROM ranked_users
WHERE rn = 1
