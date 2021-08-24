import logging
from kiteconnect import KiteTicker
import csv
import timeit
from datetime import *

logging.basicConfig(level=logging.DEBUG)

#https://kite.trade/connect/login?api_key=rcpm0qsa3tuuflu5&v=3


# Initialise
kws = KiteTicker("rcpm0qsa3tuuflu5", "ZptrIyVL0aO6w5ahc0lz7Oa0icjgyRzy")

time_to_write_to_file = 0

#from sqlOperations import *
count = 0
def on_ticks(ws, ticks):
    # Callback to receive ticks.
    start_time_get_data = timeit.default_timer()
    global count
    # print(count)
    print(str(count) + " : " + str(datetime.now()))
    count=count+1
    #logging.debug("Ticks: {}".format(ticks))

    #start_time_get_data = timeit.default_timer()
    #insert_ticks(ticks,start_time_get_data)
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
    scrip = [56530439,58604807, 58503687, 57374727 ,16592386,16560642,16560898,16563202,16492034,16492802,16562690,16568066,16569346,16570626,16574210,16579074,16593666,16619522,\
                  16625666,16625922,16629250,16644866,12523778,16580610,16495106,16491522,16495362,58072071,58075655,57828103,56530439,58246663,\
                  58076167,56413703,56729351,58076423,58246663]

    ws.subscribe([scrip[1]])

    # ws.subscribe([16592386])
    # ws.subscribe([16592386])

    # Set RELIANCE to tick in `full` mode.
    #ws.set_mode(ws.MODE_FULL, [57374727,56530439,58604807,58503687])
    ws.set_mode(ws.MODE_FULL, [scrip[1]])


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
kws.connect()