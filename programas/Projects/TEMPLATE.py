# -*- coding: utf-8 -*-
"""
Created on Fri Oct  8 16:29:16 2021

@author: J3
"""

"""
******************************************************************************
Programas para aprender con el libro de ML4AT
******************************************************************************
******************************************************************************
Our rules are:


Fuente: https:/


            


Started on Oct/2021
Version_1: 

Objetivo: 



@author: J3Viton

"""


# J3_DEBUG__ = False  #variable global (global J3_DEBUG__ )
TELEGRAM__ = True


################################ IMPORTAMOS MODULOS A UTILIZAR.
import pandas as pd
import numpy as np
import datetime as dt
import quant_j3_lib as quant_j


#/***************************************  Guardamos/Leemos Informacion en fichero JSON 
import json

with open('config.json', 'r') as file1:
    config = json.load(file1)

database_depar =    config['departamento']
database_password = config['PRODUCTION']['DB_PASSWORD']
empleado = config['empleados'][0]['nombre']

file1.close()




#/***************************************  Guardamos configuracion en fichero






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
        'documentacion sencilla...'
        print("Hello my parametro is " + self.para_02)
        
    def testing_123(self):
        slopeJ3_2points(1,3,2,4)
    def debugging_(self):
        return (J3_DEBUG__)

#################################################### Clases FIN




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


#/*******************************************************************/
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
    # Enter start and end date
    #start = '2020-1-20'
    #end = '2021-1-20'
    
    #start =dt.datetime(2000,1,1)
    start =dt.datetime.today() - dt.timedelta(days=1000)    #un año tiene 250 sesiones.
    #end = dt.datetime(2019,10,1)
    end= dt.datetime.today()  - dt.timedelta(days=1)        #Quito hoy para no ver el valor al ejecutar antes del cierre
    #end = '2021-9-19'
    
    #if(TELEGRAM__):
    #    telegram_send("2.- SALIDA Estrategia Regresion a la media V0.1. SALIDA \n ")
        

    # Create Regressionanalyis class
    #ra = Regressionanalysis('^NSEI', start, end, interval='60m')
    #ra.linear_regression(independent='Open', dependent='Close')
    # Me resulta complicado con esta libreria, no merece la pena ahora que estamos porbando, ya llegaran tiempos de afinar.
    
    """
    for i in range(len(senalesG)):
        estado=  analisis(senalesG['regresiones'][i]['ticker'], start, end, i)
        if (estado ==99):
            senalesG['regresiones'][i]['BuySell']=99
    
    
    Actualizo el fichero de configuracion si procede, claro
    with open('senales.json', 'w') as file:
        json.dump(senalesG ,file)
    file.close()
    """        
    
    print ("******************************************************************************That´s all") 
    print ("****************************************************************************************")       
    
    
    
#/**********************************************************************main()    






#/*******************************************/
#/* Programa Principal  *********************/
#/*******************************************/

main()



