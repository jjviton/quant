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

RIESGO DE RUNINA:
    https://www.youtube.com/watch?v=axyGqJFRM7Q


Fuente: 


Started on 2/enero/2022
Version_1: 

Objetivo: 


@author: J3 

"""

# J3_DEBUG__ = False  #variable global (global J3_DEBUG__ )

TELEGRAM__ = False



################################ IMPORTAMOS MODULOS A UTILIZAR.
from pykalman import KalmanFilter

import pandas as pd
import numpy as np
import datetime as dt
import yfinance as yf
import matplotlib.pyplot as plt
from time import sleep

import statsmodels.api as sm

"""
import matplotlib.pyplot as plt
plt.rcParams['figure.figsize'] = 18, 8
plt.style.use("bmh")   
"""

import quant_j3_lib as quant_j
from telegram_bot import *
dentro =True
fuera  =False



#df_sg = pd.DataFrame(columns=('estrategia','instrumento', 'fecha', 'aux1', 'aux2'))

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
    
    dfLog = pd.DataFrame(columns=('Date','Senal', 'Price','Objetivo','ExitReason'))
    dfCartera = pd.DataFrame(columns=['instrumento','long_short_out', 'date','precio','beneficio','stoploss'])
    #dfCartera.set_index('instrumento',inplace=True)
    
    #Variable
    backtesting = False  #variable de la clase, se accede con el nombre StrategyClass.backtesting

    
    def __init__(self, instrumento= 'IBE.MC', real_back=False, para2=1):
        
        StrategyClass.backtesting = real_back    #true => backTesting
        self.para_02 = para2   #variable de la isntancia
        self.__privado = "atributoPrivado"
        self.dfLog = pd.DataFrame(columns=('Date','Senal', 'Price'))
        
        self.instrumento =1
        self.startDate=1
        self.endDate =1
        
        global TELEGRAM__
        if(StrategyClass.backtesting == True):   #backtesting
            TELEGRAM__ = False
        else:
            TELEGRAM__ = True
        
        try:
            StrategyClass.dfCartera= quant_j.leerExcel('carteraKalman')
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
        StrategyClass.dfCartera= quant_j.leerExcel('carteraKalman')
        
        dfx=StrategyClass.dfLog
        dfx2=StrategyClass.dfCartera
        
        #Si no esta el instrumento en la cartera, paso a analizarlo
        if not (instrumento in StrategyClass.dfCartera.values)  :   
               #StrategyClass.dfCartera=StrategyClass.dfCartera.append({'instrumento': instrumento, 'precio': 1}, ignore_index=True) 
            self.analisis_IN(instrumento, startDate, endDate, DF)
        #Si está el isnturmetno en la cartera, miro si estoy largo o corto o fuera
        else:
            col_ =  StrategyClass.dfCartera.instrumento.isin([instrumento])   # devuelve una serie con true/false donde esta el obejto buscado
            linea_2 = col_[col_==True]   # hago una serie con los true, normalmente un solo elemento
            linea_3=linea_2.index
            linea_=linea_3[0]
            #print(linea_)
            l_s_o =   StrategyClass.dfCartera.columns.get_loc("long_short_out")
            comprado_= StrategyClass.dfCartera.iloc[linea_ , l_s_o]   
            
            if(comprado_ == 1):         #Estoy en largo, miro si salir o no.
                self.analisis_OUT(instrumento, startDate, endDate, DF)
                return
            if(comprado_== 0):          #Estoy fuera de mercado
                self.analisis_IN(instrumento, startDate, endDate, DF)
                return
            if(comprado_ ==-1):         #Estoy en corto
                return   
   
        return

        
    def analisis_IN(self, instrumento, startDate, endDate, DF):
                
        resultado= analisisENTRADA(instrumento, startDate, endDate, DF)    #jj
        
        if StrategyClass.backtesting :
            quant_j.salvarExcel(StrategyClass.dfLog, "log"+instrumento)
        quant_j.salvarExcel(StrategyClass.dfCartera, "carteraKalman")

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
        quant_j.salvarExcel(StrategyClass.dfCartera, "carteraKalman")
        
        dfx=StrategyClass.dfLog
        dfx2=StrategyClass.dfCartera
        
        return
    
    @classmethod 
    def analisis_P_L(self, ddf, beneficio=99):
        """
        Descripcion: esta estrategia no tiene un ratio P/L estático, al ser dinamico es elastico el calculo.
        
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
    # 0.- Leemos los datos    
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
        indiceLast_ = (len(df)-1)  
    except:
        return
    PrecioHoy =   df.iloc[indiceLast_,price_]
    
    """
    if (endd== '2013-03-21'):   #BreakPoint under demant :-)  j3viton
        parada=9
        print('precio hoy', PrecioHoy)
        print('precio compra', precioCompra_[linea_])
    """

    ##################################################################
    ##  STOP_LOSS

    StrategyClass.dfLog.loc[endd,'Date'] = endd
    StrategyClass.dfLog.loc[endd,'Price']= df.iloc[indiceLast_,price_]    
    StrategyClass.dfLog.loc[endd,'Senal']= 1       

    # Construct a Kalman filter
    kf = KalmanFilter(transition_matrices = [1],
                  observation_matrices = [1],
                  initial_state_mean = 0,
                  initial_state_covariance = 1,
                  observation_covariance=1,
                  transition_covariance=.01)

    # Use the observed values of the price to get a rolling mean
    state_meansS, _ =kf.smooth(df.Close)
    state_meansS = pd.Series(state_meansS.flatten(), index=df.index)
    
    df['Kalman'] = state_meansS    
    
    price_ = df.columns.get_loc("Close")  
    kalman_ = df.columns.get_loc("Kalman")  
    volumen_ = df.columns.get_loc("Volume")     
    
    # Precio baja por debajo de la linea que marca Kalman
    if( PrecioHoy < df.iloc[(indiceLast_),kalman_] ):      #
    
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
    
    
    elif (PrecioHoy > ((precioCompra_)+beneficioEsperado_)) :  # Precio compra mas 2 ATR
          
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
    
    
    if(not TELEGRAM__):
        telegram_send("3.OUT Señal Kalman v1\n"+ instrumento +"\nPrecio = " + str(df.iloc[(indiceLast_-i),price_]) )
        
    return





