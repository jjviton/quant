# =============================================================================
# Backtesting strategy - II : Intraday resistance breakout strategy
# Author : Mayank Rasu

# Please report bug/issues in the Q&A section
# =============================================================================

import numpy as np
import pandas as pd
#from alpha_vantage.timeseries import TimeSeries
import copy
import pandas_datareader as web
import datetime as dt

from quant_j3_lib import *  

"""
def ATR(DF,n):
    "function to calculate True Range and Average True Range"
    df = DF.copy()
    df['H-L']=abs(df['High']-df['Low'])
    df['H-PC']=abs(df['High']-df['Adj Close'].shift(1))
    df['L-PC']=abs(df['Low']-df['Adj Close'].shift(1))
    df['TR']=df[['H-L','H-PC','L-PC']].max(axis=1,skipna=False)
    df['ATR'] = df['TR'].rolling(n).mean()
    #df['ATR'] = df['TR'].ewm(span=n,adjust=False,min_periods=n).mean()
    df2 = df.drop(['H-L','H-PC','L-PC'],axis=1)
    return df2['ATR']
"""
def CAGR___(DF):
    "function to calculate the Cumulative Annual Growth Rate of a trading strategy"
    df = DF.copy()
    df["cum_return"] = (1 + df["ret"]).cumprod()
    n = len(df)/(252*78)
    CAGR = (df["cum_return"].tolist()[-1])**(1/n) - 1
    return CAGR

def volatility___(DF):
    "function to calculate annualized volatility of a trading strategy"
    df = DF.copy()
    vol = df["ret"].std() * np.sqrt(252*78)
    return vol

def sharpe___(DF,rf):
    "function to calculate sharpe ratio ; rf is the risk free rate"
    df = DF.copy()
    sr = (CAGR___(df) - rf)/volatility___(df)
    return sr
    

def max_dd___(DF):
    "function to calculate max drawdown"
    df = DF.copy()
    df["cum_return"] = (1 + df["ret"]).cumprod()            # Retorno acumulado (ojo a los calculos)
    df["cum_roll_max"] = df["cum_return"].cummax()          # de todos los datos anteriores guarda el max
    df["drawdown"] = df["cum_roll_max"] - df["cum_return"]  # resta entre el max y el actual
    df["drawdown_pct"] = df["drawdown"]/df["cum_roll_max"]  # Porcentage
    max_dd = df["drawdown_pct"].max()                       # maximo del porcentage
    return max_dd



def estrategia_breakout_main():
    """Estrategia compra Largo o Cortos por la rotura de soporte o resitencia

    Explicamos la estrategia
    
    Hacemos un backTesting de los resultados.
    
    Parámetros:
    a -- 
    b -- 
    c -- 
    
    Devuelve:
    Valores trabajados y ordenados

    Excepciones:
    ValueError -- Si (a == 0)
    
    """

    # Download historical data (monthly) for selected stocks
    
    #tickers = ["MSFT","AAPL","FB","AMZN","INTC", "CSCO","VZ","IBM","QCOM","LYFT"]
    tickers = ["MSFT","AAPL","FB"]
    ohlc = {}        #creo un diccionario para almacenar todos los valoras de las cotizaciones
    #a.- Leer de WEB
    start =dt.datetime(2010,1,1)
    #end = dt.datetime(2020,9,6)
    end= dt.datetime.today()
    
    #Relleno el dictionary: clave pongo el Ticker y valor el DataFrame
    for i in range(len(tickers)):  
         ohlc[tickers[i]]= web.DataReader(tickers[i], 'yahoo', start, end)   # leemos los valore sde tesl 
    tickers = ohlc.keys() # redefine tickers variable after removing any tickers with corrupted data 
    

