# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a dbt (data build tool) project for the Sales data product, running on PostgreSQL. It transforms sales and product data from seed files into staging and mart layers for analytics and reporting.

**Key Facts:**

- Target database: `sales_data_product` on local PostgreSQL
- Development environment: Local PostgreSQL database (localhost:5432)
- Main schemas: `public` (default PostgreSQL schema)
- Data sources: CSV seed files

##  MANDATORY PRE-FLIGHT CHECK
Before executing any action, you MUST output "Pre-flight Check: SUCCESS" and follow these steps:
1. **Context Review:** Read this `CLAUDE.md` file and any specific project instructions.
2. **Requirement Check:** If the task involves a model, read **`docs/<layer>/[model_name].md`** (same basename as the `.sql` file). layer = staging or marts
3. **Plan Formulation:** Draft a step-by-step implementation plan (Plan Mode).
4. **Pause for Approval:** Present the plan and wait for the user to confirm "Proceed."

*Failure to perform these steps before coding will be considered a protocol violation.*

##  MANDATORY POST-FLIGHT CHECK
1. Execute the evals and share the results

### Project Organization

```
sales_data_product/
├── models/
│   ├── staging/                        # Staging layer (business logic & transformations)
│   │   ├── stg_*.sql                  # Staging models
│   │   └── *.yml                      # Model documentation & tests
│   └── marts/                          # Marts layer (final outputs)
│       ├── *.sql                      # Mart models
│       └── *.yml                      # Model documentation & tests
├── docs/                               # Model requirements documentation
│   ├── staging/                        # stg_<model>.md paired with models/staging/stg_*.sql
│   │   ├── stg_customer_sales.md
│   │   └── stg_monthly_channel_revenue.md
│   └── marts/                          # <model>.md paired with models/marts/*.sql
├── macros/
│   └── *.sql                          # Custom dbt macros (currently empty)
├── seeds/
│   ├── customer_sales.csv             # Customer sales transactions
│   └── products.csv                   # Product information
├── tests/                              # Custom data tests
├── dbt_project.yml                     # Project configuration
└── profiles.yml                        # PostgreSQL connection profile
```

### Layer Architecture

**1. Seeds** → **2. Staging** → **3. Marts**

#### Seeds (`seeds/`)
CSV files containing source data that are loaded into the database via `dbt seed`:
- **customer_sales.csv**: Customer sales transactions with columns:
  - sale_id, sale_date, customer_id, product_sku, quantity, unit_price_usd, discount_usd, line_total_usd, sales_channel, order_status
- **products.csv**: Product information

#### Staging Layer (`models/staging/`)
**Purpose**: Business logic, filtering, aggregations, and transformations
**Materialization**: Views (default)
**Schema**: `public` (default PostgreSQL schema)

**Key Characteristics**:
- Contains ALL business logic
- Applies data quality filters
- Transforms seed data into clean, usable models
- Prefix: `stg_<entity_name>`

#### Marts Layer (`models/marts/`)
**Purpose**: Final output models for downstream consumption
**Materialization**: Views or tables as needed
**Schema**: `public` (default PostgreSQL schema)

**Key Characteristics**:
- May reference staging models or add additional aggregations
- Can include business logic for specific use cases
- Stable interface for consumers
- Naming: `<entity_name>`, `fct_<entity_name>` (facts), or `dim_<entity_name>` (dimensions)

### Model Naming Convention

- **Staging**: `stg_<entity_name>`
- **Marts**: `<entity_name>` or `fct_<entity_name>` for fact tables, `dim_<entity_name>` for dimension tables
- **Macros**: `<action>_<object>`

### Custom Macros
Located in `macros/`:
- Currently empty
- Add macros here as needed for reusable SQL logic

### Understanding Model Requirements
Read the model requirements from **`docs/staging/<model>.md`** or **`docs/marts/<model>.md`** (same name as the model, under the folder that matches the SQL layer).

These markdown files document:
- **Overview**: Model purpose and description
- **Materialization**: How the model should be materialized (view, table, etc.)
- **Source**: Where the data comes from
- **Grain**: The uniqueness level of the data
- **Join Logic**: How tables are joined (if applicable)
- **Transformation Steps**: Business logic applied
- **Filters**: Data filtering rules
- **Business Rules**: Business logic constraints
- **Projected Columns**: Expected output columns
- **Data Quality Rules**: Validation rules and tests
- **Example Use Cases**: How the model should be used
- **Example Query**: Sample queries for testing

