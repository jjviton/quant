# -*- coding: utf-8 -*-


"""
******************************************************************************
ESTRATEGIA DE INVERSION AUTOMATICA COMPLETA BASADA EN 
******************************************************************************
******************************************************************************
Our rules are:

Trade only with the trend, meaning both the 100-period linear regression line and 100-period moving average are in agreement.
When the above rule is true, take long trades when price hits the bottom band of the Keltner channel. Likewise, when both the linear regression line and moving average are in agreement in a downtrending market, a touch of the upper band of the Keltner channel would be a signal to go short.
To exit a trade, we can use either a shift in the trend – i.e., the slope of either the linear regression line or moving average changes (opposite the direction of the trade) – or a touch of the linear regression line.

Fuente: https://www.daytrading.com/linear-regression-line


            


Started on 24/May/2021
Version_1: 

Objetivo: 



@author: J3Viton

"""

# J3_DEBUG__ = False  #variable global (global J3_DEBUG__ )

TELEGRAM__ = False


################################ IMPORTAMOS MODULOS A UTILIZAR.
import pandas as pd
import numpy as np
import datetime as dt
import pandas_datareader as web

import yfinance as yf

import statsmodels.api as sm

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


#################################################### func_mensaje()
def func_mensaje():
    """Estrategia basica, v0
    Trataremos de implementar la primera estrategia usando Analisis técnico 
        ax^2 + bx + c = 0.
    Parámetros:
    a --   
    Devuelve:
    Valores trabajados y ordenados

    Excepciones:
    ValueError -- Si (a == 0)
    """
    #message = Text(Point(700,790), 'Autor Dani J 2018')

    global variable_1   #Ejemplo variable Global usada dentro de funcion local
    variable_1 = 12

    variable_2 = 32     #Ejemplo de variable local con igual nombre de la global, no se ve la global.
            
    message = Text(Point(700,790), variable_2 )
    message.setTextColor('red')
    message.setStyle('italic')
    message.setSize(8)
    message.draw(win)
#################################################### func_mensaje() FIN





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
class Regressionanalysis:
    """
    
    Ejemplo de uso:
        # Enter start and end date
        start = '2020-1-20'
        end = '2021-1-20'
    
        # Create Regressionanalyis class
        ra = Regressionanalysis('^NSEI', start, end, interval='60m')
        
        ra.linear_regression(independent='Open', dependent='Close')
        df = ra.rolling_reg(period=14)
    """
    
    # The constructor will be called during the object creation and the data feed for
    # the object is stored which could be used for further analysis
    def __init__(self, ticker, start, end, interval):

        self.ticker = ticker
        self.start = start
        self.end = end
        self.interval = interval
        self.data = yf.download(self.ticker, start=self.start,
                                end=self.end, interval=self.interval)

# --------------------------------------------------------------------------------------------------------------------

    def linear_regression(self, independent='Open', dependent='Close'):

        # This function simulates simpnle linear regression fit using given dependent and independent variables and
        # provides summary for the same
        df = self.data
        x1 = df[independent] #orignal
        
        #dff = pd.DataFrame(columns=['col_1'],index=range(len(df)))
        #x= dff['col_1']
        #x=x1.copy()
        
        #x = df.index  #recoege las fechas y no vale para numPy
        datos_ = np.array(range(len(df)))  
        dff= pd.DataFrame(datos_,columns=['col_1'])
        x=dff['col_1']
        
        #x1 = df.index 
        y = df[dependent]
        x = sm.add_constant(x1)
        x1 = sm.add_constant(x1)

        # Create regression model
        reg_model = sm.OLS(y, x).fit()

        # Generate model summary
        print(reg_model.summary())

        # Generate a component and component-plus-residual (CCPR) plot.
        fig = sm.graphics.plot_ccpr(reg_model, x )
        #fig = sm.graphics.plot_ccpr(reg_model, independent)
        fig.tight_layout(pad=1.0)

# ---------------------------------------------------------------------------------------------------------------------

    def rolling_reg(self, period=14):

        df = self.data
        df = df.dropna()
        window = period
        df['a'] = None
        df['b1'] = None

        # Calculate rolling fit by iterating each value
        for i in range(window, len(df)):
            temp = df.iloc[i-window:i, :]
            RollOLS = sm.OLS(temp.loc[:, 'Close'], sm.add_constant(
                temp.loc[:, ['Open']])).fit()
            df.iloc[i, df.columns.get_loc('a')] = RollOLS.params[0]
            df.iloc[i, df.columns.get_loc('b1')] = RollOLS.params[1]

        # The following line gives you predicted values in a row, given the prior row's estimated parameters
        df['predicted'] = df['a'].shift(1)+df['b1'].shift(1)*df['Open']

