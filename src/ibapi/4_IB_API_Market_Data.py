# -*- coding: utf-8 -*-
"""
Created on Mon May 25 21:39:38 2020

@author: JAY

@doc: https://interactivebrokers.github.io/tws-api/md_request.html

@goal: Request live data from the TWS
"""

# Import necessary libraries
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.common import BarData

from threading import Timer
import datetime
import pandas as pd
import time
import psutil
import matplotlib.pyplot as plt
from itertools import count
import numpy as np
import sys





df = pd.DataFrame()
temp_df = pd.DataFrame(index=[0], columns=["datetime", 'reqid', 'bid-ask', 'position', "price"])

order_book = np.empty([5, 4])
order_book_story = []


# Define strategy class - inherits from EClient and EWrapper
class Strategy(EClient, EWrapper):

    # Initialize the class - and inherited classes
    def __init__(self):
        EClient.__init__(self, self)

    def tickPrice(self, reqId, tickType, price, attrib):
        self.time = datetime.datetime.now()
        print(f'Id: {reqId}, TickType: {tickType}, Price: {price},time:{self.time}')
        global temp_df, df
        temp_df.datetime = self.time
        temp_df.price = price
        df = df.append(temp_df)
        temp_df.to_csv("realtime_price.csv", mode='a', header=False)

    def updateMktDepth(self, reqId, position, operation, side, price, size):
        self.time = datetime.datetime.now()
        '''
        print(f'Id: {reqId}, bid-ask: {side}, Price: {price},position:{position}, \
        time:{self.time}')
        '''
        global temp_df, df
        temp_df.datetime = self.time
        temp_df.position = position
        temp_df.price = price
        temp_df.reqid = reqId
        temp_df['bid-ask'] = side
        df = df.append(temp_df)

        # temp_df.to_csv("realtime_price.csv" , mode = 'a',header = False)
        if side == 0:
            filler_price = 1
            filler_size = 0

        else:
            filler_price = 3
            filler_size = 2

        global order_book, order_book_story
        order_book[position][filler_price] = price
        order_book[position][filler_size] = int(size)

        order_book_story.append(order_book)
        print(order_book)

    def historicalData(self, reqId, bar):
        dictionary = {'Time': bar.date, 'Open': bar.open, 'Close': bar.close}
        # self.df = self.df.append(dictionary, ignore_index=True)
        print(f'Time: {bar.date}, Open: {bar.open}, Close: {bar.close}')




    '''
    def reqTickByTickData(self, reqId: int, contract: Contract, tickType: str,
                          numberOfTicks: int, ignoreSize: bool):
    '''
    ''' 
    def realtimeBar(self, reqId, time, open_, high, low, close,
                        volume, wap, count):
        print(f'Id: {reqId}, time: {time}, count: {count},open:{open}')
    '''

# -------------------------x-----------------------x---------------------------


def getHistoricalData():
    print("Fetching Historical Data")

getHistoricalData()


# Create object of the strategy class
app = Strategy()

# Connect strategy to IB TWS
app.connect(host='127.0.0.1', port=7496, clientId=11)
print(app.isConnected())
# Create object for contract

# all_contracts = ["KOTAKBANK","HDFCBANK","HDFC","LT","TECHM"]
all_contracts = ["GBP"] #,"EUR","NZD","AUD","KRW"]

print("Req ID")
int = app.nextValidId(10)
print(int)

# Request market data from the TWS
for i in range(len(all_contracts)):
    common_contract = Contract()
    common_contract.symbol = all_contracts[i]
    common_contract.currency = 'USD'
    common_contract.secType = 'CASH'
    common_contract.exchange = 'IDEALPRO'


    # app.reqMktData(reqId=i,
    #                contract=common_contract,
    #                genericTickList='',
    #                snapshot=False,
    #                regulatorySnapshot=False,
    #                mktDataOptions=[])


    # app.reqMktDepth(reqId=i,
    #                 contract=common_contract,
    #                 numRows=5,
    #                 isSmartDepth=False,
    #                 mktDepthOptions=None)

    app.reqHistoricalData(reqId=i,
                          contract=common_contract,
                          endDateTime='',
                          durationStr='600 S',
                          barSizeSetting='1 min',
                          whatToShow='MIDPOINT',
                          useRTH=0,
                          formatDate=1,
                          keepUpToDate=False,
                          chartOptions=[])



# Timer(10, app.cancelMktData, [reqId]).start()

# Invoke another thread that will disconnect the strategy from TWS
# Timer(20, app.disconnect()).start()

# Run the strategy
print("Running")
app.run()


'''
filtered_df = df[df['reqid']==1]

level_filter = filtered_df[filtered_df['position']==1]
'''