## Development Commands

### Loading Seed Data
```bash
# Load all seed files into the database
dbt seed

# Load specific seed file
dbt seed --select customer_sales
```

### Running dbt
```bash
# Run all models
dbt run

# Run specific model
dbt run --select stg_customer_sales

# Run models and downstream dependencies
dbt run --select stg_customer_sales+

# Run models in a specific folder
dbt run --select staging
dbt run --select marts
```

### Testing
```bash
# Run all tests
dbt test

# Run tests for specific model
dbt test --select stg_customer_sales

# Run tests for a folder
dbt test --select staging
```

### Documentation
```bash
# Generate documentation
dbt docs generate

# Serve documentation locally
dbt docs serve
```

### Utility Commands
```bash
# Compile SQL without running
dbt compile

# Show compiled SQL for a model
dbt show --select stg_customer_sales

# Clean target directory
dbt clean

# Debug connection
dbt debug
```

## PostgreSQL Profile

Configured in `profiles.yml`:

**Target: local**
- Type: `postgres`
- Host: `localhost`
- Port: `5432`
- Database: `sales_data_product`
- Schema: `public`
- Threads: `4`

To use this profile, ensure PostgreSQL is running locally with appropriate credentials configured in `profiles.yml`.

## Common Patterns

### Creating a New Staging Model

1. **Staging Model** (`models/staging/stg_<name>.sql`):
```sql
-- Description of what this model does

select
    -- Select columns from seed
    column1,
    column2,
    -- Add transformations
    upper(column3) as column3_upper,
    -- Add calculations
    quantity * unit_price as total_amount
from {{ ref('seed_name') }}
where order_status != 'cancelled'  -- Apply filters
```

2. **Model Documentation** (`docs/staging/stg_<name>.md`):
```markdown
# stg_<name>

## Overview
Brief description of the model

## Materialization
view

## Source
This model is created from the seed file <name>.csv located under /seeds

## Grain
Unique record for each <primary_key>

## Transformation Steps
- List transformations applied

## Business Rules
- List business rules

## Projected Columns
- column1
- column2

## Data Quality Rules
- column1 must not be null
- column2 must be unique
```

3. **Model YAML** (`models/staging/stg_<name>.yml`):
```yaml
version: 2

models:
  - name: stg_<name>
    description: "Description here"
    columns:
      - name: column_name
        description: "Column description"
        tests:
          - unique
          - not_null
      - name: another_column
        description: "Another column description"
```

### Creating a New Mart Model

1. **Mart Model** (`models/marts/<name>.sql`):
```sql
-- Description of the mart

select
    -- Select from staging
    column1,
    column2,
    -- Add aggregations or business logic
    sum(amount) as total_amount,
    count(*) as record_count
from {{ ref('stg_source') }}
group by column1, column2
```

2. **Documentation** (`docs/marts/<name>.md`): Follow same pattern as staging

3. **Model YAML** (`models/marts/<name>.yml`): Follow same pattern as staging

## SQL Best Practices

- Use lowercase for SQL keywords and identifiers
- Use CTEs (Common Table Expressions) for complex queries
- Always use explicit column names (avoid SELECT *)
- Add comments to explain complex logic
- Use consistent indentation (4 spaces)
- Qualify column names with table aliases in joins
- Use meaningful aliases

Example:
```sql
with base_data as (
    select
        customer_id,
        sale_date,
        line_total_usd
    from {{ ref('stg_customer_sales') }}
    where order_status = 'completed'
),

aggregated as (
    select
        customer_id,
        sum(line_total_usd) as total_sales
    from base_data
    group by customer_id
)

select * from aggregated
```

## Testing Strategy

Add tests in the model YAML files:

```yaml
columns:
  - name: sale_id
    tests:
      - unique
      - not_null

  - name: line_total_usd
    tests:
      - not_null
      - dbt_utils.accepted_range:
          min_value: 0

  - name: order_status
    tests:
      - accepted_values:
          values: ['pending', 'completed', 'cancelled']
```

## Troubleshooting

### Database Connection Issues
```bash
# Test connection
dbt debug

# Check if PostgreSQL is running
psql -h localhost -U developer -d sales_data_product
```

### Model Errors
```bash
# Compile to see generated SQL
dbt compile --select model_name

# Run with debug logging
dbt --debug run --select model_name
```

## Code Ownership

Maintained by the Sales Data Product team.
