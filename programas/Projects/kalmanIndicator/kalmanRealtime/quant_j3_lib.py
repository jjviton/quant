# -*- coding: utf-8 -*-
"""
Created on Sun Sep 13 11:28:48 2020

@author: INNOVACION
"""

J3_DEBUG__ =False
  


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import statsmodels.api as sm   #se usa en el Slope del curso, quitar

from openpyxl import load_workbook

from sklearn import linear_model
from sklearn.metrics import mean_squared_error, r2_score
from scipy.signal import find_peaks, argrelextrema

#################################  Mogalef bands

def MogalefBands(df,paraA_=200,paraB_=50,instrumento="_"): 
    #// Calculation Mogalef Bands
    #// variables std1=7 linear1=3
    
    #CP=(open+high+low+2*close)/5
    cp= (df['Open']+df['High']+df['Low']+2*df['Close']) / 5
    
    F=LinearRegression[linear1](CP)
    E=std[std1](F)
    
    coef_ema200_, intercept_ema200_ =quant_j.linearRegresion_J3(df_aux2,instrumento=instrumento) #+'  de ema200')  
    
    """
    if barindex<8 then
    Median = undefined
    BandHigh = undefined
    BandLow = undefined
    
    Else
    BandHigh = F+(E*2)
    BandLow = F-(E*2)
    BandMedHigh = F+E
    BandMedLow = F-E
    
    if F<BandHigh[1]and F>BandLow[1]then
    E=E[1]
    BandHigh=BandHigh[1]
    BandLow=BandLow[1]
    BandMedHigh=BandMedHigh[1]
    BandMedLow=BandMedLow[1]
    
    endif
    
    Median =(BandHigh+BandLow)/2
    Endif
    
    return BandHigh as"Mogalef Band High", Median as "Mogalef Median Band », BandLow as "Mogalef Band Low", BandMedHigh as"Mogalef Band Med High », BandMedLow as "Mogalef Band Med Low"
    """
    return
################################ END MogalefBands

def kalmanIndicator(df,paraA_=200,paraB_=50,instrumento="_"):
    """
    Calcula el indicador de Kalman. necesita df['Close']
    
    Args:
        df (TYPE): DESCRIPTION.
        paraA_ (TYPE, optional): DESCRIPTION. Defaults to 200.
        paraB_ (TYPE, optional): DESCRIPTION. Defaults to 50.
        instrumento (TYPE, optional): DESCRIPTION. Defaults to "_".

    Returns:
        TYPE: DESCRIPTION.

    """

    
    from pykalman import KalmanFilter
    
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
    return df['Kalman']

################################################# KalmanIndicator


############################################## Save Signals

def saveSignal(fichero, estrategia, instrumento, fecha, parametro1=1, parametro2=2,parametro3=3,parametro4=4):
    """Funcion que registra en un excel las señales para suposterior anailisis
    Input Data: entreda estrategia+instrumenteo+fecha
    Returns:nada
    Ejemplo:    
                quant_j.saveSignal('nobreFicherosinXLS', 'RegresionMedia b0', instrumento,dt.datetime.today() )
    Estado: programada 
    Origen  (J3...2021)
    """
    try:
        df_sg=pd.read_excel(fichero +'.xls', index_col=0)  
        #wb = load_workbook(filename = 'empty_book.xlsx')
    except (OSError, IOError):
        print('!')
        df_sg = pd.DataFrame(columns=('estrategia','instrumento', 'fecha', 'aux1', 'aux2','aux3', 'aux4'))
    
    new_row = {'estrategia':estrategia, 'instrumento':instrumento, 'fecha':fecha, 'aux1':parametro1,'aux2':parametro2,'aux3':parametro3,'aux4':parametro4}
    #append row to the dataframe
    df_sg = df_sg.append(new_row, ignore_index=True) 
    salvarExcel(df_sg, fichero)  
    return 

############################################## Safe Signals


#################################################### RegresionLineal()
def linearRegresion_J3(ser,instrumento=" "):
    """ esta funcion llama a slopeJ3, ahcen lo mismito... solo por ser coherente con los nombre
    """
    (coef_, intercept_) = slopeJ3(ser,instrumento=instrumento)
    
    # devolvemos pendente y puntoCorte
    return(coef_, intercept_)     
#################################################### slopeJ3()
def slopeJ3(ser,n=5,instrumento=" "):
    """Function to calculate the slope of regression line for n consecutive points on a plot
    https://www.aprendemachinelearning.com/regresion-lineal-en-espanol-con-python/
    Regresion lineal de una nube de puntos.
    Funciona bastante bien, pero necesita una buena fuente de datos. Identificar Max/Min relativos??.
        
    *** DUDAS: esta funcion debemos acompañarla de otra que calcule los maximos//minimos relativos. Para calcular
    la pendiente por tramos.
    
    Input Data: entrada es una serie/array/lista NO UN DATAFRAME. Hacemos una especie de rolling slope con una 
    ventana de 'n' 05.
    Returns: pendiente[m] de la recta y el termino independiente[b]     y=mx+b
    
    Ejemplo:
            m_,b_ =slopeJ3(df['Adj Close'])  # devuelve pendiente y termino independiente
            print ("LA ECUACION DE LA RECTA CALCULADA POR LA REGRESION LINEAL ES\n  y= ", m_, "X + ",b_)
    
            var_03 = df.columns.get_loc("Adj Close")    # Para usar iLoc necesito la posicion de un 'label'
            m_,b_ =slopeJ3(df.iloc[700:1100,var_03])    # devuelve pendiente y termino independiente
            print ("LA ECUACION DE LA RECTA CALCULADA POR LA REGRESION LINEAL ES\n  y= ", m_, "X + ",b_)
       
            var_03 = df.columns.get_loc("Adj Close")    # Para usar iLoc necesito la posicion de un 'label'
            m_,b_ =slopeJ3(df.iloc[900:1100,var_03])    # devuelve pendiente y termino independiente
            print ("LA ECUACION DE LA RECTA CALCULADA POR LA REGRESION LINEAL ES\n  y= ", m_, "X + ",b_)
    
    Estado: programada 
    Origen Curso Quant    (J3...2020)
    """
    #1.- Normalizamos  ¿¿??
    #ser = (ser - ser.min())/(ser.max() - ser.min())         #Normalizamos la serie 
    
    if ser.empty:
        print('DataFrame is empty!++')
        return (0,0)

    #2.- Creo un array con la variable independiente 'X'
    X = np.array(range(len(ser)))  
    #serArray = ser.to_numpy()                  #creamos un array y lo llena de num consecutivos de la serie
    serArray = ser 
                               #si fuera un dataframe lo paso a numpy array 
    #3.- Ploteamos
    if (J3_DEBUG__):
        fig, ax = plt.subplots()  # Create a figure containing a single axes.
        ax.set_title('Regresion Lineal  '+ instrumento + '   '+ str(len(ser)))
        ax.plot(X,serArray)     
    #4.- Create linear regression object
    regr = linear_model.LinearRegression()
    #5.- Train the model using the training sets
    X1=X.reshape(-1,1)
    regr.fit(X1, serArray)
    #6.- Make predictions using the data set. Para dibujar la linea calculada por la regresion
    serLinearRegresion = regr.predict(X1)

    #7.- Pintamos la linea
    if (J3_DEBUG__):
        ax.plot(X,serLinearRegresion)
        
    #8.- parametros de la linea  y=mx+a
    # Veamos los coeficienetes obtenidos, En nuestro caso, serán la Tangente
    print('Coefficients: \n', regr.coef_)
    # Este es el valor donde corta el eje Y (en X=0)
    print('Independent term: \n', regr.intercept_)
            # Error Cuadrado Medio
            #print("Mean squared error: %.2f" % mean_squared_error(ser, serLinearRegresion))
            # Puntaje de Varianza. El mejor puntaje es un 1.0
            #print('Variance score: %.2f' % r2_score(ser, serLinearRegresion))
    # devolvemos pendente y puntoCorte
    return(regr.coef_, regr.intercept_)                        
