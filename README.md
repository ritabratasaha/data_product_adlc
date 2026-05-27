# data_product_adlc

Sample **Sales** data product built with an agentic development lifecycle (ADLC). It uses [dbt](https://docs.getdbt.com/) to transform CSV seed data into analytics-ready models on **PostgreSQL** (local or Supabase).

## Architecture

**Seeds** → **Staging** → **Marts**

| Layer | Purpose |
|-------|---------|
| `seeds/` | Source CSVs (`customer_sales`, `products`) |
| `models/staging/` | Business logic and data quality (`stg_*`) |
| `models/marts/` | Consumer-facing outputs (e.g. `monthly_channel_revenue`) |

Each model has a requirements doc in `docs/` (same basename as the `.sql` file). Python checks in `python_tests/` enforce naming conventions and schema YAML coverage.

## Product structure

```
seeds/          →  models/staging/  →  models/marts/
(customer_sales,     stg_*               presentation views
 products)           (business logic)
```

### Seeds (`seeds/`)

Raw CSV sources loaded into PostgreSQL via `dbt seed` (schema: `staging`).

| Seed | Description |
|------|-------------|
| `customer_sales` | Line-level sales transactions: customer, product SKU, quantity, pricing, discounts, channel, and order status. Grain: one row per `sale_id`. |
| `products` | Product catalog: name, category, brand, supplier, and list price. Grain: one row per `product_sku`. |

### Staging (`models/staging/`)

Views that hold business logic, filters, and aggregations. Naming: `stg_<entity>`.

| Model | Description |
|-------|-------------|
| `stg_customer_sales` | Cleansed sales lines from `customer_sales`. Enforces valid `order_status` and line-total math: `(quantity × unit_price_usd) − discount_usd`. Grain: one row per sale. |
| `stg_monthly_channel_revenue` | Monthly revenue by `sales_channel`, derived from `stg_customer_sales`. Excludes pending orders; outputs `total_revenue`, `revenue_year`, and `revenue_month`. Grain: channel × year × month. |

### Marts (`models/marts/`)

Stable, consumer-facing views. Minimal logic—mostly passthrough from staging.

| Model | Description |
|-------|-------------|
| `monthly_channel_revenue` | Presentation layer for monthly channel revenue reporting. Reads from `stg_monthly_channel_revenue`, ordered by channel and period. |

### Tests & quality

- **dbt tests** (`models/**/*.yml`, `tests/`): column uniqueness, not-null, accepted values, and custom SQL tests (e.g. line-total calculation, mart grain).
- **pytest** (`python_tests/`): repo conventions—docs paired with models, `stg_` prefix on staging models, schema YAML beside every `.sql`.

## Quick start

```bash
pip install -r requirements.txt
dbt seed --target supabase
dbt run --target supabase
dbt test --target supabase
pytest -v
```

Use `dbt debug --target supabase` to verify the database connection. See `CLAUDE.md` for full project conventions.

## Agentic development (Claude skills)

This repo is set up for **ADLC**—agents follow project rules in `CLAUDE.md` (pre-flight requirements review, post-flight `dbt compile` / `dbt show`, and evals).

**Claude skill:** `.claude/skills/data-product-engineering/` guides agents on dbt modeling—`ref()` / `source()`, tests, documentation, and validation with `dbt show`. Reference guides cover:

| Guide | Topic |
|-------|--------|
| `writing-data-tests.md` | High-value dbt tests |
| `writing-model-documentation.md` | Model and column docs |
| `model-macro-naming-conventions.md` | Naming for models and macros |
| `reading-upstream-dataproducts.md` | Cross–data-product sources |
| `managing-packages.md` | dbt packages |
| `reverse-engineer-mart-model-requirements.md` | Mart `docs/` from staging models |

**Evals:** After model changes, run the skill eval suite:

```bash
python .claude/skills/data-product-engineering/evals/run_evals.py
```

Definitions live in `evals/evals.json`; see `evals/README.md` for details.

## CI

GitHub Actions (`.github/workflows/dbt-ci.yml`) runs **pytest** and **dbt** (seed, run, test) on push/PR to `main`.
