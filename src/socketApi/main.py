# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import pandas as pd

import csv
import copy
from kiteconnect import KiteConnect
from kiteconnect import exceptions
import pandas as pd


import time
import datetime

from kiteconnect import KiteTicker
from datetime import date
import numpy as np
from nsepy.derivatives import get_expiry_date

def main(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.
    api_key = "rcpm0qsa3tuuflu5"
    from kiteconnect import KiteConnect
    kite = KiteConnect(api_key="rcpm0qsa3tuuflu5")
    kite.login_url()

    #user = kite.request_access_token(request_token="6ipFDL1i1vxyLGq4p6q89gtG3LGJ3eGp",
    #                                 secret="kt1ygk1sz3rfmsj6nazdxo7ac6y3f0s7")

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














# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
