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
import time as t
import matplotlib.pyplot as plt
import numpy as np
import datetime


class IBRelay(EClient, EWrapper):

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

        self.df["Time"] = pd.to_datetime(self.df["Time"])
        self.df['E_Time'] = (((self.df["Time"]).astype('int64'))) // 1e5
        self.combo_dict[reqId] = self.df[["Time", "E_Time", "Close"]]
        self.df = pd.DataFrame()

    def tickByTickBidAsk(self, reqId, time, bidPrice, askPrice,
                         bidSize, askSize, tickAttribBidAsk):
        super().tickByTickBidAsk(reqId, time, bidPrice, askPrice, bidSize,
                                 askSize, tickAttribBidAsk)
        print("BidAsk. ReqId:", reqId,
              "Time:", datetime.datetime.fromtimestamp(time).strftime("%Y%m%d %H:%M:%S"),
              "BidPrice:", bidPrice, "AskPrice:", askPrice, "BidSize:", bidSize,
              "AskSize:", askSize, "BidPastLow:", tickAttribBidAsk.bidPastLow, "AskPastHigh:",
              tickAttribBidAsk.askPastHigh)

        self.current_time = int(t.time() / 60)

        if (self.combo_dict[reqId - 2]["Time"].iloc[-1] != self.current_time):
            self.combo_dict[reqId - 2] = self.combo_dict[reqId - 2].append(
                {'E_Time': self.current_time, 'Close': round((bidPrice + askPrice) / 2, 5)}, ignore_index=True)

        '''
        self.tick_df.datetime =  datetime.datetime.fromtimestamp(time).strftime("%Y/%m/%d %H:%M:%S.%f")
        self.tick_df.systemtime =  datetime.datetime.now()
        self.tick_df.reqid = reqId
        self.tick_df['bidprice'] = bidPrice
        self.tick_df['askprice'] = askPrice
        self.tick_df['bidSize'] = bidSize
        self.tick_df['askSize'] = askSize
        self.tck_df = self.tck_df.append(self.tick_df)
        '''


class IBWrapper(object):
    def __init__(self):
        self.df_hist = pd.DataFrame()
        self.local_app = IBRelay()
        self.combo_dict = {}
        self.reqid = 0

    def give_historical_data(self, inst, reqid, duration='1D', barsize='1 min'):
        self.local_app.reqHistoricalData(reqId=reqid,
                                         contract=inst,
                                         endDateTime='',
                                         durationStr='1 D',
                                         barSizeSetting=barsize,
                                         whatToShow='MIDPOINT',
                                         useRTH=0,
                                         formatDate=1,
                                         keepUpToDate=False,
                                         chartOptions=[])

    def give_tick_data(self, inst, reqid):
        self.local_app.reqTickByTickData(reqId=reqid,
                                         contract=inst,
                                         tickType='BidAsk',
                                         numberOfTicks=0,
                                         ignoreSize=True)

    def make_contract(self, symbol, currency="USD", secType="CASH", exchange="IDEALPRO"):
        self.instrument = Contract()
        self.instrument.symbol = symbol
        self.instrument.currency = currency
        self.instrument.secType = secType
        self.instrument.exchange = exchange
        return self.instrument

    def connect(self, host='127.0.0.1', port=7496, clientId=3):
        self.local_app.connect(host=host, port=port, clientId=clientId)

    def initialise(self, combo_list):
        for combo in combo_list:
            for instrument in combo:
                self.cont = self.make_contract(instrument)
                self.reqid += 1
                self.give_historical_data(self.cont, self.reqid)

    def start(self, combo_list):
        for combo in combo_list:
            for instrument in combo:
                self.cont = self.make_contract(instrument)
                self.reqid += 1
                self.give_tick_data(self.cont, self.reqid)
                t.sleep(10)










