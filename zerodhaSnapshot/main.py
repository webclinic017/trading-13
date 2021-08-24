import os
import logging
def getLogger(name):
    # logger.getLogger returns the cached logger when called multiple times
    # logger.Logger created a new one every time and that avoids adding
    # duplicate handlers
    logger = logging.Logger(name)
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(os.path.join(name + '.log'), 'a')
    logger.addHandler(handler)
    return logger

# def test(i):
#   log_hm = getLogger('healthmonitor')
#   log_hm.info("Testing Log %s", i) # Should log to /some/path/healthmonitor.log






import logging
import logging.handlers
import os

handler = logging.handlers.WatchedFileHandler(
  os.environ.get("LOGFILE", "log_file.log"))

formatter = logging.Formatter(logging.BASIC_FORMAT)

handler.setFormatter(formatter)
root = logging.getLogger()
root.setLevel(os.environ.get("LOGLEVEL", "INFO"))
root.addHandler(handler)

import logging
from kiteconnect import KiteConnect
import threading
import logging
from kiteconnect import KiteConnect
logging.basicConfig(level=logging.DEBUG)
import sys
import time
from playsound import playsound
kite = None
accessToken = None

def main():
    gold_arr = []
    inst_arr = "58424071","58322183","58424327","58156807","58732551","58430727","58133767","58584327",\
                "58604807","58584583","58425095","58157319","58724359","58425351","56729095","56729351","58425863"
    #inst_arr = ["58424071"]
    penultimateLastTradedPrice_arr = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    #penultimateLastTradedPrice_arr = [0]
    while True:
      kite = loginZerodha()
      lastTradedPrice_arr = getCMP(kite, inst_arr)

      for i in range(len(lastTradedPrice_arr)):
        calcSignal(inst_arr[i], penultimateLastTradedPrice_arr[i], lastTradedPrice_arr[i])
        # print(lastTradedPrice)
      penultimateLastTradedPrice_arr = lastTradedPrice_arr
      time.sleep(300)

def calcSignal(inst_arr, penultimateTradedPrice, lastTradedPrice):
  diff = lastTradedPrice - penultimateTradedPrice
  diff = abs(diff)
  #print(inst_arr)
  #print("DIFFERENCE")
  #print(diff)
  percentDiff = (diff/lastTradedPrice) * 100
  #print("PERCENT DIFF")
  #print(percentDiff)
  log_hm = getLogger(inst_arr)
  #log_hm.info("Testing Log %s", i) # Should log to /some/path/healthmonitor.log

  root.addHandler(handler)
  log_hm.info(f"Instr: {inst_arr}, Difference: {diff}, percentDiff: {percentDiff}, lastTradedPrice: {lastTradedPrice}, penultimateTradedPrice: {penultimateTradedPrice}")

  if percentDiff > 0.15:
    print("\n")
    print("SIGNAL:" + str(inst_arr))
    #print('playing sound using playsound')
    playsound('beep-01a.mp3')
    # playsound('beep-01a.mp3')
    # playsound('beep-01a.mp3')


def calcTail(inst_arr, penultimateTradedPrice, lastTradedPrice):
  diff = lastTradedPrice - penultimateTradedPrice
  diff = abs(diff)
  #print(inst_arr)
  #print("DIFFERENCE")
  #print(diff)
  percentDiff = (diff/lastTradedPrice) * 100
  #print("PERCENT DIFF")
  #print(percentDiff)
  log_hm = getLogger(inst_arr)
  #log_hm.info("Testing Log %s", i) # Should log to /some/path/healthmonitor.log

  root.addHandler(handler)
  log_hm.info(f"Instr: {inst_arr}, Difference: {diff}, percentDiff: {percentDiff}, lastTradedPrice: {lastTradedPrice}, penultimateTradedPrice: {penultimateTradedPrice}")

  if percentDiff > 0.15:
    print("SIGNAL:" + str(inst_arr))
    #print('playing sound using playsound')
    playsound('beep-01a.mp3')
    # playsound('beep-01a.mp3')
    # playsound('beep-01a.mp3')



def getKite():
  return kite

def getAccessToken():
  return accessToken

def loginZerodha():
  global kite
  global accessToken

  api_key = "rcpm0qsa3tuuflu5"
  api_secret = "kt1ygk1sz3rfmsj6nazdxo7ac6y3f0s7"
  request_token = "lstWvD6AKuBA0l1t2bzH2ld913ZR5ndn"

  # kite = KiteConnect(api_key=api_key)
  # https://kite.trade/connect/login?api_key=rcpm0qsa3tuuflu5&v=3
  kite = KiteConnect(api_key=api_key)
  # sys.exit()

  if request_token is not None:
    # logging.info('requestToken = %s', request_token)
    # session = kite.generate_session(request_token, api_secret=api_secret)
    # print(session)
    # sys.exit()

    accessToken = "JLu0Vzkx4MYfOWWkMEPPyBmpIAnwGy4I"
    #logging.info('accessToken = %s', accessToken)
    kite.set_access_token(accessToken)
    #logging.info('Login successful. accessToken = %s', accessToken)
    return kite
    # redirect to home page with query param loggedIn=true
    # homeUrl = systemConfig['homeUrl'] + '?loggedIn=true'
    # logging.info('Redirecting to home page %s', homeUrl)
    #
    # return redirect(homeUrl, code=302)
  else:
    loginUrl = kite.login_url()
    logging.info('Redirecting to zerodha login url = %s', loginUrl)
    # return redirect(loginUrl, code=302)

  # time.sleep(5)
  exchange = 'NSE'
  tradingSymbol = 'GOLD'
  # lastTradedPrice = getCMP(exchange + ':' + tradingSymbol)


def getCMP(kite, tradingSymbol):
  kite = getKite()
  quote = kite.quote(tradingSymbol)
  print(quote)
  price_arr = []
  for i in range(len(tradingSymbol)):
    if quote:
      # print("PRICE")
      # print(quote[tradingSymbol[i]]['last_price'])
      price_arr.append(quote[tradingSymbol[i]]['last_price'])
      #return quote[tradingSymbol[i]]['last_price']
    else:
      return 0

  return price_arr

main()




























