# -*- coding: utf-8 -*-
  

"""
******************************************************************************
ESTRATEGIA DE INVERSION BASADA EN 

v7.- hemos aprendido que el arbol de decision puede funcionar bien pero tenemos que trabajar un poco los datos,
por ejemplo, los datos son una 'foto' diaria, no guardan el historico. Tenemos que calcular indicadores que guarden informaicon 
del historico (pendiente). También es importante anlaizar el peso de las distintas variables valoradas por el forest.

Ejercio con kalman y teoria básica del cruce de medias.
 





******************************************************************************
******************************************************************************
Our rules are:


Started on 3/JAN/2021
Version_1: 

Objetivo: 



@author: J3Viton

"""

J3_DEBUG__ = False  #variable global (global J3_DEBUG__ )

TELEGRAM__ = False


################################ IMPORTAMOS MODULOS A UTILIZAR.
import pandas as pd
import numpy as np
import datetime as dt
import yfinance as yf
import time
from datetime import datetime

import statsmodels.api as sm

"""
import matplotlib.pyplot as plt
plt.rcParams['figure.figsize'] = 18, 8
plt.style.use("bmh") 
"""

"""
import tkinter
import matplotlib
matplotlib.use('TkAgg')  WXAgg
"""


import tkinter
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('TkAgg')
#plt.style.use("ggplot")



import quant_j3_lib as quant_j
from telegram_bot import *


### Decision Tree

import matplotlib.pyplot as plt
#from matplotlib.ticker import FuncFormatter
#from matplotlib import cm
#import seaborn as sns

from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor, export_graphviz, _tree
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.model_selection import train_test_split, GridSearchCV, learning_curve
from sklearn.metrics import roc_auc_score, roc_curve, mean_squared_error, make_scorer
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, GradientBoostingClassifier
from sklearn.ensemble import RandomForestRegressor
#import graphviz



#df_sg = pd.DataFrame(columns=('estrategia','instrumento', 'fecha', 'aux1', 'aux2'))

#/***************************Funciones con tareas parciales */

df_metrica=pd.DataFrame(columns=['METRICA','PESO','Importancia'])  



#################################################### Clase Estrategia 

