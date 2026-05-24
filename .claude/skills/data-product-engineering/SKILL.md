---
name: data-product-engineering
description: Builds and modifies dbt models for data products build on Snowflake, writes SQL transformations using ref() and source(), creates tests, and validates results with dbt show. Use when doing any dbt work - building or modifying models and macros, debugging errors, exploring unfamiliar data sources, writing tests, or evaluating impact of changes.
metadata:
  author: dataverse
---

# Using dbt for Analytics Engineering

**Core principle:** Apply software engineering discipline (DRY, modularity, testing) to data transformation work through dbt's abstraction layer.

## When to Use

- Building new dbt models, macros, sources, or tests for Snowflake
- Modifying existing model logic or configurations
- Refactoring a dbt project structure
- Creating analytics pipelines or data transformations
- Working with warehouse data that needs modeling
- To create macros for solving data engineering tasks


## Reference Guides

This skill includes detailed reference guides for specific techniques. Read the relevant guide when needed:

| Guide | Use When |
|-------|----------|
| [references/writing-data-tests.md](references/writing-data-tests.md) | Adding tests - prioritize high-value tests over exhaustive coverage |
| [references/writing-documentation.md](references/writing-documentation.md) | Write documentation that doesn't just restate the column name |
| [references/model-macro-naming-conventions.md](references/model-macro-naming-conventions.md)| Model and Macro naming conventions |
| [references/reading-upstream-dataproducts.md](references/reading-upstream-dataproducts.md) | Add upstream data product as sources when a data product reads from another data product |
| [references/managing-packages.md](references/managing-packages.md) | Installing and managing dbt packages |



**When users request new models:** Always ask "why a new model vs extending existing?" before proceeding. Legitimate reasons exist (different grain, precalculation for performance), but users often request new models out of habit. Your job is to surface the tradeoff, not blindly comply.

## Model building guidelines

- Common guidelines for model building
  - Refer to **`models/docs/staging/<model>.md`** or **`models/docs/marts/<model>.md`** (same basename as the `.sql` file) for business requirements.
  - If dependent models or macros are not present in the repo prompt the user to share their requirements.
  - Always use data modelling best practices when working in a project
  - If the model requirement asks to create a presentation layer, go ahead and create one.
  - For materialization follow the instructions in that requirements file. If materialization instruction is not provided, please use "view" as default in your plan.
  - The last layer of the models in the staging layer should be materialised as "table". This model should be used to create the mart view.
  - Follow dbt best practices in code:
    - Always use `{{ ref }}` and `{{ source }}` over hardcoded table names
    - Use CTEs over subqueries    
  - Apply SQL best practices
    - While applying conditional operator on a string column apply upper() on both sides of the equation
    - While applying the filters mentioned in the requirements `.md` file, treat each line item as "and" condition
    - While applying conditional operator on a date column apply the to_date funtion to be sure about the outcome
    - Always avoid cross join. Double check with the user if there are any such requirements
    - If your SQL has more than 5 CTEs then check with the user if it is ok to split the model for better code readability 
    - Avoid select * and consider adding column names. This helps to optimise the data volume that is processed by the sql
    - Consider applying filter as early as possible in the data flow so that the sql performance can improve
    - Do not materialise the marts/models as tables. They should be views reading the data from intermediate tables.
    - Do not use `select * from <model>`. Rather use `select [column names] from <model>`. Mention all the column names especially in the final CTE of a model.
      ```sql
            with final as (
              select 
                column1,
                column2,
                column2 
              from {{ ref('model_name') }}
            )
            Select 
              column1,
              column2,
              column2
            from final
            where 1=1
      ```
  - Conform to the existing style of a project (medallion layers, stage/intermediate/mart, etc)
  - Before adding a new model or column, always be sure that the same logic isn't already defined elsewhere that can be used.
  
- Building NEW model, read **`models/docs/<layer>/<model>.md`** to understand:
  - Functional / Business requirements
  - Once you have understood the requirment and the user has approved the plan, create the model.sql and model.yml file
  - Enable contract = true for all yml files
  - Add description of the columns to the best of you knowledge and let the developer validate the column descriptions 

