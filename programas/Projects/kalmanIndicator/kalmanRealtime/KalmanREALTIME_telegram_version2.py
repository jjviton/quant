#!/usr/bin/env python
# coding: utf-8

# # KALMAN REAL TIME Ibex con Telegram

# Version simplificada de la estrategia para salvarla en un fichero .py y ejecutarla en automatico para hacer backtesting guiado.
# Busca los valores del Ibex al final de la sesion en rango de una hora.
# 
# Este cuaderno implementa una estrategia de inversion basada en Kalman como indicador.
# 
# Busca señales de entrada y las envía el Telegram para su analisis.
# 
# GRAFICADOR PLOTLY:  muy bueno como hace velas ( esta abajo desconectado del resto)
# 
# 
# 

# Status: <font color='red'>Funcionando !!!  v0.0    10/01/2022<font>

# In[1]:


# Raw Package
import numpy as np
import pandas as pd

from sp500 import tickers_sp500

#Data Source
import yfinance as yf

#Data viz
import plotly.graph_objs as go


# In[2]:


import analisis
import kalman as kl  #cambiar segun el módulo con la estrategia implementado
import pandas as pd
import datetime as dt
from time import time
from time import sleep
import yfinance as yf
import numpy as np
from telegram_bot import *

dentro =True
fuera  =False


# In[3]:


kalman= kl.StrategyClass(real_back=True)    #Creamos la clase
import quant_j3_lib as quant_j3


# In[4]:


telegram_send("3.- Señal Kalman RealTime b0.1n  ")


# In[5]:


def checkKalman(instrumento_ ='app'):
    #Interval required 1 minute
    try:
        data = yf.download(tickers=instrumento_, period='6mo', interval='1d')  #  1h 3mo 15m https://algotrading101.com/learn/yfinance-guide/
    except:
        print('instrumento no existe')
    
    del data["Adj Close"]
    data['Kalman']=    quant_j3.kalmanIndicator(data,paraA_=200,paraB_=50,instrumento=instrumento_)

    indiceLast_ = (len(data)-2)    ### ojo parece que da la ultima version cotizada, no la ultima hora
    price_ = data.columns.get_loc("Close")  
    kalman_ = data.columns.get_loc("Kalman")  
    volumen_ = data.columns.get_loc("Volume") 
    open_ = data.columns.get_loc("Open")  


    print(instrumento_)
    
    contador =0
    señal =fuera
    
    # Compruebo Kalman
    # Según la estrategia tenemos que buscar, dos velas alcistas no necesariamente consecutivas entre una ventana anterior. 
    # estas velas alcistas detras de una condicion de reset (dos velas rojas por debajo kalman)
    
    for i in range(5):
        #vela verde por encima de kalman entera
        if (data.iloc[(indiceLast_-i),price_] > data.iloc[(indiceLast_),kalman_]  and  
            data.iloc[(indiceLast_-i),open_] > data.iloc[(indiceLast_),kalman_]  and
            data.iloc[(indiceLast_-i),price_] > data.iloc[(indiceLast_),open_]):
            contador += 1
            data.iloc[(indiceLast_-i),volumen_] =99.0
    #tres velas verdes y la ultima verde
    if (contador > 2  and
       data.iloc[(indiceLast_),price_] > data.iloc[(indiceLast_),kalman_]  and 
       data.iloc[(indiceLast_-i),open_] > data.iloc[(indiceLast_),kalman_] ): 
        señal=dentro 
    
    #Compruebo Media 200 velas positiva
    #quant_j3.MovingAverage(data,long_=200,short_=50)
    data2= quant_j3.MovingAverage(data,long_=200,short_=50)
    # 1.- MEDIA DE 200 SESIONES ACCENDENTE
    #   Calculamos de la media aritmetica la regresion lineal para ver la esencia
    ma200_=data2.columns.get_loc("MA_200")
    data_aux2= data2.iloc[-200:, ma200_]
    data_aux2.dropna(inplace=True)  
    # 3.1.- Calculamos media de las ultimas 'n' sesiones y la regresion lineal
    coef_ema200_, intercept_ema200_ =quant_j3.linearRegresion_J3(data_aux2) #+'  de ema200') 
    
    #pendiente positiva y vela por encima media200
    """
    if (señal ==dentro):
        if (coef_ema200_ > 0  and 
            data.iloc[(indiceLast_),price_] > data_aux2[-1] and 
            data.iloc[(indiceLast_-i),open_] > data_aux2[-1] ): 
           
            señal=dentro     
        else:
            señal =fuera
    """
   
    print(instrumento_,señal)
    print ('Precio', data.iloc[(indiceLast_-i),price_], '*************  ''Kalman', data.iloc[(indiceLast_-i),kalman_])
    print ('checkIN Time',data.index[indiceLast_])
    
    if (señal ==dentro):
        print ('Entramos del mercado')
        telegram_send("3.IN Señal Kalman v1\n"+ instrumento_ +"\nPrecio = " + str(data.iloc[(indiceLast_-i),price_]) + "\n***  Kalman level = "+ str(data.iloc[(indiceLast_-i),kalman_])+
                     "\nTime: " + str(data.index[indiceLast_]))
        sleep(5)
        
        
    
    return señal
    


# In[6]:


