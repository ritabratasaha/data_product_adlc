# monthly_channel_revenue

## Overview
This mart model provides a clean presentation layer for monthly revenue aggregated by sales channel. It serves as the final output for data product consumers requiring monthly channel revenue analysis.

## Materialization
view

## Source
This model reads data from stg_monthly_channel_revenue in the staging layer.

|   Data Product        |        Data Object              | Model Layer      |
|-----------------------|---------------------------------|------------------|
|   sales_data_product  |   stg_monthly_channel_revenue   | /models/staging  |

## Grain
Unique record for each combination of sales_channel, revenue_year, and revenue_month

## Join Logic
No joins required - this is a simple passthrough from the staging model.

## Transformation Steps
- Selects all columns from stg_monthly_channel_revenue
- Orders results by sales_channel, revenue_year, revenue_month for consistent presentation

## Filters
All filtering is handled in the staging layer (stg_monthly_channel_revenue):
- Pending orders are excluded
- Only records with non-null order_status are included

## Business Rules
- Revenue calculations are performed in the staging layer
- This mart provides a stable interface for downstream consumers
- Sorting ensures consistent ordering for reporting and analytics

## Projected Columns
- sales_channel: Channel through which sales were made
- revenue_year: Year of the sales transaction
- revenue_month: Month of the sales transaction (1-12)
- total_revenue: Total revenue for the channel/year/month combination

## Data Quality Rules
- All quality rules are enforced in the staging layer (stg_monthly_channel_revenue)
- This mart inherits the data quality guarantees from staging


