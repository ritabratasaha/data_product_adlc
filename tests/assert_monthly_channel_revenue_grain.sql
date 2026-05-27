-- Test to validate the grain: unique combination of sales_channel, revenue_year, revenue_month
-- This test will fail if any combination appears more than once

with grain_check as (
    select
        sales_channel,
        revenue_year,
        revenue_month,
        count(*) as record_count
    from {{ ref('stg_monthly_channel_revenue') }}
    group by
        sales_channel,
        revenue_year,
        revenue_month
    having count(*) > 1
)

select * from grain_check
