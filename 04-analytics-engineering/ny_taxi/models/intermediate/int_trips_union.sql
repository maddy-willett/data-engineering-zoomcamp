with green_tripdata as (
    select *
    from {{ ref('stg_green_tripdata') }}
),

yellow_tripdata as (
    select *
    from {{ ref('stg_yellow_tripdata') }}
),

trips_unioned as (
    
)