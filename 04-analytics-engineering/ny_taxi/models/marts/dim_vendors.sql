with unioned_trips as (
    select * from {{ ref('int_trips_union') }}
),

vendors as (
    select 
        distinct vendor_id,
        {{ get_vendor_names('vendor_id') }} as vendor_name
    from unioned_trips
)

select * from vendors