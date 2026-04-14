SELECT passenger_count, trip_distance, PULocationID, DOLocationID, payment_type, fare_amount, tolls_amount, tip_amount
FROM `nytaxiproject-492423.zoomcamp.yellow_tripdata` WHERE fare_amount != 0;

-- CREATE A ML TABLE WITH APPROPRIATE TYPE
CREATE OR REPLACE TABLE `nytaxiproject-492423.zoomcamp.yellow_tripdata_ml` (
`passenger_count` INTEGER,
`trip_distance` FLOAT64,
`PULocationID` STRING, -- casting these to identify the category feature(s), preprocessing step
`DOLocationID` STRING, -- casting these to identify the category feature(s), preprocessing step
`payment_type` STRING, -- casting these to identify the category feature(s), preprocessing step
`fare_amount` FLOAT64,
`tolls_amount` FLOAT64,
`tip_amount` FLOAT64
) AS (
SELECT passenger_count, trip_distance, cast(PULocationID AS STRING), CAST(DOLocationID AS STRING),
CAST(payment_type AS STRING), fare_amount, tolls_amount, tip_amount
FROM `nytaxiproject-492423.zoomcamp.yellow_tripdata` WHERE fare_amount != 0
);

-- CREATE MODEL WITH DEFAULT SETTING
CREATE OR REPLACE MODEL `nytaxiproject-492423.zoomcamp.tip_model`
OPTIONS
(model_type='linear_reg',
input_label_cols=['tip_amount'], -- y label
DATA_SPLIT_METHOD='AUTO_SPLIT') AS -- split to test/train
SELECT
*
FROM
`nytaxiproject-492423.zoomcamp.yellow_tripdata_ml`
WHERE
tip_amount IS NOT NULL;

-- CHECK FEATURES
SELECT * FROM ML.FEATURE_INFO (MODEL `nytaxiproject-492423.zoomcamp.tip_model`); -- similar to .describe() in python

-- EVALUATE THE MODEL
SELECT
*
FROM
ML.EVALUATE(MODEL `nytaxiproject-492423.zoomcamp.tip_model`,
(
SELECT
*
FROM
`nytaxiproject-492423.zoomcamp.yellow_tripdata_ml`
WHERE
tip_amount IS NOT NULL
));

-- PREDICT THE MODEL
SELECT
*
FROM
ML.PREDICT(MODEL `nytaxiproject-492423.zoomcamp.tip_model`,
(
SELECT
*
FROM
`nytaxiproject-492423.zoomcamp.yellow_tripdata_ml`
WHERE
tip_amount IS NOT NULL
));

-- PREDICT AND EXPLAIN
SELECT
*
FROM
ML.EXPLAIN_PREDICT(MODEL `nytaxiproject-492423.zoomcamp.tip_model`,
(
SELECT
*
FROM
`nytaxiproject-492423.zoomcamp.yellow_tripdata_ml`
WHERE
tip_amount IS NOT NULL
), STRUCT(3 as top_k_features));

-- HYPER PARAM TUNNING
CREATE OR REPLACE MODEL `nytaxiproject-492423.zoomcamp.tip_model`
OPTIONS
(model_type='linear_reg',
input_label_cols=['tip_amount'],
DATA_SPLIT_METHOD='AUTO_SPLIT',
num_trials=5,
max_parallel_trials=2,
l1_reg=hparam_range(0, 20),
l2_reg=hparam_candidates([0, 0.1, 1, 10])) AS
SELECT
*
FROM
`nytaxiproject-492423.zoomcamp.yellow_tripdata_ml`
WHERE
tip_amount IS NOT NULL;
