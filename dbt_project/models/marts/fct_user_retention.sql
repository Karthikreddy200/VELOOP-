-- dbt_project/models/marts/fct_user_retention.sql
-- Gold retention fact table: Day 0–30 cohort survival calculations

WITH users AS (
    SELECT 
        user_id,
        cleaned_registration_datetime AS registration_date,
        DATE_TRUNC('week', cleaned_registration_datetime) AS cohort_week,
        acquisition_source
    FROM {{ ref('stg_users') }}
),

activity AS (
    SELECT 
        user_id,
        DATE(event_datetime) AS activity_date
    FROM {{ ref('stg_events') }}
    GROUP BY user_id, DATE(event_datetime)
),

user_tenure_activity AS (
    SELECT 
        u.cohort_week,
        u.acquisition_source,
        u.user_id,
        DATEDIFF('day', u.registration_date, a.activity_date) AS day_offset
    FROM users u
    JOIN activity a ON u.user_id = a.user_id
    WHERE DATEDIFF('day', u.registration_date, a.activity_date) BETWEEN 0 AND 30
),

cohort_sizes AS (
    SELECT 
        cohort_week,
        acquisition_source,
        COUNT(DISTINCT user_id) AS cohort_size
    FROM users
    GROUP BY cohort_week, acquisition_source
)

SELECT 
    c.cohort_week,
    c.acquisition_source,
    c.cohort_size,
    100.0 AS day_0_retention_pct,
    ROUND(COUNT(DISTINCT CASE WHEN t.day_offset = 1 THEN t.user_id END) * 100.0 / c.cohort_size, 2) AS day_1_retention_pct,
    ROUND(COUNT(DISTINCT CASE WHEN t.day_offset BETWEEN 6 AND 8 THEN t.user_id END) * 100.0 / c.cohort_size, 2) AS day_7_retention_pct,
    ROUND(COUNT(DISTINCT CASE WHEN t.day_offset BETWEEN 13 AND 15 THEN t.user_id END) * 100.0 / c.cohort_size, 2) AS day_14_retention_pct,
    ROUND(COUNT(DISTINCT CASE WHEN t.day_offset BETWEEN 28 AND 30 THEN t.user_id END) * 100.0 / c.cohort_size, 2) AS day_30_retention_pct
FROM cohort_sizes c
LEFT JOIN user_tenure_activity t 
    ON c.cohort_week = t.cohort_week 
   AND c.acquisition_source = t.acquisition_source
GROUP BY c.cohort_week, c.acquisition_source, c.cohort_size