#################################################### slopeJ3()

 


#################################################### slopeJ3()
def slopeJ3_2points(x1,y1,x2,y2):
    """Funcion que calcula pendiente y punto de corte para dos puntos dadosde una serie temporal. 
    *** DUDAS: 
    
    Input Data: dos puntos (timeStamp_1, precio_1)
    Returns: pendiente[m] de la recta y el termino independiente[b]     y=mx+b
    
    Ejemplo:
    
    Estado: programandose
    Origen J3   (J3...2020)
    """
    pendiente_= (y2-y1)/(x2-x1)
    pto_corte_= (y1)-(pendiente_*x1)
 
    
    if (J3_DEBUG__):
        print('***************** Pendiente de dos puntos:')
        # Veamos los coeficienetes obtenidos, En nuestro caso, serán la Tangente
        print('\t Coefficients: ', pendiente_)
        # Este es el valor donde corta el eje Y (en X=0)
        print('\t Pto corte: ', pto_corte_)
        print('\n')
            
    # devolvemos pendente y puntoCorte
    return(pendiente_, pto_corte_)                        
#################################################### slopeJ3_2points()


#################################################### slope()
def slope(ser,n=5):
    """Function to calculate the slope of regression line for n consecutive points on a plot
    
    
    *** DUDAS: yo lo haria de otra manera con tensorflow u otras. Pero no reinventes la rueda, hazla girar!!!!
    No me parece que esté bien, normaliza las x, cuando es una serie de valores. lo hace en radianes. 
    Se puede hacer más sencillo. Intentaremos probarlo y hacer algo mejor...
    
    Input Data: entrada es una serie/array/lista NO UN DATAFRAME. Hacemos una especie de rolling slope con una 
    ventana de 'n' 05.
    Returns: 
    
    Estado: programada 
    Origen Curso Quant    (J3...2020)
    """
    ser = (ser - ser.min())/(ser.max() - ser.min())         #Normalizamos la serie 
    x = np.array(range(len(ser)))                           #creamos un array y lo llena de num consecutivos
    x = (x - x.min())/(x.max() - x.min())                   #normaliza ¿¿??
    slopes = [i*0 for i in range(n-1)]                      #Array de slopes, inicializando las n-1 primeras a cero
    
    for i in range(n,len(ser)+1):
        y_scaled = ser[i-n:i]                               # slice desde (i-n)hasta (i)
        x_scaled = x[:n]                                    # cojo los 'n' primeros valores (de una serie consecutiva normalizada)MiNoEntender
        x_scaled = sm.add_constant(x_scaled)                # añade constante para que la regresion (y=mx+a)
        model = sm.OLS(y_scaled,x_scaled)                   #migrar esto a tensorlfow y sckitylearn
        results = model.fit()
        slopes.append(results.params[-1])                   #sacamos la pendiente
    slope_angle = (np.rad2deg(np.arctan(np.array(slopes)))) #radienes to degree ¿¿??
    return np.array(slope_angle)                            
#################################################### slope()


#################################################### OBV()
def OBV(DF):
    """function to calculate On Balance Volume
    Indicador de MOMENTO.  Sobre la base de que si el volumen subre bruscmante presionará el precio al alza.
    Si el precio sube, suma el volumen de hoy al OBV; si baja lo resta.
    Indicador que genrea falsas señales, NO usar solo!!
    
    *** DUDAS: 
    
    Input Data: it needs a dataFrame containing a column [Adj_Close]
    Returns: devuelve una serie de datos con el OBV
    
    Estado: programada 
    Origen Curso Quant    (J3...2020)
    """
    df = DF.copy()
    df['daily_ret'] = df['Adj Close'].pct_change()          #porcentage de cambio repecto del anterior valor
    df['direction'] = np.where(df['daily_ret']>=0,1,-1)     #Orden similar a excel-> (condicion, if true, if false)
    df['direction'][0] = 0
    df['vol_adj'] = df['Volume'] * df['direction']
    df['obv'] = df['vol_adj'].cumsum()              #Devuelve la suma acumulada de la serie hasta ahora
    
    del df["daily_ret"]
    del df["direction"]
    del df["vol_adj"]
    
    return df['obv']

#################################################### OBV()

#################################################### CAGR()
def CAGR(DF):
    """function to calculate Computed Annual Growth Rate
    Beneficio anualizado en porcentaje

    *** DUDAS: 
    
    Input Data: it needs a dataFrame containing a column [Adj_Close]
    Returns: 
    
    Estado: programada 
    Origen Curso Quant    (J3...2020)
    """    
    df = DF.copy()
    df["daily_ret"] = DF["Adj Close"].pct_change()          #Porcentaje de cambio respecto del anterior value
    df["cum_return"] = (1 + df["daily_ret"]).cumprod()      #Return cumulative product over a DataFrame or Series axis.
                                                            #va guardando en la celda el prodcuto acumulado de la anteriores
    n = len(df)/252                                         #Calculo numero de años de la serie
    CAGR = (df["cum_return"][-1])**(1/n) - 1                #Calculo CARG
    return CAGR
#################################################### CAGR()

#SharpeRatio  https://www.selfbank.es/centro-de-ayuda/fondos-de-inversion/que-es-el-ratio-de-sharpe


#################################################### Volatililty()
def volatility(DF):
    """function to calculate annualized volatility of a Close series
    
    Basicamente es la desviacion standar de los precio repecto de la media/Esperanza matematica
    Lo multiplican por sqr(252), numero de sesiones al año  ¿¿??
    No debemos pasar mas de un año de datos
    *** DUDAS: es un porcentaje. No es una cantidad en valor absuloto euros.  quizas DataFrame.diff(periods=1, axis=0)
    
    Input Data: it needs a dataFrame containing a column [Adj_Close]
    Returns: a number representing Volatility.
    
    Estado: programada 
    Origen Curso Quant    (J3...2020)
    """
    df = DF.copy()
    df["daily_ret"] = DF["Adj Close"].pct_change()   #Porcentage de cambio repescto anterior
    vol = df["daily_ret"].std() * np.sqrt(252)       #standart deviation   
    
    return vol
