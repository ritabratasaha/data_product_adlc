# Evaluation suite

## Run all evals

```bash
cd sales_data_product
conda activate dbtenv
python .claude/skills/data-product-engineering/evals/run_evals.py
```

Loads [evals.json](evals.json), runs every eval in order (driven by `assertions[].type` in the JSON), prints a results table. Exit code `0` if all pass.

## Files

| File | Purpose |
|------|---------|
| [evals.json](evals.json) | Eval definitions and agent prompts |
| [run_evals.py](run_evals.py) | Loads evals, runs checks, prints the results table |

## Agent review

For manual scoring (process, style, efficiency), use the `prompt` arrays in `evals.json` with Claude or your eval harness.
