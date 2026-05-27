# customer_sales

## Overview
This seed file contains customer sales transaction data including sale amounts, discounts, products purchased, sales channels, and order status.

## Source
CSV seed file: `seeds/customer_sales.csv`

## Grain
Unique record for each sale_id (transaction identifier)

## Schema
Seeds are loaded into the `staging` schema (configured in dbt_project.yml)

## Columns

- **sale_id**: Unique identifier for each sale transaction (primary key)
- **sale_date**: Date when the sale occurred
- **customer_id**: Unique identifier for the customer
- **product_sku**: Product Stock Keeping Unit identifier
- **quantity**: Number of units sold
- **unit_price_usd**: Price per unit in USD
- **discount_usd**: Discount applied to the transaction in USD
- **line_total_usd**: Total amount for the line item in USD (calculated as: quantity * unit_price_usd - discount_usd)
- **sales_channel**: Sales channel (Online, Retail Store, B2B Portal)
- **order_status**: Status of the order (Completed, Shipped, Pending, Returned)

## Data Quality Rules

- sale_id must be unique
- sale_id must not be null
- line_total_usd should equal (quantity * unit_price_usd) - discount_usd

## Example Use Cases

## Example Query

```sql
SELECT
    sale_id,
    sale_date,
    customer_id,
    product_sku,
    quantity,
    line_total_usd,
    sales_channel,
    order_status
FROM {{ ref('customer_sales') }}
WHERE order_status = 'Completed'
  AND sale_date >= '2025-01-01'
ORDER BY sale_date DESC
```