################################################### Volatililty()

#################################################### Volatililty_j()
def volatility_j(DF):
    """function to calculate annualized volatility of a Close series
    
    Mi fucnion de volatilidad.
    En este caso caluclo la volatilidad como una diferencia desde precio medio. Usando la desviacion standart 'veo'
    como los precios se mueven alrededor de la media. No me gusta el peso elevado que toman los ouliers  (extremos), aunque
    estos extremos pueden ser bueno para hacer una estrategia de regresion a la media ¿¿??
    
    Input Data: it needs a dataFrame containing a column [Adj_Close]
    Returns: devuelve dos datos: la volatilidad Standart (matematica) y la volatilidad media. Estos concepto sin relacionarlos
    con el precio sirve de poco. Ojo que la media no es de valores absolutos (y deberia para no compensarse)
    
    Estado: programada
    Origen J3     (J3...2020)
    """
    df = DF.copy()
    df["daily_ret"] = DF["Adj Close"].diff()   #diferencia respecto anterior valor de la fila (el dia de antes)
    volatilidad_std = df["daily_ret"].std()        #standart deviation en valor absoluto (entre que valores se mueve normalmente)
    volatilidadMedia=df['daily_ret'].mean()
    
    return (volatilidad_std, volatilidadMedia)

################################################### Volatililty_j()

#################################################### Media Movil Simple
def MovingAverageSingle(DF,n=50,instrumento="_"):
    """Function to calculate 
    typical values 
    
    Input Data: it needs a dataFrame containing a column [Adj_Close]
    Returns; same dataFrame with a new column [...] and new column[Signal] and [Histo]
    
    Estado: programada y probada. 
    Origen      (J3...2020)
    """

    df = DF.copy()
    ma_ = pd.Series( pd.Series.rolling(df['Adj Close'],n).mean(), name='MA_')    
    df=df.join(ma_)
     
    return df

#################################################### Media Movil Simple


#################################################### Media Movil Simple (larga y corta)
def MovingAverage(DF,long_=200,short_=50,instrumento="_"):
    """Function to calculate 
    typical values 
    
    Input Data: it needs a dataFrame containing a column [Adj_Close]
    Returns; same dataFrame with a new column [...] and new column[Signal] and [Histo]
    
    Estado: programada y probada. 
    Origen      (J3...2020)
    """

    df = DF.copy()

    #MA = pd.Series( pd.Series.rolling(df['Adj Close'],n).mean() ,name='MA_'+str(n))
    ma_L = pd.Series( pd.Series.rolling(df['Close'],long_).mean(), name='MA_'+ str(long_))
    ma_S = pd.Series( pd.Series.rolling(df['Close'],short_).mean(), name='MA_'+ str(short_))
    df=df.join(ma_L)
    df=df.join(ma_S)
    
    #visualizar
    if (J3_DEBUG__):
        print (df.head())
        dfAux2=df[['Close', 'MA_'+str(long_), 'MA_'+str(short_)]]
        dfAux2.plot(figsize=(16,8),title='Moving Average   '+ instrumento)
  
    return df

#################################################### Media Movil Simple



#################################################### Media Movil Exponencial EMA
def ExponentialMovingAverage(DF,long_=200,short_=30):
    """Function to calculate 
    typical values 
    
    Input Data: it needs a dataFrame containing a column [Adj_Close]
    Returns; 
    
    Estado: programada y probada. 
    Origen      (J3...2020)
    """

    df = DF.copy()
    #df.Close.plot()     #ploatemos basicamente
    
    #MA = pd.Series( pd.Series.rolling(df['Adj Close'],n).mean() ,name='MA_'+str(n))
    ema_L = pd.Series( pd.Series.ewm(df['Close'],span=long_, min_periods=long_-1,adjust=False).mean(), name='EMA_'+ str(long_))
    ema_S = pd.Series( pd.Series.ewm(df['Close'],span=short_, min_periods=short_ -1,adjust=False).mean(), name='EMA_'+ str(short_ ))
    #    ema_S = pd.Series( pd.Series.rolling(df['Adj Close'],short_).mean(), name='MA_'+ str(short_))
    df=df.join(ema_L)   #añade una columna al dataFrame
    df=df.join(ema_S)
    
    #visualizar
    if (J3_DEBUG__):
        print (df.head())
        colors=['cyan', 'lightgreen', 'green']
        dfAux=df[['Close', 'EMA_200', 'EMA_20']]
        dfAux.plot(figsize=(16,8),title='Exponential Moving Average',color=colors)
  
    return df

#################################################### Media Movil Exponencial

#################################################### MACD
def MACD(DF,a=12,b=26,c=9):
    """Function to calculate MACD
       typical values a = 12; b =26, c =9
       
       Input Data: it needs a dataFrame containing a column [Adj_Close]
       Returns; same dataFrame with a new column [MACD] and new column[Signal] and [Histo]
       
       Estado: programada y probada. 
       Origen Curso Quant     (J3...2020)
       """
       
    df = DF.copy()
    df["MA_Fast"]=df["Adj Close"].ewm(span=a,min_periods=a).mean()  #medias exponencial ponderado
    df["MA_Slow"]=df["Adj Close"].ewm(span=b,min_periods=b).mean()
    df["MACD"]=df["MA_Fast"]-df["MA_Slow"]
    df["Signal"]=df["MACD"].ewm(span=c,min_periods=c).mean()
    df.dropna(inplace=True)  #remover missing values
    #Caluclo histograma
    df["Histo"]= df["MACD"]-df["Signal"]
    #Clean intermediate column
    del df["MA_Fast"]
    del df["MA_Slow"]
    
    #plot
    df.iloc[:, [6,7,8]].plot()   #Pintamos el MACD y Signal y Histo
    
    return df
#################################################### MACD

#################################################### ATR
def ATR(DF,n=20):
    """Function to calculate ATR True Range and Average True Range
       typical values n=20
       ATR calcula tres diferencias maximas(hoy max-min; hoyHight-previousClose; hoyLow-previousClose) 
       y se queda con la mayor. Luego media movil de n periodos 
       Digamos que es un indicador de volatilidad reciente
       OJO: hace media simple... más interesante la ponderada exponencial
       
       Input Data: it needs a dataFrame containing a columns Hight, Low, Close
       Returns; ATR, AT
       
       Estado:  
       Origen Curso Quant     (J3...2020)
       """    
       
    df = DF.copy()
    df['H-L']=abs(df['High']-df['Low'])                     # Today High minus Low  
    df['H-PC']=abs(df['High']-df['Close'].shift(1))     # Shift nos mueve a la fila anterior (presentHigh menos previousClose)
    df['L-PC']=abs(df['Low']-df['Close'].shift(1))      # Today´s Low minus previousClose
    df['TR']=df[['H-L','H-PC','L-PC']].max(axis=1,skipna=False)  # Obtiene el Max de las tres columnas
    #df['ATR'] = df['TR'].rolling(n).mean()
    df['ATR'] = df['TR'].ewm(span=n,adjust=False,min_periods=n).mean()  #En caso de querer hacer media exponencial
    ##df2 = df.drop(['H-L','H-PC','L-PC'],axis=1)     #Quitamos columnas intermedias
    df.dropna(inplace=True)                        #Quita las filas que que el ATR en nan     
    
    #df.iloc[:, [6,7]].plot()   #Pintamos 
    return df['ATR']
