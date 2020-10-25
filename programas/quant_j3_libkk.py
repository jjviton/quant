# -*- coding: utf-8 -*-
"""
Created on Sun Sep 13 11:28:48 2020

@author: INNOVACION
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np



################################################## Tendencia 
def tendencia_estadistica(serie, periodo =5, parametro=1):
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
    df = pd.DataFrame(columns=('serie', 'promedio', 'tendencia'))
        #Copiamos la serie en el dataframe.
    df['serie']=serie
    
    if (not(periodo%2)): periodo+=1  #Consiguo una ventana impara para el calculo del promedio de N valores
    
    # 3.- Calculo el Promedio de los 'periodo' valores = medida de los valores
    for x in range (0, (df_len-periodo+1)): 
        var=0
        for y in range(0,periodo): 
            var= var + serie[y+x]
        df.iloc[x]['promedio'] = var/periodo
    # 4.- Calculo la Tendencia desde los 'promedios' 
    for x in range (0, (df_len-periodo)): 
        df.iloc[x+periodo]['tendencia']= (df.iloc[x]['promedio']+df.iloc[x+1]['promedio']) /2    
    
    for x in range(0, periodo):
        df.iloc[x]['tendencia']=0
    
    #4.- Plotear
    df.plot.line()
    plt.show()
    
    var=0
    return (df['tendencia'])
################################################## Tendencia FIN



################################################## MAX_min_Relativos
def MAX_min_Relativos(serie, tipo=1):
    """ Este metodo calcula los maximos y minimos de una SERIE de un Dataframe.
    
    Si cogemos una columna de un DataFrame tenemos una serie. ojo que la serie no eun DF, por ejemplo para plotear.
    Creamos una colunna nueva, con el valor de máximo en Pos y los mínimos en NEG 
    
    
    Comentarios J3: este metodo de calculo de max-min por filtrado movil de ventana de 6 valores no me convence.
    Mirar esta librería scipy.signal.find_peaks
    
    """
    
    
    #global df
    
    #a= end-start
    #print(a)
    #df_len=len(df.index)  #numero de filas del dataFrame
    #print(a)
    
    serie = (serie - serie.min())/(serie.max() - serie.min())  # yo creo que esto normaliza la serie
    df_len= len(serie)
    
    ventana = 3  # Valores por la dereceh y por la izquierda que son < que el MAX
    dff = pd.DataFrame(columns=('max_min', 'MAX_count', 'MIN_count', 'tres'))
    #error df['max_min'][0]	=0
    
    MxMn=[]
    MxMnSerie=pd.Series(MxMn)
    
    #print(df['Volume'][2])      #Ojo que un dataframe es [columna][fila]

    if(tipo==1):
        #MxMnSerie = [i*0 for i in range(10+ventana)]  #inicializando los valores con un for !!!
        for x in range(0, (ventana+10)):
            MxMnSerie[x]=0
        for x in range((df_len-2), (df_len)):
            MxMnSerie[x]=0            
        for x in range ((10+ventana), (df_len-2)):   #ajustar el rango bien.
            #var01=serie[x-ventana]
            #df['max_min'][x]=99
                  #me aseguro que se rellenen todos los valores
             
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
                    MxMnSerie[x]=(-1) * serie[x]  # usar iloc
                    MxMnSerie[x-1]= (-0.1)  # Marca que lo siguiente es minimo
            else:
                MxMnSerie[x]=0
     
            
     ###################################################################
     #  Cuento los max decreciente sucesivos y min crecientes sucesivos
     
     # 1.-Inicializo referencia Max y Min primera que encontramos
    for x in range(0, df_len):
        if (MxMnSerie[x]==(-0.1)):
            minRef=MxMnSerie[x+1]
            #break
    for x in range(0, df_len):
         if (MxMnSerie[x]==(0.1)):
            maxRef=MxMnSerie[x+1]
            #break
        
     # 2.- Cuento max o min consecutivos  
    tendenciaLastValue  =1        
    tendenciaLast       =1          #Flag marca ultima tendencia [1=pos // -1=neg]

    for x in range(0,df_len):
        dff.iloc[x]["MAX_count"] = 0

    """
    for x in range(0, df_len):
        #dff.iloc[x]['MAX_count']=tendenciaLast
        if ((MxMnSerie[x] == 0.1)and(tendenciaLast > 0)):
            if(MxMnSerie[x+1]>maxRef):
                tendenciaLast +=1
                dff.iloc[x]['MAX_count']=tendenciaLast
                maxRef = MxMnSerie
    """
            
    var =9       
     #s = pd.Series([np.random.randint(1,100) for i in range(1,100)])
  
    
    # Para graficar tenemos que converti la serie en dataframe y el index hacerlo secuencial
    x=  MxMnSerie.index
    y=  MxMnSerie.values
    secuencial= np.arange(0,serie.size, 1)
    
    ser=pd.Series(index=secuencial, data=MxMnSerie.values)
    serOriginal=pd.Series(index=secuencial, data=serie.values)
    
    dff=ser.to_frame()
    dff.reset_index(inplace=True)
    dff.columns = ['muestra','value']
    dff.plot(kind='scatter', x='muestra',y='value')  
    plt.show()
    
    dfff=serOriginal.to_frame()
    dfff.reset_index(inplace=True)
    dfff.columns = ['muestra','value']
    dfff.plot(x='muestra',y='value')  
    plt.show()
    
    
           
    ## new        
    #ploteando en Matplotlib
    plt.suptitle("Gráfica")        
    ax1=plt.subplot2grid((6,1),(0,0), rowspan=5, colspan=1)
    ax2=plt.subplot2grid((6,1),(5,0), rowspan=1, colspan=1, sharex=ax1)
    
    ax1.plot(dff.index, serOriginal,color='red')
    #ax1.plot(dff.index, dff['value'])
    #ax1.plot(dff.index, dff['value'], color='springgreen')
    ax1.scatter(dff.index, dff['value'], color='springgreen')
    ax2.bar(dff.index, dff['value'])   #volumen
    
    
    
            
    #df[['Low','High']].plot()
    #df[['max_min']].plot()

################################################## MAX_min_Relativos FIN




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