class StrategyClass:

    """CLASE ESTRATEGIA

       
    """  
    
    dfLog = pd.DataFrame(columns=('Date','Senal', 'Price','Objetivo','ExitReason'))
    dfCartera = pd.DataFrame(columns=['instrumento','long_short_out', 'date','precio','beneficio','stoploss'])
    #dfCartera.set_index('instrumento',inplace=True)
    
    
    #Variable
    backtesting = False  #variable de la clase, se accede con el nombre

    
    def __init__(self, instrumento= 'IBE.MC', backTest=False, para2=1):
        StrategyClass.backtesting = backTest
        self.para_02 = para2   #variable de la isntancia
        self.__privado = "atributoPrivado"
        self.dfLog = pd.DataFrame(columns=('Date','Senal', 'Price'))
             
        self.instrumento =1
        self.startDate=1
        self.endDate =1
        
        global TELEGRAM__
        if(StrategyClass.backtesting == True):
            TELEGRAM__ = False
        else:
            TELEGRAM__ = True
        
        try:
            StrategyClass.dfCartera= quant_j.leerExcel('carteraRegre')
            dfx2=StrategyClass.dfCartera
        except:
            print (' fichero carteraXX no existe...')
            return
        
    def analisis(self, instrumento, startDate, endDate, DF):
        """Funcion de entrada al analisis. Primero buscamos en el excel 'Cartera' si estamos invertidos en el instrumento, long_short_out. 
        Si no está el insturmento creamos la entrada en cartera. 
        Si tenemos el instrumento y estamos dentro analizamos si salimos (self.analisis_OUT), viceversa (self.analisis_OUT). 
        Returns:nada

        """

        """ Variables de la clase, no las locales   
        self.instrumento=instrumento 
        self.startDate=startDate
        self.endDate = endDate
        """     
        StrategyClass.dflog= quant_j.leerExcel('log'+instrumento)
        StrategyClass.dfCartera= quant_j.leerExcel('carteraRegre')
        
        dfx=StrategyClass.dfLog
        dfx2=StrategyClass.dfCartera
        
        #Si no esta el instrumento en la cartera, paso a analizarlo
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
                
        resultado= analisisENTRADA(instrumento, startDate, endDate, DF)    #jj
        
        if StrategyClass.backtesting :
            quant_j.salvarExcel(StrategyClass.dfLog, "log"+instrumento)
        quant_j.salvarExcel(StrategyClass.dfCartera, "carteraRegre")

        dfx=StrategyClass.dfLog
        dfx2=StrategyClass.dfCartera
        print (dfx2)

        return resultado  # SELL_ HOLD_
    
    def analisis_OUT(self, instrumento, startDate, endDate, DF):
        
        print('aqui estoy en out')
        estrategiaSALIDA(instrumento, startDate, endDate, DF)
        
        #Actualizamos el Log y la Cartera
        if StrategyClass.backtesting :
            quant_j.salvarExcel(StrategyClass.dfLog, "log"+instrumento)
        quant_j.salvarExcel(StrategyClass.dfCartera, "carteraRegre")
        
        dfx=StrategyClass.dfLog
        dfx2=StrategyClass.dfCartera
        
        return
    @classmethod 
    def analisis_P_L(self, ddf, beneficio, instrumento):
        """
        Descripcion: this method evaluates the convenience of the inversion measuring Profit and loss
        Currrent method asumes profit line three times bigger than stopLoss line
        
        Parameters
        ----------
        ddf : TYPE
            DESCRIPTION.
        beneficio : TYPE
            DESCRIPTION.

        Returns
        -------
        TYPE
            DESCRIPTION.

        """
        # Caluclo el ATR de la serie de precios
        df=quant_j.ATR(ddf,n=20)
        #last ATR 
        a=df[-1]
        b=ddf['Close'][-1]
        c=beneficio[0]
        #Estrategia hacia nuestro mejor interés.
        if ( 2*a > (c)): # 2*ATR > beneficio  -> noGo!!!
            print('Operacion poco eficiente')
            return False

        return True
    
    @classmethod 
    def analisisEconomics(self, instrumento):
        """
        Descripcion: this method evaluates the convenience of the inversion measuring Profit and loss
        Currrent method asumes profit line three times bigger than stopLoss line
        

        """
    ########################################
    ## ECONOMICS
    
        data=StrategyClass.dfLog
    
        data['Dif_Close'] = data.Price.pct_change()
    
        data['Retornos'] = data.Dif_Close * data.Senal.shift(1)
        
        data['Capital'] = (data.Retornos + 1).cumprod() * 100
        
        StrategyClass.dfLog=data

        if StrategyClass.backtesting :
            quant_j.salvarExcel(StrategyClass.dfLog, "log"+instrumento)
           
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

    Funcion que gestiona la estrategia de salida. Analiza dos casos, salida por StopLoss o por TakeProfit. (por ahora no hacemos trailing stopLoss)
        
    ToDo:
        Trailing Stoploss
        Costes de transaccion
        Money management
        Mejorar teoria del stoploss y takeProfit.

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
    
    col_ =          StrategyClass.dfCartera.instrumento.isin([instrumento]) 
    linea_2 = col_[col_==True]
    linea_3=linea_2.index
    linea_=linea_3[0]    
    l_s_o =         StrategyClass.dfCartera.columns.get_loc("long_short_out")
    comprado_=      StrategyClass.dfCartera.iloc[linea_ , l_s_o]      
    precio_ =       StrategyClass.dfCartera.columns.get_loc("precio")
    precioCompra_=  StrategyClass.dfCartera.iloc[linea_ , precio_]   
    beneficio_ =    StrategyClass.dfCartera.columns.get_loc("beneficio")
    beneficioEsperado_=  StrategyClass.dfCartera.iloc[linea_ , beneficio_]  
    stoplossLOC_ =    StrategyClass.dfCartera.columns.get_loc("stoploss")
    stoploss_=  StrategyClass.dfCartera.iloc[linea_ , stoplossLOC_]   
    
    #Condicion de salida " precio baja un 10% el precio de entrada
    
    price_ =      df.columns.get_loc("Close")   
    try:
        #indiceHoy_ = np.where(df.index == endd)[0][0]
        indiceHoy_ = (len(df)-1)  
    except:
        return
    PrecioHoy =   df.iloc[indiceHoy_,price_]
    
    """
    if (endd== '2013-03-21'):   #BreakPoint under demant :-)  j3viton
        parada=9
        print('precio hoy', PrecioHoy)
        print('precio compra', precioCompra_[linea_])
    """

    ##################################################################
    ##  STOP_LOSS

    StrategyClass.dfLog.loc[endd,'Date'] = endd
    StrategyClass.dfLog.loc[endd,'Price']= df.iloc[indiceHoy_,price_]    
    StrategyClass.dfLog.loc[endd,'Senal']= 1       

   
    
    if( PrecioHoy < (precioCompra_ - (beneficioEsperado_/3)) ):      #Un poco de money management  Otra: (PrecioEntrada-2*ATR)
        señal =  0   # salta el stoploss y me salgo ?????
        StrategyClass.dfCartera.iloc[linea_ , l_s_o]  = 0   #OUT         
        #StrategyClass.dfCartera.iloc[linea_ , precio_]  = PrecioHoy
        
        #StrategyClass.dfLog.loc[endd,'Date'] = endd
        StrategyClass.dfLog.loc[endd,'Senal']= 0
        #StrategyClass.dfLog.loc[endd,'Price']= df.iloc[indiceHoy_,price_]           
        #if( PrecioHoy < (precioCompra_) ):
        StrategyClass.dfLog.loc[endd,'ExitReason'] = -1    # Marca la razon de la salida -1 salgo por stopLoss, 1 takeProfit

        
        dfx=StrategyClass.dfLog
        dfx2=StrategyClass.dfCartera
    

    ####################################################################
    ## TAKE_PROFIT
    
    
    elif (PrecioHoy > ((precioCompra_)+beneficioEsperado_)) :
          
        señal =  0
        StrategyClass.dfCartera.iloc[linea_ , l_s_o]  = 0      #OUT      
        #StrategyClass.dfCartera.iloc[linea_ , precio_]  = PrecioHoy  
          
        #StrategyClass.dfLog.loc[endd,'Date'] = endd
        StrategyClass.dfLog.loc[endd,'Senal']= 0
        #StrategyClass.dfLog.loc[endd,'Price']= df.iloc[indiceHoy_,price_]  
        StrategyClass.dfLog.loc[endd,'ExitReason'] = +1    # Marca la razon de la salida -1 salgo por stopLoss, 1 takeProfit

        
        dfx=StrategyClass.dfLog
        dfx2=StrategyClass.dfCartera 
        
    #StrategyClass.dfCartera.iloc[linea_ , precio_]  = PrecioHoy  
        
    return






