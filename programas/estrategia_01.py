# -*- coding: utf-8 -*-
"""
Created on Mon Jul  6 13:18:18 2020

Notas interesantes:
   

@author: INNOVACION
"""

import pandas_datareader as web
import datetime as dt
import numpy as np
import pandas as pd
import mplfinance as mpf

import matplotlib.pyplot as plt
from matplotlib import style
import matplotlib.dates as mdates

from quant_j3_lib import *  #ojo si no esta en el directorio y no se importó con PY
from breakout import *


style.use ('ggplot')   #poner Spider in graph automatico



#/***************************Funciones con tareas parciales */


def mensaje():
    'Calcula el promedio de dos números.'
    return 32
#___________________________________________ mensaje FIN  




################################################## main()
def main():
    """Estrategia basica, v0

    Trataremos de implementar la primera estrategia usando Analisis técnico
    
        ax^2 + bx + c = 0.

    Utiliza la fórmula general (también conocida
    coloquialmente como el "chicharronero").

    Parámetros:
    a -- 
    b -- 
    c -- 
    
    Devuelve:
    Valores trabajados y ordenados

    Excepciones:
    ValueError -- Si (a == 0)
    
    """


    #Inicializaciones
    drop = []               # initializing list to store 
    a1 = np.array([1, 2, 3, 4, 5]) #defining the ndarray
    #a= pd.Series([a, b, c])
    diccionario_01 = {}     # inicializo un diccionario
    
  
    start =dt.datetime(2010,1,1)
    #end = dt.datetime(2020,9,6)
    end= dt.datetime.today()
    tickers = ['AAPL', 'MSFT', '^GSPC', 'ELE.MC']  # apple,microsfoft,sp500, endesa
    
    #a.- Leer de WEB
    df =web.DataReader(tickers[3], 'yahoo', start, end)   # leemos los valore sde tesl    #Guardarlo en fichero .CSV
    df.to_csv('endesa.csv')
    #b.- Leer de .CSV
    df = pd.read_csv('endesa.csv', parse_dates=True, index_col=0)
    #mostrar comienzo final del fichero
    
    print(df.head())
    print(df.tail())
    
    #PLOTEAR
    """
    df[['Low','High']].plot()
    df.plot()
    plt.show()
    """
  
    
  
    ################
    #Ejemplos depueracion de la libreria
    
    #df['tendencia']=tendencia_estadistica(df["Adj Close"], periodo =6, parametro=1)
    #MAX_min_Relativos(df["tendencia"], dataFrameStock= df)
    #salvarExcel(df)
    
    #MACD(df)
    #ATR(df)
    #BollBnd(df)
    #RSI(df)
    #MovingAverage(df)
    #ExponentialMovingAverage(df)
    #volatilidad_std, volatilidadMedia= volatility_j(df)
    #OBV(df[])
    """
    m_,b_ =slopeJ3(df['Adj Close'])  # devuelve pendiente y termino independiente
    print ("LA ECUACION DE LA RECTA CALCULADA POR LA REGRESION LINEAL ES\n  y= ", m_, "X + ",b_)
    var_03 = df.columns.get_loc("Adj Close")    # Para usar iLoc necesito la posicion de un 'label'
    m_,b_ =slopeJ3(df.iloc[700:1100,var_03])    # devuelve pendiente y termino independiente
    print ("LA ECUACION DE LA RECTA CALCULADA POR LA REGRESION LINEAL ES\n  y= ", m_, "X + ",b_)
    var_03 = df.columns.get_loc("Adj Close")    # Para usar iLoc necesito la posicion de un 'label'
    m_,b_ =slopeJ3(df.iloc[900:1100,var_03])    # devuelve pendiente y termino independiente
    print ("LA ECUACION DE LA RECTA CALCULADA POR LA REGRESION LINEAL ES\n  y= ", m_, "X + ",b_)
    """
    
    #################################################### BreakOut()
    estrategia_breakout_main()
   
    
    #Otros calculos
    
    #CALCULANDO MOVING AVERAGE
    df['100ma']=df['Adj Close'].rolling(window=100).mean()
    df['40ma']=df['Adj Close'].rolling(window=40).mean()
    print(df.tail())
    
    #ploteando en Matplotlib
    """
    ax1=plt.subplot2grid((6,1),(0,0), rowspan=5, colspan=1)
    ax2=plt.subplot2grid((6,1),(5,0), rowspan=1, colspan=1, sharex=ax1)
    
    
    ax1.plot(df.index, df['Adj Close'])
    ax1.plot(df.index, df['100ma'])
    ax1.plot(df.index, df['40ma'], color='springgreen')
    ax2.bar(df.index, df['Volume'])
    
    plt.show()
    """
    
    
    #**************************** RESAMPLE DATA para agrupar periodos
    df_ohlc =df['Adj Close'].resample('10D').ohlc()   #mean//sum
    df_ohlc['volume']=df['Volume'].resample('10D').sum()
    print(df_ohlc.head())
    
    
    
    #**************************** Codigo para graficar velas usando mpf 
    #mc = mpf.make_marketcolors(up='g',down='r',edge='black',volume='blue')
    #s  = mpf.make_mpf_style(marketcolors=mc)
    #mpf.plot(df_ohlc,type='candle',volume=True, style=s)
    
    """
    a=9
    a+=9
    print(a)
    MAX_min_Relativos()
    print(a)
    regresionLineal()
    
"""    

################################################## main() FIN


#/*******************************************/
#/* Programa Principal  *********************/
#/*******************************************/

main()



"""
El indice del miedo. Hoffmann  Vixal-4
"""
