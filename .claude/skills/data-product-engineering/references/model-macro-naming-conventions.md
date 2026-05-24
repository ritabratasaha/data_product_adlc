# Naming models and macros

Follow these naming conventions while naming the models and macros

- Naming conventions
  - staging models should start with prefix `stg_*`
  - mart models have no prefix 
    - If it has a corresponding `/docs/marts/<model>.md` then use that name. 
    - If it does not have a corresponding `/docs/marts/<model>.md` and is created directly from the staging model then remove `stg_` prefix and use the rest of the business name
  - macro names should match with the macro.md file in `/docs/macros/<macro.md>` 