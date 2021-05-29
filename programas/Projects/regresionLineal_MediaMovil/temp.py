# -*- coding: utf-8 -*-


"""
******************************************************************************
ESTRATEGIA DE INVERSION AUTOMATICA COMPLETA BASADA EN 
******************************************************************************
******************************************************************************


Started on 24/May/2021
Version_1: 

Objetivo: 



@author: J3Viton

"""

# J3_DEBUG__ = False  #variable global (global J3_DEBUG__ )



################################ IMPORTAMOS MODULOS A UTILIZAR.
import pandas as pd
import numpy as np
import datetime as dt
import pandas_datareader as web

import matplotlib.pyplot as plt
plt.rcParams['figure.figsize'] = 18, 8
plt.style.use("bmh")   


import quant_j3_lib as quant_j


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
    
   
#/******************************** FUNCION PRINCIPAL *********/    
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
    
   
  


#/*******************************************/
#/* Programa Principal  *********************/
#/*******************************************/

main()
