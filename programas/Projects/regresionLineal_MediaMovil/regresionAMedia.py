# -*- coding: utf-8 -*-


"""
******************************************************************************
ESTRATEGIA DE INVERSION AUTOMATICA COMPLETA BASADA EN 
******************************************************************************
******************************************************************************
Our rules are:

Trade only with the trend, meaning both the 200-period linear regression line and 200-period moving average are in agreement.
When the above rule is true, take long trades when price hits the bottom band of the Keltner channel. Likewise, when both the linear regression line and moving average are in agreement in a downtrending market, a touch of the upper band of the Keltner channel would be a signal to go short.
To exit a trade, we can use either a shift in the trend – i.e., the slope of either the linear regression line or moving average changes (opposite the direction of the trade) – or a touch of the linear regression line.

Fuente: https://www.daytrading.com/linear-regression-line


            


Started on 24/May/2021
Version_1: 

Objetivo: 



@author: J3Viton

"""

# J3_DEBUG__ = False  #variable global (global J3_DEBUG__ )

TELEGRAM__ = True




################################ IMPORTAMOS MODULOS A UTILIZAR.
import pandas as pd
import numpy as np
import datetime as dt
import pandas_datareader as web
import time

import yfinance as yf

import statsmodels.api as sm
import matplotlib

import matplotlib.pyplot as plt
plt.rcParams['figure.figsize'] = 18, 8
plt.style.use("bmh")   


import quant_j3_lib as quant_j
from telegram_bot import *



df_sg = pd.DataFrame(columns=('estrategia','instrumento', 'fecha', 'aux1', 'aux2'))

#/***************************Funciones con tareas parciales */


#/***************************************  Guardamos Informacion en fichero JSON 
import json

with open('config.json', 'r') as file1:
    config = json.load(file1)

database_depar =    config['departamento']
database_password = config['PRODUCTION']['DB_PASSWORD']
empleado = config['empleados'][0]['nombre']



with open('senales.json', 'r') as file:
    senales = json.load(file)

file1.close()
file.close()

#/***************************************  Guardamos configuracion en fichero

#################################################### Clase para testing

class TestingClass:

    """CLASE PARA TESTEO 
    Con esta funcion vamos a gestionar el testeo de funiones y el modo debug para 
    pintar graficos y cademas.
    Tenemos la variable global __J3 Debug, tendria que cambiarlo a uyn metodo.
       
    """    
    def __init__(self, para1, para2):
        self.para_01 = para1
        self.para_02 = para2

    def myfunc(self):
        'documentacion sencilla...'
        print("Hello my parametro is " + self.para_02)
        
    def testing_123(self):
        slopeJ3_2points(1,3,2,4)
    def debugging_(self):
        return (J3_DEBUG__)

#################################################### Clases FIN


#################################################### CLASE ANALISIS REGRESION LINEAL




