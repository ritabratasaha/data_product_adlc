"""
Check that every dbt model has a schema .yml or .yaml file.

Rule
----
For each models/**/*.sql file, there must be a matching .yml or .yaml
in the same folder with the same basename.

Example:
    models/staging/stg_customer_sales.sql
    models/staging/stg_customer_sales.yml

Run from the sales_data_product directory:

    pytest python_tests/test_model_schema_yaml.py -v
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def test_models_have_schema_yaml():
    """
    Every dbt model .sql under models/ must have a matching .yml or .yaml
    in the same directory.
    """
    errors = []

    for sql_file in (ROOT / "models").rglob("*.sql"):
        stem = sql_file.stem
        folder = sql_file.parent
        has_yaml = (folder / f"{stem}.yml").is_file() or (folder / f"{stem}.yaml").is_file()
        if not has_yaml:
            rel = sql_file.relative_to(ROOT)
            errors.append(f"{rel}: missing {stem}.yml or {stem}.yaml")

    assert not errors, "\n".join(errors)
