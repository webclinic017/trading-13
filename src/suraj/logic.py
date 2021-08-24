# -*- coding: utf-8 -*-
"""
Created on Wed Jun 30 18:55:58 2021

@author: micke
"""

from src.suraj.ibwrapper import IBWrapper
from ibapi.contract import Contract
from threading import Timer
from multiprocessing import Process
import time

##################make an object
extender = 750

list_currency = ["INR"]

def get_data(currency):
    mb = IBWrapper(extender)
    mb.local_app.disconnect
    ############################### give the combo_list

    #combo_list = [["RELIANCE", "ADANIENT"]]
    #combo_list = [["EUR", "NZD"]]
    combo_list = [[currency]]
    #####################################establish connections
    print("Establishing connection")
    mb.connect()

    ######################################Start time


    #####################################initialise combos

    print("Initializing")
    mb.initialise(combo_list)

    time.sleep(10)

    ##################################### Compute indicators

    print("Starting")
    mb.start(combo_list)

    ##################################### Algo Start


    ######################################################

    Timer(120, mb.local_app.disconnect).start()
    mb.local_app.run()
    mb.local_app.disconnect

for i in list_currency:
    get_data(i)

'''    
x = mb.local_app.combo_dict    
%timeit x[1]['Close'].mean().
y = x[1]['Close'].to_numpy()
%timeit y.mean()
'''