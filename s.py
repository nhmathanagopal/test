
from kiteconnect import KiteConnect
import os
import datetime as dt
import pandas as pd
import numpy as np
import time
import requests
from datetime import date
from datetime import datetime
import sys


#generate trading session
access_token = open("access_token.txt",'r').read()
key_secret = open("api_key.txt",'r').read().split()
kite = KiteConnect(api_key=key_secret[0])
kite.set_access_token(access_token)


#get dump of all NSE instruments
instrument_dump = kite.instruments("NSE")
instrument_df = pd.DataFrame(instrument_dump)


def instrumentLookup(instrument_df,symbol):
    """Looks up instrument token for a given script from instrument dump"""
    try:
        return instrument_df[instrument_df.tradingsymbol==symbol].instrument_token.values[0]
    except:
        return -1


def fetchOHLC(ticker,interval,duration):
    """extracts historical data and outputs in the form of dataframe"""
    instrument = instrumentLookup(instrument_df,ticker)
    data = pd.DataFrame(kite.historical_data(instrument,dt.date.today()-dt.timedelta(duration), dt.date.today(),interval))
    data.set_index("date",inplace=True)
    return data




def SLOrder(symbol,buy_sell,quantity):    
    # Place an intraday stop loss order on NSE - handles market orders converted to limit orders
    pos_df = pd.DataFrame(kite.positions()["day"])
   
    
    if buy_sell == "buy":
        s_price = float(pos_df[pos_df["tradingsymbol"]==symbol]["sell_price"])
        t_type_sl=kite.TRANSACTION_TYPE_SELL
        sl_price = s_price + (s_price * 1.25)/100 
    elif buy_sell == "sell":
        b_price = float(pos_df[pos_df["tradingsymbol"]==symbol]["buy_price"])
        t_type_sl=kite.TRANSACTION_TYPE_BUY
        sl_price = b_price - (b_price * 1.25)/100
    print(sl_price)
  # kite.place_order(tradingsymbol=symbol,
  #                    exchange=kite.EXCHANGE_NSE,
  #                    transaction_type=t_type_sl,
  #                    quantity=quantity,
  #                    order_type=kite.ORDER_TYPE_SL,
  #                    price=sl_price,
  #                    trigger_price = sl_price,
  #                    product=kite.PRODUCT_MIS,
  #                    variety=kite.VARIETY_REGULAR)


   
      

            
#############################################################################################################
#############################################################################################################
n = len(sys.argv)
b_s = sys.argv[1]
quantity = sys.argv[2]

buy_tic = list()
for i in range(3, n):
    buy_tic.append(sys.argv[i])

for sym in buy_tic:
    SLOrder(sym,b_s,quantity)
 