def analisisENTRADA(instrumento, startt, endd, df):    #analisis_v2
    """Estrategia usando MACHINE LEARNING. 
    Si no recibe el DF en la llamada coge los datos de yahoofinances

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
            print ('descargo datos en Spyder')
            #yf.download("AMZN AAPL GOOG", start="2017-01-01", end="2017-04-30")
            #df =web.DataReader(instrumento, 'yahoo', start, end)    DA ERROR DE YAHOO FINANCES
        else:
            print (' Datos desde archivo')
    except:
        resultados['senal']   =  503     #Service Unavaliable
        return resultados
 

    if df.empty:
        print('DataFrame is empty!J')
        resultados['senal']   =  503     #Service Unavaliable
        return resultados

    #Test
    # df=quant_j.PGO(df)    
 

    #######################################################################
    ######################################################  ESTRATEGIA
    
    """
    EMA25>50
    EMA 50>100
    MACD golden cross histograma >0 macd>señal
    rsi>50
    TP 1,0% ePrice
    SL 0,5% ePrice
    """

    # 0.- Creamos una columna con secuencial (variable independiente)
    df['x']=np.arange(1, len(df)+1)

    # 1.- Feature engineering. Creamos más datos
    
    df= quant_j.kalmanIndicator(df,instrumento="_")

    # 1.1 Data engineering
    
    # concepto cruce de medias con kalman.
    df_aux30 =df.loc[:,['Close','Volume']]   # Copiamos una parte del dataframe

    #df_aux30.rename(columns={'Kalman':'Close'}, inplace=True)  #Cambio el nombre de la columna para poder llamara las funicones que usan la columna Close
    
    df_aux30=quant_j.ExponentialMovingAverage(df_aux30,long_=100,short_=50)
    df_aux30.rename(columns={'EMA_100':'EMAK_100','EMA_50':'EMAK_50' }, inplace=True)     

    df_aux30=quant_j.ExponentialMovingAverage(df_aux30,long_=49,short_=25)
    df_aux30.rename(columns={'EMA_49':'EMAK_49','EMA_25':'EMAK_25' }, inplace=True)     
    
    df_aux30= quant_j.MACD(df_aux30,a=12,b=26,c=9)
    
    df_aux30= quant_j.RSI(df_aux30, n=14)
    
    #vuelo el valor de close por kalman
    df_aux30.rename(columns={'Close':'Kalman'}, inplace=True)     
    df_aux30['Close'] = df['Close']
    
    #Calcualmos predictores con los indicadores
    df_aux30['ClgtEMA10'] = np.where(df_aux30['Close'] > df_aux30['EMAK_50'], 1, -1)
    df_aux30['EMA10gtEMA30'] = np.where(df_aux30['EMAK_50'] > df_aux30['EMAK_100'], 1, -1)
    df_aux30['MACDSIGgtMACD'] = np.where(df_aux30['Signal'] > df_aux30['MACD'], 1, -1)
    
    
    df_aux30['25mayor50'] = np.where(df_aux30['EMAK_25'] > df_aux30['EMAK_50'], 1, -1)
    df_aux30['50mayor100'] = np.where(df_aux30['EMAK_49'] > df_aux30['EMAK_100'], 1, -1)
    df_aux30['macdHistMayor0'] = np.where(df_aux30['Histo'] > 0, 1, -1)
    df_aux30['RSImayor50'] = np.where(df_aux30['RSI'] > 50, 1, -1)
    
    
    
    
    
    ############################################################################################### ETIQUETA
    lag_=1
    df_aux30['y']= df_aux30.Close.shift((-1)*lag_)          # ponemos la condicon del valor de la accion en 10 dias (ejemplo para empezar)
    
    df_aux30['Return'] = df_aux30['Close'].pct_change(1).shift(-1)
    df_aux30['target_cls'] = np.where(df_aux30.Return > 0.1, 1, 0)
    df_aux30['target_rgs'] = df_aux30['Return']

    
    """
    df['Return'] = df['Settle'].pct_change(1).shift(-1)
    df['target_cls'] = np.where(df.Return > 0, 1, 0)
    df['target_rgs'] = df['Return']
    df.tail()
    """

    df_aux30.dropna(inplace=True)                     # limpio columnas sin datos
    
                    
    #############  DECISION TREE
    #Tengo en DF datos de entrada y etiqueta
    
    #seleciono datos relevantes
    df_aux40 =df_aux30.loc[:,['25mayor50','50mayor100','macdHistMayor0','RSImayor50']]   # Copiamos una parte del dataframe
    
        
    y2 = df_aux30.target_cls
    X2 = df_aux40
    #X2.drop('y', axis=1, inplace=True)
        
    #Partimos el dataser en dos de manera random
    #☺X_train, X_test, y_train, y_test = train_test_split(X2, y2, test_size=0.2, random_state=42)
    
    # Hacemos un split separando los ultimos datos de la serie en lugar de ramdon.
    
    X_train= X2.iloc[:-24]
    X_test=  X2.iloc[-24:]
    y_train= y2.iloc[:-24]
    y_test=  y2.iloc[-24:]
    
    
           
    start_time = time.time()
   
    #########################################
    # RandomForest
    #########################################
    #rf_clf = RandomForestRegressor(random_state=1)
    rf_clf = RandomForestClassifier(random_state=0)
    rf_clf.fit(X=X_train, y=y_train)
    
    y_pred = rf_clf.predict(X_test)
        
    print("score",rf_clf.score(X_test, y_test))
    
 
    #########################################
    # Analisis del randomForest
    #########################################
    
    # Get numerical feature importances
    importances = list(rf_clf.feature_importances_)
    #importances.sort()
    # List of features for later use
    feature_list = list(X2.columns)

    df_metrica['METRICA']=feature_list[0:(len(feature_list) )]   
    df_metrica['PESO']=importances  
    df_metrica.sort_values('PESO',ascending=False, inplace=True)
    df_metrica.reset_index(inplace = True, drop = True)
    df_metrica.fillna(0, inplace=True)
    

    """    
    for ii in range(len(feature_list)):
        for jj in feature_list:
            if (df_metrica.loc[ii,'METRICA']==jj):
                df_metrica.loc[ii,'Importancia']=df_metrica.loc[ii,'Importancia']+ii   #0.'METRICA'
    """

        
    print(instrumento)
    print(df_metrica)
    #print("¿Siguiente? ", end="")
    #nombre = input()

    
    # Concpeto regresion lineal con kalman
    

    
    ###########  Ploteamos
    
    
    colors=['lightgreen', 'green']

    dfAux = pd.DataFrame(y_pred, columns=['y_pred'])  #array to dataframe
    
    df2 = pd.DataFrame(data=y_test.values, columns=['y_test'])   #serie a colummna. Ojo quitamos index 
    
    dfx = pd.merge(df2, dfAux,left_index=True, right_index=True)

    dfx.plot(title='Random Forest  Ticker-> ' +instrumento,color=colors)
    
    plt.show()
    
    stop_time = time.time()
    print("example run in %.2fs" % (stop_time - start_time))
    
    print(dfx)
    #no=input()
    
    """
    x = np.linspace(0, 2 * np.pi, 200)
    y = np.sin(x)
    
    fig, ax = plt.subplots()
    ax.plot(x, y)
    plt.show()
    """
    
    return True
    
    
    """
    # 2.- Ambas pendientes//tendencias son ascendentes (ma220 y linearRegresion)
     
    try:
        #indiceHoy_ = np.where(df.index == endd)[0][0]
        indiceHoy_ = (len(df)-1)  

    except:
        print('bye')
        return
    
    price_ = df.columns.get_loc("Close")        
    
    if (coef_linear>0  and  coef_ema200_>0):
        bb_up_ = df.columns.get_loc("BB_up")
        bb_dn_ = df.columns.get_loc("BB_dn")
        price_ = df.columns.get_loc("Close")   
        #indiceHoy_ = len(df)-1
        
        a=df.iloc[indiceHoy_,price_] 
        b=1* df.iloc[indiceHoy_,bb_dn_]
        
        
        if( (df.iloc[indiceHoy_,price_] < ( 1* df.iloc[indiceHoy_,bb_dn_])) and (df.iloc[indiceHoy_,price_] > ( 1* df.iloc[indiceHoy_,ema200_]) )):   #Precio por debajo de la banda de Bollinger, dentro de tendencia ascendente
            señal =True
        else:
            señal = False
        
        
        beneficio = ((200*coef_linear + intercept_linear)-( df.iloc[indiceHoy_,price_] ))    # (punto de corte de la recta regresion MENOS precio de hoy)
        if (beneficio[0]<0):   #caso estraño pero subidad rapidad dejan la regresion lineal por abajo
            señal = False           
    """
    ######################################################  ESTRATEGIA
    #######################################################################    
 
    
    ####################
    ## SEÑAL DE COMPRA
    
    ### Analizamos el P&L de la operacion
    if(señal == True):
        goNogo= StrategyClass.analisis_P_L(df, beneficio, instrumento)
        señal = goNogo
        print('***************** NoGo')  
    
    
    if (señal == True):
        print('***************** Señal...')        
        parada=8
 
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
        StrategyClass.dfLog.loc[endd,'Beneficio']= beneficio[0] 
        
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
        beneficio__ = StrategyClass.dfCartera.columns.get_loc("beneficio")
        stoploss__ = StrategyClass.dfCartera.columns.get_loc("stoploss")
        
        
        linea_ = StrategyClass.dfCartera.instrumento.isin([instrumento])
        
        StrategyClass.dfCartera.iloc[linea_ , l_s_o]        = 1
        StrategyClass.dfCartera.iloc[linea_ , date__]       = endd        
        StrategyClass.dfCartera.iloc[linea_, precio__]      = df.iloc[indiceHoy_,price_]
        StrategyClass.dfCartera.iloc[linea_, beneficio__]   = beneficio[0] 
        
        
        #stoploss en 2x ATR
        dff=quant_j.ATR(df,n=20)
        #last ATR 
        a=dff[-1]
        StrategyClass.dfCartera.iloc[linea_, stoploss__]    = 2*a
        
        
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
    
    else:  #señal==False
        ########## Tenemos Señal, devolvemos la informacion       
        #resultados = dict();    # Creamos un diccionario para devolver los datos
        
        
        ################### Almaceno información en un dataframe log
        StrategyClass.dfLog.loc[endd,'Date'] =endd
        StrategyClass.dfLog.loc[endd,'Senal']=0
        StrategyClass.dfLog.loc[endd,'Price']=df.iloc[indiceHoy_,price_]   
        
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

#################################################################### CLASE ANALISIS REGRESION LINEAL
####################################################################################################



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
    
    decisionTree1= StrategyClass(backTest=True)    #Creamos la clase
    
    if(TELEGRAM__):
        telegram_send("4 DecisionTree1 V0\n ")
    dfe = pd.DataFrame({'A' : []})   #df empty
    
    #### FECHAS
    #start =dt.datetime(2000,1,1)
    start =dt.datetime.today() - dt.timedelta(days=600)    #un año tiene 250 sesiones.
    #end = dt.datetime(2019,10,1)
    end= dt.datetime.today()  - dt.timedelta(days=1)        #Quito hoy para no ver el valor al ejecutar antes del cierre
    #end = '2021-9-19'
    
    #TICKERS
    tickers__ = [ 'EURUSD=X','EURGBP=X','EURJPY=X','USDCAD=X','GBPUSD=X','USDJPY=X','GBPJPY=X','BTC-USD', '^DJI', '^GDAXI', '^GSPC', 'SI=F', 'GC=F','NQ=F','AAPL', 'MSFT', '^GSPC', 'ELE.MC','SAN.MC', 'BBVA.MC',
               'ETH-USD', 'LTC-USD', 'NEO-USD', 'XMR-USD', 'ZEC-USD' ]  #,'ANA.MC','MTS.MC','GRF.MC']  # apple,microsfoft,sp500, endesa
    tickers = ['NQ=F','SAB.MC','ACX.MC','PHM.MC','SAN.MC','MRL.MC','TEF.MC','AMS.MC','VIS.MC','MTS.MC'] 
    tickers_ = ['COL.MC','IBE.MC','NTGY.MC','SAB.MC','ACX.MC','PHM.MC','SAN.MC','MRL.MC','TEF.MC','AMS.MC','VIS.MC','MTS.MC','MAP.MC','CLNX.MC','BBVA.MC','CABK.MC','MEL.MC','AENA.MC','BKT.MC','REE.MC','FDR.MC','ACS.MC','ITX.MC','ENG.MC','ANA.MC','ELE.MC','GRF.MC','IAG.MC','SGRE.MC']
    tickersCurrencies =['EURUSD=X', 'EURGBP=X' ,'EURCHF=X', 'EURJPY=X', 'EURNZD=X', 'EURCAD=X', 'EURAUD=X','USDCHF=X', 
             'USDJPY=X','GBPCAD=X', 'GBPUSD=X', 'GBPJPY=X', 'GBPCHF=X', 'GBPNZD=X', 'GBPAUD=X',
             'NZDCAD=X', 'NZDUSD=X', 'NZDCHF=X', 'NZDJPY=X','JPY=X','EURSEK=X','USDCAD=X','AUDCAD=X',
             'KC=F','HG=F', 'CORN', 'CL=F', 'ZS=F','ZW=F','GC=F','X','ZW=F','NQ=F',
             'ETH-USD','PFE'
             ]
    

    #VALORES DEL IBEX 
    
    for i in range(len(tickers)): 
        print(tickers[i])
        decisionTree1.analisis(tickers[i], start, end, dfe)
        #time.sleep (1)
        
    #CURRENCIES
    
    for i in range(len(tickersCurrencies)): 
        print(tickersCurrencies[i])
        decisionTree1.analisis(tickersCurrencies[i], start, end, dfe)        
        #time.sleep (1)
    """    
    
    #VALORES DEL SP50
    sp_url= 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    sp=pd.read_html(sp_url,header=0)[0]
    print (sp.info())
    
    for i in range(len(sp)):
         symbol=sp.iloc[i,0] 
         #df = yf.download(symbol, start, end)
         print(symbol)
         decisionTree1.analisis(symbol, start, end, dfe )
         #time.sleep (1)
    
    
    """
    
    #################################################################        
    ######################################################BACKTESTING
    if (False):  #backtesting
        # Rango completo para backTesting
        start2 =dt.datetime(2010,1,6)
        #start2 =dt.datetime.today()-dt.timedelta(days=1)
        #end2 =dt.datetime(2021,12,18)
        end2 =dt.datetime.today()  #-dt.timedelta(days=1)
        start_G= start2.strftime("%Y-%m-%d")
        end_G  =   end2.strftime("%Y-%m-%d")
        TOTAL_len= (end2-start2).days
        print('Tamaño timeseries a analizar:  ', TOTAL_len, 'sesiones')
        
        #ventana de analisis 200 sesiones
        #startWindow2 =dt.datetime(2012,1,5)
        startWindow2 = start2
        endWindow2   =startWindow2 + dt.timedelta(days=500) 
        startWindow= startWindow2.strftime("%Y-%m-%d")
        endWindow  =   endWindow2.strftime("%Y-%m-%d")
        window_len= (endWindow2-startWindow2).days
        print('Tamaño de la ventana a analizar paso a paso:  ', window_len, 'sesiones')
         
        instrumento ='MSFT' #'ACX.MC'
        dff = yf.download(instrumento, start_G,end_G)
        
        #decisionTree1= StrategyClass()    #Creamos la clase
        
        #decisionTree1.analisis_P_L(dff, 4)  #Solo para probar el ATR
        
        
        
        #TOTAL_len =1000   
        for i in range(TOTAL_len):
            endWindow3   =endWindow2 + dt.timedelta(days=i) 
            endWindow    =endWindow3.strftime("%Y-%m-%d")
            print ('end date:', endWindow)
            
            if(endWindow in dff.index):
                df_aux= dff.loc[startWindow:endWindow]    #voy pasando los datos desplazando la ventana
                
                recogo = decisionTree1.analisis(instrumento, startWindow, endWindow, df_aux) #Llamada a la clase estrategia. LA CLAVE DE TODO!!!
                
                
                print ('...................................................Analizando, muestra', i, 'de', TOTAL_len, 'fecha', endWindow)
                print ('......................................................................_______________.................')
                #print(colored('Hello, World!', 'green', 'on_red'))
     
            else:
                print('..............Día sin sesión, next please')    
            
            
        
        ########################################
        ## ECONOMICS
        StrategyClass.analisisEconomics(instrumento)
        
    ########################################################### backtestingFIN    
    ##########################################################################
    
    print ("******************************************************************************That´s all") 
    print ("****************************************************************************************")       
    
    
    
#/**********************************************************************main()    
 








