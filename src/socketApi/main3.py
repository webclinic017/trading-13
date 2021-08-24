# -*- coding: utf-8 -*-
"""
Created on Thu Apr 15 23:11:35 2021

@author: micke
"""

import pandas as pd
#import mysql.connector

import csv
import copy

from kiteconnect import KiteConnect

from kiteconnect import exceptions
import pandas as pd

import nsepy

import time
import datetime

from nsepy.derivatives import get_expiry_date

from kiteconnect import KiteTicker
from datetime import date

import numpy as np

api_key = "rcpm0qsa3tuuflu5"
api_secret = "kt1ygk1sz3rfmsj6nazdxo7ac6y3f0s7"

kite = KiteConnect(api_key=api_key)

print(kite.login_url())
#request_token = "d8LmOgJOtrOc1RowH5ugfz8O7HS0m99n"
#data = kite.generate_session("d8LmOgJOtrOc1RowH5ugfz8O7HS0m99n", api_secret= api_secret)
#print(data)
#sys.exit()
# https://api.kite.trade/instruments
# https://kite.trade/connect/login?api_key=rcpm0qsa3tuuflu5&v=3

# access_token = "6HeAH4qvh0isfyu1xervWAs7vI7y4rF0"

kite.set_access_token("6tzvHAzUTmUDLj7xxOxlf2xOiXwLseyk")

YEAR = "21"
MONTH = "APR"
SEGMENT = "NFO:"

today = date.today()

expiry_date = get_expiry_date(year=today.year, month=today.month)

kws = KiteTicker(api_key, "6tzvHAzUTmUDLj7xxOxlf2xOiXwLseyk")

iv_df = pd.DataFrame(columns=['instrument_token', 'timestamp', 'last_price'])

temp = pd.DataFrame()

tokens = [57374727]
dict = {57374727: 'GOLD21AUGFUT'}


def on_ticks(ws, ticks):
    ticks = [dict[ticks[0]['instrument_token']], ticks[0]['timestamp'], ticks[0]['last_price']]
    #       temp['instrument_token']=ticks[0]['instrument_token']
    #       temp['time'] = ticks[0]['timestamp']
    #       temp['last_price'] = ticks[0]['last_price']
    print(ticks)
    global iv_df
    iv_df = iv_df.append(temp, ignore_index=True)


def on_connect(ws, response):
    ws.subscribe(tokens)
    ws.set_mode(ws.MODE_FULL, tokens)


kws.on_ticks = on_ticks
kws.on_connect = on_connect
kws.connect(threaded=True)
count = 0
while True:
    count += 1
    if (count % 2 == 0):
        if kws.is_connected():
            kws.set_mode(kws.MODE_FULL, tokens)
        else:
            if kws.is_connected():
                kws.set_mode(kws.MODE_FULL, tokens)
        time.sleep(0.350)

kws.close()
