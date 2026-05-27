-- tests/assert_line_total_calculation.sql
-- Custom test to validate that line_total_usd matches the business rule calculation
-- Business rule: line_total_usd = (quantity * unit_price_usd) - discount_usd
-- This test will fail if any row has a mismatch

with validation as (
    select
        sale_id,
        line_total_usd,
        quantity,
        unit_price_usd,
        discount_usd,
        -- Calculate expected value
        (quantity * unit_price_usd) - discount_usd as expected_line_total,
        -- Use ROUND to avoid floating point precision issues
        round(line_total_usd::numeric, 2) as actual_rounded,
        round(((quantity * unit_price_usd) - discount_usd)::numeric, 2) as expected_rounded,
        abs(round(line_total_usd::numeric, 2) - round(((quantity * unit_price_usd) - discount_usd)::numeric, 2)) as difference
    from {{ ref('stg_customer_sales') }}
)

select
    sale_id,
    line_total_usd as actual_line_total,
    expected_line_total,
    difference
from validation
-- Test fails if there are any rows with differences greater than 0.01 (1 cent tolerance for rounding)
where difference > 0.01
