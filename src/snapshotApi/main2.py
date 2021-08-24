# -*- coding: utf-8 -*-
"""
Created on Mon May 25 19:36:13 2020

@author: JAY

@doc: http://interactivebrokers.github.io/tws-api/historical_bars.html

@goal: Fetch historical data of a financial instrument
"""

# Import necessary libraries
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from threading import Timer
import pandas as pd


# Define strategy class - inherits from EClient and EWrapper
class Strategy(EClient, EWrapper):

    # Initialize the class - and inherited classes
    def __init__(self):
        EClient.__init__(self, self)
        self.df = pd.DataFrame(columns=['Time', 'Open', 'Close'])

    # Receive historical bars from TWS
    def historicalData(self, reqId, bar):
        dictionary = {'Time': bar.date, 'Open': bar.open, 'Close': bar.close}
        self.df = self.df.append(dictionary, ignore_index=True)
        print(f'Time: {bar.date}, Open: {bar.open}, Close: {bar.close}')

    # Display a message once historical data is retreived
    def historicalDataEnd(self, reqId, start, end):
        print('\nHistorical Data Retrieved\n')
        print(self.df.head())


# -------------------------x-----------------------x---------------------------

# Create object of the strategy class
app = Strategy()

# Connect strategy to IB TWS
app.connect(host='127.0.0.1', port=7496, clientId=10)
print(app.isConnected())

# Create object for contract
eurusd_contract = Contract()
eurusd_contract.symbol = 'EUR'
eurusd_contract.currency = 'USD'
eurusd_contract.secType = 'CASH'
eurusd_contract.exchange = 'IDEALPRO'

# Request for historical data
app.reqHistoricalData(reqId=30,
                      contract=eurusd_contract,
                      endDateTime='',
                      durationStr='60000 S',
                      barSizeSetting='1 min',
                      whatToShow='MIDPOINT',
                      useRTH=0,
                      formatDate=1,
                      keepUpToDate=False,
                      chartOptions=[])


# Run the strategy
app.run()