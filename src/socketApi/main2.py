# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import pandas as pd

import csv
import copy
from kiteconnect import KiteConnect
from kiteconnect import exceptions
import pandas as pd

import sys
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

    #kite = KiteConnect(api_key=api_key)
    #https://kite.trade/connect/login?api_key=rcpm0qsa3tuuflu5&v=3

    # Redirect the user to the login url obtained
    # from kite.login_url(), and receive the request_token
    # from the registered redirect url after the login flow.
    # Once you have the request_token, obtain the access_token
    # as follows.

    #data = kite.generate_session("45ULLlmNYysCypdrzZF8qS2YUZ51qwHd", api_secret="kt1ygk1sz3rfmsj6nazdxo7ac6y3f0s7")
    #kite.set_access_token("nWVNW7D4UX73rpqwa2Flvs5UWkYTvGgU")

    import logging
    from kiteconnect import KiteConnect

    logging.basicConfig(level=logging.DEBUG)

    kite = KiteConnect(api_key=api_key)

    # Redirect the user to the login url obtained
    # from kite.login_url(), and receive the request_token
    # from the registered redirect url after the login flow.
    # Once you have the request_token, obtain the access_token
    # as follows.

    data = kite.generate_session("edZSb8lLp1qo626DGGLHpqb76Ks57cHN", api_secret="kt1ygk1sz3rfmsj6nazdxo7ac6y3f0s7")
    print(data)
    sys.exit()
    kite.set_access_token("dLFK4fWx1ITARGRxausj7DPR3XHTnk3Y")

    print(kite)
    #sys.exit()

    #print(kite.instruments())
    print(kite.quote("NSE:INFY"))

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main('PyCharm')

