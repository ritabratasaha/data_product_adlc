# products

## Overview
This seed file contains product catalog data including product information, pricing, categories, brands, and supplier details.

## Source
CSV seed file: `seeds/products.csv`

## Grain
Unique record for each product_sku (product identifier)

## Schema
Seeds are loaded into the `staging` schema (configured in dbt_project.yml)

## Columns

- **product_sku**: Product Stock Keeping Unit identifier (primary key)
- **product_name**: Name of the product
- **category**: Product category (Electronics, Home & Kitchen, Apparel, Grocery)
- **subcategory**: Product subcategory for granular classification
- **brand**: Brand name of the product
- **list_price_usd**: List price in USD
- **unit_of_measure**: Unit of measure (EA = Each)
- **is_active**: Active status flag (1=active, 0=inactive)
- **supplier_id**: Supplier identifier
- **product_launch_date**: Date when product was launched

## Data Quality Rules

- product_sku must be unique
- product_sku must not be null
- is_active should be 1 or 0

## Example Use Cases

## Example Query

```sql
SELECT
    product_sku,
    product_name,
    category,
    brand,
    list_price_usd
FROM {{ ref('products') }}
WHERE is_active = 1
ORDER BY category, product_name
```


