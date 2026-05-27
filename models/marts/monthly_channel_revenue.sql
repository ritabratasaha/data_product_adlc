-- Mart model for monthly channel revenue
-- Presentation layer for data consumers
-- Source: stg_monthly_channel_revenue model
-- Grain: One row per unique combination of (sales_channel, revenue_year, revenue_month)

{{ config(materialized='view') }}

select
    sales_channel,
    revenue_year,
    revenue_month,
    total_revenue

from {{ ref('stg_monthly_channel_revenue') }}
order by
    sales_channel,
    revenue_year,
    revenue_month