- Before modifying or updating EXISTING models, read their existing YAML doc and **`models/docs/<layer>/<model>.md`**:
  - Find the model's YAML file (can be any `.yml` or `.yaml` file in the models directory, but normally colocated with the SQL file)
  - Check the model's `description` to understand its purpose
  - Read column-level `description` fields to understand what each column represents
  - Review any `meta` properties that document business logic or ownership
  - Review the existing requirements `.md` for the model and understand the full context
  - Once you have understood the exisiting logic search for the "Requirement Ledger" section based on the latest date to find for the most recent expected enhancements.
  - Suggest changes based on the most recent enhancement requirements.
  - Once user has approved the plan, update the model.sql and model.yml file
  - This context prevents misusing columns or duplicating existing logic

  
# Get Historical Context

Understanding how a dbt model has changed over time is crucial for making informed modifications or troubleshooting. For each dbt model `.md` file, you can gather historical context using the following approach:

- **Use `git blame` and `git log` on the model's `.md`, `.sql`, and `.yml` files** to see who made changes, what was changed, and when.
- This history will help you understand *why* a model or column exists, *when* business logic was added or modified, and the decision process over time.

## How to Get Historical Context for a dbt Model

**To get a concise report of how a dbt model evolved:**

1. **Identify the relevant files.**  
   - SQL / YAML (next to each other): `models/intermediate/my_model.sql`, `models/intermediate/my_model.yml` (or `models/marts/...`).  
   - Requirements / Requirement ledger: **`models/docs/intermediate/my_model.md`** or **`models/docs/marts/my_model.md`** (same basename as the model).
2. **Run `git blame` to see line-by-line authorship and change dates.**

   ```sh
   git blame models/path/to/my_model.sql
   git blame models/path/to/my_model.yml
   git blame models/docs/intermediate/my_model.md
   ```

3. **Run `git log` to see all commit messages related to the file.**

   ```sh
   git log --follow models/path/to/my_model.sql
   git log --follow models/path/to/my_model.yml
   git log --follow models/docs/intermediate/my_model.md
   ```

4. **Optional: See diffs for content change over time.**

   ```sh
   git log -p --follow models/path/to/my_model.sql
   ```

5. **Summarize and flow this context into your analysis.**  
   - Look for patterns in changes, such as repeated bug fixes, logic rewrites, or shifting business definitions.
   - Reference the commit messages and old code/description when discussing possible improvements or bugs.

**Use this skill when:**
- You want to understand *why* a dbt model or column exists.
- You've encountered confusing or undocumented logic.
- The business meaning or requirements are unclear from current documentation.
- Before proposing breaking changes or refactoring.

**Caution:**  
- Always supplement git history with business requirements in the **`models/docs/...` requirements file** and YAML docs.
- If commit messages are unclear, ask team members for oral history if possible.

This historical skill ensures that your model changes respect the context, avoid regressions, and support transparent communication with data stakeholders.



## Model building guidelines for marts

- Mart models should read from staging models using `{{ ref }}`
- Mart models should be materialised as views to ensure the consumer gets maximum througput
- These models should not have complex transformations. All transformations should be done in the staging layer

## Macro writing guidelines

- When using a date column from the database in any conditional operation with a date string,  always convert the date string to date datatype
- If there is a variable that is hardcoded, consider using a set variables within a macro using the Jinja {% set %} statement. 
 

## You must look at the data to be able to correctly model the data

When implementing a model, you must use `dbt show` regularly to:
  - preview the input data you will work with, so that you use relevant columns and values
  - preview the results of your model, so that you know your work is correct
  - run basic data profiling (counts, min, max, nulls) of input and output data, to check for misconfigured joins or other logic errors

## Handling external data


## dbt conventions (defaults)

Use the same **model basename** for the `.sql` file, the `.yml` file, and **`models/docs/<layer>/<model>.md`**.

## Common Mistakes and Red Flags

| Mistake | Fix |
|---------|-----|
| Assuming schema knowledge | Read the model.yml or model.yaml before writing SQL |
| Not reading existing model YAML docs | Read descriptions before modifying — column names don't reveal business meaning |
| Not reading the model's requirements file under `models/docs/` | Read `models/docs/intermediate/` or `models/docs/marts/` before modifying — column names don't reveal business meaning |
| Creating unnecessary models | Extend existing models when possible. Ask why before adding new ones — users request out of habit |
| Hardcoding table names | Always use `{{ ref() }}` and `{{ source() }}` |
| Running DDL directly against warehouse | Use dbt commands exclusively |

**STOP if you're about to:** write SQL without checking column names, modify a model without reading its YAML, skip `dbt show` validation, or create a new model when a column addition would suffice.
