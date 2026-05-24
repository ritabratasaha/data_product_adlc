#!/usr/bin/env python3
"""Load evals.json, run each eval in order, print a results table."""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
while not (ROOT / "dbt_project.yml").is_file():
    ROOT = ROOT.parent

evals = json.loads((Path(__file__).parent / "evals.json").read_text())["evals"]
models_dir = ROOT / "models"
rows = []

for ev in evals:
    ok = True

    if ev["name"] == "ref-vs-source-conventions":
        for f in models_dir.rglob("*.sql") if models_dir.is_dir() else []:
            for line in f.read_text().splitlines():
                if re.search(r"\b(from|join)\s+", line, re.I) and "{{" not in line and "." in line:
                    ok = False

    for rule in ev.get("assertions", []):
        kind = rule.get("type")

        if kind == "contains":
            needle = rule["value"]
            for f in models_dir.rglob("*.sql") if models_dir.is_dir() else []:
                yml = f.with_suffix(".yml") if f.with_suffix(".yml").is_file() else f.with_suffix(".yaml")
                if not yml.is_file() or needle not in yml.read_text():
                    ok = False

        elif kind == "max_lines":
            limit = rule["value"]
            for f in models_dir.rglob("*.sql") if models_dir.is_dir() else []:
                if len(f.read_text().splitlines()) >= limit:
                    ok = False

        elif kind == "file_pair":
            for f in models_dir.rglob("*.sql") if models_dir.is_dir() else []:
                if not f.with_suffix(".yml").is_file() and not f.with_suffix(".yaml").is_file():
                    ok = False

        elif kind == "model_description":
            for f in models_dir.rglob("*.sql") if models_dir.is_dir() else []:
                layer = f.relative_to(models_dir).parts[0]
                doc = ROOT / "docs" / layer / f"{f.stem}.md"
                yml = f.with_suffix(".yml") if f.with_suffix(".yml").is_file() else f.with_suffix(".yaml")
                if not doc.is_file() or not yml.is_file() or "description:" not in yml.read_text():
                    ok = False
            macros_dir = ROOT / "macros"
            if macros_dir.is_dir():
                for f in macros_dir.glob("*.sql"):
                    if not (ROOT / "docs" / "macros" / f"{f.stem}.md").is_file():
                        ok = False
                    elif not f.read_text().lstrip().startswith("--"):
                        ok = False

    rows.append((ev["id"], ev["name"], "PASS" if ok else "FAIL"))

print(f"\n{'ID':<4}  {'Eval':<42}  {'Result':<6}\n{'-' * 56}")
for id_, name, result in rows:
    print(f"{id_:<4}  {name:<42}  {result:<6}")

passed = sum(r == "PASS" for _, _, r in rows)
print(f"\n{passed}/{len(rows)} passed\n")
sys.exit(0 if passed == len(rows) else 1)
