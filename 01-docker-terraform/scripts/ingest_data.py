#!/usr/bin/env python
# coding: utf-8

import click
import pandas as pd
from sqlalchemy import create_engine
from tqdm.auto import tqdm
import sys

dtype = {
    "VendorID": "Int64",
    "passenger_count": "Int64",
    "trip_distance": "float64",
    "RatecodeID": "Int64",
    "store_and_fwd_flag": "string",
    "PULocationID": "Int64",
    "DOLocationID": "Int64",
    "payment_type": "Int64",
    "fare_amount": "float64",
    "extra": "float64",
    "mta_tax": "float64",
    "tip_amount": "float64",
    "tolls_amount": "float64",
    "improvement_surcharge": "float64",
    "total_amount": "float64",
    "congestion_surcharge": "float64"
}

parse_dates = [
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime"
]

def df_transform(df): ## to dynamically find date columns if the names are not matching
    date_cols = [c for c in df.columns if 'datetime' in c]
    for col in date_cols:
        df[col] = pd.to_datetime(df[col])
    return df 

def ingest_data(url: str, engine, target_table: str, chunksize: int = 100000) -> None:
    is_parquet = url.endswith('.parquet')
    print(f"Detected {'Parquet' if is_parquet else 'CSV'} format.")

    if is_parquet: 
        try: 
            df = pd.read_parquet(url)
            df = df_transform(df)

            #create a table and insert all at once
            df.head(0).to_sql(name = target_table, con = engine, if_exists = "replace")
            df.to_sql(name = target_table, con = engine, if_exists = "append")
            print(f"Successfully ingested {len(df)} rows from Parquet.")
        except Exception as e:
            print(f"Error processing Parquet: {e}")
            sys.exit(1)
    else: 
            is_taxi = any(x in url for x in ["yellow", "green"])
            df_iter = pd.read_csv(url, dtype = dtype if is_taxi else None, iterator = True, chunksize = chunksize, low_memory = False)

            try: 
                first_chunk = next(df_iter)
                first_chunk = df_transform(first_chunk)

                #create table with schema for first chunk
                first_chunk.head(0).to_sql(name = target_table, con = engine, if_exists = "replace")
                print(f"Table {target_table} created/reset.")

                #insert first chunk into table
                first_chunk.to_sql(name = target_table, con = engine, if_exists = "append")
                print(f"Inserted first chunk: {len(first_chunk)} rows")

                #iterate through the rest of the file
                for df_chunk in tqdm(df_iter):
                     df_chunk = df_transform(df_chunk)
                     df_chunk.to_sql(name = target_table, con = engine, if_exists = "append")
                
            except StopIteration:
                 print("File was empty or only contained a header.")
            except Exception as e:
                 print(f"Error during CSV ingestion: {e}")

    print(f'Done ingesting to {target_table}')

# adding CLI input from user using click
@click.command()
@click.option('--pg-user', default='root', help='PostgreSQL username')
@click.option('--pg-pass', default='root', help='PostgreSQL password')
@click.option('--pg-host', default='localhost', help='PostgreSQL host')
@click.option('--pg-port', default='5432', help='PostgreSQL port')
@click.option('--pg-db', default='ny_taxi', help='PostgreSQL database name')
@click.option('--year', default=2021, type=int, help='Year of the data')
@click.option('--month', default=1, type=int, help='Month of the data')
@click.option('--chunksize', default=100000, type=int, help='Chunk size for ingestion')
@click.option('--target-table', default='yellow_taxi_data', help='Target table name')
@click.option('--url', default=None, help='Direct URL to a CSV or Parquet file')

def main(pg_user, pg_pass, pg_host, pg_port, pg_db, year, month, url, chunksize, target_table):
     #creating the SQLAlchemy engine
    engine = create_engine(f'postgresql://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}')

     #default to Yellow Taxi 2021-01 CSV if no URL is provided
    if not url: 
        url_prefix = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow'
        url = f'{url_prefix}/yellow_tripdata_{year:04d}-{month:02d}.csv.gz'

    print(f"Starting ingestion process for: {url}")

    ingest_data(
        url=url,
        engine=engine,
        target_table=target_table,
        chunksize=chunksize
    )

if __name__ == '__main__':
    main()
     