#################################################### ATR


#################################################### BB
def BollBnd(DF,n=20):
    """Function to calculate BollingerBands
       typical values n=20
       Calculo: mediaMovil del precio de cierre, menos/más 2 standart deviations
       OJO: hace media simple... más interesante la ponderada exponencial
       
       Input Data: it needs a dataFrame containing a columns Close
       Returns; MA, BB_up, BB_down, BB_width
       
       Estado:  
       Origen Curso Quant     (J3...2020)
       """
       
    df = DF.copy()
    df["MA"] = df['Close'].rolling(n).mean()    #calculo media movil SIMPLE del valor de cierre
    # Bandas son la media más/menos 2 standart deviation
    df["BB_up"] = df["MA"] + 2*df['Close'].rolling(n).std(ddof=0) #ddof=0 is required since we want to take the standard deviation of the population and not sample
    df["BB_dn"] = df["MA"] - 2*df['Close'].rolling(n).std(ddof=0) #ddof=0 is required since we want to take the standard deviation of the population and not sample
    df["BB_width"] = df["BB_up"] - df["BB_dn"]
    df.dropna(inplace=True)

    if (J3_DEBUG__):
        BB_up_=df.columns.get_loc("BB_up")
        BB_dn_=df.columns.get_loc("BB_dn")
        colors=['violet', 'lightgreen', 'lime']
        df.iloc[-n:, [4,BB_up_,BB_dn_]].plot(title="BollingerBands LAST "+str(n),color=colors)   #Pintamos los ultimos 100 valores
        df.iloc[-220:, [4,BB_up_,BB_dn_]].plot(title="BollingerBands LAST 220",color=colors)   #Pintamo,s el rango especificado desde atrás
        df.iloc[:,     [4,BB_up_,BB_dn_]].plot(title="BollingerBands ",color=colors)


    return df

#################################################### BB


#################################################### RSI
def RSI(DF, n=14):
    """Function to calculate RSI
       typical values n=14
       Calculo: 
       
       Input Data: it needs a dataFrame containing a columns Close
       Returns; dataFrame plus RSI column
       
       Estado:  
       Origen Curso Quant     (J3...2020)
       """

    df = DF.copy()
    df['delta']=df['Adj Close'] - df['Adj Close'].shift(1)
    df['gain']=np.where(df['delta']>=0,df['delta'],0)
    df['loss']=np.where(df['delta']<0,abs(df['delta']),0)
    avg_gain = []
    avg_loss = []
    gain = df['gain'].tolist()      #convertir a una lista/array
    loss = df['loss'].tolist()
    for i in range(len(df)):
        if i < n:
            avg_gain.append(np.NaN)
            avg_loss.append(np.NaN)
        elif i == n:
            avg_gain.append(df['gain'].rolling(n).mean().tolist()[n])
            avg_loss.append(df['loss'].rolling(n).mean().tolist()[n])
        elif i > n:
            avg_gain.append(((n-1)*avg_gain[i-1] + gain[i])/n)
            avg_loss.append(((n-1)*avg_loss[i-1] + loss[i])/n)
    df['avg_gain']=np.array(avg_gain)
    df['avg_loss']=np.array(avg_loss)
    df['RS'] = df['avg_gain']/df['avg_loss']
    df['RSI'] = 100 - (100/(1+df['RS']))
    #Borramos datos intermedios
    del df["delta"]
    del df["gain"]
    del df["loss"]
    del df["avg_gain"]
    del df["avg_loss"]
    del df["RS"]
    
    #Ploteamos
    df['RSI'].plot()
    
    return df

#################################################### RSI



#################################################### Pretty Good Osscilator
def PGO(DF, n=20):
    """Function to calculate Pretty Good OScillator
       typical values n=14
       Calculo: El pretty good indicator es un calculo entre el precio de cierre, la media
       movil simple y el ATR
       
       Input Data: it needs a dataFrame containing a columns Close
       Returns; dataFrame plus PGO column
       
       Improvements: SMA hacerla de un periodo, no de dos que 'mancha todo'
       
       Estado:  
       Origen WEB     (J3...2021)
       """

    df = DF.copy()  
    #def MovingAverageSingle(DF,n=50,instrumento="_"):
    df=MovingAverageSingle(df,n,instrumento="_")
    df=df.join(ATR(df,n=20))
    
    df.dropna(inplace=True)
    
    df['PGO']=(df['Adj Close']-df['MA_'])/ df['ATR']
    
       
    #Ploteamos
    #df['RSI'].plot()
    if (J3_DEBUG__):
        print (df.head())
        colors=['cyan', 'lightgreen', 'green']
        dfAux=df[['PGO']]
        dfAux.plot(figsize=(16,8),title='PrettyGoodIndicator',color=colors)
    
    return df

#################################################### Pretty Good Osscilator





################################################## Tendencia 
def tendencia_estadistica(serie, periodo =4, parametro=1):
    """Calculamos la tendencia de una serie teorica basado en estadistica.

    Recibe un PD.SERIE y un parametro
    
    Parámetros:
        periodo= ventana de valores sobre la que filtramos, (deberia ser impar)
        a -- RFU

    Excepciones:
    ValueError -- Si (a == 0)
    
    Devuelve:
            NYD, no yet define :-)

    Mejoras:
            girar el data frame para trabajar con las fechas recientes primero
    """
  
    # 1.- Normalizamos la serie y calculamos la longuitud
    serie = (serie - serie.min())/(serie.max() - serie.min())  # yo creo que esto normaliza la serie
    df_len= len(serie)
    #2.- Creo un dataFrame para almacenar los calculos intermedios
    df = pd.DataFrame(columns=('serie', 'promedio', 'tendencia'))   #serie indice 0, promedio indice 1
        #Copiamos la serie en el dataframe.
    df['serie']=serie
    
    if (not(periodo%2)): periodo+=1  #Consiguo una ventana impara para el calculo del promedio de N valores
    
    # 3.- Calculo el Promedio de los 'periodo' valores = medida de los valores
    for x in range (0, (df_len-periodo+1)): 
        var=0
        for y in range(0,periodo): 
            var= var + serie[y+x]
        df.iat[x,1] = var/periodo       # Acceso a unico elemento df  [renglon, colunna]
    # 4.- Calculo la Tendencia desde los 'promedios' 
    for x in range (0, (df_len-periodo)): 
        df.iat[x+periodo,2]= (df.iat[x,1]+df.iat[x+1,1]) /2    
    
    for x in range(0, periodo):
        df.iat[x,2]=0
    
    #4.- Plotear
    df.plot.line()
    plt.show()
    
    #5.- Guardo el Excel
    salvarExcel(df, "tenden01")
    
    var=0
    return (df['tendencia'])
################################################## Tendencia FIN



