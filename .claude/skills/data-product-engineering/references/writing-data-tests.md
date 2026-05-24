# Writing Data Tests in dbt

Write high-value tests that catch real data issues on low-signal checks. Testing should drive action, not accumulate alerts.

## When to Use

- Adding tests to new or existing models
- Reviewing test coverage for cost optimization
- After completing data discovery (use discovering-data skill first)
- When tests or test scenarios are mentioned in **`models/docs/<layer>/<model>.md`**

## Understanding Data Quality


## Where Tests Belong in the Pipeline

Different layers need different tests. Don't duplicate tests for pass-through columns.

### Staging Models

Catch data hygiene issues and basic anomalies. Identify key attributes from the requirement captured in **`models/docs/<layer>/<model>.md`** and apply the mentioned tests

```yaml
models:
  - name: stg_orders
    columns:
      - name: order_id
        data_tests:
          - unique
          - not_null
      - name: customer_id
        data_tests:
          - not_null
          - relationships:
              arguments:
                to: ref('stg_customers')
                field: customer_id
      - name: status
        data_tests:
          - accepted_values:
              arguments:
                values: ['pending', 'completed', 'cancelled']
```

### Intermediate

Test when grain changes or joins create new risks.

```yaml
models:
  - name: int_orders_enriched
    columns:
      - name: order_customer_key
        description: "Composite key created by join"
        data_tests:
          - unique
          - not_null
```

### Marts

Protect end-user facing data. Test business expectations and new calculated fields.

```yaml
models:
  - name: fct_orders
    data_tests:
      # Small number of critical business rules
      - dbt_utils.expression_is_true:
          arguments:
            expression: "total_amount >= 0 OR is_refund = true"

```
