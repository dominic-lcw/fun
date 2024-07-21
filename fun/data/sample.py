import duckdb

print(duckdb.execute("SELECT * FROM './fun/data/bankdataset.parquet'").df())