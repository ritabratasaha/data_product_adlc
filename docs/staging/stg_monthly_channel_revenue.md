# stg_monthly_channel_revenue

## Overview
This model has sample customer and their sales information


## Materialization
view

## Source
This model reads the data from stg_customer_sales. 

    |   Data Product        |        Data Object              | Model Layer      |
    |-----------------------|---------------------------------|------------------|
    |   sales_data_product  |   stg_customer_sales            | /models/staging  |
    

## Grain
Unique record for each sales_channel , year and month

## Join Logic

## Transformation Steps

    - total_revenue is calculated as an aggregate of line_total_usd for a given sales_channel
    - revenue_year :  year of the sale_date
    - revenue_month : month of the sales_date

## Filters

- Orders status = pending are not considered for revenue calculation

## Business Rules

## Projected Columns

    - sales_channel
    - total_revenue
    - revenue_year
    - revenue_month

## Data Quality Rules

- The status of the order cannot be blank or null
- line_total_usd = (quantity * unit_price_usd) - discount_usd

## Example Use Cases

## Example Query

## Create a mart view from this model ?

Yes. Create a mart view in models/marts for this model. 
This will be the presentation layer for the data product consumers



