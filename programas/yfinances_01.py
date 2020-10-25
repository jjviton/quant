# -*- coding: utf-8 -*-
"""
Created on Mon Aug 31 17:56:10 2020

@author: INNOVACION
"""


import yfinance as yf

#data=yf.download("MSFT", period ="6mo")  # por periodo
data2=yf.download("MSFT", start="2020-01-01", end="2020-08-30") #por fechas
data3=yf.download("MSFT", period="1mo", interval="5m")  # por periodo