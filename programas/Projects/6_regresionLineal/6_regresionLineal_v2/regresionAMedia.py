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

En el ficchero regreMedia almaceno todas las señañes de entrada y su pendiente
En el fichro CarteraRegre almaceno la popsicion de mercado (tendria que mejorarlo para hacer un log real)
Proceso:    la ejecucion automatica me deja señales en el Telegram, luego hago un backtesting con el Notebook, para comprobar la Esperanza matematica y decidir
            Beneficio al corte de la linea de regresion lineal TP
            StopLoss 2*ATR en la entrada (mejorable)

Empiezo pruebas tímidas en real Mayo-2022

Mejoras:    Evaluar la pendiente, pero deberia normalizar el valor primero para comparar bien la calidad de la pendiente.
            Por qué no en largos????



Started on 24/NOV/2021
Version_1: 

Objetivo: 

    
BACKTEST:
    http://localhost:8888/notebooks/Documents/J3/100.-%20cursos/Quant_udemy/programas/Projects/6_regresionLineal/backTestREGRESIONLINEAL.ipynb


@author: J3Viton

"""

# J3_DEBUG__ = False  #variable global (global J3_DEBUG__ )

TELEGRAM__ = True



################################ IMPORTAMOS MODULOS A UTILIZAR.
import pandas as pd
import numpy as np
import datetime as dt
#import pandas_datareader as web
import yfinance as yf

import statsmodels.api as sm

"""
import matplotlib.pyplot as plt
plt.rcParams['figure.figsize'] = 18, 8
plt.style.use("bmh")   
"""
import sys
import os
sys.path.insert(0,"C:\\Users\\INNOVACION\\Documents\\J3\\100.- cursos\\Quant_udemy\\programas\\Projects\\libreria")
import quant_j3_lib as quant_j
from telegram_bot import *
from sp500 import tickers_sp500



df_sg = pd.DataFrame(columns=('estrategia','Instrumento', 'fecha', 'aux1', 'aux2'))

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
    
    dfLog = pd.DataFrame(columns=('Date','Senal', 'Price','Objetivo','ExitReason','Beneficio','Dif_Close','Retornos','Capital'))
    dfCartera = pd.DataFrame(columns=['Instrumento','long_short_out', 'date','precio','beneficio','stoploss'])
    #dfCartera.set_index('instrumento',inplace=True)
    
    #Variable
    backtesting = False  #variable de la clase, se accede con el nombre

    
    def __init__(self, instrumento= 'IBE.MC', back=False, para2=1):
        StrategyClass.backtesting = back
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
        
        #var=dfx2[instrumento]
        
        
        #Si no esta el instrumento en la cartera, paso a analizarlo
        if not (instrumento in StrategyClass.dfCartera.values)  :   
               #StrategyClass.dfCartera=StrategyClass.dfCartera.append({'instrumento': instrumento, 'precio': 1}, ignore_index=True) 
            self.analisis_IN(instrumento, startDate, endDate, DF)
        #Si está el isnturmetno en la cartera, miro si eestoy largo o corto o fuera
        else:
            col_ =  StrategyClass.dfCartera.Instrumento.isin([instrumento])   # devuelve una serie con true/false donde esta el obejto buscado
            col_2 = col_[col_==True]   # hago una serie con los true, normalmente un solo elemento
            linea_2 = col_2.loc[col_2==True]
            
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
        ##print (dfx2)

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
        if ( 2*a > (c)):                            # 2*ATR > beneficio  -> noGo!!!
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
    
    col_ =          StrategyClass.dfCartera.Instrumento.isin([instrumento]) 
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

   
    
    #if( PrecioHoy < (precioCompra_ - (beneficioEsperado_/3)) ):      #Un poco de money management  Otra: (PrecioEntrada-2*ATR)
    if( PrecioHoy < (precioCompra_ - (stoploss_)) ):
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
        if(TELEGRAM__):
            telegram_send("!! SL en la estrategia Regresión lineal v7\nStopLoss " +instrumento)
             

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
        if(TELEGRAM__):
            telegram_send("!! TP en la estrategia Regresión lineal v7\nTakeProfit " +instrumento)
         
        
    return



def analisisENTRADA(instrumento, startt, endd, df):    #analisis_v2
    """Estrategia linear regresion. Pendiente de la regresion linear de cierre y pendiente de EMA200 positiva. Cuando el precio
    en la banda de boulinger inferior entrar.
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
    
    # 0.- Leemos los datos    
    try:
        if df.empty:
            df = yf.download(instrumento, startt, endd)
            df.dropna(inplace=True)  
            print ('descargo datos desde Spyder')
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


    parada =9 
    
    # 1.- MEDIA DE 200 SESIONES ACCENDENTE
    #   Calculamos de la media aritmetica la regresion lineal para ver la esencia
    ema200_=df.columns.get_loc("EMA_200")
    df_aux2= df.iloc[-200:, ema200_]
    df_aux2.dropna(inplace=True)  
    if df_aux2.empty:
        print('dataframe vacio en 455')
        return 

    # 3.1.- Calculamos media de las ultimas 'n' sesiones y la regresion lineal
    coef_ema200_, intercept_ema200_ =quant_j.linearRegresion_J3(df_aux2,instrumento=instrumento) #+'  de ema200')  
    
    
    # 4.- Bollinger 
    df= quant_j.BollBnd(df,n=20)
    
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
        
        a=   df.iloc[indiceHoy_,price_] 
        b=1* df.iloc[indiceHoy_,bb_dn_]
        
        
        if( (df.iloc[indiceHoy_,price_] < ( 1* df.iloc[indiceHoy_,bb_dn_])) and (df.iloc[indiceHoy_,price_] > ( 1* df.iloc[indiceHoy_,ema200_]) )):   #Precio por debajo de la banda de Bollinger, dentro de tendencia ascendente
            señal =True
        else:
            señal = False
        
        ############
        # BENEFICIO
        ############
        beneficio = ((200*coef_linear + intercept_linear)-( df.iloc[indiceHoy_,price_] ))    # (punto de corte de la recta regresion MENOS precio de hoy)
        if (beneficio[0]<0):   #caso estraño pero subidad rapidad dejan la regresion lineal por abajo
            señal = False           
    
    ######################################################  ESTRATEGIA
    #######################################################################    
 
    
    ####################
    ## SEÑAL DE COMPRA
    
    ### Analizamos el P&L de la operacion
    if(señal == True):
        goNogo= StrategyClass.analisis_P_L(df, beneficio, instrumento)
        señal = goNogo
        print('***************** NoGo')  
        if (not señal):
            StrategyClass.dfLog.loc[endd,'ExitReason'] = -99    # Marca la razon de la salida -1 salgo por stopLoss, 1 takeProfit,99 podo rentable para entrar
    
    
    
    if (señal == True):
        print('***************** Señal...')        
        parada=8
 
        #Guardo en EXCEL file
        quant_j.saveSignal('RegresMedia_', 'RegresionMedia b0 (IN)', instrumento,endd, coef_linear[0], coef_ema200_[0], df.iloc[indiceHoy_,price_] , beneficio[0])
        
        #Mando señal al bot telegram
        if(TELEGRAM__):
            telegram_send("Señal Estrategia 6 Regresión lineal v7\nMira (IN) " +instrumento)
            telegram_send("TP--> +(precioCompra_+beneficioEsperado_) +  SL--> +(precioCompra_ - (stoploss_))")
        
            
        #Llamo a calcular la esperaza matematica
        ##os.system("python backTestRL_EsperanzaMat.py "+instrumento +" >signalFile"+instrumento+".txt")
        
        ##telegram_send_document("signalFile"+instrumento+".txt")
         
            
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
               StrategyClass.dfCartera=StrategyClass.dfCartera.append({'Instrumento': instrumento, 'precio': 1}, ignore_index=True)

        df1=StrategyClass.dfLog
        df2=StrategyClass.dfCartera
        
        #StrategyClass.dfCartera.set_index('instrumento',inplace=True)
        l_s_o =  StrategyClass.dfCartera.columns.get_loc("long_short_out")
        date__ = StrategyClass.dfCartera.columns.get_loc("date")
        precio__ = StrategyClass.dfCartera.columns.get_loc("precio")
        beneficio__ = StrategyClass.dfCartera.columns.get_loc("beneficio")
        stoploss__ = StrategyClass.dfCartera.columns.get_loc("stoploss")
        
        
        linea_ = StrategyClass.dfCartera.Instrumento.isin([instrumento])
        
        StrategyClass.dfCartera.iloc[linea_ , l_s_o]        = 1
        StrategyClass.dfCartera.iloc[linea_ , date__]       = endd        
        StrategyClass.dfCartera.iloc[linea_, precio__]      = df.iloc[indiceHoy_,price_]
        StrategyClass.dfCartera.iloc[linea_, beneficio__]   = beneficio[0] 
        
        ######################
        # STOPLOSS en 2x ATR
        ######################
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
    
    """
    # pruebas excel
    dfC= quant_j.leerExcel('carteraRegre')

    dfC.loc[0,'precio'] = 123
    quant_j.salvarExcel(dfC, "carteraRegre")
    
    #pruebas excel
    """
    
    regreMedia= StrategyClass(back=False)    #Creamos la clase
    
    if(TELEGRAM__):
        telegram_send("3.- Estrategia_6 Regresion lineal v7\n ")
    dfe = pd.DataFrame({'A' : []})   #df empty
    
    #### FECHAS
    #start =dt.datetime(2000,1,1)
    start =dt.datetime.today() - dt.timedelta(days=500)    #un año tiene 250 sesiones.
    #end = dt.datetime(2019,10,1)
    end= dt.datetime.today()  - dt.timedelta(days=1)        #Quito hoy para no ver el valor al ejecutar antes del cierre
    #end = '2022-9-15'  ##solo para pruebas ESte dia tengo varias señales
    
    #TICKERS
    
    #traerlos vaores de aqui C:\Users\INNOVACION\Documents\J3\100.- cursos\Quant_udemy\programas\Projects\regresionLineal_MediaMovil
    
    tickers5 = ['AAPL', 'MSFT', '^GSPC', 'ELE.MC','SAN.MC', 'BBVA.MC']  #,'ANA.MC','MTS.MC','GRF.MC']  # apple,microsfoft,sp500, endesa
    tickers2 = ['cnc'] 
    tickers = ['FER.MC','COL.MC','IBE.MC','NTGY.MC','SAB.MC','ACX.MC','PHM.MC','SAN.MC','MRL.MC','TEF.MC','AMS.MC','VIS.MC','MTS.MC','MAP.MC','CLNX.MC','BBVA.MC','CABK.MC','LOG.MC','MEL.MC','AENA.MC','BKT.MC','REE.MC','FDR.MC','ACS.MC','ITX.MC','ENG.MC','ANA.MC','ELE.MC','GRF.MC','IAG.MC','ROVI.MC','SGRE.MC']
    tickersCurrencies =['EURUSD=X', 'EURGBP=X' ,'EURCHF=X', 'EURJPY=X', 'EURNZD=X', 'EURCAD=X', 'EURAUD=X','USDCHF=X', 
             'USDJPY=X','GBPCAD=X', 'GBPUSD=X', 'GBPJPY=X', 'GBPCHF=X', 'GBPNZD=X', 'GBPAUD=X',
             'NZDCAD=X', 'NZDUSD=X', 'NZDCHF=X', 'NZDJPY=X','JPY=X','EURSEK=X','USDCAD=X','AUDCAD=X',
             'KC=F','HG=F', 'CORN', 'CL=F', 'ZS=F','ZW=F','GC=F','X','ZW=F',
             'ETH-USD','PFE'
             ]
    

    #VALORES DEL IBEX 
    for i in range(len(tickers)): 
        print(tickers[i])
        regreMedia.analisis(tickers[i], start, end, dfe)
        #time.sleep (1)
        
    
    #VALORES DEL SP500
    for i in range(len(tickers_sp500)): 
        print(tickers_sp500[i])
        regreMedia.analisis(tickers_sp500[i], start, end, dfe)

        
 
    #CURRENCIES
    
    for i in range(len(tickersCurrencies)): 
        print(tickersCurrencies[i])
        regreMedia.analisis(tickersCurrencies[i], start, end, dfe)        
        #time.sleep (1)
    
    

    
    
    
    
    #################################################################        
    ######################################################BACKTESTING
    
    #Codigo elimeinado, el back testing lo hago con Jupyter
 
        
    ########################################################### backtestingFIN    
    ##########################################################################
    
    print ("******************************************************************************That´s all") 
    print ("****************************************************************************************")       
    
    
    
#/**********************************************************************main()    
 








