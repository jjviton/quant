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

En esta verison del programa organizamos en clases y lo tenemso preparado para hacer backTesting.
            
Jupyter: http://localhost:8888/notebooks/Documents/J3/100.-%20cursos/Quant_udemy/programas/Projects/regresionLineal_MediaMovil/backtest_beta0.ipynb

Started on 24/NOV/2021
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

"""
import matplotlib.pyplot as plt
plt.rcParams['figure.figsize'] = 18, 8
plt.style.use("bmh")   
"""

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




#################################################### Clase Estrategia 

class StrategyClass:

    """CLASE ESTRATEGIA

       
    """  
    
    dfLog = pd.DataFrame(columns=('Date','Senal', 'Price','Objetivo'))
    dfCartera = pd.DataFrame(columns=['instrumento','long_short_out', 'date','precio'])
    #dfCartera.set_index('instrumento',inplace=True)

    
    def __init__(self, instrumento= 'IBE.MC', para1=1, para2=1):
        self.para_01 = para1
        self.para_02 = para2
        self.__privado = "atributoPrivado"
        self.dfLog = pd.DataFrame(columns=('Date','Senal', 'Price'))
        
        self.instrumento =1
        self.startDate=1
        self.endDate =1
        
        StrategyClass.dfCartera= quant_j.leerExcel('carteraRegre')
        dfx2=StrategyClass.dfCartera
        
    def analisis(self, instrumento, startDate, endDate, DF):
        """Funcion que....
        Returns:nada

        """

        """    
        self.instrumento=instrumento 
        self.startDate=startDate
        self.endDate = endDate
        """     
        StrategyClass.dfCartera= quant_j.leerExcel('log'+instrumento)
        StrategyClass.dfCartera= quant_j.leerExcel('carteraRegre')
        
        dfx=StrategyClass.dfLog
        dfx2=StrategyClass.dfCartera
        
        #SI no esta el instrumento en la cartera, paso a analizarlo
        if not (instrumento in StrategyClass.dfCartera.values)  :   
               #StrategyClass.dfCartera=StrategyClass.dfCartera.append({'instrumento': instrumento, 'precio': 1}, ignore_index=True) 
            self.analisis_IN(instrumento, startDate, endDate, DF)
        #Si está el isnturmetno en la cartera, miro si eestoy largo o corto o fuera
        else:
            col_ =  StrategyClass.dfCartera.instrumento.isin([instrumento])   # devuelve una serie con true/false donde esta el obejto buscado
            linea_2 = col_[col_==True]   # hago una serie con los true, normalmente un solo elemento
            linea_3=linea_2.index
            linea_=linea_3[0]
            #print(linea_)
            l_s_o =   StrategyClass.dfCartera.columns.get_loc("long_short_out")
            comprado_= StrategyClass.dfCartera.iloc[linea_ , l_s_o]   
            if(comprado_ == 1):      #Estoy en largo, miro si salir o no.
                self.analisis_OUT(instrumento, startDate, endDate, DF)
                return
            if(comprado_== 0):    # Estoy fuera de mercado
                self.analisis_IN(instrumento, startDate, endDate, DF)
                return
            if(comprado_ ==-1):   # Estoy en corto
                return   
   
        return

        
    def analisis_IN(self, instrumento, startDate, endDate, DF):
        
        """
        self.instrumento = instrumento
        self.startDate=startDate
        self.endDate = endDate
        """
        
        resultado= analisis_v2(instrumento, startDate, endDate, DF)    #jj
        
        quant_j.salvarExcel(StrategyClass.dfLog, "log"+instrumento)
        quant_j.salvarExcel(StrategyClass.dfCartera, "carteraRegre")

        dfx=StrategyClass.dfLog
        dfx2=StrategyClass.dfCartera
        print (dfx2)

        return resultado  # SELL_ HOLD_
    
    def analisis_OUT(self, instrumento, startDate, endDate, DF):
        
        """
        self.instrumento = instrumento
        self.startDate=startDate
        self.endDate = endDate
        """
        print('aqui estoy en out')
        estrategiaSALIDA(instrumento, startDate, endDate, DF)
        
        #Actualizamos el Log y la Cartera
        quant_j.salvarExcel(StrategyClass.dfLog, "log"+instrumento)
        quant_j.salvarExcel(StrategyClass.dfCartera, "carteraRegre")
        
        dfx=StrategyClass.dfLog
        dfx2=StrategyClass.dfCartera
        
        return
    
    def analisis_Log(self):
        return True
    
    def backTesting(self):
        return True

    def myfunc(self):
        'documentacion sencilla...'
        print("Hello my parametro is " + self.para_02)
        
    def testing_123(self):
        slopeJ3_2points(1,3,2,4)
    def debugging_(self):
        return (J3_DEBUG__)

