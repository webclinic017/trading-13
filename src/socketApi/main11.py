from kiteconnect import KiteConnect
import time
from kiteconnect import KiteTicker

#api_key = open('api_key.txt', 'r').read()
api_key = "rcpm0qsa3tuuflu5"
#access_token = open('access_token.txt', 'r').read()

kws = KiteTicker(api_key, "eWZPQ3h89X7OYkPwsRjRRNH0FiAF2UTA")
#tokens = [5215745, 633601, 1195009, 779521, 758529, 1256193, 194561, 1837825, 952577, 1723649, 3930881,
#4451329, 593665, 3431425, 2905857]
tokens = [53787399, 53520391, 54123271]
dict = {53787399: 'CRUDEOIL18SEPFUT', 53520391: 'SILVERM18NOVFUT', 54123271: 'GOLDM18OCTFUT'}


def on_ticks(ws, ticks):
    ticks = [dict[ticks[0]['instrument_token']], ticks[0]['timestamp'], ticks[0]['last_price']]
    print(ticks)


def on_connect(ws, response):
    ws.subscribe(tokens)
    ws.set_mode(ws.MODE_FULL, tokens)



def on_close(ws, code, reason):
    # On connection close stop the main loop
    # Reconnection will not happen after executing `ws.stop()`
    ws.stop()

kws.on_ticks = on_ticks
kws.on_connect = on_connect
kws.on_close = on_close
print("Trying to connect")
kws.connect(threaded=True)
count = 0

# kws.on_ticks = on_ticks
# kws.on_connect = on_connect
# kws.on_close = on_close
#
#
#
# # Infinite loop on the main thread. Nothing after this will run.
# # You have to use the pre-defined callbacks to manage subscriptions.
# kws.connect()


# while True:
print(count)
count += 1
if (count % 2 == 0):
    if kws.is_connected():
        kws.set_mode(kws.MODE_FULL, tokens)
    else:
        if kws.is_connected():
            kws.set_mode(kws.MODE_FULL, tokens)
    time.sleep(0.350)