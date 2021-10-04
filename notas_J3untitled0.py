# -*- coding: utf-8 -*-
"""
Created on Sun Aug  8 19:44:26 2021

@author: INNOVACION
"""


#####################################################


ACTUALIZAR EL NAVEGADOR A GOOGLE.!!!!!

Cambié de Yahoo a Google Finance y funciona para mí, así que desde

data.DataReader(ticker, 'yahoo', start_date, end_date)
a

data.DataReader(ticker, 'google', start_date, end_date)
y adapté mi "viejo" Yahoo! símbolos de:

tickers = ['AAPL','MSFT','GE','IBM','AA','DAL','UAL', 'PEP', 'KO']
a

tickers = ['NASDAQ:AAPL','NASDAQ:MSFT','NYSE:GE','NYSE:IBM','NYSE:AA','NYSE:DAL','NYSE:UAL', 'NYSE:PEP', 'NYSE:KO']