#################################################### Clase FIN


def estrategiaSALIDA(instrumento, startt, endd, df):
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
    # 0.- Lemos los datos    
    try:
        if df.empty:
            df = yf.download(instrumento, startt, endd)
            df.dropna(inplace=True)  
            print ('descargo datos desde Spyder')
            #yf.download("AMZN AAPL GOOG", start="2017-01-01", end="2017-04-30")
            #df =web.DataReader(instrumento, 'yahoo', start, end)    DA ERROR DE YAHOO FINANCES
        else:
            print (' datos desde archivo')
    except:
        #resultados['senal']   =  503     #Service Unavaliable
        return #resultados
    """
            col_ =  StrategyClass.dfCartera.instrumento.isin([instrumento])   # devuelve una serie con true/false donde esta el obejto buscado
            linea_2 = col_[col_==True]   # hago una serie con los true, normalmente un solo elemento
            linea_3=linea_2.index
            linea_=linea_3[0]
            #print(linea_)
    """
    
 
    
    col_ =          StrategyClass.dfCartera.instrumento.isin([instrumento]) 
    linea_2 = col_[col_==True]
    linea_3=linea_2.index
    linea_=linea_3[0]    
    l_s_o =         StrategyClass.dfCartera.columns.get_loc("long_short_out")
    comprado_=      StrategyClass.dfCartera.iloc[linea_ , l_s_o]      
    precio_ =       StrategyClass.dfCartera.columns.get_loc("precio")
    precioCompra_=  StrategyClass.dfCartera.iloc[linea_ , precio_]      
    
    #Condicion de salida " precio baja un 10% el precio de entrada
    
    price_ =      df.columns.get_loc("Close")   
    indiceHoy_ = len(df)-1                          #Revisar este punto
    PrecioHoy =   df.iloc[indiceHoy_,price_]
    
    if (endd== '2013-03-21'):
        parada=9
        print('precio hoy', PrecioHoy)
        print('precio compra', precioCompra_[linea_])
    
    if( PrecioHoy < (precioCompra_)   or (PrecioHoy > 1,20*(precioCompra_) ) ):    #-(precioCompra*0.1))) :
        señal =  0   # salta el stoploss y me salgo
        StrategyClass.dfCartera.iloc[linea_ , l_s_o]  = 0            
        StrategyClass.dfCartera.iloc[linea_ , precio_]  = PrecioHoy
        
        
        StrategyClass.dfLog.loc[endd,'Date'] = endd
        StrategyClass.dfLog.loc[endd,'Senal']= 0
        StrategyClass.dfLog.loc[endd,'Price']= df.iloc[indiceHoy_,price_]    
        
        dfx=StrategyClass.dfLog
        dfx2=StrategyClass.dfCartera
    else:
        StrategyClass.dfLog.loc[endd,'Date'] = endd
        StrategyClass.dfLog.loc[endd,'Senal']= 1
        StrategyClass.dfLog.loc[endd,'Price']= df.iloc[indiceHoy_,price_]    
        
        dfx=StrategyClass.dfLog
        dfx2=StrategyClass.dfCartera        
        
    return





