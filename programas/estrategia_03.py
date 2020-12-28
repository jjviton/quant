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
import seaborn as sns
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
    # 1.- RECOGEMOS DATOS DE UNA FUENTE FIABLE (QUANDL/YFINANCES)
    #quandl.ApiConfig.api_key = "_T1Kr-ySr5mkA3Za1bKb" # mi clave
    #qd_data = quandl.get("AAPL", start_date= "2010-01-01", end_date= "2020-01-01")
    #qd_data = quandl.get('SHARADAR/SEP', ticker='AAPL')
    # nos qudamos con los datos ajustados
    
    # Recogemos los valores desde yahooFinances
    #start =dt.datetime(2000,1,1)
    start =dt.datetime.today() - dt.timedelta(days=150)
    #end = dt.datetime(2004,1,25)
    end= dt.datetime.today()
    tickers = ['AAPL', 'MSFT', '^GSPC', 'ELE.MC']  # apple,microsfoft,sp500, endesa
    valorNum =3
    
    #a.- Leer de WEB
    df =web.DataReader(tickers[valorNum], 'yahoo', start, end)   # leemos los valore sde tesl    #Guardarlo en fichero .CSV
    #df.to_csv('endesa.csv')
    #b.- Leer de .CSV
    #df = pd.read_csv('endesa.csv', parse_dates=True, index_col=0)
    #mostrar comienzo final del fichero
    
    print(" Valores de ", tickers[valorNum])
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
    ax1.set_title('Valor Cierre')
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
    Tendencias= MAX_min_Relativos_v3(df['Close'])
    
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
