import duckdb
import pyarrow as pa

# get Q2 2023 to through april 2024 (latest available data)
trips_ls = []
months = [
    '2023-04',
    # '2023-05', 
    # '2023-06', 
    # '2023-07', 
    # '2023-08', 
    # '2023-09', 
    # '2023-10', 
    # '2023-11', 
    # '2023-12', 
    # '2024-01', 
    # '2024-02', 
    # '2024-03', 
    # '2024-04'
    ]
for month in months:
    table_path = f'https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{month}.parquet'
    table = duckdb.sql(f"SELECT * FROM '{table_path}'").arrow()
    trips_ls.append(table)
    print(f"Month {month} has {table.num_rows} rows")

# concatenate all tables
trips = pa.concat_tables(trips_ls)

duckdb.sql("COPY trips TO './fun/data/trips.parquet'")

print(trips.num_rows)