def analisis_v2(instrumento, startt, endd, df):
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
    resultados = dict();    # Creamos un diccionario para devolver los datos
    resultados['senal']   =  0
    
    # 0.- Lemos los datos    
    try:
        if df.empty:
            df = yf.download(instrumento, startt, endd)
            df.dropna(inplace=True)  
            print ('descargo datos desde Spyder')
            #yf.download("AMZN AAPL GOOG", start="2017-01-01", end="2017-04-30")
            #df =web.DataReader(instrumento, 'yahoo', start, end)    DA ERROR DE YAHOO FINANCES
        else:
            print (' datos desde archivo')
    except:
        resultados['senal']   =  503     #Service Unavaliable
        return resultados
 

    if df.empty:
        print('DataFrame is empty!!!!')
        resultados['senal']   =  503     #Service Unavaliable
        return resultados

    #Test
    # df=quant_j.PGO(df)    
 
    # 1.- Calculamos media de las ultimas sesiones y la regresion lineal
    coef_, intercept_ =quant_j.linearRegresion_J3(df['Close'],instrumento=instrumento)

    # 2.- Calculamos la Media Movil    
    df=quant_j.MovingAverage(df,long_=200,short_=50, instrumento=instrumento)

    # 2_1.- Calculamos la media Movil Exponencial
    df= quant_j.ExponentialMovingAverage(df,long_=200,short_=20)    
    
    # 3.- regresion lineal precio n ultimas sesiones  (220 = sesiones anuales)
    col_ = df.columns.get_loc("Close")
    df_aux= df.iloc[-200:, col_]  #4-> Adj Close
    # 3.1.- Calculamos media de las ultimas 'n' sesiones y la regresion lineal
    coef_linear, intercept_linear =quant_j.linearRegresion_J3(df_aux,instrumento=instrumento)



    ######################################################  ESTRATEGIA
    parada =9 
    
    # 1.- MEDIA DE 200 SESIONES ACCENDENTE
    #   Calculamos de la media aritmetica la regresion lineal para ver la esencia
    ema200_=df.columns.get_loc("EMA_200")
    df_aux2= df.iloc[-200:, ema200_]
    df_aux2.dropna(inplace=True)  
    # 3.1.- Calculamos media de las ultimas 'n' sesiones y la regresion lineal
    coef_ema200_, intercept_ema200_ =quant_j.linearRegresion_J3(df_aux2,instrumento=instrumento) #+'  de ema200')  
    
    
    # 4.- Bollinger 
    df= quant_j.BollBnd(df,n=20)
    
    # 2.- Ambas pendientes//tendencias son ascendentes (ma220 y linearRegresion)

    if (coef_linear>0  and  coef_ema200_>0):
        bb_up_ = df.columns.get_loc("BB_up")
        bb_dn_ = df.columns.get_loc("BB_dn")
        price_ = df.columns.get_loc("Close")   
        indiceHoy_ = len(df)-1
        
        a=df.iloc[indiceHoy_,price_] 
        b=1* df.iloc[indiceHoy_,bb_dn_]
        
        
        if( df.iloc[indiceHoy_,price_] < ( 1* df.iloc[indiceHoy_,bb_dn_]) ):   #Precio por debajo de la banda de Bollinger, dentro de tendencia ascendente
            señal =True
        else:
            señal = False
        
    if (señal == True):
        print('***************** Señal...')        
        parada=8
        beneficio = ((200*coef_linear + intercept_linear)-( df.iloc[indiceHoy_,price_] ))
        
        #Guardo en EXCEL file
        quant_j.saveSignal('RegresMedia_', 'RegresionMedia b0 (IN)', instrumento,endd, coef_linear, coef_ema200_, df.iloc[indiceHoy_,price_] , beneficio)
        
        #Mando señal al bot telegram
        if(TELEGRAM__):
            telegram_send("Señal en la estrategia Regresión a la Media b0.0.\nMira " +instrumento)
         
            
        df1=StrategyClass.dfLog
        df2=StrategyClass.dfCartera
            
        ################### Almaceno información en un dataframe log
        #TOBEImprove: añadir nueva linea en el dataFrame para la entrada nueva
        StrategyClass.dfLog.loc[endd,'Date'] = endd
        StrategyClass.dfLog.loc[endd,'Senal']= 1
        StrategyClass.dfLog.loc[endd,'Price']= df.iloc[indiceHoy_,price_]    
        
        ################### Almaceno información en la cartera
        #if(StrategyClass.dfCartera['Instrumento']):
        if not (instrumento in StrategyClass.dfCartera.values)  :   
               StrategyClass.dfCartera=StrategyClass.dfCartera.append({'instrumento': instrumento, 'precio': 1}, ignore_index=True)

        df1=StrategyClass.dfLog
        df2=StrategyClass.dfCartera
        
        #StrategyClass.dfCartera.set_index('instrumento',inplace=True)
        l_s_o =  StrategyClass.dfCartera.columns.get_loc("long_short_out")
        date__ = StrategyClass.dfCartera.columns.get_loc("date")
        precio__ = StrategyClass.dfCartera.columns.get_loc("precio")
        
        linea_ = StrategyClass.dfCartera.instrumento.isin([instrumento])
        
        StrategyClass.dfCartera.iloc[linea_ , l_s_o]        = 1
        StrategyClass.dfCartera.iloc[linea_ , date__]       = endd        
        StrategyClass.dfCartera.iloc[linea_, precio__]      = df.iloc[indiceHoy_,price_]
        
        #StrategyClass.dfCartera.loc['Objetivo']    =beneficio[0]  + df.iloc[indiceHoy_,price_]
        #dfCartera = pd.DataFrame(columns=('instrumemto','long_short_out', 'date'))
        
        df1=StrategyClass.dfLog
        df2=StrategyClass.dfCartera
          
        ########## Tenemos Señal, devolvemos la informacion       
        #resultados = dict();    # Creamos un diccionario para devolver los datos
        resultados['instrumento'] =     instrumento
        resultados['date']   =          endd
        resultados['senal']   =         int(1)     #100 equivale a comprar...
        resultados['PrecioEntrada'] =   df.iloc[indiceHoy_,price_]
        resultados['PrecioObjetivo']=   beneficio[0]  + df.iloc[indiceHoy_,price_]
        return resultados
    else:
        ########## Tenemos Señal, devolvemos la informacion       
        #resultados = dict();    # Creamos un diccionario para devolver los datos
        
        
        ################### Almaceno información en un dataframe log
        StrategyClass.dfLog.loc[endd,'Date'] =endd
        StrategyClass.dfLog.loc[endd,'Senal']=0
        StrategyClass.dfLog.loc[endd,'Price']=0   
        
        ################### Almaceno información en la cartera
        """
        StrategyClass.dfCartera.loc[end,'Instrumento'] =instrumento
        StrategyClass.dfCartera.loc[end,'LongOutShort']=0
        StrategyClass.dfCartera.loc[end,'Price']       =0
        StrategyClass.dfCartera.loc[end,'Objetivo']    =0
        """
        
        resultados['instrumento'] =     instrumento
        resultados['date']   =          endd
        resultados['senal']   =         0     #0 equivale a mantener
        resultados['PrecioEntrada'] =   0
        resultados['PrecioObjetivo']=   0
        return resultados

    #return 99  #devolvemos False si no tenemos señal

