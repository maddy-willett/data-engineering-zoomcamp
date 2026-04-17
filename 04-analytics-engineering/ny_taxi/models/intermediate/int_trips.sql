-- enrich data and deduplicate rows
-- generate unique ids
-- data quality analysis in analyses/trips_data_quality.sql

with unioned as (
    select * from {{ ref('int_trips_union') }}
),

payment_types as (
    select * from {{ ref('payment_type_lookup') }}
),

cleaned_and_enriched as (
    select 
        -- generate unique ids
        {{ dbt_utils.generate_surrogate_key(['u.vendor_id', 'u.pickup_datetime', 'u.pickup_location_id', 'u.service_type']) }} as trip_id,

        -- identifiers 
        u.vendor_id,
        u.service_type,
        u.rate_code_id,
        u.pickup_location_id,
        u.dropoff_location_id,

        -- location ids
        u.pickup_datetime,
        u.dropoff_datetime,

        -- trip details
        u.store_and_fwd_flag,
        u.passenger_count,
        u.trip_distance,
        u.trip_type,

        -- payment info 
        u.fare_amount,
        u.extra,
        u.mta_tax,
        u.tip_amount,
        u.tolls_amount,
        u.ehail_fee,
        u.improvement_surcharge,
        u.total_amount,

        -- payment type desc
        coalesce(u.payment_type, 0) as payment_type,
        coalesce(pt.description, 'Unknown') as payment_type_description
    from 
        unioned u left join payment_types pt on coalesce(u.payment_type, 0) = pt.payment_type
)

select * from cleaned_and_enriched
-- deduplicate: if multiple trips match (same vendor, second, location, service), keep first
qualify row_number() over (partition by vendor_id, pickup_datetime, pickup_location_id, service_type order by dropoff_datetime) = 1