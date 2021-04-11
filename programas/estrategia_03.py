"""
ESTRATEGIA DE INVERSION AUTOMATICA COMPLETA BASADA EN RSI
******************************************************************************
******************************************************************************
    fuente:https://www.youtube.com/watch?v=4dVB_g5YeSE

Started on 13/12/2020

Objetivo: Despues de realizar varios cursos de inversion algoritmica y de estudiar un poquito, la mejor 
manera de empezar es programar una estrategia completa y tratar todas las dificultades que puedan salir.
Animo....

@author: J3Viton

"""



################################ IMPORTAMOS MODULOS A UTILIZAR.
import pandas as pd
import numpy as np
import itertools
#import seaborn as sns
import datetime as dt
import pandas_datareader as web

import matplotlib.pyplot as plt
plt.rcParams['figure.figsize'] = 18, 8
#plt.style.use('ggplot')
plt.style.use("bmh")   


import quandl  #Para recoger datos
import ta as ta  #Biblioteca generica


from quant_j3_lib import * 
from DataSet_J import *
from telegram_bot import *

variable_1 = 32
variable_2 = 23
"""
Variables Scope:
    La variable se crea en la asignacion.
    Las globlaes se declaran primero en la funcion local y luego, en otra linea se asignan.
    Las variables tienen el scope más pequeño que el interprete pueda acoger
    El prefijo global, nos lleva la variable global
"""



#/***************************Funciones con tareas parciales */



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



#################################################### Clases

class Person:

    """Estrategia basica, v0
    
    Trataremos de implementar la primera estrategia usando Analisis técnico
    
        ax^2 + bx + c = 0.
    
    Utiliza la fórmula general (también conocida
    coloquialmente como el "chicharronero").
    
       
    """    
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def myfunc(self):
        'docuemntacion sencilla...'
        print("Hello my name is " + self.name)

#################################################### Clases FIN


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
        'docuemntacion sencilla...'
        print("Hello my parametro is " + self.para_02)
        
    def testing_123(self):
        slopeJ3_2points(1,3,2,4)
    def debugging_(self):
        return (J3_DEBUG__)

#################################################### Clases FIN



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
    
    """
    TESTEO DE FUNCIONES ............................................................
    """
    #Llamadas a la Clase
    ##### objetoTEST = TestingClass (3,2)
    #objetoTEST.testing_123()
    
    
    # 1.- RECOGEMOS DATOS DE UNA FUENTE FIABLE (QUANDL/YFINANCES)
    #quandl.ApiConfig.api_key = "_T1Kr-ySr5mkA3Za1bKb" # mi clave
    #qd_data = quandl.get("AAPL", start_date= "2010-01-01", end_date= "2020-01-01")
    #qd_data = quandl.get('SHARADAR/SEP', ticker='AAPL')
    # nos qudamos con los datos ajustados
    
    # Recogemos los valores desde yahooFinances
    start =dt.datetime(2000,1,1)
    #start =dt.datetime.today() - dt.timedelta(days=150)
    #end = dt.datetime(2020,12,30)
    end= dt.datetime.today()- dt.timedelta(days=2)
    
    
    tickers = ['AAPL', 'MSFT', '^GSPC', 'ELE.MC','SAN.MC', 'BBVA.MC','ANA.MC','MTS.MC','GRF.MC']  # apple,microsfoft,sp500, endesa
    #valorNum = 7
    for i in range(len(tickers)): 
        analisis(tickers[i], start, end)
     
    print ("that´s all")        
    
