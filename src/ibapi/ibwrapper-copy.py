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
import sys

def f(x):
    if int(x) >= 21:
        y = 'Normal Employee'
    else:
        y = 'Experienced Employee'
    return y

def identify_minute(current_time):
    #print("IDENTIFY MINUTE FUNCTION")
    print(current_time)
    print(type(current_time))

    print(current_time.to_pydatetime())
    print(type(current_time.to_pydatetime()))

    print(current_time.to_pydatetime().strftime("%S"))
    print(type(current_time.to_pydatetime().strftime("%S")))

    if int(current_time.to_pydatetime().strftime("%S")) == 0:
        return "MINUTE"
    else:
        return "SECOND"


def identify_minute_tick(current_time):
    #print("IDENTIFY MINUTE FUNCTION")
    try:
        print(current_time)
        print(type(current_time))

        print(current_time.to_pydatetime())
        print(type(current_time.to_pydatetime()))

        print(current_time.to_pydatetime().strftime("%S"))
        print(type(current_time.to_pydatetime().strftime("%S")))

        if int(current_time.to_pydatetime().strftime("%S")) == 0:
            return "MINUTE"
        else:
            return "SECOND"
    except Exception as e:
        print(str(e))
        return current_time

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
        print("Fetching Historical Data")
        # print(f'Time: {bar.date}, Open: {bar.open}, Close: {bar.close}')

    # Display a message once historical data is retreived
    def historicalDataEnd(self, reqId, start, end):
        print('\nHistorical Data Retrieved\n')
        print(self.df.head())

        self.df["Time"] = pd.to_datetime(self.df["Time"])
        self.df['E_Time'] = (((self.df["Time"]).astype('int64'))) // 1e5
        self.df["E_Time_in_seconds"] = 0
        self.df["E_Time_in_minutes"] = 0
        self.combo_dict[reqId] = self.df[["Time", "E_Time_in_seconds", "E_Time_in_minutes", "Close"]]


        #This is a temporary region, that needs to be tested because tick data is not working
        # print("Historical Data Retreived, moving to test data now")
        # #self.combo_dict[reqId]['E_Time_in_seconds'] = self.combo_dict[reqId - 1]['E_Time_in_minutes'].apply(identify_minute)
        # self.combo_dict[reqId]['TEST COLUMN'] = self.combo_dict[reqId]['Time'].apply(identify_minute)
        # pd.set_option('display.expand_frame_repr', False)
        # print(self.combo_dict[reqId].head())
        # print(self.combo_dict[reqId])
        #
        # # This is a temporary region, that needs to be tested because tick data is not working

        self.df = pd.DataFrame()




    def tickByTickBidAsk(self, reqId, time, bidPrice, askPrice,
                         bidSize, askSize, tickAttribBidAsk):
        super().tickByTickBidAsk(reqId, time, bidPrice, askPrice, bidSize,
                                 askSize, tickAttribBidAsk)

        print("Tick by tick bid ask data")

        # print("BidAsk. ReqId:", reqId,
        #       "Time:", datetime.datetime.fromtimestamp(time).strftime("%Y%m%d %H:%M:%S"),
        #       "BidPrice:", bidPrice, "AskPrice:", askPrice, "BidSize:", bidSize,
        #       "AskSize:", askSize, "BidPastLow:", tickAttribBidAsk.bidPastLow, "AskPastHigh:",
        #       tickAttribBidAsk.askPastHigh)

        self.current_time = t.time()
        current_time_in_minutes = datetime.datetime.fromtimestamp(self.current_time).strftime('%c')

        #self.combo_dict[reqId - 1] = self.combo_dict[reqId - 1].append({'E_Time': "CURRENT TIME", 'Close': round((bidPrice + askPrice) / 2, 5)}, ignore_index=True)
        self.combo_dict[reqId - 1] = self.combo_dict[reqId - 1].append(
            {'E_Time_in_seconds': self.current_time, "E_Time_in_minutes": current_time_in_minutes , \
             'Close': round((bidPrice + askPrice) / 2, 5)}, ignore_index=True)

        self.combo_dict[reqId - 1]['Identify_Minute'] = self.combo_dict[reqId - 1]['Time'].apply(identify_minute_tick)

        pd.set_option('display.expand_frame_repr', False)
        pd.set_option('max_colwidth', None)
        print(self.combo_dict[reqId - 1].head())




        sys.exit(1)

        # self.identify_minute(self.current_time)
        # print("DEBUG")

        # self.current_time = int(t.time() / 60)
        #
        # if (self.combo_dict[reqId - 2]["Time"].iloc[-1] != self.current_time):
        #     self.combo_dict[reqId - 2] = self.combo_dict[reqId - 2].append(
        #         {'E_Time': self.current_time, 'Close': round((bidPrice + askPrice) / 2, 5)}, ignore_index=True)

        print(type(self.combo_dict[reqId-1]))
        print(self.combo_dict[reqId - 1])
        print("HALT")


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


    def give_historical_data(self, inst, reqid, duration='1H', barsize='30 secs'):
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
        print("Establising connection")
        try:
            self.local_app.connect(host=host, port=port, clientId=clientId)
        except Exception as e:
            print(e)

    def initialise(self, combo_list):
        for combo in combo_list:
            for instrument in combo:
                self.cont = self.make_contract(instrument)
                self.reqid += 1
                print("ReqId:" + str(self.reqid))
                self.give_historical_data(self.cont, self.reqid)

    def start(self, combo_list):
        print("Fetch Tick Data")
        for combo in combo_list:
            for instrument in combo:
                self.cont = self.make_contract(instrument)
                self.reqid += 1
                self.give_tick_data(self.cont, self.reqid)
                #t.sleep(10)



#numpy epoch index record.