#/******************************** FUNCION PRINCIPAL main() *********/
def main():
    """Estrategia basica Regresion a la media, v0

    
    Para una serie de valores del IBEX y del SP500, calculamos la mediaExponencial de 200 sesiones (y su regresion lineal), 
    la regresion lineal de la nube de puntos del cierre (recta que más se aproxima a esos datos). 
    Luego si la pendiente de ambas regresiones es positiva y el precio toca la banda de Bollinger inferior...
    La estrategia dice que el precio va a subir ir a buscar la linea de la regresion a la media calcualda.
    
    Guardamos las señales en un Json y en un excel.
    Enviamos las señales a un bot tegram
    Excel guardamos todos los datos relevantes, incluyendo pendientes de 
        
    Parámetros:
    a -- 
    b -- 
    c -- 
    
    Devuelve:
    Valores 

    Excepciones:
    ValueError -- Si (a == 0)
    
    """    

    
    # Enter start and end date
    #start = '2020-1-20'
    #end = '2021-1-20'
    
    #start =dt.datetime(2000,1,1)
    start =dt.datetime.today() - dt.timedelta(days=400)    #un año tiene 250 sesiones.
    #end = dt.datetime(2019,10,1)
    end= dt.datetime.today()  - dt.timedelta(days=1)        #Quito hoy para no ver el valor al ejecutar antes del cierre
    #end = '2021-9-19'
    
    if(TELEGRAM__):
        telegram_send("2.- Estrategia Regresion a la media V0.1.\n ")
        

    # Create Regressionanalyis class
    #ra = Regressionanalysis('^NSEI', start, end, interval='60m')
    #ra.linear_regression(independent='Open', dependent='Close')
    # Me resulta complicado con esta libreria, no merece la pena ahora que estamos porbando, ya llegaran tiempos de afinar.
    
    tickers5 = ['AAPL', 'MSFT', '^GSPC', 'ELE.MC','SAN.MC', 'BBVA.MC']  #,'ANA.MC','MTS.MC','GRF.MC']  # apple,microsfoft,sp500, endesa
    tickers_ = ['BKT.MC'] 
    tickers = ['FER.MC','COL.MC','IBE.MC','NTGY.MC','SAB.MC','ACX.MC','PHM.MC','SAN.MC','MRL.MC','TEF.MC','AMS.MC','VIS.MC','MTS.MC','MAP.MC','CLNX.MC','BBVA.MC','CABK.MC','MEL.MC','AENA.MC','BKT.MC','REE.MC','FDR.MC','ACS.MC','ITX.MC','ENG.MC','ANA.MC','ELE.MC','GRF.MC','IAG.MC','SGRE.MC']
    tickersCurrencies =['EURUSD=X', 'EURGBP=X' ,'EURCHF=X', 'EURJPY=X', 'EURNZD=X', 'EURCAD=X', 'EURAUD=X','USDCHF=X', 
             'USDJPY=X','GBPCAD=X', 'GBPUSD=X', 'GBPJPY=X', 'GBPCHF=X', 'GBPNZD=X', 'GBPAUD=X',
             'NZDCAD=X', 'NZDUSD=X', 'NZDCHF=X', 'NZDJPY=X','JPY=X','EURSEK=X','USDCAD=X','AUDCAD=X',
             'KC=F','HG=F', 'CORN', 'CL=F', 'ZS=F','ZW=F','GC=F','X','ZW=F',
             'ETH-USD','PFE'
             ]
        
    #VALORES DEL IBEX 

    for i in range(len(tickers)): 
        print(tickers[i])
        analisis(tickers[i], start, end)
        #time.sleep (1)
        
    
    for i in range(len(tickersCurrencies)): 
        print(tickersCurrencies[i])
        analisis(tickersCurrencies[i], start, end)        
        #time.sleep (1)
        
    
    #VALORES DEL SP50
    
    sp_url= 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    sp=pd.read_html(sp_url,header=0)[0]
    print (sp.info())
    
    for i in range(len(sp)):
         symbol=sp.iloc[i,0] 
         #df = yf.download(symbol, start, end)
         print(symbol)
         analisis(symbol, start, end)
         #time.sleep (1)
    
    
    
    
    print ("******************************************************************************That´s all") 
    print ("****************************************************************************************")       
    
    
    
#/**********************************************************************main()    
 
MaquinaE = {'reposo':0, 'tendencia_UP':1, 'tendencia_DOWN':2, 'touchBollinger_botton':3}
estado = MaquinaE['reposo']

   
   
