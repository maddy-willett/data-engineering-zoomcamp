# Homework 3: Data Warehousing & BigQuery

## BigQuery Setup
I created an `external` & `regular` table using the Yellow Taxi Trip Records (i.e. not partitioned/clustered). Here is the SQL query I used to accomplish this: 
```sql
--- creating an external table referring to the gcs path
CREATE OR REPLACE EXTERNAL TABLE `nytaxiproject-492423.zoomcamp.hw3_yellow_external`
OPTIONS(
  format = 'Parquet',
  uris = ['gs://maddys_homework3_bucket/yellow_tripdata_2024-01.parquet', 'gs://maddys_homework3_bucket/yellow_tripdata_2024-02.parquet', 'gs://maddys_homework3_bucket/yellow_tripdata_2024-03.parquet', 'gs://maddys_homework3_bucket/yellow_tripdata_2024-04.parquet', 'gs://maddys_homework3_bucket/yellow_tripdata_2024-05.parquet', 'gs://maddys_homework3_bucket/yellow_tripdata_2024-06.parquet']
);

-- creating the a regular table
LOAD DATA OVERWRITE `nytaxiproject-492423.zoomcamp.hw3_yellow_regular`
FROM FILES (
  format = 'PARQUET',
  uris = ['gs://maddys_homework3_bucket/yellow_tripdata_2024-01.parquet', 'gs://maddys_homework3_bucket/yellow_tripdata_2024-02.parquet', 'gs://maddys_homework3_bucket/yellow_tripdata_2024-03.parquet', 'gs://maddys_homework3_bucket/yellow_tripdata_2024-04.parquet', 'gs://maddys_homework3_bucket/yellow_tripdata_2024-05.parquet', 'gs://maddys_homework3_bucket/yellow_tripdata_2024-06.parquet']
);
```

## Question 1: Counting records
The count of records for the 2024 Yellow Taxi Data is **20,332,093**. How did I get this? 
```sql
-- row count
SELECT 
  count(*) as row_count
FROM
  `nytaxiproject-492423.zoomcamp.hw3_yellow_external`;
```

## Question 2: Data read estimation
The **estimated amount** of data that will be read when I run the query to `count the distint number of PULocationIDs for the entire data` is **0 MB for the External Table and 155.12 MB for the Materialized Table**. There is 0MB for the external table due to the table being only referenced to the GCS bucket, it is not being managed by BigQuery. 

## Question 3: Understanding columnar storage
The estimated number of Bytes are different when I attempt to query the PULocationID from the regular table compared to when I attempt to query both the PULocationID & DOLocationID from the same table because **BigQuery is a columnar database, and it only scans the specific columns requested in the query. Querying two columns (PULocationID, DOLocationID) requires reading more data than querying one column (PULocationID), leading to a higher estimated number of bytes processed.**

## Question 4: Counting zero fare trips
The amount of records that have a fare_amount of 0 is **8,333**. How did I get this? 
```sql
SELECT
  count(*) as row_amount
FROM
  `nytaxiproject-492423.zoomcamp.hw3_yellow_regular`
WHERE
  fare_amount = 0;
```

## Question 5: Partitioning & clustering
The best strategy to make an optimized table in BigQuery if my query will always filter based on tpep_dropoff_datetime and order the results by VendorID is to **partition by tpep_dropoff_datetime and cluster on VendorID**

Here is the query to create this new table: 
```sql
CREATE OR REPLACE TABLE `nytaxiproject-492423.zoomcamp.hw3_yellow_pc`
PARTITION BY DATE(tpep_pickup_datetime)
CLUSTER BY VendorID AS 
SELECT * FROM `nytaxiproject-492423.zoomcamp.hw3_yellow_external`;
```

## Question 6: Partition benefits
Using the partitioned & clustered table now, the new estimated Byte size from question 3 is **310.24 MB for non-partitioned table and 26.84 MB for the partitioned table**. 

## Question 7: External table storage
When I create an External Table, the data is stored in the **GCP Bucket**.

## Question 8 Clustering best practices
False, it is not always best practice to cluster your data. This is due to the costs being unknown upfront. 

## Question 9: Understanding table scans
Querying an external table in BigQuery estimates **0 bytes** because it retrieves the total row count directly from the table's *metadata* instead of scanning individual data blocks. Since a materialized view is physically stored in BigQuery's managed storage, the engine can access these pre-calculated statistics instantly without "touching" any columns.