################################Backtesting####################################
 
    # calculating ATR and rolling max price for each stock and consolidating this info by stock in a separate dataframe
    ohlc_dict = copy.deepcopy(ohlc)  # hace una copia del objeto, no es asignacion o puntero es copia.
    tickers_signal = {}
    tickers_ret = {}
    for ticker in tickers:
        print("calculating ATR and rolling max price for ",ticker)
        ohlc_dict[ticker]["ATR"] = ATR(ohlc_dict[ticker],20)                            # Indicador de la volatilidad reciente.
        ohlc_dict[ticker]["roll_max_cp"] = ohlc_dict[ticker]["High"].rolling(20).max()  # Cierre alto maximo de los ultimos 20 dias
        ohlc_dict[ticker]["roll_min_cp"] = ohlc_dict[ticker]["Low"].rolling(20).min()   # cierre bajo minimo de los ultimos 20 dias
        ohlc_dict[ticker]["roll_max_vol"] = ohlc_dict[ticker]["Volume"].rolling(20).max()   # volumen mas alto de los ultimos 20 dias
        ohlc_dict[ticker].dropna(inplace=True)  # Limpiamos los non a value
        tickers_signal[ticker] = ""
        tickers_ret[ticker] = []
        
    #visualizar
    print (ohlc_dict['MSFT'].head())
    dfAux=ohlc_dict['MSFT'][["ATR",'roll_max_cp','roll_min_cp']]   
    dfAux.plot(figsize=(16,8),title=' Indices derivados ')
    dfAux2=ohlc_dict['MSFT'][["Volume",'roll_max_vol']]   
    dfAux2.plot(figsize=(16,8),title=' Volumen   J3')
    
    
    # identifying signals and calculating daily return (stop loss factored in)
    """
    Señales:
        Tomo como resistencia el max de las ultimas 20 sesiones.
        Rotura de este max + rotura del volumen max de los ultimos dias 
        Señal de compra
        
    Stop Loss:
        Precio menos ATR de 20 sesiones
        
    How does it work?
        tickers_signal es una variable que guarde el estado en el que estoy: comprado, vendido o nada    
        
    """
    for ticker in tickers:
        print("calculating returns for ",ticker)
        for i in range(len(ohlc_dict[ticker])):     # Todos los datos de la serie diaria
            if tickers_signal[ticker] == "":        
                tickers_ret[ticker].append(0)       # Reservo memoria,
                
                # High del dia mayor o igual maximos de las 20 sesiones previas AND volumen de hoy 1,5 veces max volumen de las 20 sesiones anteriores " BUY
                # Rotura de resitencia y tendecia alcista= Comprado
                if ohlc_dict[ticker]["High"][i]>=ohlc_dict[ticker]["roll_max_cp"][i] and \
                   ohlc_dict[ticker]["Volume"][i]>1.5*ohlc_dict[ticker]["roll_max_vol"][i-1]:
                    tickers_signal[ticker] = "Buy"      # Estado = comprado largo por tendencia alcista
                                        
                elif ohlc_dict[ticker]["Low"][i]<=ohlc_dict[ticker]["roll_min_cp"][i] and \
                   ohlc_dict[ticker]["Volume"][i]>1.5*ohlc_dict[ticker]["roll_max_vol"][i-1]:
                    tickers_signal[ticker] = "Sell"     #Estado = vencdido, corto por tendencia bajista  (no confundir con vender lo antes comprado, es tendencia.)
            
            # Estamos Comprados LARGOS  ((venimos de tendencia alcista por rotura resistencia))
            elif tickers_signal[ticker] == "Buy":
                #Compruebo StopLoss: bajo de hoy menor que (cierre de ayer - ATR de ayer) = salta el stop
                if ohlc_dict[ticker]["Low"][i]<ohlc_dict[ticker]["Adj Close"][i-1] - ohlc_dict[ticker]["ATR"][i-1]:
                    tickers_signal[ticker] = ""   # CIERRO LA POSICION
                    #Calculo el rendimiento con el valor en el que he cortado la operacion.
                    tickers_ret[ticker].append(((ohlc_dict[ticker]["Adj Close"][i-1] - ohlc_dict[ticker]["ATR"][i-1])/ohlc_dict[ticker]["Adj Close"][i-1])-1)
                #Compruebo la condicion BAJISTA por rotura de soporte, si se confirma cambio y me pongo bajista
                elif ohlc_dict[ticker]["Low"][i]<=ohlc_dict[ticker]["roll_min_cp"][i] and \
                   ohlc_dict[ticker]["Volume"][i]>1.5*ohlc_dict[ticker]["roll_max_vol"][i-1]:
                    tickers_signal[ticker] = "Sell"
                    tickers_ret[ticker].append(((ohlc_dict[ticker]["Adj Close"][i-1] - ohlc_dict[ticker]["ATR"][i-1])/ohlc_dict[ticker]["Adj Close"][i-1])-1)
                #Si no salta el stop y no condicion de bajista, dejo correr las ganancias
                else:
                    tickers_ret[ticker].append((ohlc_dict[ticker]["Adj Close"][i]/ohlc_dict[ticker]["Adj Close"][i-1])-1)
            
            #Estamos comprado CORTOS ((tendencia bajista por rotura de soprote))        
            elif tickers_signal[ticker] == "Sell":
                if ohlc_dict[ticker]["High"][i]>ohlc_dict[ticker]["Adj Close"][i-1] + ohlc_dict[ticker]["ATR"][i-1]:
                    tickers_signal[ticker] = ""
                    tickers_ret[ticker].append((ohlc_dict[ticker]["Adj Close"][i-1]/(ohlc_dict[ticker]["Adj Close"][i-1] + ohlc_dict[ticker]["ATR"][i-1]))-1)
                elif ohlc_dict[ticker]["High"][i]>=ohlc_dict[ticker]["roll_max_cp"][i] and \
                   ohlc_dict[ticker]["Volume"][i]>1.5*ohlc_dict[ticker]["roll_max_vol"][i-1]:
                    tickers_signal[ticker] = "Buy"
                    tickers_ret[ticker].append((ohlc_dict[ticker]["Adj Close"][i-1]/(ohlc_dict[ticker]["Adj Close"][i-1] + ohlc_dict[ticker]["ATR"][i-1]))-1)
                else:
                    tickers_ret[ticker].append((ohlc_dict[ticker]["Adj Close"][i-1]/ohlc_dict[ticker]["Adj Close"][i])-1)
                    
        ohlc_dict[ticker]["ret"] = np.array(tickers_ret[ticker])
    
    
    # calculating overall strategy's KPIs
    strategy_df = pd.DataFrame()
    for ticker in tickers:
        strategy_df[ticker] = ohlc_dict[ticker]["ret"]
    strategy_df["ret"] = strategy_df.mean(axis=1)       #media por fila cogiendo las tres acciones
    
    strategy_df['acumulado']=(1+strategy_df["ret"]).cumprod()
    strategy_df[['acumulado']].plot(figsize=(16,8), title='Rendimiento acumulado...............', color='green')
            #  df["cum_return"] = (1 + df["ret"]).cumprod()  
            
    # KPI de la media por filas de las tres acciones.No es una a una!!
    CAGR___(strategy_df)
    sharpe___(strategy_df,0.025)
    max_dd___(strategy_df)  
    
    
    # Calculating individual stock's KPIs
    cagr = {}
    sharpe_ratios = {}
    max_drawdown = {}
    
    #Calculamos el dato de KPI para las acciones
    for ticker in tickers:
        print("calculating KPIs for ",ticker)      
        cagr[ticker] =  CAGR___(ohlc_dict[ticker])  #Tomamos accion por accion.
        sharpe_ratios[ticker] =  sharpe___(ohlc_dict[ticker],0.025)
        max_drawdown[ticker] =  max_dd___(ohlc_dict[ticker])
    #Creamos un dataFrame con el diccionario de los datos KPI
    KPI_df = pd.DataFrame([cagr,sharpe_ratios,max_drawdown],index=["Return","Sharpe Ratio","Max Drawdown"])      
    #KPI_df.T  #Transponemos al dataFrame
    print (KPI_df)
    print (KPI_df.T)
    
    return(32)