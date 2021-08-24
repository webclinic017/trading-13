import logging
from kiteconnect import KiteTicker
import sys

index=sys.argv[1]
print("INDEX: " + str(index))


str_scrip=sys.argv[2]
print("Scrip: " + str(str_scrip))
# global index = index_temp

logging.basicConfig(level=logging.DEBUG)

#https://kite.trade/connect/login?api_key=rcpm0qsa3tuuflu5&v=3


# Initialise
kws = KiteTicker("rcpm0qsa3tuuflu5", "yiJc9guJs9gAg2lWrNYWEk4w7ZjP06Yl")

time_to_write_to_file = 0

from src.socketApi.sqlOperations import *
count = 0
def on_ticks(ws, ticks):
    # Callback to receive ticks.
    start_time_get_data = timeit.default_timer()
    global count
    global index
    global str_scrip
    # print(count)
    print(str(count) + " : " + str(str_scrip) + " : " + str(datetime.now()))
    count=count+1
    logging.debug("Ticks: {}".format(ticks))

    #Insert data to sql
    start_time_get_data = timeit.default_timer()
    insert_ticks(ticks,start_time_get_data)

    # end_time_get_data = timeit.default_timer()
    # time_to_fetch_data = end_time_get_data - start_time_get_data

    #Create file if not present #Pending

    #start_time_write_to_db = timeit.default_timer()

    # with open(str(instrument_token), mode='a') as employee_file:
    #     employee_writer = csv.writer(employee_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
    #     employee_writer.writerow([tradable, mode, instrument_token,
    #                               last_price, last_quantity, average_price, volume, buy_quantity, sell_quantity, change, last_trade_time, \
    #                               oi, oi_day_high, oi_day_low, \
    #                               timestamp, \
    #                               ohlc_open, ohlc_high, ohlc_low, ohlc_close, \
    #                               buy0_quantity, buy0_price, buy0_orders, \
    #                               buy1_quantity, buy1_price, buy1_orders, \
    #                               buy2_quantity, buy2_price, buy2_orders, \
    #                               buy3_quantity, buy3_price, buy3_orders, \
    #                               buy4_quantity, buy4_price, buy4_orders, \
    #                               sell0_quantity, sell0_price, sell0_orders, \
    #                               sell1_quantity, sell1_price, sell1_orders, \
    #                               sell2_quantity, sell2_price, sell2_orders, \
    #                               sell3_quantity, sell3_price, sell3_orders, \
    #                               sell4_quantity, sell4_price, sell4_orders, \
    #                               time_to_fetch_data,
    #                               ])
    #
    #     stop = timeit.default_timer()
    #     # time_to_write_to_file = stop-start
    #     # employee_writer.writerow(['John Smith', 'Accounting', 'November'])

    # t1 = threading.Thread(target=on_connect, args=(16592386,))
    # t2 = threading.Thread(target=on_connect, args=(16592386,))
    #
    # # starting thread 1
    # t1.start()
    # # starting thread 2
    # t2.start()
    #
    # # wait until thread 1 is completely executed
    # t1.join()
    # # wait until thread 2 is completely executed
    # t2.join()


def on_connect(ws, response):
    # Callback on successful connect.
    # Subscribe to a list of instrument_tokens (RELIANCE and ACC here).
    #ws.subscribe([57374727,56530439,58604807,58503687])

    #scrip = [15676930,15677186,15720450,15720706,15721730,15722242,15723010,15723522,15726850,15729154,15730690,15735810,15737090,15777282,15784194,15785474,15787522,15789570,15790338,15790594,15793410]
    scrip = [15676930, 15677186, 15720450]
    # scrip = [15787522]


    global index
    print("INDEX INSIDE ON CONNECT FUNCTION : " + str(index))
    print("Instrument token from On connect function: " + str(scrip[int(index)]))
    ws.subscribe([scrip[int(index)]])

    # ws.subscribe([16592386])
    # ws.subscribe([16592386])

    # Set RELIANCE to tick in `full` mode.
    #ws.set_mode(ws.MODE_FULL, [57374727,56530439,58604807,58503687])
    ws.set_mode(ws.MODE_FULL, [scrip[int(index)]])


def on_close(ws, code, reason):
    # On connection close stop the main loop
    # Reconnection will not happen after executing `ws.stop()`
    # ws.stop()
    pass


def on_error(self, code, reason):
    print("Error from On error code")
    conn()
# Assign the callbacks.


def on_message():
    print("Error from On Message code")


def on_reconnect():
    print("Error from On Reconect code")
    conn()

# kws.on_ticks = on_ticks
# kws.on_connect = on_connect
# kws.on_close = on_close
# kws.on_error = on_error
# kws.on_message = on_message
# kws.on_reconnect = on_reconnect

# Infinite loop on the main thread. Nothing after this will run.
# You have to use the pre-defined callbacks to manage subscriptions.

import time
def conn():
    try:
        kws = KiteTicker("rcpm0qsa3tuuflu5", "yiJc9guJs9gAg2lWrNYWEk4w7ZjP06Yl")
        kws.on_ticks = on_ticks
        kws.on_connect = on_connect
        kws.on_close = on_close
        # kws.on_error = on_error
        # kws.on_message = on_message
        # kws.on_reconnect = on_reconnect
        kws.connect()
        state = kws.is_connected()
        print("CONN: " + str(kws.is_connected()))
        if not state:
            print("Sleeping 5 sec")
            time.sleep(10)
        #     kws.connect()
    except Exception as e:
        print("Connection Exception: " + str(e))
        kws = KiteTicker("rcpm0qsa3tuuflu5", "Pgk43FcE3Ksp1nnv5YWumKlWzv5MigcB")
        kws.on_ticks = on_ticks
        kws.on_connect = on_connect
        kws.on_close = on_close
        # kws.on_error = on_error
        # kws.on_message = on_message
        # kws.on_reconnect = on_reconnect
        kws.connect()
        # kws.on_ticks = on_ticks
        # kws.on_connect = on_connect
        # kws.on_close = on_close
        # conn()

conn()