def checkKalman_OUT(instrumento_ ='app'):
    #Interval required 1 minute
    try:
        data = yf.download(tickers=instrumento_, period='6mo', interval='1d')  #5m
    except:
        print('instrumento no existe')
    
    del data["Adj Close"]
    data['Kalman']= quant_j3.kalmanIndicator(data,paraA_=200,paraB_=50,instrumento=instrumento_)

    indiceLast_ = (len(data)-2)    ### ojo parece que da la ultima version cotizada, no la ultima hora
    price_ = data.columns.get_loc("Close")  
    kalman_ = data.columns.get_loc("Kalman")  
    volumen_ = data.columns.get_loc("Volume") 
    open_ = data.columns.get_loc("Open")  

    print(instrumento_)
    
    contador =0
    señal =dentro
    
    # Compruebo Kalman
    # Borro la señal si dos velas por debajo de kalman
    
    for i in range(5):
        #Precio por debajo de Kalman cuento uno en el contador
        if (data.iloc[(indiceLast_-i),price_] < data.iloc[(indiceLast_),kalman_] and
           data.iloc[(indiceLast_-i),open_] < data.iloc[(indiceLast_),kalman_] and
           data.iloc[(indiceLast_-i),price_] < data.iloc[(indiceLast_),open_]):
            contador += 1
            data.iloc[(indiceLast_-i),volumen_] =99.0
    if (contador > 3): 
        señal=fuera
        print ('Salimos del mercado')
    
    
    
    print(instrumento_,señal)

    print ('checkOUT Time',data.index[indiceLast_])
    
    
    if (señal ==fuera):
        print ('SALIMOS del mercado')
        telegram_send("3.OUT Señal Kalman v1\n"+ instrumento_ +"\nPrecio = " + str(data.iloc[(indiceLast_-i),price_]) + "\n***  Kalman level = "+ str(data.iloc[(indiceLast_-i),kalman_])+
                     "\nTime: " + str(data.index[indiceLast_]))
        sleep(5)
    
    

    return señal


# In[7]:


miDelay =2

#TICKERS

tickers = ['FER.MC','SAN.MC','COL.MC','IBE.MC','NTGY.MC','SAB.MC','ACX.MC','PHM.MC','MRL.MC','TEF.MC','AMS.MC','VIS.MC','MTS.MC','MAP.MC','CLNX.MC','BBVA.MC','CABK.MC','MEL.MC','AENA.MC','BKT.MC','REE.MC','FDR.MC','ACS.MC','ITX.MC','ENG.MC','ANA.MC','ELE.MC','GRF.MC','IAG.MC','SGRE.MC']

tickersCurrencies =['EURUSD=X', 'EURGBP=X' ,'EURCHF=X', 'EURJPY=X', 'EURNZD=X', 'EURCAD=X', 'EURAUD=X','USDCHF=X', 
         'USDJPY=X','GBPCAD=X', 'GBPUSD=X', 'GBPJPY=X', 'GBPCHF=X', 'GBPNZD=X', 'GBPAUD=X',
         'NZDCAD=X', 'NZDUSD=X', 'NZDCHF=X', 'NZDJPY=X','JPY=X','EURSEK=X','USDCAD=X','AUDCAD=X',
         'KC=F','HG=F', 'CORN', 'CL=F', 'ZS=F','ZW=F','GC=F','ZW=F',
         'ETH-USD','PFE',
        '^IXIC', '^GSPC', '^GDAXI'
         ]


   


try: 
    df1 = pd.read_csv('tickersSP500_estadoIN_OUT.csv')   #('tickersIbex_estadoIN_OUT.csv')
    # converting to dict
    Ibex_dict = dict(df1.values)
    
    #df2 = pd.read_csv('tickersCurrencies_estadoIN_OUT.csv')
    # converting to dict
    #Currencies_dict = dict(df2.values)

except:
    #Currencies_dict = dict.fromkeys(tickersCurrencies, fuera) #convertir el array en un diccionario
    Ibex_dict = dict.fromkeys(tickers_sp500, fuera)





#VALORES DEL IBEX 
for i in range(len(tickers_sp500)): 

    if (Ibex_dict[tickers_sp500[i]]==fuera):
        señal= checkKalman(tickers_sp500[i])     
        Ibex_dict[tickers_sp500[i]]=señal
        sleep(miDelay)
    else: 
        señal= checkKalman_OUT(tickers_sp500[i])     
        Ibex_dict[tickers_sp500[i]]=señal
        sleep(miDelay)            

df=pd.DataFrame(list(Ibex_dict.items()),
               columns=['tickers', 'in_out'])
df.to_csv('tickersSP500_estadoIN_OUT.csv',index=False)
    
          


# # GRAFICADOR

# In[8]:


"""

#Interval required 1 minute
#data = yf.download(tickers='REE.MC', period='1d', interval='1m')

#declare figure
fig = go.Figure()

#Candlestick
fig.add_trace(go.Candlestick(x=data.index,
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                close=data['Close'], name = 'market data'))

# Add titles

fig.layout.update(
    title='REE.MC live share price evolution',
    yaxis_title='Stock Price (USD per Shares)')

# X-Axes

fig.update_xaxes(
    rangeslider_visible=True,
    rangeselector=dict(
        buttons=list([
            dict(count=15, label="15m", step="minute", stepmode="backward"),
            dict(count=45, label="45m", step="minute", stepmode="backward"),
            dict(count=1, label="HTD", step="hour", stepmode="todate"),
            dict(count=3, label="3h", step="hour", stepmode="backward"),
            dict(step="all")
        ])
    )
)

#Show
fig.show()

"""