# -*- coding: utf-8 -*-
"""
Created on Mon Aug 31 17:56:10 2020

@author: INNOVACION
"""

import datetime as dt
import yfinance as yf
import pandas as pd

#import quant_j3_lib as ju
from quant_j3_lib import *  #ojo si no esta en el directorio y no se importó con PY

stocks = ["AMZN","MSFT","INTC","GOOG","INFY.NS","3988.HK"]
start = dt.datetime.today()-dt.timedelta(360)
end = dt.datetime.today()
cl_price = pd.DataFrame() # empty dataframe which will be filled with closing prices of each stock
ohlcv_data = {} # empty dictionary which will be filled with ohlcv dataframe for each ticker

# looping over tickers and creating a dataframe with close prices
for ticker in stocks:
    cl_price[ticker] = yf.download(ticker,start,end)["Adj Close"]
    

# looping over tickers and storing OHLCV dataframe in dictionary
for ticker in stocks:
    ohlcv_data[ticker] = yf.download(ticker,start,end)


var=ohlcv_data["AMZN"]["Volume"]

formula_cuadratica(1, 2, 1)

formula_cuadratica(4, 4, 4)