def analisisENTRADA(instrumento, startt, endd, df):    #analisis_v2
    """  ESTRATEGIA BASADA EN KALMAN COMO INDICADOR DE TENDENCIA 
    (Me resulta raro, kalman es un estimador ... no sé, habrá que pensarlo)
    
    Entreda: Cuando sale de sobreventa, segunda vela por encima de la linea sobreventa = entrada
    Stoploss: Entre en sobreventa o cruza bajista la linea central despues de haberla rebasado (break even)
    TakeProfit: si llega a sobrevente salir cuadno la linea cambia de color
    
    Si no recibe el DF en la llamada coge los datos de yahoofinances

    
    """      
    señal =False
    resultados = dict();    # Creamos un diccionario para devolver los datos
    resultados['senal']   =  0
    
    # 0.- Lemos los datos    
    try:
        if df.empty:
            df = yf.download(instrumento, startt, endd)
            df.dropna(inplace=True)  
            print ('Descargo datos desde Spyder')
            #yf.download("AMZN AAPL GOOG", start="2017-01-01", end="2017-04-30")
            #df =web.DataReader(instrumento, 'yahoo', start, end)    DA ERROR DE YAHOO FINANCES
        else:
            print ('DDatos desde archivo')
    except:
        resultados['senal']   =  503     #Service Unavaliable
        return resultados
 

    if df.empty:
        print('DataFrame is empty!!!!')
        resultados['senal']   =  503     #Service Unavaliable
        return resultados

    #Test
    # df=quant_j.PGO(df)    
 

    #######################################################################
    ######################################################  ESTRATEGIA

    # 1.- CALCULAMOS EL FILTRO DE KALMAN
   
    """
    # Construct a Kalman filter
    kf = KalmanFilter(transition_matrices = [1],
                  observation_matrices = [1],
                  initial_state_mean = 0,
                  initial_state_covariance = 1,
                  observation_covariance=1,
                  transition_covariance=.01)

    # Use the observed values of the price to get a rolling mean
    #state_means, _ = kf.filter(df.Close)
    state_meansS, _ =kf.smooth(df.Close)
    #state_means = pd.Series(state_means.flatten(), index=df.index)
    state_meansS = pd.Series(state_meansS.flatten(), index=df.index)
    
    df['Kalman'] = state_meansS
    """
    
    df['Kalman']=    quant_j.kalmanIndicator(df,paraA_=200,paraB_=50,instrumento=instrumento)

    indiceLast_ = (len(df)-2)    ### ojo parece que da la ultima version cotizada, no la ultima hora (en rango de horas)
    price_ = df.columns.get_loc("Close")  
    kalman_ = df.columns.get_loc("Kalman")  
    volumen_ = df.columns.get_loc("Volume") 
    open_ = df.columns.get_loc("Open")  
    
    print(instrumento)
   
    contador =0
    señal =fuera
   
    # Compruebo Kalman
    # Según la estrategia tenemos que buscar, dos velas alcistas no necesariamente consecutivas entre una ventana anterior. 
    # estas velas alcistas detras de una condicion de reset (dos velas rojas por debajo kalman)
    
    for i in range(5):
        #vela verde por encima de kalman entera
        if (df.iloc[(indiceLast_-i),price_] > df.iloc[(indiceLast_),kalman_]  and  
            df.iloc[(indiceLast_-i),open_] > df.iloc[(indiceLast_),kalman_]  and
            df.iloc[(indiceLast_-i),price_] > df.iloc[(indiceLast_),open_]):
            contador += 1
            df.iloc[(indiceLast_-i),volumen_] =99.0
    #tres velas verdes y la ultima verde
    if (contador > 2  and
       df.iloc[(indiceLast_),price_] > df.iloc[(indiceLast_),kalman_]  and 
       df.iloc[(indiceLast_-i),open_] > df.iloc[(indiceLast_),kalman_] ): 
        señal=dentro 
    
    #Compruebo Media 200 velas positiva
    #quant_j3.MovingAverage(data,long_=200,short_=50)
    data2= quant_j.MovingAverage(df,long_=200,short_=50)
    # 1.- MEDIA DE 200 SESIONES ACCENDENTE
    #   Calculamos de la media aritmetica la regresion lineal para ver la esencia
    ma200_=data2.columns.get_loc("MA_200")
    data_aux2= data2.iloc[-200:, ma200_]
    data_aux2.dropna(inplace=True)  
    # 3.1.- Calculamos media de las ultimas 'n' sesiones y la regresion lineal
    coef_ema200_, intercept_ema200_ =quant_j.linearRegresion_J3(data_aux2) #+'  de ema200') 
    
      
    #pendiente positiva y vela por encima media200
    if (señal ==dentro):
        if (coef_ema200_ > 0  and 
            df.iloc[(indiceLast_),price_] > data_aux2[-1] and 
            df.iloc[(indiceLast_-i),open_] > data_aux2[-1] ): 
           
            señal=dentro     
        else:
            señal =fuera

  
    print(instrumento,señal)
    print ('Precio', df.iloc[(indiceLast_-i),price_], '*************  ''Kalman', df.iloc[(indiceLast_-i),kalman_])
    print ('checkIN Time',df.index[indiceLast_])
    
    if (señal ==dentro):
        print ('Entramos del mercado')
        
        if(not TELEGRAM__):
            telegram_send("3.IN Señal Kalman v1\n"+ instrumento +"\nPrecio = " + str(df.iloc[(indiceLast_-i),price_]) + "\n***  Kalman level = "+ str(df.iloc[(indiceLast_-i),kalman_])+
                     "\nTime: " + str(df.index[indiceLast_]))
        #sleep(5)
           
       
        
    # Plot original data and estimated mean
    #plt.plot(state_means)
    plt.plot(df.Kalman[-410:])
    plt.plot(df.Close[-410:])
    #plt.plot(mean30)
    #plt.plot(mean60)
    #plt.plot(mean90)
    plt.title('Kalman filter estimate j')
    plt.legend(['KalmanSmooth', 'X']) #, '30-day Moving Average', '60-day Moving Average','90-day Moving Average'])
    plt.xlabel('Day')
    plt.ylabel('Price');
    
    
