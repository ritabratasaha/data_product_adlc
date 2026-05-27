"""
Rule-based pytest checks for dbt model and macro naming.

Each .sql file must pair with a requirements doc under docs/ using the
same basename (without the file extension).

Rules
-----
Staging (models/staging/*.sql)
    - Name must start with stg_
    - Must have docs/staging/<name>.md
      Example: stg_customer_sales.sql  <->  docs/staging/stg_customer_sales.md

Marts (models/marts/*.sql)
    - Name must not start with marts_
    - Must have docs/marts/<name>.md
      Example: monthly_revenue.sql  <->  docs/marts/monthly_revenue.md

Macros (macros/*.sql)
    - Must have docs/macros/<name>.md
      Example: cents_to_dollars.sql  <->  docs/macros/cents_to_dollars.md

Run from the sales_data_product directory:

    pytest python_tests/test_naming_conventions.py -v
"""

from pathlib import Path

# sales_data_product/ (parent of python_tests/)
ROOT = Path(__file__).resolve().parent.parent


def _sql_stems(folder: Path) -> list[str]:
    """Basenames of .sql files in folder (e.g. stg_customer_sales)."""
    return [p.stem for p in folder.glob("*.sql")] if folder.is_dir() else []


def _doc_stems(folder: Path) -> set[str]:
    """Basenames of .md files in folder (e.g. stg_customer_sales)."""
    return {p.stem for p in folder.glob("*.md")} if folder.is_dir() else set()


def test_staging_models():
    """
    Every staging model must:
    - start with stg_
    - have a matching doc at docs/staging/<model_name>.md
    """
    models = ROOT / "models" / "staging"
    docs = _doc_stems(ROOT / "docs" / "staging")
    errors = []

    for name in _sql_stems(models):
        if not name.startswith("stg_"):
            errors.append(f"{name}: must start with stg_")
        if name not in docs:
            errors.append(f"{name}: missing docs/staging/{name}.md")

    assert not errors, "\n".join(errors)


def test_mart_models():
    """
    Every mart model must:
    - not start with marts_
    - have a matching doc at docs/marts/<model_name>.md
    """
    models = ROOT / "models" / "marts"
    docs = _doc_stems(ROOT / "docs" / "marts")
    errors = []

    for name in _sql_stems(models):
        if name.startswith("marts_"):
            errors.append(f"{name}: must not start with marts_")
        if name not in docs:
            errors.append(f"{name}: missing docs/marts/{name}.md")

    assert not errors, "\n".join(errors)


def test_macros():
    """
    Every macro must have a matching doc at docs/macros/<macro_name>.md.
    """
    macros = ROOT / "macros"
    docs = _doc_stems(ROOT / "docs" / "macros")
    errors = []

    for name in _sql_stems(macros):
        if name not in docs:
            errors.append(f"{name}: missing docs/macros/{name}.md")

    assert not errors, "\n".join(errors)
