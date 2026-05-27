# Reverse engineer mart model requirements

Use this skill reference when the requirement is to reverse engineer and create a requirement markdown (model.md) for mart models from a staging model.

## Template to be used

# model name

Name of the model

# Overview

Description of the model

# Materialization

View or a Table

## Source

This model reads the data from stg_customer_sales. 

    |   Data Product        |        Data Object              | Model Layer      |
    |-----------------------|---------------------------------|------------------|
    |   data product name   |   stage data model              | /models/staging  |
    

## Grain

Replicate the staging model grain

## Join Logic

None

## Transformation Steps

None. It should be a select all columns from the staging model

## Filters

None

## Business Rules

None

## Projected Columns

List of columns that the model projects

## Data Quality Rules




