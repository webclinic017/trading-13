# -*- coding: utf-8 -*-
"""
Created on Sat Apr 24 14:13:07 2021

@author: micke
"""

import pymysql
from datetime import *
import timeit
db = pymysql.connect(host = 'localhost' , user = 'root' , password = 'toor',database = 'zerodha_api')

insert_into_table = 'insert into all_data (tradable , mode_of_scrip, instrument_token, last_price, last_quantity, average_price , volume , buy_quantity , ' \
                    'sell_quantity ,change_of_price , last_trade_time , oi , oi_day_high , oi_day_low , data_timestamp , ohlc_open , ohlc_high , ohlc_low , ohlc_close , buy0_quantity , \
buy0_price , buy0_orders , buy1_quantity , buy1_price , buy1_orders , buy2_quantity , buy2_price , buy2_orders , buy3_quantity , buy3_price , buy3_orders , buy4_quantity , \
buy4_price , buy4_orders , sell0_quantity , sell0_price , sell0_orders , sell1_quantity , sell1_price , sell1_orders , sell2_quantity , sell2_price , sell2_orders , \
sell3_quantity , sell3_price , sell3_orders , sell4_quantity , sell4_price , sell4_orders , time_to_fetch_data )  \
values ( \
%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, \
%s, %s, %s, %s \
)'

insert_into_table = 'insert into all_data (tradable , mode_of_scrip, instrument_token, last_price, last_quantity, average_price , volume , buy_quantity , ' \
                    'sell_quantity ,change_of_price , last_trade_time , oi , oi_day_high , oi_day_low,  data_timestamp, ohlc_open , ohlc_high , ohlc_low , ohlc_close , buy0_quantity , \
buy0_price , buy0_orders , buy1_quantity , buy1_price , buy1_orders , buy2_quantity , buy2_price , buy2_orders , buy3_quantity , buy3_price , buy3_orders , buy4_quantity , \
buy4_price , buy4_orders , sell0_quantity , sell0_price , sell0_orders , sell1_quantity , sell1_price , sell1_orders , sell2_quantity , sell2_price , sell2_orders , \
sell3_quantity , sell3_price , sell3_orders , sell4_quantity , sell4_price , sell4_orders , time_to_fetch_data, start_time_write_data   )  \
values ( \
%s, %s, %s, %s, %s, \
%s, %s, %s, %s, %s, \
%s, %s, %s, %s, %s, \
%s, %s, %s, %s, %s, \
%s, %s, %s, %s, %s, \
%s, %s, %s, %s, %s, \
%s, %s, %s, %s, %s, \
%s, %s, %s, %s, %s, \
%s, %s, %s, %s, %s, \
%s, %s, %s, %s, %s, \
%s )'

def insert_ticks(ticks, start_time_get_data):

    tradable = ticks[0]['tradable']
    mode = ticks[0]['mode']
    instrument_token = ticks[0]['instrument_token']
    last_price = ticks[0]['last_price']
    last_quantity = ticks[0]['last_quantity']
    average_price = ticks[0]['average_price']
    volume = ticks[0]['volume']
    buy_quantity = ticks[0]['buy_quantity']
    sell_quantity = ticks[0]['sell_quantity']
    change = ticks[0]['change']
    last_trade_time = ticks[0]['last_trade_time']
    oi = ticks[0]['oi']
    oi_day_high = ticks[0]['oi_day_high']
    oi_day_low = ticks[0]['oi_day_low']
    timestamp = ticks[0]['timestamp']
    ohlc_open = ticks[0]['ohlc']['open']
    ohlc_high = ticks[0]['ohlc']['high']
    ohlc_low = ticks[0]['ohlc']['low']
    ohlc_close = ticks[0]['ohlc']['close']

    #Buy Orders
    buy0_quantity = ticks[0]['depth']['buy'][0]['quantity']
    buy0_price = ticks[0]['depth']['buy'][0]['price']
    buy0_orders = ticks[0]['depth']['buy'][0]['orders']

    buy1_quantity = ticks[0]['depth']['buy'][1]['quantity']
    buy1_price = ticks[0]['depth']['buy'][1]['price']
    buy1_orders = ticks[0]['depth']['buy'][1]['orders']

    buy2_quantity = ticks[0]['depth']['buy'][2]['quantity']
    buy2_price = ticks[0]['depth']['buy'][2]['price']
    buy2_orders = ticks[0]['depth']['buy'][2]['orders']

    buy3_quantity = ticks[0]['depth']['buy'][3]['quantity']
    buy3_price = ticks[0]['depth']['buy'][3]['price']
    buy3_orders = ticks[0]['depth']['buy'][3]['orders']

    buy4_quantity = ticks[0]['depth']['buy'][4]['quantity']
    buy4_price = ticks[0]['depth']['buy'][4]['price']
    buy4_orders = ticks[0]['depth']['buy'][4]['orders']

    #Sell Orders
    sell0_quantity = ticks[0]['depth']['sell'][0]['quantity']
    sell0_price = ticks[0]['depth']['sell'][0]['price']
    sell0_orders = ticks[0]['depth']['sell'][0]['orders']

    sell1_quantity = ticks[0]['depth']['sell'][1]['quantity']
    sell1_price = ticks[0]['depth']['sell'][1]['price']
    sell1_orders = ticks[0]['depth']['sell'][1]['orders']

    sell2_quantity = ticks[0]['depth']['sell'][2]['quantity']
    sell2_price = ticks[0]['depth']['sell'][2]['price']
    sell2_orders = ticks[0]['depth']['sell'][2]['orders']

    sell3_quantity = ticks[0]['depth']['sell'][3]['quantity']
    sell3_price = ticks[0]['depth']['sell'][3]['price']
    sell3_orders = ticks[0]['depth']['sell'][3]['orders']

    sell4_quantity = ticks[0]['depth']['sell'][4]['quantity']
    sell4_price = ticks[0]['depth']['sell'][4]['price']
    sell4_orders = ticks[0]['depth']['sell'][4]['orders']
    #time_to_fetch_data = 0.00

    end_time_get_data = timeit.default_timer()
    time_to_fetch_data = end_time_get_data - start_time_get_data

    start_time_write_data = datetime.now()

    c = db.cursor()
    for tick in ticks:
        c.execute(
            insert_into_table, (
                tradable, mode, instrument_token, \
                last_price, last_quantity, average_price, volume, buy_quantity, sell_quantity, change, last_trade_time, \
                oi, oi_day_high, oi_day_low, \
                timestamp, \
                ohlc_open, ohlc_high, ohlc_low, ohlc_close, \
                buy0_quantity, buy0_price, buy0_orders, \
                buy1_quantity, buy1_price, buy1_orders, \
                buy2_quantity, buy2_price, buy2_orders, \
                buy3_quantity, buy3_price, buy3_orders, \
                buy4_quantity, buy4_price, buy4_orders, \
                sell0_quantity, sell0_price, sell0_orders, \
                sell1_quantity, sell1_price, sell1_orders, \
                sell2_quantity, sell2_price, sell2_orders, \
                sell3_quantity, sell3_price, sell3_orders, \
                sell4_quantity, sell4_price, sell4_orders, \
                time_to_fetch_data, start_time_write_data
            )
            )
    try :
        db.commit()
    except Exception as e:
        print(str(e))
        db.rollback()