#################################################### CLASE ANALISIS REGRESION LINEAL




#/******************************** FUNCION PRINCIPAL main() *********/
#     def main():   
if __name__ == '__main__':    
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

    """ Probando la Clase
    
    
    """
    """
    ##############################  BACKTESTING
    # Rango completo para backTesting
    start2 =dt.datetime(2005,1,2)
    end2   =dt.datetime(2021,11,10)
    start_G= start2.strftime("%Y-%m-%d")
    end_G  =   end2.strftime("%Y-%m-%d")
    TOTAL_len= (end2-start2).days
    print('Tamaño timeseries a analizar:  ', TOTAL_len, 'sesiones')
    
    #ventana de analisis 200 sesiones
    startWindow2 =dt.datetime(2010,1,5)
    endWindow2   =startWindow2 + dt.timedelta(days=200) 
    startWindow= startWindow2.strftime("%Y-%m-%d")
    endWindow  =   endWindow2.strftime("%Y-%m-%d")
    window_len= (endWindow2-startWindow2).days
    print('Tamaño de la ventana a analizar paso a paso:  ', window_len, 'sesiones')
    


    dfe = pd.DataFrame({'A' : []})    
     
    for i in range(TOTAL_len):
        endWindow3   =endWindow2 + dt.timedelta(days=i) 
        endWindow    =endWindow3.strftime("%Y-%m-%d")
        print (endWindow)
        
        if(endWindow in dff.index):
            recogo = regreMedia.analisis_IN('MTS.MC', startWindow, endWindow, dfe) #Llamada a la clase estrategia. LA CLAVE DE TODO!!!
            print ('.............Analizando, muestra', i, 'fecha', endWindow)
            if(recogo['senal'] == 1 ):
                dff.loc[[endWindow],['Senal']]= 1
            elif(recogo['senal'] == 0 ):
                dff.loc[[endWindow],['Senal']]= 0
            elif(recogo['senal'] == -1 ):
                dff.loc[[endWindow],['Senal']]= -1            
            elif(recogo['senal'] == 503 ):
                #dff.loc[[endWindow],['Senal']]= 0          
                a=9
        else:
            print('..............Día sin sesión, next please')    
         
    
    ##############################  BACKTESTING

    """
    
    # Enter start and end date
    #start = '2020-1-20'
    #end = '2021-1-20'
    
    ##start =dt.datetime(2000,1,1)
    #            start =dt.datetime.today() - dt.timedelta(days=500)    #un año tiene 250 sesiones.
    ##end = dt.datetime(2021,9,22)
    #           end= dt.datetime.today()  - dt.timedelta(days=1)        #Quito hoy para no ver el valor al ejecutar antes del cierre
    #end = '2021-9-19'
    
    if(TELEGRAM__):
        telegram_send("2.- Estrategia Regresion a la media V0.1.\n ")
        

    # Create Regressionanalyis class
    #ra = Regressionanalysis('^NSEI', start, end, interval='60m')
    #ra.linear_regression(independent='Open', dependent='Close')
    # Me resulta complicado con esta libreria, no merece la pena ahora que estamos porbando, ya llegaran tiempos de afinar.
    
    tickers5 = ['AAPL', 'MSFT', '^GSPC', 'ELE.MC','SAN.MC', 'BBVA.MC']  #,'ANA.MC','MTS.MC','GRF.MC']  # apple,microsfoft,sp500, endesa
    tickers = ['MTS.MC'] 
    tickers_ = ['FER.MC','COL.MC','IBE.MC','NTGY.MC','SAB.MC','ACX.MC','PHM.MC','SAN.MC','MRL.MC','TEF.MC','AMS.MC','VIS.MC','MTS.MC','MAP.MC','CLNX.MC','BBVA.MC','CABK.MC','MEL.MC','AENA.MC','BKT.MC','REE.MC','FDR.MC','ACS.MC','ITX.MC','ENG.MC','ANA.MC','ELE.MC','GRF.MC','IAG.MC','SGRE.MC']
    tickersCurrencies =['EURUSD=X', 'EURGBP=X' ,'EURCHF=X', 'EURJPY=X', 'EURNZD=X', 'EURCAD=X', 'EURAUD=X','USDCHF=X', 
             'USDJPY=X','GBPCAD=X', 'GBPUSD=X', 'GBPJPY=X', 'GBPCHF=X', 'GBPNZD=X', 'GBPAUD=X',
             'NZDCAD=X', 'NZDUSD=X', 'NZDCHF=X', 'NZDJPY=X','JPY=X','EURSEK=X','USDCAD=X','AUDCAD=X',
             'KC=F','HG=F', 'CORN', 'CL=F', 'ZS=F','ZW=F','GC=F','X','ZW=F',
             'ETH-USD','PFE'
             ]
        
    #From Jupyter
    # Rango completo para backTesting
    start2 =dt.datetime(2005,1,2)
    end2   =dt.datetime(2021,11,23)
    start_G= start2.strftime("%Y-%m-%d")
    end_G  =   end2.strftime("%Y-%m-%d")
    TOTAL_len= (end2-start2).days
    print('Tamaño timeseries a analizar:  ', TOTAL_len, 'sesiones')
    
    #ventana de analisis 200 sesiones
    startWindow2 =dt.datetime(2010,1,5)
    endWindow2   =startWindow2 + dt.timedelta(days=1000) 
    startWindow= startWindow2.strftime("%Y-%m-%d")
    endWindow  =   endWindow2.strftime("%Y-%m-%d")
    window_len= (endWindow2-startWindow2).days
    print('Tamaño de la ventana a analizar paso a paso:  ', window_len, 'sesiones')
     
    instrumento ="AAPL"
    dff = yf.download(instrumento, start_G,end_G)
    
    regreMedia= StrategyClass()    #Creamos la clase
    
    dfe = pd.DataFrame({'A' : []})   #df empty
    
    #TOTAL_len =1000    
    for i in range(TOTAL_len):
        endWindow3   =endWindow2 + dt.timedelta(days=i) 
        endWindow    =endWindow3.strftime("%Y-%m-%d")
        print ('end date:', endWindow)
        
        if(endWindow in dff.index):
            df_aux= dff.loc[startWindow:endWindow]    #voy pasando los datos desplazando la ventana
            recogo = regreMedia.analisis(instrumento, startWindow, endWindow, df_aux) #Llamada a la clase estrategia. LA CLAVE DE TODO!!!
            print ('...................................................Analizando, muestra', i, 'fecha', endWindow)
            """
            if(recogo['senal'] == 1 ):
                dff.loc[[endWindow],['Senal']]= 1
            elif(recogo['senal'] == 0 ):
                dff.loc[[endWindow],['Senal']]= 0
            elif(recogo['senal'] == -1 ):
                dff.loc[[endWindow],['Senal']]= -1            
            elif(recogo['senal'] == 503 ):
                dff.loc[[endWindow],['Senal']]= 0          
            """    
        else:
            print('..............Día sin sesión, next please')    
        
        
    
    
        ## ECONOMICS
        
        
    
    data=StrategyClass.dfLog

    data['Dif_Close'] = data.Price.pct_change()

    data['Retornos'] = data.Dif_Close * data.Senal.shift(1)
    
    data['Capital'] = (data.Retornos + 1).cumprod() * 100
    
    StrategyClass.dfLog=data
    quant_j.salvarExcel(StrategyClass.dfLog, "log"+instrumento)
    
    data.to_pickle('almacen')    #df = pd.read_pickle(file_name)

    
    
    """
    ###################### Probando la CLASE estrategy
    
    dfe = pd.DataFrame({'A' : []})   #df empty

    regreMedia= StrategyClass()    #Creamos la clase
    
    #recogo = regreMedia.analisis_IN(tickers_[0], start, end, dfe)
    ######################## fin probando la Clase
    
    dfe = pd.DataFrame({'A' : []}) 
    regreMedia.analisis('IBE.MC', start, end, dfe)    
    
    #VALORES DEL IBEX 
    for i in range(len(tickers_)): 
        print(tickers_[i])
        regreMedia.analisis_IN(tickers_[i], start, end, dfe)
        
    
    
    """
    """
     
    for i in range(len(tickersCurrencies)): 
        print(tickersCurrencies[i])
        analisis_v2(tickersCurrencies[i], start, end,dfe)        
        
    
    #VALORES DEL SP50
    
    sp_url= 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    sp=pd.read_html(sp_url,header=0)[0]
    print (sp.info())
    
    for i in range(len(sp)):
         symbol=sp.iloc[i,0] 
         #df = yf.download(symbol, start, end)
         print(symbol)
         analisis_v2(symbol, start, end, dfe)
    
    
    """
    
    print ("******************************************************************************That´s all") 
    print ("****************************************************************************************")       
    
    
    
#/**********************************************************************main()    
 
MaquinaE = {'reposo':0, 'tendencia_UP':1, 'tendencia_DOWN':2, 'touchBollinger_botton':3}
estado = MaquinaE['reposo']

   
   
#/******************************** FUNCION PRINCIPAL *********/    
def analisis_JJ(instrumento, start, end):
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
    
    # 1.- MEDIA DE 200 SESIONES ACCENDENTE
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
        print('***************** Señal...')
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

# main()






