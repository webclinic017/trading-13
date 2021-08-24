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
from threading import Timer


# Define strategy class - inherits from EClient and EWrapper
class Strategy(EClient, EWrapper):

    # Initialize the class - and inherited classes
    def __init__(self):
        EClient.__init__(self, self)

    def tickPrice(self, reqId, tickType, price, attrib):
        print(f'Price:Id: {reqId}, TickType: {tickType}, Price: {price}')

    # def tickSize(self, reqId, tickType, size:int):
    #     """Market data tick size callback. Handles all size-related ticks."""
    #     print(f'Size: Id: {reqId}, TickType: {tickType}, Size: {size}')

    try:
        def realtimeBar(self, reqId, time, open_, high, low, close, volume, wap, count):
            print(f'Realtimebar: Id: {reqId}')
            print(f'HW')
    except Exception as e:
        print(str(e))
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

gbpusd_contract = Contract()
gbpusd_contract.symbol = 'GBP'
gbpusd_contract.currency = 'USD'
gbpusd_contract.secType = 'CASH'
gbpusd_contract.exchange = 'IDEALPRO'


reqId = 74

# Request market data from the TWS
app.reqMktData(reqId=reqId,
               contract=eurusd_contract,
               genericTickList='',
               snapshot=False,
               regulatorySnapshot=False,
               mktDataOptions=[])


# app.reqRealTimeBars(reqId=reqId,
#                     contract=gbpusd_contract,
#                     barSize=5,
#                     whatToShow="TRADES",
#                     useRTH=1,
#                     realTimeBarsOptions="XYZ")



# Timer(10, app.cancelMktData, [reqId]).start()

# Invoke another thread that will disconnect the strategy from TWS
Timer(20, app.disconnect).start()

# Run the strategy
app.run()


# eeee = EWrapper()
