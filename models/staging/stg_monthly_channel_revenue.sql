-- Staging model for monthly channel revenue aggregations
-- Source: stg_customer_sales model
-- Grain: One row per unique combination of (sales_channel, revenue_year, revenue_month)

{{ config(materialized='view') }}

with source_data as (

    select
        sales_channel,
        sale_date,
        line_total_usd,
        order_status

    from {{ ref('stg_customer_sales') }}

),

filtered_data as (

    select
        sales_channel,
        sale_date,
        line_total_usd

    from source_data
    where 1=1
        and order_status != 'Pending'
        and order_status is not null

),

final as (

    select
        sales_channel,
        cast(extract(year from sale_date) as integer) as revenue_year,
        cast(extract(month from sale_date) as integer) as revenue_month,
        sum(line_total_usd) as total_revenue

    from filtered_data
    group by
        sales_channel,
        extract(year from sale_date),
        extract(month from sale_date)

)

select
    sales_channel,
    revenue_year,
    revenue_month,
    total_revenue

from final
