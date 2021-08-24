import logging
from kiteconnect import KiteTicker
import csv

logging.basicConfig(level=logging.DEBUG)

#https://kite.trade/connect/login?api_key=rcpm0qsa3tuuflu5&v=3

# Initialise
kws = KiteTicker("rcpm0qsa3tuuflu5", "Uo8WM3M1K6IDRbVJMSYbgISvZ4KxFKOa")

time_to_write_to_file = 0

from src.socketApi.sqlOperations import *

def on_ticks(ws, ticks):
    # Callback to receive ticks.
    #logging.debug("Ticks: {}".format(ticks))

    #start_time_get_data = timeit.default_timer()
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


    # end_time_get_data = timeit.default_timer()
    # time_to_fetch_data = end_time_get_data - start_time_get_data


    #scrips = ["57374727", "56530439", "58604807", "58503687"]

    #Create file if not present #Pending

    start_time_write_to_db = timeit.default_timer()

    with open(str(instrument_token), mode='a') as employee_file:
        employee_writer = csv.writer(employee_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
        employee_writer.writerow([tradable, mode, instrument_token,
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
                                  time_to_fetch_data,
                                  ])

        stop = timeit.default_timer()
        # time_to_write_to_file = stop-start
        # employee_writer.writerow(['John Smith', 'Accounting', 'November'])

def on_connect(ws, response):
    # Callback on successful connect.
    # Subscribe to a list of instrument_tokens (RELIANCE and ACC here).
    #ws.subscribe([57374727,56530439,58604807,58503687])
    ws.subscribe([16592386,16560642,16560898,16563202,16492034,16492802,16562690,16568066,16569346,16570626,16574210,16579074,16593666,16619522,\
                  16625666,16625922,16629250,16644866,12523778,16580610,16495106,16491522,16495362,58072071,58075655,57828103,56530439,58246663,\
                  58076167,56413703,56729351,58076423])

    # Set RELIANCE to tick in `full` mode.
    #ws.set_mode(ws.MODE_FULL, [57374727,56530439,58604807,58503687])
    ws.set_mode(ws.MODE_FULL, [16592386,16560642,16560898,16563202,16492034,16492802,16562690,16568066,16569346,16570626,16574210,16579074,16593666,16619522,\
                  16625666,16625922,16629250,16644866,12523778,16580610,16495106,16491522,16495362,58072071,58075655,57828103,56530439,58246663,\
                  58076167,56413703,56729351,58076423])


def on_close(ws, code, reason):
    # On connection close stop the main loop
    # Reconnection will not happen after executing `ws.stop()`
    ws.stop()

# Assign the callbacks.



kws.on_ticks = on_ticks
kws.on_connect = on_connect
kws.on_close = on_close



# Infinite loop on the main thread. Nothing after this will run.
# You have to use the pre-defined callbacks to manage subscriptions.
kws.connect(threaded=True)