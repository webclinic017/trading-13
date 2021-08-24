import os
import sys


import requests

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=CRYPTO_INTRADAY&symbol=ETH&market=USD&interval=5min&datatype=csv&apikey=75C9100OJGINJSD5'
r = requests.get(url)
#data = r.json()

print(str(r.content.decode("utf-8")))
