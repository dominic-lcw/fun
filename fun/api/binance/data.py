from typing import Dict
import duckdb
import requests
from datetime import datetime

__all__ = ['get_btc_price', 'get_btc_historical_price', 'insert_historical_data']

def get_btc_price():
    response = requests.get('https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT')
    data = response.json()
    return data['price']

def get_btc_historical_price(interval='1d', limit=500):
    params = {'symbol': 'BTCUSDT', 'interval': interval, 'limit': limit}
    response = requests.get('https://api.binance.com/api/v3/klines', params=params)
    data = response.json()
    return data

def get_btc_table():
    """
    Get the BTC price and historical data and insert them into a DuckDB table
    """
    historical_data = get_btc_historical_price()
    duckdb.execute("CREATE TABLE IF NOT EXISTS btc_historical_data (riskdate DATE, open FLOAT, high FLOAT, low FLOAT, close FLOAT, volume FLOAT)")
    for entry in historical_data:
        timestamp = int(entry[0]) // 1000  # Convert milliseconds to seconds
        open_price = float(entry[1])
        high_price = float(entry[2])
        low_price = float(entry[3])
        close_price = float(entry[4])
        volume = float(entry[5])
        riskdate = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
        duckdb.execute("INSERT INTO btc_historical_data VALUES (?, ?, ?, ?, ?, ?)", (riskdate, open_price, high_price, low_price, close_price, volume))
    
    print(duckdb.execute("SELECT * FROM btc_historical_data").df())

if __name__ == "__main__":
    get_btc_table()

    # Local usage only
    duckdb.execute("COPY btc_historical_data TO '/Users/dominicleung/projects/ag-grid-duckdb-datasource/sample/public/btc_historical_data.parquet'")