################################################## MAX_min_Relativos
def MAX_min_Relativos(serie, dataFrameStock,tipo=1):
    """ Este metodo calcula los maximos y minimos de una SERIE de un Dataframe.
    
    Si cogemos una columna de un DataFrame tenemos una serie. ojo que la serie no es un DF, por ejemplo para plotear.
    Creamos una colunna nueva, con el valor de máximo en Pos y los mínimos en NEG 
    
    
    Comentarios J3: este metodo de calculo de max-min por filtrado movil de ventana de 6 valores no me convence.
    Mirar esta librería scipy.signal.find_peaks
    
    """
    
    
    #global df
    
    #a= end-start
    #print(a)
    #df_len=len(df.index)  #numero de filas del dataFrame
    #print(a)
    
    #serie = (serie - serie.min())/(serie.max() - serie.min())  # yo creo que esto normaliza la serie
    df_len= len(serie)
    
    ventana = 3  # Valores por la dereceh y por la izquierda que son < que el MAX
    dff = pd.DataFrame(columns=('serie','max_min', 'MAX_count', 'MIN_count', 'tres'))
    dff['serie']=serie
    #error df['max_min'][0]	=0
    
    MxMn=[]
    MxMnSerie=pd.Series(MxMn)
    
    #print(df['Volume'][2])      #Ojo que un dataframe es [columna][fila]

    if(tipo==1):
        #MxMnSerie = [i*0 for i in range(10+ventana)]  #inicializando los valores con un for !!!
        for x in range(0, (ventana+10)):
            MxMnSerie[x]=0
        for x in range((df_len-ventana), (df_len)):
            MxMnSerie[x]=0            

        for x in range ((10+ventana), (df_len-ventana)):   #ajustar el rango bien.
            
            # En una ventana de 5 valores apunto si el valor es el max
            if ( serie[x-ventana]   < serie[x]  and
                 serie[x-ventana+1] < serie[x]  and
                 serie[x-ventana+2] < serie[x]  and 
                 serie[x+ventana-1] < serie[x]  and
                 serie[x+ventana-2] < serie[x]  and
                 serie[x+ventana]   < serie[x]  ):
                    MxMnSerie[x]=serie[x]
                    MxMnSerie[x-1]= (0.1) # Marca que lo siguiente es un maximo
                
            elif ( serie[x-ventana]   > serie[x]  and
                 serie[x-ventana+2] > serie[x]  and
                 serie[x-ventana+1] > serie[x]  and
                 serie[x+ventana-1] > serie[x]  and
                 serie[x+ventana-2] > serie[x]  and
                 serie[x+ventana]   > serie[x]  ):
                    MxMnSerie[x]=serie[x]  # usar iloc
                    MxMnSerie[x-1]= (-0.1)  # Marca que lo siguiente es minimo
            else:
                MxMnSerie[x]=0
     
            
     ###################################################################
     #  Cuento los max decreciente sucesivos y min crecientes sucesivos
     
     # 1.-Inicializo referencia Max y Min primera que encontramos
    for x in range(0, df_len):
        if (MxMnSerie[x]==(-0.1)):
            minRef=(1)*MxMnSerie[x+1]
            break
    for x in range(0, df_len):
         if (MxMnSerie[x]==(0.1)):
            maxRef=MxMnSerie[x+1]
            break
        
#################################### 2.- Cuento max o min consecutivos  

    tendenciaLastValue       =1        
    tendenciaLastCount2 = 0
    tendenciaLastCount =0          #Flag marca ultima tendencia [1=pos // -1=neg]

    #for x in range(0,df_len):
    #    dff.iat[x,2] = 0            #columna MAX_count=2
    noProgresa =0
    noProgresa2= 0
    
    for x in range(0, df_len):
        #dff.iat[x,2]=tendenciaLastCount
        #Tendencia bulllish
        if ((MxMnSerie[x] == -0.1)):
            if((1)*MxMnSerie[x+1]>minRef):      #minimo Creciente
                tendenciaLastCount +=0.1
                dff.iat[x,2]=tendenciaLastCount
                minRef = (1)*MxMnSerie[x+1]
            elif((1)*MxMnSerie[x+1]<minRef):    #minimo No crece, marco
                noProgresa +=1
                
        if ((MxMnSerie[x] == 0.1)):
            if(MxMnSerie[x+1]>maxRef):      #minimo Creciente
                tendenciaLastCount +=0.1
                dff.iat[x,2]=tendenciaLastCount
                maxRef = MxMnSerie[x+1]
            elif(MxMnSerie[x+1]<maxRef):    #maximo No crece, marco
                noProgresa +=1
                
        if (noProgresa >3):
            tendenciaLastCount =0
            noProgresa =0
        
        #Tendencia bearish
        if ((MxMnSerie[x] == -0.1)):
            if((1)*MxMnSerie[x+1]<minRef):      #minimo Creciente
                tendenciaLastCount2 -=0.1
                dff.iat[x,2]=tendenciaLastCount2
                minRef = (1)*MxMnSerie[x+1]
            elif((1)*MxMnSerie[x+1]>minRef):    #minimo No crece, marco
                noProgresa2 +=1
                
        if ((MxMnSerie[x] == 0.1)):
            if(MxMnSerie[x+1]<minRef):      #minimo Creciente
                tendenciaLastCount2 -=0.1
                dff.iat[x,2]=tendenciaLastCount2
                maxRef = MxMnSerie[x+1]
            elif(MxMnSerie[x+1]>minRef):    #maximo No crece, marco
                noProgresa2 +=1
        
        if (noProgresa2 >3):
            tendenciaLastCount2 = 0
            noProgresa2 =0
           
    
    #dff.plot(y=dff['MAX_count'], kind='line') 
#################################### 2.- Cuento max o min consecutivos   
            
    var =9       
     #s = pd.Series([np.random.randint(1,100) for i in range(1,100)])
  
    
    # Para graficar tenemos que converti la serie en dataframe y el index hacerlo secuencial
    x=  MxMnSerie.index
    y=  MxMnSerie.values
    secuencial= np.arange(0,serie.size, 1)
    
    ser=        pd.Series(index=secuencial, data=MxMnSerie.values)
    serOriginal=pd.Series(index=secuencial, data=serie.values)
    
    df2=ser.to_frame()
    df2.reset_index(inplace=True)
    df2.columns = ['muestra','value']
    df2.plot(kind='scatter', x='muestra',y='value')  
    plt.show()
    
    df3=serOriginal.to_frame()
    df3.reset_index(inplace=True)
    df3.columns = ['muestra','value']
    df3.plot(x='muestra',y='value')  
    plt.show()
    
    
           
    ## new        
    #ploteando en Matplotlib
    plt.suptitle("Gráfica")        
    ax1=plt.subplot2grid((6,1),(0,0), rowspan=5, colspan=1)
    ax2=plt.subplot2grid((6,1),(5,0), rowspan=1, colspan=1, sharex=ax1)
    
    ax1.plot(df2.index, serOriginal,color='red')
    #ax1.plot(dff.index, dff['value'])
    ax1.scatter(df2.index, dff['MAX_count'], color='blue')
    ax1.scatter(df2.index, df2['value'], color='springgreen')
    #ax2.bar(df2.index, df2['value'])   #volumen
    ax2.bar(df2.index, dataFrameStock['Volume'])
    
    # *.- Salvar Execl
    salvarExcel(dff, "tenden01_1")
    salvarExcel(df2,'tenden01_2')
    
            
    #df[['Low','High']].plot()
    #df[['max_min']].plot()

