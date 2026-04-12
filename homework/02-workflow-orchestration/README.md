# Quiz Questions
--

## Question 1: 
Within the execution for `Yellow` Taxi data for the year `2020` and month `12`: the uncompressed file size (i.e. the output file `yellow_tripdata_2020-12.csv` of the `extract` task is: **128.3MiB**

**How did I get this?** After loading the data into my GCS with Kestra, I went into the execution tab then the `extract` task and checked the outputs which contained the uncompressed file size. 

## Question 2:
The rendered valye of the variable `file` when the inputs `taxi` is set to `green`, `year` is set to `2020`, and `month` is set to `04` is: **`green_tripdata_2020-04.csv`**

## Question 3: 
For the `Yellow` Taxi dataset for all CSV files in the year 2020, there are **24,648,499** rows. 

**How did I get this?** After loading in all the 2020 data, I queried the row count in BigQuery.

```sql
select 
  count(*)
from 
  `zoomcamp.yellow_tripdata`
where
  filename like '%2020%'
```

## Question 4:
For the `Green` Taxi dataset for all CSV files in the year 2020, there are **1,734,051** rows. 

**How did I get this?** After loading in all the 2020 data, I queried the row count in BigQuery.

```sql
select 
  count(*)
from 
  `zoomcamp.green_tripdata`
where
  filename like '%2020%'
```

## Question 5: 
For the `Yellow` Taxi dataset for all CSV files in March of 2021, there are **1,925,152** rows. 

**How did I get this?** After loading in all the 2020 data, I queried the row count in BigQuery.

```sql
select 
  count(*)
from 
  `zoomcamp.yellow_tripdata`
where
  filename like '%2021-03%'
```

## Question 6: 
I would configure the timezone to New York in a Schedule trigger by **adding a `timezone` property set to `America/New_York` in the `Schedule` trigger configuration.**

```yaml
triggers:
  - id: green_schedule
    type: io.kestra.plugin.core.trigger.Schedule
    cron: "0 9 1 * *"
    timezone: America/New_York
    inputs:
      taxi: green
```