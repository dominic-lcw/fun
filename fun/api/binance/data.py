from typing import Dict
import requests

__all__ = ['get_btc_price']

def get_btc_price():
    response = requests.get('https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT')
    data = response.json()
    return data['price']

def get_btc_historical_price(interval='1d', limit=500):
    params = {'symbol': 'BTCUSDT', 'interval': interval, 'limit': limit}
    response = requests.get('https://api.binance.com/api/v3/klines', params=params)
    data = response.json()
    return data

if __name__ == "__main__":
    print( get_btc_price() )