################################################## MAX_min_Relativos FIN



################################################## SalvarExcel
def salvarExcel(df, nombreFichero):
   
    df.to_excel(nombreFichero+".xlsx", 
             index=True,
             sheet_name="data")
    var =9
################################################## SalvarExcel

################################################## LeerExcel
def leerExcel(nombreFichero):
    df = pd.DataFrame({'A' : []})  
    try:
        df=pd.read_excel(nombreFichero+'.xlsx', index_col=0)  
    except:
        print ('fichero no existe')
    return df        

################################################## LeerExcel


################################################## formula_cuadratica 
def formula_cuadratica(a, b, c):
    """Resuelve una ecuación cuadrática.

    Devuelve en una tupla las dos raíces que resuelven la
    ecuación cuadrática:
    
        ax^2 + bx + c = 0.

    Utiliza la fórmula general (también conocida
    coloquialmente como el "chicharronero").

    Parámetros:
    a -- coeficiente cuadrático (debe ser distinto de 0)
    b -- coeficiente lineal
    c -- término independiente

    Excepciones:
    ValueError -- Si (a == 0)
    
    """
    if a == 0:
        raise ValueError(
            'Coeficiente cuadrático no debe ser 0.')
    from cmath import sqrt
    discriminante = b ** 2 - 4 * a * c
    x1 = (-b + sqrt(discriminante)) / (2 * a)
    x2 = (-b - sqrt(discriminante)) / (2 * a)
    return (x1, x2)
################################################## formula_cuadratica FIN
#formula_cuadratica(2, 3, 4)


################################################## MAX_min_Relativos_v3
def tendecia_v1(df, peaks, valleys):
    """ Vamos a intentar medir la fuerza de la tendencia de maximos decrecientes
    tengo la serie de valores y las posiciones de maximos y minimos.
    SIN ACABAR!!! por cambio de estrategia
   
    Comentarios J3: 
      
    Return:
       
    
    """
    
    df['pendienteMAIN']=100   #Añado una colunma al dataframe para heredarla en el array
    serArray = df.to_numpy()  
    
    # 1.-Si los maximos son decrecientes la tendencia es negativa
    marca=0
    for i in range (1,len(peaks)):
        # primero: maximos decrecientes
        if(serArray[peaks[i-1]][0]>serArray[peaks[i]][0]):   #mx van bajando
            serArray[peaks[i]][4]=0
            continue
        else:   #se ha roto la tendencia bajista por un max creciente respecto del anterior
                #Calculo la fuerza del tramo que se cierra (mejorar con regresionLineal)
            print(peaks[i], serArray[peaks[i]][0])
            #numero de sesiones bajando
            print(serArray[0][0])
            print(peaks[i])
            marca=i  #apunto donde se rompe la tendencia
            serArray[peaks[i]][3]=peaks[i]    #posicion en la serie
            serArray[peaks[i]][4]=1    # mx subiendo
            
        # segundo: minimos crecientes
        """
        if(serArray[valleys[i]][0]<serArray[valleys[i+1]][0]):   #mx van bajando
            serArray[0][3]=1
            continue
        else:   #se ha roto la tendencia bajista por un max creciente respecto del anterior
                #Calculo la pendiente del tramo que se cierra (mejorar con regresionLineal)
            print(peaks[i], serArray[peaks[i]][0])         
        """    
         
    
    
    # 2.- Si los minimos son creciente la tendencia es positiva



      
    
    #Devuelve el dataframe con la serie y la pendiente en cada punto.Más dos arrays de Picos y Valley.
    return ()
    
################################################## tendecia_v1 FIN





