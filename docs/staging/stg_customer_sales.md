# stg_customer_sales

## Overview
This model has sample customer and their sales information


## Materialization
view

## Source
This model is created from the seed file customer_sales.csv located under /seeds

## Grain
Unique record for each sales_id

## Join Logic

## Transformation Steps

## Filters

## Projected Columns

    - sale_id
    - sale_date
    - customer_id
    - product_sku
    - quantity
    - unit_price_usd
    - discount_usd
    - line_total_usd
    - sales_channel
    - order_status

## Data Quality Rules

- The status of the order cannot be blank or null
- line_total_usd = (quantity * unit_price_usd) - discount_usd


## Create a mart view from this model ?

Default -- No


