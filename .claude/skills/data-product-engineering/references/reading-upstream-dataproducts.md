# Reading upstream data products

While building a data product we may need to read the marts schema of the upstream data product.
A data product often equals to a snowflake database in Dataverse
If the requirements of the models needs you to read tables from upstream data product then update the source.yml file in /models/staging directory
Here is a sample of a good source.yml

```yml

version: 2
sources:
  - name: bookingsmaster_models
    database: bookingsmaster_db
    schema: marts
    tables:
      - name: icm_dtbookings
      - name: icm_dtopportunity
  - name: renewals_models
    database: renewals_db
    schema: marts
    tables:
      - name: core_global_renewal_potential

```


