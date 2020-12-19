# -*- coding: utf-8 -*-
"""
Created on Sun Sep 13 11:28:48 2020

@author: INNOVACION
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import statsmodels.api as sm   #se usa en el Slope del curso, quitar

from sklearn import linear_model
from sklearn.metrics import mean_squared_error, r2_score
from scipy.signal import find_peaks



#################################################### slopeJ3()
def slopeJ3(ser,n=5):
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

    #2.- Creo un array con la variable independiente 'X'
    X = np.array(range(len(ser)))  
    serArray = ser.to_numpy()                  #creamos un array y lo llena de num consecutivos de la serie
    #3.- Ploteamos
    fig, ax = plt.subplots()  # Create a figure containing a single axes.
    ax.plot(X,serArray)     
    #4.- Create linear regression object
    regr = linear_model.LinearRegression()
    #5.- Train the model using the training sets
    X1=X.reshape(-1,1)
    regr.fit(X1, serArray)
    #6.- Make predictions using the data set. Para dibujar la linea calculada por la regresion
    serLinearRegresion = regr.predict(X1)
    #7.- Pintamos la linea
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
def MovingAverage(DF,long_=200,short_=50):
    """Function to calculate 
    typical values 
    
    Input Data: it needs a dataFrame containing a column [Adj_Close]
    Returns; same dataFrame with a new column [MACD] and new column[Signal] and [Histo]
    
    Estado: programada y probada. 
    Origen      (J3...2020)
    """

    df = DF.copy()
    df.Close.plot()     #ploatemos basicamente
    
    #MA = pd.Series( pd.Series.rolling(df['Adj Close'],n).mean() ,name='MA_'+str(n))
    ma_L = pd.Series( pd.Series.rolling(df['Adj Close'],long_).mean(), name='MA_'+ str(long_))
    ma_S = pd.Series( pd.Series.rolling(df['Adj Close'],short_).mean(), name='MA_'+ str(short_))
    df=df.join(ma_L)
    df=df.join(ma_S)
    
    #visualizar
    print (df.head())
    dfAux=df[['Adj Close', 'MA_200', 'MA_50']]
    dfAux.plot(figsize=(16,8),title='Moving Average')
  
    return df

#################################################### Media Movil Simple



#################################################### Media Movil Exponencial EMA
def ExponentialMovingAverage(DF,long_=200,short_=30):
    """Function to calculate 
    typical values 
    
    Input Data: it needs a dataFrame containing a column [Adj_Close]
    Returns; same dataFrame with a new column [MACD] and new column[Signal] and [Histo]
    
    Estado: programada y probada. 
    Origen      (J3...2020)
    """

    df = DF.copy()
    df.Close.plot()     #ploatemos basicamente
    
    #MA = pd.Series( pd.Series.rolling(df['Adj Close'],n).mean() ,name='MA_'+str(n))
    ema_L = pd.Series( pd.Series.ewm(df['Adj Close'],span=long_, min_periods=long_-1,adjust=False).mean(), name='EMA_'+ str(long_))
    ema_S = pd.Series( pd.Series.ewm(df['Adj Close'],span=short_, min_periods=short_ -1,adjust=False).mean(), name='EMA_'+ str(short_ ))
    #    ema_S = pd.Series( pd.Series.rolling(df['Adj Close'],short_).mean(), name='MA_'+ str(short_))
    df=df.join(ema_L)   #añade una columna al dataFrame
    df=df.join(ema_S)
    
    #visualizar
    print (df.head())
    dfAux=df[['Adj Close', 'EMA_200', 'EMA_30']]
    dfAux.plot(figsize=(16,8),title='Exponential Moving Average')
  
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
    df['H-PC']=abs(df['High']-df['Adj Close'].shift(1))     # Shift nos mueve a la fila anterior (presentHigh menos previousClose)
    df['L-PC']=abs(df['Low']-df['Adj Close'].shift(1))      # Today´s Low minus previousClose
    df['TR']=df[['H-L','H-PC','L-PC']].max(axis=1,skipna=False)  # Obtiene el Max de las tres columnas
    df['ATR'] = df['TR'].rolling(n).mean()
    #df['ATR'] = df['TR'].ewm(span=n,adjust=False,min_periods=n).mean()  #En caso de querer hacer media exponencial
    df2 = df.drop(['H-L','H-PC','L-PC'],axis=1)     #Quitamos columnas intermedias
    df2.dropna(inplace=True)                        #Quita las filas que que el ATR en nan     
    
    df2.iloc[:, [6,7]].plot()   #Pintamos 
    return df2['ATR']
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
    df["MA"] = df['Adj Close'].rolling(n).mean()    #calculo media movil SIMPLE del valor de cierre
    # Bandas son la media más/menos 2 standart deviation
    df["BB_up"] = df["MA"] + 2*df['Adj Close'].rolling(n).std(ddof=0) #ddof=0 is required since we want to take the standard deviation of the population and not sample
    df["BB_dn"] = df["MA"] - 2*df['Adj Close'].rolling(n).std(ddof=0) #ddof=0 is required since we want to take the standard deviation of the population and not sample
    df["BB_width"] = df["BB_up"] - df["BB_dn"]
    df.dropna(inplace=True)

    df.iloc[-100:, [6,7,8]].plot(title="BollingerBands")   #Pintamos los ultimos 100 valores
    df.iloc[-500:-100, [6,7,8]].plot(title="BollingerBands")   #Pintamos el rango especificado desde atrás


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
   
    df.to_excel(nombreFichero+".xls", 
             index=True,
             sheet_name="data")
    var =9
################################################## SalvarExcel


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



################################################## MAX_min_Relativos_v2
def MAX_min_Relativos_v2(serie, distancia = 5):
    """ Este metodo calcula los maximos y minimos de una SERIE de un Dataframe.
    Calcula los min/max relativos con scipy.signal y una ventana de 5 valores
    luego con la curva de minimos hacemos una regresion lineal para saber la pendiente
    devolvemos la pendiente y la precision con la que se ajusta (para saber la bondad)
    
    Si 

    Comentarios J3: La funcion find_peak puede dar mucho mas juego con sus parametros. Estudiarla!!
    
    """
      
    # 1.-Calculo los max y minimos relativos
    serieInv = serie.mul(-1) 
    #scipy.signal.find_peaks(x, height=None, threshold=None, distance=None, prominence=None, width=None, wlen=None, rel_height=0.5, plateau_size=None)
    peaks,_=find_peaks(serie, distance=distancia)
    valley,_=find_peaks(serieInv, distance=distancia)
     
    
    fig2=plt.figure()
    secuencial= np.arange(0,serie.size, 1)
    plt.plot(secuencial, serie, '.')
    
    plt.plot(peaks,serie[peaks],'green')
    plt.plot(valley,serie[valley],'red')
    #plt.plot(peaks,serie[peaks], 'x','green')
    #plt.plot(valley,serie[valley], 'v','red')
    plt.show()
    
    # 2.- Regresion lineal del periodo para dibujar la linea de tendencia
    #3.- Ploteamos
    X = np.array(range(len(valley))) 
    fig, ax = plt.subplots()  # Create a figure containing a single axes.
    #ax.plot(X,serie[peaks]) 
    ax.plot(X,serie[valley]) 
 
    #serArray = ser.to_numpy()                  #creamos un array y lo llena de num consecutivos de la serie
    regr_p = linear_model.LinearRegression()
    regr_v = linear_model.LinearRegression()
    # 3.- Train the model using the training sets
    X1=X.reshape(-1,1)
    regr_v.fit(X1, serie[valley])
    #6.- Make predictions using the data set. Para dibujar la linea calculada por la regresion
    serLinearRegresion_v = regr_v.predict(X1)
    #7.- Pintamos la linea
    ax.plot(X,serLinearRegresion_v) 
    ax.set_title("línea de Valores y Regresion Lineal")
    
    
    # 8.- Calculo de coeficientes
    pendiente= regr_v.coef_
    X2=serLinearRegresion_v.reshape(-1,1)               #Reshape para cambiar filas por columnas
    MS_error = mean_squared_error(X2,serie[valley])     #Best possible score is 0.0
    precision = regr_v.score(X2,serie[valley])          #The best possible score is 1.0 
    print('Pendiente', pendiente)
    print('MeanSquareError {best=0}  ', MS_error)
    print('Precision       {best=1}  ', precision)
    
    #  Creo un dataFrame con Rango, Pendiente y MS_Error y Precicision.   
    Tendencia_ = pd.DataFrame(index=[1,2,3],columns=['rango','pendiente', 'meanSquareError', 'precicision']) #empty dataframe which will be filled with
    
    Tendencia_.loc[1,'pendiente']=pendiente  #♥Grabar en dataframe????
    
    return ()
    
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