#/******************************** FUNCION PRINCIPAL *********/    
def analisis(instrumento, start, end):
    """Estrategia divergencias Precio vr RSI, v0

    Funcion que recibe el nombre de un insturmeto para analizar. busca datos en Yahoo y realiza la priemra estrategia con 
    por divergencias con RSI y graba un excel.
    
        
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
    señal =False
    
    # 0.- Lemos los datos 
 
    
    try:
        df = yf.download(instrumento, start, end)
        df.dropna(inplace=True)  
        #yf.download("AMZN AAPL GOOG", start="2017-01-01", end="2017-04-30")
        #df =web.DataReader(instrumento, 'yahoo', start, end)    DA ERROR DE YAHOO FINANCES
    except:
        return False
 
    if df.empty:
        print('DataFrame is empty!')
        return False

    #Test
    # df=quant_j.PGO(df)    
 
    # 1.- Calculamos media de las ultimas sesiones y la regresion lineal
    coef_, intercept_ =quant_j.linearRegresion_J3(df['Adj Close'],instrumento=instrumento)

    # 2.- Calculamos la Media Movil    
    df=quant_j.MovingAverage(df,long_=200,short_=50, instrumento=instrumento)

    # 2_1.- Calculamos la media Movil Exponencial
    df= quant_j.ExponentialMovingAverage(df,long_=200,short_=20)    
    
    # 3.- regresion lineal precio n ultimas sesiones  (220 = sesiones anuales)
    df_aux= df.iloc[-200:, [4]]   #4-> Adj Close
    # 3.1.- Calculamos media de las ultimas 'n' sesiones y la regresion lineal
    coef_linear, intercept_linear =quant_j.linearRegresion_J3(df_aux,instrumento=instrumento)



    ######################################################  ESTRATEGIA
    parada =9 
    
    # 1.- MEDIA DE 200 SESIONES ASCENDENTE
    #   Calculamos de la media aritmetica la regresion lineal para ver la esencia
    ema200_=df.columns.get_loc("EMA_200")
    df_aux2= df.iloc[-200:, ema200_]
    df_aux2.dropna(inplace=True)  
    # 3.1.- Calculamos media de las ultimas 'n' sesiones y la regresion lineal
    coef_ema200_, intercept_ema200_ =quant_j.linearRegresion_J3(df_aux2,instrumento=instrumento+'  de ema200')  
    
    
    # 4.- Bollinger 
    df= quant_j.BollBnd(df,n=20)
    
    # 2.- Ambas pendientes//tendencias son ascendentes (ma220 y linearRegresion)

    if (coef_linear>0  and  coef_ema200_>0):
        bb_up_ = df.columns.get_loc("BB_up")
        bb_dn_ = df.columns.get_loc("BB_dn")
        price_ = df.columns.get_loc("Adj Close")   
        indiceHoy_ = len(df)-1
        
        a=df.iloc[indiceHoy_,price_] 
        b=1* df.iloc[indiceHoy_,bb_dn_]
        
        
        if( df.iloc[indiceHoy_,price_] < ( 1* df.iloc[indiceHoy_,bb_dn_]) ):   #Precio por debajo de la banda de Bollinger, dentro de tendencia ascendente
            señal =True
        else:
            señal = False
        
    if (señal == True):
        parada=8
        beneficio =(200*coef_linear + intercept_linear)-( df.iloc[indiceHoy_,price_] )
        
        #Guardo en EXCEL file
        quant_j.saveSignal('RegresMedia_', 'RegresionMedia b0 (IN)', instrumento,end, coef_linear, coef_ema200_, df.iloc[indiceHoy_,price_] , beneficio)
        
        #Mando señal al bot telegram
        if(TELEGRAM__):
            telegram_send("Señal en la estrategia Regresión a la Media b0.0.\nMira " +instrumento)
        
        #actualizamos JSON, senales.
        #Añado un mienbro a la lista
        senales['regresiones'].append({"ticker": "jjj", "fecha": "26-09-2021", "BuySell" : 0, "coef_precio": 9.99, "intercep_precio": 9.9, "coef_ema": 9.9, "intercep_ema": 9.9, "precioIN": 9, "beneficio": 9.9})
        
        indice =senales['indice']
                
        senales['regresiones'][indice]['ticker']=instrumento
        senales['regresiones'][indice]['BuySell']=1
        senales['regresiones'][indice]['coef_ema']=coef_ema200_[0]
        senales['regresiones'][indice]['intercep_ema']=intercept_ema200_
        senales['regresiones'][indice]['coef_precio']=coef_linear[0][0]         #no sé muy bien por qué esta difererencia de ser array o serie
        senales['regresiones'][indice]['intercep_precio']=intercept_linear[0]
        senales['regresiones'][indice]['precioIN']=df.iloc[indiceHoy_,price_]
        senales['regresiones'][indice]['beneficio']=beneficio[0][0]
        senales['regresiones'][indice]['fecha']=end.strftime('%d-%m-%Y')
        senales['indice']=indice+1
        with open('senales.json', 'w') as file:
            json.dump(senales ,file)
        file.close()
            



#/*******************************************/
#/* Programa Principal  *********************/
#/*******************************************/

main()
