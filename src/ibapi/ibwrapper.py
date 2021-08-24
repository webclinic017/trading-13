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
import datetime as dt



def epoch_to_datetime(epoch_seconds):
    return dt.datetime.fromtimestamp(epoch_seconds).strftime('%Y-%m-%d %H:%M:%S')

def epoch_to_datetime_second(epoch_seconds):
    return dt.datetime.fromtimestamp(epoch_seconds).strftime('%S')

time_of_tick_data_prev = 0

class IBRelay(EClient, EWrapper):

    def __init__(self, extender):
        EClient.__init__(self, self)
        self.df = pd.DataFrame()
        self.tick_df = pd.DataFrame(index=[0],
                                    columns=["datetime", "systemtime", 'reqid', "bidprice", "askprice", "bidSize",
                                             "askSize"])
        self.tck_df = pd.DataFrame()
        self.combo_dict = {}
        self.extender = extender
        self.time_of_tick_data_prev = 0

    def historicalData(self, reqId, bar):
        dictionary = {'Time': bar.date, 'Open': bar.open, 'High': bar.high, 'Low': bar.low, 'Close': bar.close}
        self.df = self.df.append(dictionary, ignore_index=True)
        print(f'Time: {bar.date}, Open: {bar.open}, Close: {bar.close}')

    # Display a message once historical data is retreived
    def historicalDataEnd(self, reqId, start, end):
        print('\nHistorical Data Retrieved\n')
        print(self.df.head())

        self.df["Time"] = pd.to_datetime(self.df["Time"])
        self.df['E_Time'] = (((self.df["Time"] - dt.datetime(1970, 1, 1)).dt.total_seconds()) / 60).astype(int)
        self.combo_dict[reqId] = self.df[["Time", "E_Time", "Close"]].to_records()
        self.combo_dict[reqId].resize((self.extender, 1))
        self.df = pd.DataFrame()

    def tickByTickBidAsk(self, reqId, time, bidPrice, askPrice,
                         bidSize, askSize, tickAttribBidAsk):
        super().tickByTickBidAsk(reqId, time, bidPrice, askPrice, bidSize,
                                 askSize, tickAttribBidAsk)
        # print("BidAsk. ReqId:", reqId, "Time:", time,
        #       "BidPrice:", bidPrice, "AskPrice:", askPrice, "BidSize:", bidSize,
        #       "AskSize:", askSize, "BidPastLow:", tickAttribBidAsk.bidPastLow, "AskPastHigh:",
        #       tickAttribBidAsk.askPastHigh)

        #print(int(t.time() / 60))
        #print("Time:" + str(epoch_to_datetime(int(t.time()))) + "  --- " + epoch_to_datetime(time))

        print("Current Time in seconds:" + str(epoch_to_datetime_second(int(t.time()))) + "  --- Tick data time in seconds: " + epoch_to_datetime_second(time))

        time_of_tick_data = epoch_to_datetime_second(time)


        # if str(time_of_tick_data) == '00':
        #     print("MINUTE END, TIME TO APPEND")

        if str(time_of_tick_data) > '50' and int(self.time_of_tick_data_prev) < int(time_of_tick_data):
            print("Data Prev: " + str(self.time_of_tick_data_prev) + " Data Current: " + str(time_of_tick_data) + \
                  " Greater than 50 and prev is less than current, try to append")
            # print("Data Prev: " + str(self.time_of_tick_data_prev))
            # print("Data Current: " + str(time_of_tick_data))
            self.time_of_tick_data_prev = time_of_tick_data
        elif str(time_of_tick_data) < '50':
            # print("Less than 50, reset everything")
            # print("Data Prev: " + str(self.time_of_tick_data_prev))
            # print("Data Current: " + str(time_of_tick_data))
            self.time_of_tick_data_prev = 0


        #Based on the value of the data in the global_dict,
        #global_dict[reqId] = bidPrice




        # if (self.combo_dict[reqId - 2]["Time"].iloc[-1] != self.current_time):
        #     self.combo_dict[reqId - 2] = self.combo_dict[reqId - 2].append(
        #         {'E_Time': self.current_time, 'Close': round((bidPrice + askPrice) / 2, 5)}, ignore_index=True)

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
    def __init__(self, extender):
        self.df_hist = pd.DataFrame()
        self.local_app = IBRelay(extender)
        self.combo_dict = {}
        self.reqid = 0

    def give_historical_data(self, inst, reqid, duration='1 D', barsize='1 min'):
        self.local_app.reqHistoricalData(reqId=reqid,
                                         contract=inst,
                                         endDateTime='',
                                         durationStr=duration,
                                         barSizeSetting=barsize,
                                         whatToShow='MIDPOINT',
                                         useRTH=0,
                                         formatDate=1,
                                         keepUpToDate=False,
                                         chartOptions=[])

    global_dict = {1: 0, 2: 0}

    def give_tick_data(self, inst, reqid):
        #Create a thread with a target function()
        #threading.Thread(target = inserter(),args = "")

        print("Fetching Bid Ask Tick data ")
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

        #minute_check thread.
        from threading import Thread
        from time import sleep

        def threaded_function(arg):
            for i in range(arg):
                # print("Current Time in seconds:" + str(epoch_to_datetime_second(
                #     int(t.time()))) + "  --- Tick data time in seconds: " + epoch_to_datetime_second(time))
                time_now = epoch_to_datetime_second(int(t.time()))
                # time_of_tick_data = epoch_to_datetime_second(time_now)

                if str(time_now) == "00":
                    print("Now is a minute " + str(time_now))
                else:
                    print("Now is not a minute " + str(time_now))

                sleep(1)

        thread = Thread(target=threaded_function, args=(30,))
        thread.start()
        print("thread finished...exiting")

        #This segment is supposed to be a thread
        for combo in combo_list:
            print("For loop execution start")
            for instrument in combo:
                self.cont = self.make_contract(instrument)
                self.reqid += 1
                self.give_tick_data(self.cont, self.reqid)
                t.sleep(10)

        thread.join()









