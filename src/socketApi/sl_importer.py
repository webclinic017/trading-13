# -*- coding: utf-8 -*-
"""
Created on Sat Apr 24 14:56:12 2021

@author: micke
"""

import mysql.connector as sql
import pandas as pd

db = sql.connect(host='localhost', user='root', password='toor', database='zerodha_api')

data = pd.read_sql('select * from ticks', con=db)
data = pd.DataFrame(data)
data = data.set_index(['date'])
data = data.ix[:, ['last_price']]
print(data)