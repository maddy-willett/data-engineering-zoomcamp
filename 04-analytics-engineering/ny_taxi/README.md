# My New York Taxi Data dbt Project & Notes 

## What is the structure of a dbt project? 

```
- 04-analytics-engineering
|
-- logs/
-- ny_taxi/
    |
    -- analysis/ 
    -- macros/ 
    -- models/ 
    -- seeds/ 
    -- snapshots/ 
    -- tests/ 
    -- .gitignore
    -- dbt_project.yml
-- scripts/
    |
    -- python_ingestion_mod4.py
```

## Analysis folder

* A place for SQL files that you don't want to expose
* Generally used for data quality purposes (not used frequently)

## Macros folder

* They behave like Python functions (resuable logic) (e.g. UDFs)
* They help you encapsulate logic (in one place)

## Models folder

* dbt suggests 3 subfolders: 
    ### staging
    * Sources (i.e. raw table from database)
    * Staging files are 1 to 1 copy of your data with minimal cleaning steps (not for heavy duity cleaning)
        * ex: data type conversions, renaming columns, etc.

    ### intermediate
    * Anything that is not raw nor ready to be exposed
    * No guidelines, just nice for heavy duty cleaning or complex logic

    ### marts
    * If it is in marts, it is ready for consumption
    * Tables ready for dashboards
    * Properly modeled, clean tables, star schemas

## Seeds folder

* A space to upload csv and flat files (to add them to dbt later)
* Quick and dirty approach (better to fix at source)

## Snapshots folder

 * Take a picture of a table at a moment in time
 * Useful to track the history of a column that overwrites itself (like status)

## Test folder

 * A place to put assertions in SQL format
 * A place for singular tests
 * If this SQL command returns more than 0 rows, the dbt build fails (e.g. if the sum of a percentage column is > 100, then this will alert the error)

## dbt_project.yml file

 * The backbone of the sbt project
 * Define global objects / variables / defaults 
 * Project names, datasets, profiles, etc.

# Dimensinal Modeling 
The goal os Kimball's framework is to make the data **understandable to business users** and make **queries fast/optimal**. Unlike third nominal form (3NF), dimensional modeling deliberately allows some data redundancy. The priority is usability and performance, not eliminating duplication. 

## Face Tales (fct) vs. Dimensional Tables (dim) (aka Star Schema)
* **Face tables** - measurements, metrics, business events, think of these are *verbs*. For example, "A sale happened", "An order was placed". They correspond to a business process. (one row per dimension)
* **Dimension tables** - the context around those facts, think of these as *nouns*. For example: "Who bought it? Which product? When?". They correspond to a business entity like a customer or a product. (attributes of an entity)
Together they form the **star schema** - the fact table in the center, dimension tables radiating out around it. It is the classic layout you'll see in mot data warehouses. 

 ## Resources
 [Analytics Engineering Lectures]{https://github.com/DataTalksClub/data-engineering-zoomcamp/tree/main/04-analytics-engineering}