################################################## MAX_min_Relativos_v3
def MAX_min_Relativos_v3(serie, distancia = 2):
    """ Este metodo calcula los maximos y minimos de una SERIE de un Dataframe.
    Calcula los min/max relativos con scipy.signal argrelextrema y una ventana de x valores
    La funcion Scipy find peaks no va bien pues no compara con los vecinos, mejor la greater.
    
    Calculamos la pendiente entre las lienas que delimitan los maximos y/o minimos, sin regresion

    Comentarios J3: 
        OJO que este calculo de la tendencia es un indicador retrasado, va por detras del precio,
        cuidado sobre todo en los ultimos valores.
    Return:
        Devuelve la serie + pendiente desde el max/min anterior hasta el punto atual, ultima pendiente desde ultimo
        max/min tomando los puntos restantes.
        Array de posicion en la serie de picos y valles.
    
    """
      
    # 1.-Calculo los max y minimos relativos. Distancia entre max min
    """
    serieInv = serie.mul(-1) 
    #scipy.signal.find_peaks(x, height=None, threshold=None, distance=None, prominence=None, width=None, wlen=None, rel_height=0.5, plateau_size=None)
    peaks,_=find_peaks(serie, distance=distancia)
    valley,_=find_peaks(serieInv, distance=distancia)
    """
    # La funcion Argrelextrema busca los maximos relativos denttro de un rango de distancia 'orden'
    # Devuelve una tupla de arrays
    #serie['marcas_Mx_Mn']=1   #Añado una colunma al dataframe para heredarla en el array
    serArray = serie.to_numpy()   
    peaks=argrelextrema(serArray, np.greater, order=distancia)
    valley=argrelextrema(serArray, np.less, order=distancia)
    
    """  Ejemplo de la persona de telegram. Python ++
    f[pair]['min'] = df[pair].iloc[argrelextrema(price.values, np.less_equal, order = 100)[-1]]
    df[pair]['max'] = df[pair].iloc[argrelextrema(price.values, np.greater_equal, order = 100)[-1]]
    """

    # 1.1.- CALCULANDO ....
    dff = pd.DataFrame(columns=('serie','pendiente_MX','pendiente_MN','marcasMxMn'))   #index=[1,2,3],
    dj =pd.DataFrame()
    
    for i in range(0, len(serie)):  
        dff.loc[i,'serie']=serie[i]     #copio la serie porque al ser una serie temporal tiempo index time y no un secuencial   
    
    #Grabo los picos y valles en el array
    for i in range(0,len(peaks[0])):
        dff.loc[peaks[0][i],'marcasMxMn']=2
    for i in range(0,len(valley[0])):
        dff.loc[valley[0][i],'marcasMxMn']=1
        
    
    dff.fillna(0, inplace=True)
    XX = np.array(range(len(dff))) 
  
    # *.- Ploteamos   
    if (J3_DEBUG__):
        fig2=plt.figure()
        secuencial= np.arange(0,serie.size, 1)
        # La serie ce cierres
        plt.plot(secuencial, serie, '.', label='serie')
        plt.plot(secuencial, serie,'c')
        # Picos y Valles
        plt.plot(peaks[0],serie[peaks[0]],'red', label='peaks')
        plt.plot(valley[0],serie[valley[0]],'green', label='valley')
        #plt.plot(peaks[peaksMax],a[peaksMax],'v') 
        #plt.plot(peaks[peaksMin],a[peaksMin],'v',color='yellow') 
        plt.legend()    
        plt.show()
    
    # 2.- Calculo la pendiente por arriba de maximos y por abajo de minimos
    #Peaks--------------------
    j=1
    pendiente=0
    
    for i in range(1, len(serie)-1):
        #Pendiente = (incremento_de_Y / incremento_de_X)
        #a=peaks[0][j]
        b=len(peaks[0])
        c=j
        d=i
        if( j<=(len(peaks[0])-1)):
            if ((i)==peaks[0][j]):
                incremento_de_X = peaks[0][j] - peaks[0][j-1]  
                incremento_de_Y =  serie[peaks[0][j]] - serie[peaks[0][j-1]] 
                pendiente = incremento_de_Y / incremento_de_X
                j+=1
        dff.loc[i,'pendiente_MX']=pendiente
    
    #Valleys------------------------
    j=1
    pendiente=0
    
    for i in range(1, len(serie)-1):
        #Pendiente = (incremento_de_Y / incremento_de_X)
        #a=peaks[0][j]
        b=len(peaks[0])
        c=j
        d=i
        if( j<=(len(valley[0])-1)):
            if ((i)==valley[0][j]):
                incremento_de_X = valley[0][j] - valley[0][j-1]  
                incremento_de_Y =  serie[valley[0][j]] - serie[valley[0][j-1]] 
                pendiente = incremento_de_Y / incremento_de_X
                j+=1
        dff.loc[i,'pendiente_MN']=pendiente
        
        
    # Ultimo tramo de la recta (no tengo referecnias, regresion lineal¿?)
    
    """tengo que trabajar mejor el final de la serie que es lo importante para divergencias
    creo que desde el ultimo punto pico/valley calcular regresion
    """
    
    ###########################################################################
    # Calculo la tendencia de la cola de datos desde el ultimo max/min.   
    z = serie[-1]               #ultimo valor de la serie
    p = serie[peaks[0][-1]]     #ultimo valor de la serie de maximos
    v = serie[valley[0][-1]]    #ultimo valor de la serie de maximos
    
    if(peaks[0][-1] > valley[0][-1]):    #ultimo valor es un pico
        x=peaks[0][-1]
        cola = serArray[x:]
    else:
        x=valley[0][-1]
        cola = serArray[x:]
        
    print(x)
    print('cola =',cola)
    """
    incre_Y=cola[len(cola)-1]-cola[0]
    incre_X=len(cola)-1
    pendiente = incre_Y / incre_X
    print (pendiente)
    for i in range(x, len(dff)):
        dff.loc[i,'pendiente_MN']=pendiente
        dff.loc[i,'pendiente_MX']=pendiente 
    """
    
    # CAlculo la pendiente de la cola de datos con regresion lineal
    pendiente, independiente = slopeJ3(cola)
    for i in range(x, len(dff)):
        dff.loc[i,'pendiente_MN']=pendiente
        dff.loc[i,'pendiente_MX']=pendiente     
    
    
    """ 
    ### ESPECIAL para el ultimo tramo de la serie desde el ultimo MAX/min  ¿hacer una regresion para determinar ultimas tendencias?
    ## Especial, trato el último dato de la serie que siempre se queda fuera de el array [peaks], por tener una ventana de 4
    z = serie[-1]           #ultimo valor de la serie
    y = serie[peaks[-1]]    #ultimo valor de la serie de maximos
    if z>=y:
        peaks=np.append(peaks, len(serie)-1)
        #peaks[1+len(peaks)] = z
    else:
        valley=np.append(valley, len(serie)-1)
    """
        
    
    #salvarExcel(dff, 'pendiente_5enero') 
        
    # *.- Ploteamos  
    if (J3_DEBUG__):
        fig2=plt.figure()
        secuencial= np.arange(0,dff['serie'].size, 1)
        # La serie ce cierres
        plt.plot(secuencial, dff['serie'], '.', label='serie')
        plt.plot(secuencial, dff['serie'],'c')
        plt.plot(secuencial, 20+5*dff['pendiente_MX'],'tomato', label='pendiente_MX')
        plt.plot(secuencial, 20+5*dff['pendiente_MN'],'palegreen', label='pendiente_MN')
        # Picos y Valles
        plt.plot(peaks[0],serie[peaks[0]],'red', label='peaks')
        plt.plot(valley[0],serie[valley[0]],'green', label='valley')
        #plt.plot(peaks[peaksMax],a[peaksMax],'v') 
        #plt.plot(peaks[peaksMin],a[peaksMin],'v',color='yellow') 
        plt.legend()    
        plt.show()         
    
    #Devuelve el dataframe con la serie y la pendiente en cada punto.Más dos arrays de Picos y Valley.
    return (dff, peaks[0], valley[0])
    
################################################## MAX_min_Relativos_v3 FIN




