# Module 1 Homework: Docker & SQL (Answers & Explainations)

### Question 1. Understanding Docker images

When running a docker image with the `python:3.13` image and the entrypoint set to `bash`, the version of `pip` in the image is: **pip 25.3**

How did I do this? 
* First I ran the command `docker run -it --entrypoint=bash python:3.13` which starts an interactive container from the `python:3.13` image and overrides the default command to open in a Bash shell. 
* Second I ran the command `pip --version` which then prints the version of `pip` installed inside the container!


### Question 2. Understanding Docker networking and docker-compose

Given the following `docker-compose.yaml`, the `hostname` and `port` that pgadmin should use to connect to the postgres database is: **db:5432**

How did I get this? 
* This section of the `docker-compose.yaml` file is where the answer to this question reside: 

```yaml
services:
  db: 
    container_name: postgres
    image: postgres:17-alpine
    environment:
      POSTGRES_USER: 'postgres'
      POSTGRES_PASSWORD: 'postgres'
      POSTGRES_DB: 'ny_taxi'
    ports:
      - '5433:5432'
    volumes:
      - vol-pgdata:/var/lib/postgresql/data
```

The *hostname* is db because it's the service name defined at the top "db:". For the *port*, `5432` is used because `pgadmin` is inside the same Docker network as the database. It connects to the *Contaier port* (the right side of `5433:5432`) rather than the *Host port* (`5433`) used by my phsical machine.


### Question 3. Counting short trips (& ingesting a new dataset)

Answer: **8,007**

The process to ingesting the new green_taxi & zone datasets into my pgAdmin account is shown below: 
* First, ensuring my Docker container is running (I do this by running this command `docker-compose up -d` inside the *config* folder)
    * This then runs the container that starts both the `5432` & `8085` ports for the pgAdmin local web app
* Then I run the ingestion script and provide the urls for both new datasets to be loaded into the pgAdmin interface. (below is the provided command with the provided user variables which is run inside the *scripts* folder)
    ``` bash 
    python ingest_data.py \   
    --pg-user=root \   
    --pg-pass=root  \ 
    --pg-db=ny_taxi \
    --pg-host=localhost \  
    --pg-port=5432 \
    --target-table=green_taxi_data \  
    --url="https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2025-11.parquet"
  ```
* Lastly, now that the data is all ingested into the pgAdmin space, the SQL query to answer how many trips had a `trip_distance` of less than or equal to 1 mile (ith a lpep_pickup_datetime between '2025-11-01' and '2025-12-01', exclusive of the upper bound):
    ``` sql
    select 
	    count(index) as trip_count
    from 
	    green_taxi_data
    where
	    lpep_pickup_datetime >= '2025-11-01' 
	    and lpep_pickup_datetime < '2025-12-01'
	    and trip_distance <= 1.0;
    ```

### Question 4. Longest trip for each day
The pick up day with the longest trip distance (only including trips with `trip_distance` less than 100 miles) was: **2025-11-14**

Here is the query to answer this:
``` sql 
  with longest_trip as (
select 
	date_trunc('day', lpep_pickup_datetime) as pickup_day,
	trip_distance
from 
	green_taxi_data
where
	trip_distance < 100
)

select 
	pickup_day
from 
	longest_trip
order by
	trip_distance desc
limit 1;
```

### Question 5. Biggest pickup zone
The pickup zone with the largest `total_amount` (aka sum of all trips) on 2025-11-18 was: **East Harlem North**

Here is the query to answer this: 
``` sql
select
  z."Zone",
  sum(g.total_amount) as total_amount_sum
from 
  green_taxi_data g iner join zones z on g."PULocationID" = z."LocationID"
where 
  cast(g.lpep_pickup_datetime as date) = '2025-11-18'
group by 
  z."Zone"
order by 
  total_amount_sum desc
limit 1;
```

### Question 6. Largest tip
For the passengers picked up in East Harlem North on 2025-11-18, the drop off zone that had the largest tip was: **Yorkville West**

Here is the query to get this answer:
``` sql
select
  z_do."Zone" as dropoff_zone,
   g.tip_amount
from 
  green_taxi_data g inner join zones z_pu on g."PULocationID" = z_pu."LocationID"
  inner join zones z_do on g."DOLocationID" = z_do."LocationID"
where 
  z_pu."Zone" = 'East Harlem North'
  and g.lpep_pickup_datetime >= '2025-11-01'
  and g.lpep_pickup_datetime < '2025-12-01'
order by 
  g.tip_amount desc
limit 1;
```

### Question 7. Terraform Workflow
The sequence for 1) Downloading the provider plugins and setting up backend, 2) Generating proposed changes and auto-executing the plan, and 3) Remove all resources managed by terraform is:

`terraform innit`, `terraform apply -auto-apply`, `terraform destroy` (you can use `terraform plan` to help visualize all what you're asking for before deploying to your cloud provider.) 