################################################################################################
   
    """
    # 2.- Comprobar si en las utimas sesiones precio por encima de Kalman

    price_ = df.columns.get_loc("Close")  
    kalman_ = df.columns.get_loc("Kalman")  
    volumen_ = df.columns.get_loc("Volume") 
     
    try:
        #indiceLast_ = np.where(df.index == (endd-dt.timedelta(days=1)))[0][0]  #cambiar esto por ultimo indice
        indiceLast_ = (len(df)-1)  
        #var=df.iloc[(indiceLast_),kalman_]
    except:
        print ('bye')
        return
    
 
    
    contador =0
    for i in range(5):
        #Precio por encima de Kalman cuento uno en el contador
        if (df.iloc[(indiceLast_-i),price_] > df.iloc[(indiceLast_),kalman_]):
            contador += 1
            df.iloc[(indiceLast_-i),volumen_] =99.0

    if (contador > 2):       # dos cierres por encima del indice.
       señal =True
    """   
       
    beneficio =np.array([1.1,2.0])  # heredeado el concepto de beneficio aqui, no se usa más
    
    # 3.- Calculo el ATR de la serie de precios
    dff=quant_j.ATR(df,n=20)
    #last ATR 
    a=dff[-1]
    #last Price
    b=df['Close'][-1]
    beneficio[0] = (1.0 * a)    #dos veces el ATR


    ######################################################  ESTRATEGIA
    #######################################################################    
 
    
    ####################
    ## SEÑAL DE COMPRA
    
    ### Analizamos el P&L de la operacion
    if(señal == True):
        goNogo= StrategyClass.analisis_P_L(df, beneficio[0])
        señal = goNogo
        print('***************** GoNoGo')  
    
    
    if (señal == True):
        print('***************** Señal...')        
        parada=8
 
        #Guardo registros en EXCEL file
        quant_j.saveSignal('Kalman_', 'Kalman b0 (IN)', instrumento,endd, 99, 99, df.iloc[indiceLast_,price_] , beneficio[0])
        
        #Mando señal al bot telegram
        if(TELEGRAM__):
            telegram_send("Señal en la estrategia filtro Kalman b0.0.\nMira " +instrumento)
         
            
        df1=StrategyClass.dfLog
        df2=StrategyClass.dfCartera
            
        ################### Almaceno información en un dataframe log
        #TOBEImprove: añadir nueva linea en el dataFrame para la entrada nueva
        StrategyClass.dfLog.loc[endd,'Date'] = endd
        StrategyClass.dfLog.loc[endd,'Senal']= 1
        StrategyClass.dfLog.loc[endd,'Price']= df.iloc[indiceLast_,price_] 
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
        StrategyClass.dfCartera.iloc[linea_, precio__]      = df.iloc[indiceLast_,price_]
        StrategyClass.dfCartera.iloc[linea_, beneficio__]   = beneficio[0] 
        StrategyClass.dfCartera.iloc[linea_, stoploss__]    = 99 
        
        
        #StrategyClass.dfCartera.loc['Objetivo']    =beneficio[0]  + df.iloc[indiceHoy_,price_]
        #dfCartera = pd.DataFrame(columns=('instrumemto','long_short_out', 'date'))
        
        df1=StrategyClass.dfLog
        df2=StrategyClass.dfCartera
          
        ########## Tenemos Señal, devolvemos la informacion       
        #resultados = dict();    # Creamos un diccionario para devolver los datos
        resultados['instrumento'] =     instrumento
        resultados['date']   =          endd
        resultados['senal']   =         int(1)     #100 equivale a comprar...
        resultados['PrecioEntrada'] =   df.iloc[indiceLast_,price_]
        resultados['PrecioObjetivo']=   beneficio[0]  + df.iloc[indiceLast_,price_]
        return resultados
    
    else:  #señal==False
        ########## Tenemos Señal, devolvemos la informacion       
        #resultados = dict();    # Creamos un diccionario para devolver los datos
        
        
        ################### Almaceno información en un dataframe log
        StrategyClass.dfLog.loc[endd,'Date'] =endd
        StrategyClass.dfLog.loc[endd,'Senal']=0
        StrategyClass.dfLog.loc[endd,'Price']=df.iloc[indiceLast_,price_]   
        
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
    """Estrategia basica kalmaN filter
    
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
    
    kalmanClass= StrategyClass(real_back=True)    #Creamos la clase, para backTESTING
    
    """
    if( TELEGRAM__):
        telegram_send("3.- Estrategia KALMAN V0.0\n ")
    dfe = pd.DataFrame({'A' : []})   #df empty
    
    #### FECHAS
    start =dt.datetime(2000,1,1)
    #start =dt.datetime.today() - dt.timedelta(days=400)    #un año tiene 250 sesiones.
    end = dt.datetime(2021,10,1)
    #end= dt.datetime.today()  - dt.timedelta(days=1)        #Quito hoy para no ver el valor al ejecutar antes del cierre
    #end = '2021-9-19'
    
    #TICKERS
    tickers5 = ['AAPL', 'MSFT', '^GSPC', 'ELE.MC','SAN.MC', 'BBVA.MC']  #,'ANA.MC','MTS.MC','GRF.MC']  # apple,microsfoft,sp500, endesa
    tickers__ = ['MTS.MC'] 
    tickers = ['FER.MC','COL.MC','IBE.MC','NTGY.MC','SAB.MC','ACX.MC','PHM.MC','SAN.MC','MRL.MC','TEF.MC','AMS.MC','VIS.MC','MTS.MC','MAP.MC','CLNX.MC','BBVA.MC','CABK.MC','MEL.MC','AENA.MC','BKT.MC','REE.MC','FDR.MC','ACS.MC','ITX.MC','ENG.MC','ANA.MC','ELE.MC','GRF.MC','IAG.MC','SGRE.MC']
    tickersCurrencies =['EURUSD=X', 'EURGBP=X' ,'EURCHF=X', 'EURJPY=X', 'EURNZD=X', 'EURCAD=X', 'EURAUD=X','USDCHF=X', 
             'USDJPY=X','GBPCAD=X', 'GBPUSD=X', 'GBPJPY=X', 'GBPCHF=X', 'GBPNZD=X', 'GBPAUD=X',
             'NZDCAD=X', 'NZDUSD=X', 'NZDCHF=X', 'NZDJPY=X','JPY=X','EURSEK=X','USDCAD=X','AUDCAD=X',
             'KC=F','HG=F', 'CORN', 'CL=F', 'ZS=F','ZW=F','GC=F','X','ZW=F',
             'ETH-USD','PFE'
             ]
    

    #VALORES DEL IBEX 
    for i in range(len(tickers__)): 
        print(tickers__[i])
        kalmanClass.analisis(tickers__[i], start, end, dfe)
        #time.sleep (1)

         
    #CURRENCIES
    for i in range(len(tickersCurrencies)): 
        print(tickersCurrencies[i])
        kalmanClass.analisis(tickersCurrencies[i], start, end, dfe)        
        #time.sleep (1)
        
    
    #VALORES DEL SP50
    sp_url= 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    sp=pd.read_html(sp_url,header=0)[0]
    print (sp.info())
    
    for i in range(len(sp)):
         symbol=sp.iloc[i,0] 
         #df = yf.download(symbol, start, end)
         print(symbol)
         kalmanClass.analisis(symbol, start, end, dfe )
         #time.sleep (1)
    """
    
    
    
    #################################################################        
    ######################################################BACKTESTING
    if (True):  #backtesting
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
         
        instrumento ='FTNT'
        dff = yf.download(instrumento, start_G,end_G)
        
        #regreMedia= StrategyClass()    #Creamos la clase
        
        #regreMedia.analisis_P_L(dff, 4)  #Solo para probar el ATR
        
        
        
        TOTAL_len =500     # para acotar
        for i in range(TOTAL_len):
            endWindow3   =endWindow2 + dt.timedelta(days=i) 
            endWindow    =endWindow3.strftime("%Y-%m-%d")
            print ('end date:', endWindow)
            
            if(endWindow in dff.index):
                df_aux= dff.loc[startWindow:endWindow]    #voy pasando los datos desplazando la ventana
                
                recogo = kalmanClass.analisis(instrumento, startWindow, endWindow, df_aux) #Llamada a la clase estrategia. LA CLAVE DE TODO!!!
                
                
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
 








