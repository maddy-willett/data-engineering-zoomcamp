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