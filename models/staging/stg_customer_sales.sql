-- Staging model for customer sales transactions
-- Source: customer_sales.csv seed file
-- Grain: One row per sale_id

{{ config(materialized='view') }}

with source_data as (

    select
        sale_id,
        sale_date,
        customer_id,
        product_sku,
        quantity,
        unit_price_usd,
        discount_usd,
        line_total_usd,
        sales_channel,
        order_status

    from {{ ref('customer_sales') }}

),

final as (

    select
        sale_id,
        sale_date,
        customer_id,
        product_sku,
        quantity,
        unit_price_usd,
        discount_usd,
        line_total_usd,
        sales_channel,
        order_status

    from source_data
    where 1=1
        and order_status is not null

)

select
    sale_id,
    sale_date,
    customer_id,
    product_sku,
    quantity,
    unit_price_usd,
    discount_usd,
    line_total_usd,
    sales_channel,
    order_status

from final