################################################## MAX_min_Relativos_v2
def MAX_min_Relativos_v2(serie, distancia = 4):
    """ Este metodo calcula los maximos y minimos de una SERIE de un Dataframe.
    Calcula los min/max relativos con scipy.signal y una ventana de 5 valores
    Luego con la curva de minimos hacemos una regresion lineal para saber la pendiente
    devolvemos la pendiente y la precision con la que se ajusta (para saber la bondad)

    Comentarios J3: La funcion find_peak puede dar mucho mas juego con sus parametros. Estudiarla!!
    
    """
      
    # 1.-Calculo los max y minimos relativos. Distancia entre max min
    serieInv = serie.mul(-1) 
    #scipy.signal.find_peaks(x, height=None, threshold=None, distance=None, prominence=None, width=None, wlen=None, rel_height=0.5, plateau_size=None)
    peaks,_=find_peaks(serie, distance=distancia)
    valley,_=find_peaks(serieInv, distance=distancia)
    a=serie[peaks]   
    peaksMax,_=find_peaks(a)
    aInv=a.mul(-1)
    peaksMin,_=find_peaks(aInv)
    
    # 1.1.- CALCULANDO MOVING AVERAGEs
    dff = pd.DataFrame() 
    dff['serie']=serie   #convierto serie en dataFrame
    dff['10ma']=dff['serie'].rolling(window=10).mean() 
    dff['20ma']=dff['serie'].rolling(window=20).mean()  
    dff['50ma']=dff['serie'].rolling(window=50).mean()   
    #dff.dropna(inplace=True)            #quitamos las filas/rows que tengas algun NaN... mejor sustituir por ceros
    dff.fillna(0, inplace=True)
    XX = np.array(range(len(dff))) 
  
    # *.- Ploteamos    
    fig2=plt.figure()
    secuencial= np.arange(0,serie.size, 1)
    # La serie ce cierres
    plt.plot(secuencial, serie, '.', label='serie')
    plt.plot(secuencial, serie,'c')
    # Picos y Valles
    plt.plot(peaks,serie[peaks],'red', label='peaks')
    plt.plot(valley,serie[valley],'green', label='valley')
    plt.plot(peaks[peaksMax],a[peaksMax],'v') 
    plt.plot(peaks[peaksMin],a[peaksMin],'v',color='yellow') 
    # Las distintas mediasMoviles
    plt.plot(XX, dff['10ma'], 'brown', label='10ma')
    plt.plot(XX, dff['20ma'], 'orange', label='20ma')
    plt.plot(XX, dff['50ma'], 'yellow', label='50ma')
    #plt.plot(peaks,serie[peaks], 'x','green')
    #plt.plot(valley,serie[valley], 'v','red')    
    plt.legend()    
    plt.show()
    
    # 2.- Regresion lineal del periodo dado para dibujar la linea de tendencia  (Peaks and Valleys)
    #3.- Ploteamos
    X = np.array(range(len(valley))) 
    Xp = np.array(range(len(peaks)))
    fig, ax = plt.subplots()  # Create a figure containing a single axes.
    ax.plot(peaks,serie[peaks], 'lightcoral',label="picos") 

    ax.plot(valley,serie[valley], 'springgreen',label="valles") 
    ax.plot(XX, dff['50ma'], 'gold', label='50ma')
 
    #serArray = ser.to_numpy()                  #creamos un array y lo llena de num consecutivos de la serie
    regr_p  = linear_model.LinearRegression()
    regr_v  = linear_model.LinearRegression()
    regr_ma = linear_model.LinearRegression()
    # 3.- Train the model using the training sets
    #       X1=X.reshape(-1,1)
    #       Xp1=Xp.reshape(-1,1)
    X1=valley.reshape(-1,1)
    Xp1=peaks.reshape(-1,1)
    XX1=XX.reshape(-1,1)
    regr_v.fit(X1, serie[valley])
    regr_p.fit(Xp1, serie[peaks])
    regr_ma.fit(XX1, dff['50ma'])
    
    #6.- Make predictions using the data set. Para dibujar la linea calculada por la regresion
    serLinearRegresion_v = regr_v.predict(X1)
    serLinearRegresion_p = regr_p.predict(Xp1)
    serLinearRegresion_ma = regr_ma.predict(XX1)
    #7.- Pintamos la linea calculada con la regresión
    ax.plot(valley,serLinearRegresion_v,'limegreen',label='Tendencia de Valles') 
    ax.plot(peaks,serLinearRegresion_p,'red',label='Tendencia de Picos')
    ax.plot(XX,serLinearRegresion_ma,'yellow',label='Tendencia de Moving Average-Media Móvil')
    ax.legend()
    ax.set_title("Línea de valores y Regresión lineal")
    
    
    # 8.- Calculo de coeficientes y los guardo en un DataFrame
    
    #  Creo un dataFrame con Rango, Pendiente y MS_Error y Precicision.   
    Tendencia_ = pd.DataFrame(index=[1,2,3],columns=['tipo','pendiente', 'meanSquareError_0', 'precision_1']) #empty dataframe which will be filled with

    
    #Valles
    pendiente= regr_v.coef_
    X2=serLinearRegresion_v.reshape(-1,1)               #Reshape para cambiar filas por columnas
    precision = regr_v.score(X2,serie[valley])          #The best possible score is 1.0 
    MS_error = mean_squared_error(X2,serie[valley])     #Best possible score is 0.0

    Tendencia_.loc[1,'tipo']= 'valley'
    Tendencia_.loc[1,'pendiente']=pendiente
    Tendencia_.loc[1,'meanSquareError_0']=MS_error
    Tendencia_.loc[1,'precision_1']= precision
    
    #Picos
    pendiente= regr_p.coef_
    Xp2=serLinearRegresion_p.reshape(-1,1)               #Reshape para cambiar filas por columnas
    precision = regr_v.score(Xp2,serie[peaks])          #The best possible score is 1.0 
    MS_error = mean_squared_error(Xp2,serie[peaks])     #Best possible score is 0.0

    Tendencia_.loc[2,'tipo']= 'peaks'
    Tendencia_.loc[2,'pendiente']=pendiente
    Tendencia_.loc[2,'meanSquareError_0']=MS_error
    Tendencia_.loc[2,'precision_1']= precision   
    
    #MovingAvarege
    pendiente= regr_ma.coef_
    Xma2=serLinearRegresion_ma.reshape(-1,1)               #Reshape para cambiar filas por columnas
    precision = regr_ma.score(Xma2,dff['50ma'])          #The best possible score is 1.0 
    MS_error = mean_squared_error(Xma2,dff['50ma'])     #Best possible score is 0.0

    Tendencia_.loc[3,'tipo']= 'MovingAverage'
    Tendencia_.loc[3,'pendiente']=pendiente
    Tendencia_.loc[3,'meanSquareError_0']=MS_error
    Tendencia_.loc[3,'precision_1']= precision      
    
    print('Pendiente', pendiente)
    print('MeanSquareError {best=0}  ', MS_error)
    print('Precision       {best=1}  ', precision)
    
    return (Tendencia_)
    
################################################## MAX_min_Relativos_v2 FIN



"""
#################################### 2.- Cuento max o min consecutivos  
Este algoritmo para calcular tendencia no funciona.
Probar a sumar max y min crecientes a ver que pasa
    tendenciaLastValue       =1        
    tendenciaLastCount       =1          #Flag marca ultima tendencia [1=pos // -1=neg]

    for x in range(0,df_len):
        dff.iat[x,2] = 0            #columna MAX_count=2

    
    for x in range(0, df_len):
        dff.iat[x,2]=tendenciaLastCount
        #Tendencia bulllish
        if ((MxMnSerie[x] == -0.1)and(tendenciaLastCount > 0)):
            if(MxMnSerie[x+1]>minRef):
                tendenciaLastCount +=1
                dff.iat[x,2]=tendenciaLastCount
                minRef = MxMnSerie[x+1]
            else:
                tendenciaLastCount = -1  # se rompe la tendencia, un minimo menor hace cambiar
                dff.iat[x,2]=tendenciaLastCount
                minRef = MxMnSerie[x+1]
        #Tendencia bearish
        if ((MxMnSerie[x] == 0.1)and(tendenciaLastCount < 0)):
            if(MxMnSerie[x+1]<maxRef):
                tendenciaLastCount -=1
                dff.iat[x,2]=tendenciaLastCount
                maxRef = MxMnSerie[x+1]
            else:
                tendenciaLastCount = 1  # se rompe la tendencia, un minimo menor hace cambiar
                dff.iat[x,2]=tendenciaLastCount
                maxRef = MxMnSerie[x+1] 
    
#################################### 2.- Cuento max o min consecutivos   




"""


"""
CAJA de HERRRAMIENTAS
El dia 1 el el 1-1-1.
def convert_date_to_excel_ordinal(day, month, year):
       offset = 693594
       current = date(year,month,day)
       n = current.toordinal()
       return (n - offset)


"""