# -*- coding: utf-8 -*-
"""
Created on Wed Jun 30 18:55:58 2021

@author: micke
"""

from ibwrapper import IBWrapper
from ibapi.contract import Contract
from threading import Timer
from multiprocessing import Process
import time

##################make an object
extender = 750

mb = IBWrapper(extender)

############################### give the combo_list

#combo_list = [["RELIANCE", "ADANIENT"]]
combo_list = [["EUR", "NZD"]]
#####################################establish connections
mb.connect()

######################################Start time


#####################################initialise combos


mb.initialise(combo_list)

time.sleep(10)

##################################### Compute indicators

mb.start(combo_list)

##################################### Algo Start


######################################################

Timer(120, mb.local_app.disconnect).start()
mb.local_app.run()

'''    
x = mb.local_app.combo_dict    
%timeit x[1]['Close'].mean().
y = x[1]['Close'].to_numpy()
%timeit y.mean()
'''