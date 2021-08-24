# -*- coding: utf-8 -*-
"""
Created on Wed Jun 30 18:49:44 2021

@author: micke
"""
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from threading import Timer
import pandas as pd
import time
import matplotlib.pyplot as plt
import numpy as np
import datetime


class IBRelay(EClient, EWrapper):
    # Native classes
    def __init__(self):
        EClient.__init__(self, self)
        self.df = pd.DataFrame()
        self.tick_df = pd.DataFrame(index=[0],
                                    columns=["datetime", "systemtime", 'reqid', "bidprice", "askprice", "bidSize",
                                             "askSize"])
        self.tck_df = pd.DataFrame()
        self.combo_dict = {}

    def historicalData(self, reqId, bar):
        dictionary = {'Time': bar.date, 'Open': bar.open, 'High': bar.high, 'Low': bar.low, 'Close': bar.close}
        self.df = self.df.append(dictionary, ignore_index=True)
        print(f'Time: {bar.date}, Open: {bar.open}, Close: {bar.close}')

    # Display a message once historical data is retreived
    def historicalDataEnd(self, reqId, start, end):
        print('\nHistorical Data Retrieved\n')
        print(self.df.head())
        self.combo_dict[reqId] = self.df
        self.df = pd.DataFrame()

    def tickByTickBidAsk(self, reqId, time, bidPrice, askPrice,
                         bidSize, askSize, tickAttribBidAsk):
        super().tickByTickBidAsk(reqId, time, bidPrice, askPrice, bidSize,
                                 askSize, tickAttribBidAsk)
        # print("BidAsk. ReqId:", reqId,
        #      "Time:", datetime.datetime.fromtimestamp(time).strftime("%Y%m%d %H:%M:%S"),
        #     "BidPrice:", bidPrice, "AskPrice:", askPrice, "BidSize:", bidSize,
        #      "AskSize:", askSize, "BidPastLow:", tickAttribBidAsk.bidPastLow, "AskPastHigh:", tickAttribBidAsk.askPastHigh)
        print("Receiving Tick data")
        self.tick_df.datetime = datetime.datetime.fromtimestamp(time).strftime("%Y/%m/%d %H:%M:%S.%f")
        self.tick_df.systemtime = datetime.datetime.now()
        self.tick_df.reqid = reqId
        self.tick_df['bidprice'] = bidPrice
        self.tick_df['askprice'] = askPrice
        self.tick_df['bidSize'] = bidSize
        self.tick_df['askSize'] = askSize
        self.tck_df = self.tck_df.append(self.tick_df)

    def reqTickByTickData(self, reqId, contract, tickType, numberOfTicks, ignoreSize):
        print(reqId)
        print(numberOfTicks)