#/******************************** FUNCION PRINCIPAL main() *********/ 
    
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
    
    #a.- Leer de WEB
    #df =web.DataReader(tickers[valorNum], 'yahoo', start, end)   # leemos los valore sde tesl    #Guardarlo en fichero .CSV
    df =web.DataReader(instrumento, 'yahoo', start, end)   # leemos los valore sde tesl    #Guardarlo en fichero .CSV
    #df.to_csv('endesa.csv')
    #b.- Leer de .CSV
    #df = pd.read_csv('endesa.csv', parse_dates=True, index_col=0)
    #mostrar comienzo final del fichero
    
    print(" Valores de ", instrumento)
    print(df.head())
    print(df.tail())    
    
    
    """
    ajustadas = [f for f in qd_data.columns if f.startswith('Adj')]  #devuelve una lista con las cadenas de las columnas
    qd_data = qd_data[ajustadas].copy()
    qd_data.columns = [f[5:] for f in qd_data.columns]   # quitamos las 5 primeras letas "ADJ. "   
    print(qd_data.head())
    """     
    # 2.- Calculamos el RSI
    df['RSI']= ta.momentum.rsi(df['Close'])
    df['MiIndice']= list(range(len(df)))
    
    # 2bis.- Calculamos MA
    df= MovingAverage(df,long_=40,short_=10)

    # 3.- Dibujamos las gráficas
    fig, (ax1,ax2) = plt.subplots(2,1, figsize=(18, 8))
    
    x_values = list(range(len(df)))  #creo un array de consecutivos para la x del plot
      
    """
    ax1.plot(1,1,x_values, df['Close'], color="red", label='cierre')
    ax2.plot(2,1,x_values, df['RSI'], color="green", label='rsi')
    ax2.set_xlabel('sesiones')
    ax1.set_title('Valor Cierre')
    ax2.set_title('RSI')
    #Plotear puntos
    ax2.plot(20, 67, '^')  
    #Plotaer lineas constantes
    ax2.hlines(30,0,len(df), colors='grey', linestyles='solid', linestyle='--', label='30')
    ax2.hlines(70,0,len(df), colors='grey', linestyles='solid', linestyle='--', label='70')
    

    ax1.legend(['','Cierre'], loc=1)
    ax2.legend(['','rsi','keyPoint','30','70'], loc=2)
    """
    
    ax1.plot(1,1,df.index, df['Close'], color="red", label='cierre')
    ax2.plot(2,1,df.index, df['RSI'], color="green", label='rsi')
    ax2.set_xlabel('Sesiones')
    ax1.set_title('Valor Cierre  '+instrumento)
    ax2.set_title('RSI')
    ax1.set_xlim(start, end)
    ax2.set_xlim(start, end)

    #Plotaer lineas constantes de los limites RSI
    ax2.hlines(30,start,end, colors='yellow', linestyles='solid', label='30')
    ax2.hlines(70,start,end, colors='yellow', linestyles='solid',  label='70')
    
    ax1.legend(['Cierre'], loc=1)
    ax2.legend(['rsi','30','70'], loc=2)    
    
    #Plotear puntos
    ax2.plot(start, 67, '^', color='red')  
    plt.show()
    
    
    #Llamadas a la Clase
    objetoJuan = Person("Viton", 36)
    objetoJuan.myfunc()

    
    #slopeJ3(df['Adj Close'])
    #MovingAverage(df,long_=200,short_=50)
    
    #TESTING
    #salvarExcel(df, "tendencia")
    dff,peaks,valleys= MAX_min_Relativos_v3(df['Close'])
    dff_RSI,peaks_RSI,valleys_RSI= MAX_min_Relativos_v3(df['RSI'])
    '''
    salvarExcel(dff, "endesa_valor")
    salvarExcel(dff_RSI, "endesa_RSI")
    salvarExcel(df, "endesa_base")
    '''

    # #################################################
    # #################################################
    # #################################################    
    # VAMOS A CREAR LA ESTRATEGIA 
    
    # 1.- Buscamos divergencia preci versu RSI en niveles de RSI de Sobrevendido (<30) 
    # 2.- Divergencia: precio Maximos decreciente y RSI minmos crecientes.
    # 3.- Señal
    
    ############ traza
    index_de_RSI_menor_que_valor = 'nada'
    valorMax =0
    valor2MaxDecreciente =0
    indice2MaxDecreciente =0
    var2Max_RSI=0
    date2varMax_RSI=0
    fecha=0
    diaInicioPrecio=dt.datetime.today()
    diaInicioRSI=dt.datetime.today()
    diaFinPrecio=dt.datetime.today()
    diaFinRSI=dt.datetime.today()
    ref_KeyData =1
    
    rsi_=df.columns.get_loc("RSI")
    marcaMxMn_=dff.columns.get_loc("marcasMxMn")
    valorSerie_=dff.columns.get_loc("serie")

    datosRelevantes = pd.DataFrame(columns=('fecha1', 'valorMIN_1', 'fecha2','valorMIN_2','fechaRSI1', 'valorMIN_RSI_1', 'fechaRSI2','valorMIN_RSI_2','fechaValorMAX_1','valorMAX_1','fechaValorMAX_2','valorMAX_2' ))    
    
    marca='buscando_RSI'
    marca2='nada'
    marca3='nada'
    i_1=0
    i_2=0
    maxBajando = False
    RSIsubiendo = False
    
    
    for i in range(15,len(df)):     #me falta saber como conseguir el indice numerico de una etiqueta
        
        if(i==174):
            a=5
    
        # RSI menos de 30 **************************************************************************RSI    
        if(marca== 'buscando_RSI' and df.iloc[i,rsi_] < 20):   #Me tegno que currar un maquina de estados son switch/case
            #print ('rsi <40  en', i)   
            marca='RSI_encontrado'
            index_de_RSI_menor_que_valor =df.index[i]
        if(marca== 'RSI_encontrado' and df.iloc[i,rsi_] > 40):   #el RSI se sale de overSlod
            marca='buscando_RSI'
            marca2= 'nada'
            marca3= 'nada'
            #marca='RSI_encontrado'  # quitar solo para testeo del rango 100!!!!
        #********************************************************************************************RSI
        
        
        # SON MINIMOS del precio decreciendo
        if(marca== 'RSI_encontrado'): 
            # minimos del precio decreciendo**************************************** valor_Min_decreciente
            if (dff.iloc[i,marcaMxMn_] == 1 and marca2== 'nada'):
                marca2= 'primerMax'
                varMax=dff.iloc[i,0]  #almaceno posicion
                valorMax =dff.iloc[i,0]
                datevalorMax = df.index[i]
                diaInicioPrecio =df.index[i]
                i_1=i
                #print ("señal 20 en" ,i)
                
            if (dff.iloc[i,marcaMxMn_] == 1 and 
                (marca2== 'primerMax' or marca2== 'ultimoMaxDecreciente') and 
                dff.iloc[i,0] < varMax):
                
                varMax=dff.iloc[i,0]  #almaceno posicion
                marca2= 'ultimoMaxDecreciente'            
                valor2MaxDecreciente=dff.iloc[i,0]
                datevalor2MaxDecreciente = df.index[i]
                indice2MaxDecreciente = i
                diaFinPrecio =df.index[i]
                i_2=i
                #print ("señal 21 en" ,i)
                            
            if (dff.iloc[i,marcaMxMn_] == 1 and                 
                (marca2== 'primerMax' or marca2== 'ultimoMaxDecreciente') and                 
                dff.iloc[i,0] > varMax):                
                #no es maximo decreciente
                marca2= 'nada'   
                diaInicioPrecio =dt.datetime.today()
                diaFinPrecio =dt.datetime.today()
                #print ("señal 22 en" ,i)                         
            #*********************************************************************** Valor_Min_decreciente
       
            
            # *********************************************************************  mínimos RSI creciente
            if (dff_RSI.iloc[i,marcaMxMn_] == 1 and marca3== 'nada'):
                marca3= 'primerMIN_RSI'
                varMax_RSI=dff_RSI.iloc[i,0]
                valorMax_RSI =dff_RSI.iloc[i,0]
                datevarMax_RSI=df.index[i]
                diaInicioRSI =df.index[i]
                
            if (dff_RSI.iloc[i,marcaMxMn_] == 1 and 
                (marca3== 'primerMIN_RSI' or marca3== 'ultimoMinCreciente_RSI')and                                 
                dff_RSI.iloc[i,0] > varMax_RSI):

                varMax_RSI=dff_RSI.iloc[i,0]  #almaceno posicion
                marca3= 'ultimoMinCreciente_RSI'
                var2Max_RSI=dff_RSI.iloc[i,0]
                date2varMax_RSI=df.index[i]
                diaFinRSI =df.index[i]


            if (dff_RSI.iloc[i,marcaMxMn_] == 1 and 
                (marca3== 'primerMIN_RSI' or marca3== 'ultimoMinCreciente_RSI')and 
                dff_RSI.iloc[i,0] < varMax_RSI):
                # minimo no creciente
                marca3= 'nada'
                diaInicioRSI =dt.datetime.today()
                diaFinRSI =dt.datetime.today()
            # *********************************************************************  mínimos RSI creciente
                
            
            # ************************************ Fechas en mismo intervalo temporal
            ventana = 20   #ubicar en el mismo tiempo las dos condiciones
            if (( dt.timedelta(days=ventana) > abs(diaInicioPrecio - diaInicioRSI )) and 
                ( dt.timedelta(days=ventana) > abs (diaFinPrecio - diaFinRSI ))):
                intervaloValido=True
            else:
                intervaloValido=False
            
            # ************************************* Determinar la tendencia de los Maximos del valor, para esperar la ruptura
            # estamos analizando si sería mejor la rotura de la media movil de las ultimas sesiones, da un efecto parecido ¿vale?
            
            #1.-Buscar los maximos en el intervalo donde se dan las condiciones anteriores
            if (False):     # quito esta parte en favor de las medias moviles
                if((intervaloValido and marca2== 'ultimoMaxDecreciente' and marca3== 'ultimoMinCreciente_RSI') and (True)): 
                    
                    
                    #J3
                    ventanita = 5 
                    primero=False
                    for jj in range((i_1-ventanita),(i_2+ventanita)):   # Intervalo de lon minimos consecutivos
                        if(dff.iloc[jj,marcaMxMn_] == 2):      #busco marca de maximo en la tabla
                            if (primero ==False):
                                
                                valor_1=dff.iloc[jj,0]
                                valor_2=dff.iloc[jj,0]
                                fechaValor_1= df.index[jj]
                                fechaValor_2= df.index[jj]
                                primero=True
                            else:
                                valor_2=dff.iloc[jj,0]
                                fechaValor_2= df.index[jj]
                       
                    #slopeJ3_2points(x1,y1,x2,y2):                
                    #slopeJ3_2points(fechaValor_1,valor_1,fechaValor_2,valor_2)      
                    #revisar si Dff y Df cumplen para calcular la pendiente          
           
            #1bis.- Analisis con MediaMovil del punto de entrada

            # Ya tengo la MA corta y larga; ahora comprobar que le precio supere al alza
                             #J3
            ventanita = 20 
            close_=df.columns.get_loc("Close")
            ma_=df.columns.get_loc("MA_10")
            for jj in range((i),(i+ventanita)):   # busco el corte en futuro inmediato
                if(jj>len(df)):
                    break
                if(df.iloc[jj,close_] > df.iloc[jj,ma_]):
                    valor_2=dff.iloc[jj,0]
                    fechaValor_2= df.index[jj]
                    break
            
                
            
            
            
            # **************************************************** PRESENTACION DE RESULTADO Y EXCEL
            
            #2.- Creo un dataFrame para almacenar PUNTOS RELEVANTES
  
            if(intervaloValido and marca2== 'ultimoMaxDecreciente' and marca3== 'ultimoMinCreciente_RSI'):   #ojo
                print ("señal en" ,i)
                print ('index_de_RSI_menor_que_valor',index_de_RSI_menor_que_valor)                
                print ('valorMax',valorMax, 'en fecha', datevalorMax)
                print ('valor2MaxDecreciente',valor2MaxDecreciente, 'en fecha', datevalor2MaxDecreciente)                    
                print ('valorMin RSI',valorMax_RSI , 'en fecha', datevarMax_RSI )
                print ('valor2MinCrecietne RSI',var2Max_RSI, 'en fecha', date2varMax_RSI)
                print ('fecha', df.index[i])
                
                datosRelevantes.loc[ref_KeyData,'valorMIN_1']= valorMax
                datosRelevantes.loc[ref_KeyData,'valorMIN_2']= valor2MaxDecreciente
                datosRelevantes.loc[ref_KeyData,'fecha1']= datevalorMax
                datosRelevantes.loc[ref_KeyData,'fecha2']= datevalor2MaxDecreciente
 
                datosRelevantes.loc[ref_KeyData,'valorMIN_RSI_1']= valorMax_RSI
                datosRelevantes.loc[ref_KeyData,'valorMIN_RSI_2']= var2Max_RSI
                datosRelevantes.loc[ref_KeyData,'fechaRSI1']= datevarMax_RSI
                datosRelevantes.loc[ref_KeyData,'fechaRSI2']= date2varMax_RSI
                
                # Quito del excel los maximos decrecientes, voy a probar con la MA.
                #datosRelevantes.loc[ref_KeyData,'valorMAX_1']= valor_1
                datosRelevantes.loc[ref_KeyData,'valorCORTE']= valor_2
                #datosRelevantes.loc[ref_KeyData,'fechaValorMAX_1']= fechaValor_1
                datosRelevantes.loc[ref_KeyData,'fechaValorCORTE']= fechaValor_2
                
    
                
                ref_KeyData =ref_KeyData+1

                   
                continue #break
        
    """ 
    señal en 773
    index_de_RSI_menor_que_valor 2017-12-28 00:00:00
    valorMax 18.30500030517578 en fecha 2018-01-04 00:00:00
    valor2MaxDecreciente 18.299999237060547 en fecha 2018-01-09 00:00:00
    valorMin RSI 17.764999389648438 en fecha 2018-01-02 00:00:00
    valor2MinCrecietne RSI 18.125 en fecha 2018-01-08 00:00:00
    fecha 2018-01-09 00:00:00
    """
      
        
    print(datosRelevantes.head())
    print(datosRelevantes.tail())          
    salvarExcel(datosRelevantes , "deliverables/"+instrumento+"_señal_PRECIO_RSI")  
    

    
    
    
    
    
    # #################################################


    #tendecia_v1(dff, peaks, valleys)
    #salvarExcel(dff, "tendencia_3")
    
    
    #print(dff.tail())
    #print(valleys)
    #print(peaks)
    
    #df['tendencia']=tendencia_estadistica(df["Adj Close"], periodo =6, parametro=1)
    #MAX_min_Relativos(df["tendencia"], dataFrameStock= df)
    
    #Tendencias= MAX_min_Relativos_v2(df_test07['p'], distancia = 5)
    #print(Tendencias.head())
    #telegram_send('desde aqui te mandaré alertas para tu analisis')
    
    

#Final funcion main()************************************************/







#/*******************************************/
#/* Programa Principal  *********************/
#/*******************************************/

main()
