import duckdb

print(duckdb.sql("SELECT * FROM './fun/data/bankdataset.parquet'"))