# --------------------------------------------------------------------------------------------------------------

        # Calculate profit or loss

        df['pnl'] = 0
        # The position is long profit = buy price (open) - sell price (close)
        df.loc[(df['predicted'] < df['Open']), 'pnl'] = df['Open']-df['Close']
        # The position is short the profit will be cover price(close) - Short price(open)
        df.loc[(df['predicted'] > df['Open']), 'pnl'] = df['Close']-df['Open']

        # Count profit making and loss making trades

        npt = df[df["pnl"] > 0].count()["pnl"]
        nlt = df[df["pnl"] < 0].count()["pnl"]

        # Calculate metrics like returns(%), max drawdown

        df['ret'] = 0

        df.loc[(df['predicted'] < df['Open']), 'ret'] = (
            df['Open']-df['Close'])/df['Open']

        df.loc[(df['predicted'] > df['Open']), 'ret'] = (
            df['Close']-df['Open'])/df['Open']
        daily_pct_c1 = df['ret']

        daily_pct_c1.reset_index(drop=True)

        # Drawdown and max drawdown

        window = int(252*6.5)
        rolling_max = df['ret'].rolling(window, min_periods=1).max()
        drawdown = df['ret']/rolling_max - 1.0

        # Print the results in a simulated tab
        fig, ax = plt.subplots(3, figsize=(10, 6), constrained_layout=True)
        ax[0].hist(daily_pct_c1, bins=50)
        ax[0].set(title='Retutns(%) Distribution')
        ax[1].set(title='Backtest Estimate')
        ax[1].text(0.5, 0.3, "NET pnl (POINTS) "+str(df["pnl"].sum()),
                   color='green', fontsize=12, ha='center')
        ax[1].text(0.5, 0.5, "Accuracy (%) "+str("%.5f" %
                                                 float((npt/(npt+nlt))*100)), color="green", fontsize=12, ha='center')
        ax[1].text(0.5, 0.7, "Total number of trades "+str(npt+nlt),
                   color='green', fontsize=12, ha='center')
        ax[2].plot(df.index, (drawdown), 'r')
        ax[2].set(title='Drawdown Curve')
        plt.show()

        return df




#/******************************** FUNCION PRINCIPAL main() *********/
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
    # Enter start and end date
    #start = '2020-1-20'
    #end = '2021-1-20'
    
    #start =dt.datetime(2000,1,1)
    start =dt.datetime.today() - dt.timedelta(days=1000)    #un año tiene 250 sesiones.
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
    tickers_ = ['CLNX.MC'] 
    tickers = ['FER.MC','COL.MC','IBE.MC','NTGY.MC','SAB.MC','ACX.MC','PHM.MC','SAN.MC','MRL.MC','TEF.MC','AMS.MC','VIS.MC','MTS.MC','MAP.MC','CLNX.MC','BBVA.MC','CABK.MC','MEL.MC','AENA.MC','BKT.MC','REE.MC','FDR.MC','ACS.MC','ITX.MC','ENG.MC','ANA.MC','ELE.MC','GRF.MC','IAG.MC','SGRE.MC']
        
    #valorNum = 7
    for i in range(len(tickers)): 
        analisis(tickers[i], start, end)
    
    
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
 
    
    
    df = yf.download(instrumento, start, end)
    #yf.download("AMZN AAPL GOOG", start="2017-01-01", end="2017-04-30")
    #df =web.DataReader(instrumento, 'yahoo', start, end)    DA ERROR DE YAHOO FINANCES
    
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
    
    # 1.- MEDIA DE 200 SESIONES ACCENDENTE
    #   Calculamos de la media aritmetica la regresion lineal para ver la esencia
    ema200_=df.columns.get_loc("EMA_200")
    df_aux2= df.iloc[-200:, ema200_]
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
        quant_j.saveSignal('RegresMedia_', 'RegresionMedia b0 (IN)', instrumento,end, coef_linear, coef_ema200_, df.iloc[indiceHoy_,price_] , beneficio)
        
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
