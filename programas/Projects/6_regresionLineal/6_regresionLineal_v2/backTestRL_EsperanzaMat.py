#!/usr/bin/env python
# coding: utf-8

# # <font color='red'>Backtest vectorizado para una estrategia 'Regresion lineal' definida.</font>
# 
# ### Hackeado by J3viton (learning BackTesting 2021).

# ---

# En este notebook vamos a automatizar el backtesting para estrategias. Previamente tenemos que definir **la estrategia** usando el template (import estrategia_XX as rrgg), donde definimos la clase estrategia que contiene los metodos de analisis, entreda y salida de mercado. Este módulo se programa y adapta para cada estrategia. Luego en el metodo 'analisis' se crea un fichero excel con las metricas y rendimientos para evaluar la estrategia.
# 
# Vamos a usar el módulo Pandas, para realizar un backtest vectorizado, es decir calcular el resultado del backtest sin iterar sobre las filas (barras) de la serie temporal.

# Posteriormente graficamos y mostramos los parametros generales que nos permiten analizar la estrategia.
# 
# #### J3Viton  2021
# 
# link a la base:
# 
# https://github.com/Python-para-Trading/Webinars-Docs/blob/master/Webinar%202/Webinar%202%20-%20Backtest%20con%20Pandas%20v%202.ipynb.

# ---

# # DEFINICION DEL SISTEMA

# Como es usual, importamos los módulos que vamos a necesitar para las distintas tareas, y preparamos Matplotlib para una mejor visualización de los gráficos en el notebook.
# 
# Se importa un modulo llamado analisis, en realidad se trata de un archivo .py con algunas funciones de apoyo para el trabajo, debe estar guardado en la misma carpeta que este notebook.
# Se importa el módulo 'estrategia_XX', donde se define la estrategia de entreda y salida

# Es importante tener clara la lógica del sistema, pues debemos plasmarla de forma sencilla y correcta en el dataframe para realizar el backtest del mismo.
# 

# In[1]:


import analisis
import regresionAMedia as rrgg  #cambiar segun el módulo con la estrategia implementado
import pandas as pd
import datetime as dt
from time import time
import yfinance as yf
import numpy as np
import sys


# In[2]:


#get_ipython().run_line_magic('matplotlib', 'inline')
#import matplotlib.pyplot as plt
#plt.rcParams['figure.figsize'] = 18, 8
#plt.style.use('ggplot')

#from IPython.display import display, Markdown


# ***0.- RECOGIDA DE DATOS INICIALES***
# Introducimos el instrumento y las fechas
# 

# In[3]:


instrumento_ = 'HSY'  # ticker del valor en yahooFinance

#instrumento_ = sys.argv[1]

Fecha_Cominezo_Backtesting = dt.datetime(2015,1,2)
#Fecha_Final_Backtesting    = dt.datetime(2022,9,15)
Fecha_Final_Backtesting    = dt.datetime.today()



# ***1.- Rango fechas a analizar***
# 
# Definimos el rango global de datos historicos que vamos a evaluar.
# Definimos la ventana que vamos a ir desplazando por todo el espectro para ir analilazando como se comporta la estrategia. La funion 'analisis' nos vale para tiempo real y para backtesting, para back le pasamos la ventana como si la fecha de fin de la ventana fuera la fecha de hoy.
# Tener en cuenta que la 'ventana' tiene uqe tener una anchura que nos permita hacer los calculos en rolling (ejemplo EMA 200)

# In[4]:


# Rango completo para backTesting
#start2 =dt.datetime(2008,1,2)
start2= Fecha_Cominezo_Backtesting 
#end2   =dt.datetime(2021,11,18)
end2= Fecha_Final_Backtesting 
start_G= start2.strftime("%Y-%m-%d")
end_G  =   end2.strftime("%Y-%m-%d")
TOTAL_len= (end2-start2).days
print('Tamaño timeseries global a analizar:  ', TOTAL_len, 'sesiones')

#ventana de analisis 200 sesiones
startWindow2 = start2  #dt.datetime(2008,1,5)
endWindow2   =startWindow2 + dt.timedelta(days=500) #ventana grande para que se puedan hacer los calculos de EMA200
startWindow= startWindow2.strftime("%Y-%m-%d")
endWindow  =   endWindow2.strftime("%Y-%m-%d")
window_len= (endWindow2-startWindow2).days
print('Tamaño de la ventana a analizar paso a paso:  ', window_len, 'sesiones')


# In[5]:


#dff = pd.DataFrame(columns=('Close','Volume', 'Senal', 'Dif_Close', 'Retornos','Capital'))


# ***2.- Descarrggamos los datos para el marco Global***

# In[6]:


instrumento = instrumento_  # 'rovi.mc'  #Vamos título a título. Mejora: Conjunto de títulos


# In[7]:


dff = yf.download(instrumento, start_G,end_G)


# In[8]:


dff.dropna(inplace=True)  
dff.head()


# ***3.- Creamos la clase strategy que tiene toda la lógica***

# In[9]:


regreMedia= rrgg.StrategyClass(back=True)    #Creamos la clase


# ***4.- Recorremos el dataframe con valores buscando las señales de la estrategia***

# In[10]:


dff.index


# In[ ]:





# ## Proceso de backTesting ##
# 
# En este 'for' vamos recorriendo la muestra del historico de datos (TOTAL), desplazando una sesión hacia el futuro 
# en cada iteracion. Vamos pasando la movilola del pasado sesión a sesión por el análisis descrito en Strategy class.
# 
# Ouput:
# El sistema registra los siguientes parámetros:
# 
# .-
# .-
# .-
# 

# In[11]:


startWindow


# In[12]:


tiempo_inicial = time()   # Tomamos tiempos para ver cuanto tarda en hacer la estrategia


# In[13]:


dfe = pd.DataFrame({'A' : []})   #df empty


# ***En este 'for' desplazamos la ventana sesión a sesión a lo larrggo de todo el rango de fechas. Dejamos que las funciones de la clase estrategia hagan el trabajo de comprar//vender y anotar***
# 

# In[14]:


#Para pruebas
#TOTAL_len =500  #conentar para hacer un backtesting completo

for i in range(TOTAL_len):
    endWindow3   =endWindow2 + dt.timedelta(days=i) 
    endWindow    =endWindow3.strftime("%Y-%m-%d")
    print ('end date:', endWindow)
    
    if(endWindow in dff.index):
        df_aux= dff.loc[startWindow:endWindow]       #voy pasando los datos desplazando la ventana
        
        recogo = regreMedia.analisis(instrumento, startWindow, endWindow, df_aux) #Llamada a la clase estrategia. LA CLAVE DE TODO!!!
        
        print ('................................................Analizando, muestra', i, 'de', TOTAL_len, 'fecha', endWindow)
        
            
    else:
        print('..............Día sin sesión, next please')

        


# ***Recogemos los datos de las entradas que ha realizado la Estrategia***

# In[15]:


data=rrgg.StrategyClass.dfLog
#data.dropna(inplace=True) 


# In[16]:


##data.tail()


# In[17]:


##data['Senal'].plot(title = 'Señales de compra de la estrategia ' )
# Ploteando una parte
#data.loc['2010':'2022','Senal'].plot(title = 'Señales Regresión a la media ' +instrumento,xlim=('2010','2022'))


# In[18]:


tiempo_final = time() 
 
tiempo_ejecucion = (tiempo_final - tiempo_inicial)/60
 
print ('El tiempo de ejecucion fue:',tiempo_ejecucion,"minutos") #En segundos


# In[19]:


data.loc['2011-01-04':'2019-11-04']


# In[20]:


#Guardamos el resultado del analisis en un pickle
#dff.to_pickle("./primerBack_IBE.pkl")


# ***3.- Ingeniería de datos para calcular la bondad de la estrategia***

# In[21]:



data['Dif_Close'] = data.Price.pct_change()
data['Retornos'] = data.Dif_Close * data.Senal.shift(1)   
data['Capital'] = (data.Retornos + 1).cumprod() * 100
    
rrgg.StrategyClass.dfLog=data  #Ojo a esta liena, no me cuadra.

#quant_j.salvarExcel(StrategyClass.dfLog, "log"+instrumento)   
#data.to_pickle('almacen')    #df = pd.read_pickle(file_name)


# >Para calcular los retornos del sistema, calculamos la diferencia relativativa entre el precio de cierre y el del día anterior. Para posteriormente multiplicarlo por la señal que del día anterior que nos indicaba la posición a tomar (si estaba comprado, sumo beneficio).

# In[22]:


##data.tail()


# In[23]:


##data[60:]


# >El capital, por comodidad, lo calcularemos en base 100, es decir como si iniciaramos la inversión con 100 unidades monetarias. Para su calculo arrastramos el producto acumulado de los retornos mas 1, multiplicados como dijimos por 100.

# Pero para observar gráficamente la evolución del sistema necesitamos un gráfico con mas información. Para ello definimos una función que nos mostrará un gráfico con la evolución de nuestra estrategia, comparandola con la del activo. En un subgráfico se visualizará el drawdown del sistema, comparado de nuevo con el del activo. Y por útlimo las posiciones que toma el sistema.

# In[24]:


def grafico (df):
    estudio = df.copy()
    
    DD_bh, maxDD, maxDD_ini, maxDD_fin = analisis.DrawDown(estudio.Dif_Close[60:], info = False) 
    
    DD, maxDD, maxDD_ini, maxDD_fin = analisis.DrawDown(estudio.Retornos.fillna(0), info = False) 

    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, sharex=True, figsize=(18, 12), gridspec_kw = {'height_ratios':[3, 1, 1]})
    fig.suptitle('Estrategia vs B & H', fontsize=20)

    #Primer plot analiza la evolcuion de una inversion de 100€ en buy&hold y la estrategia)
    ax1.plot(estudio.Capital)
    ax1.plot((estudio.Price) * (100/estudio.Price[1]))
    ax1.set_title('Capital')
    ax1.legend(['Estrategia','Buy & Hold'])

    ax2.plot(DD*100, c='0.5')
    ax2.plot(DD_bh*100, c='y')
    ax2.fill_between(DD.index, 0, DD*100, color='0.7')
    ax2.set_title('Drawdown')
    ax2.legend(['Estrategia','Buy & Hold'])

    ax3.plot(estudio.Senal, c='orange')
    #ax3.fill_between(estudio.index, 0, estudio.Senal*100, color='orange')
    ax3.set_title('Posición')

    plt.show()
    return


# In[25]:


##print(instrumento)


# In[26]:


#grafico(data)


# ---

# In[27]:


#data[55:70]


# ---

# # ANALISIS DEL SISTEMA

# In[28]:

print("**********************************************************************")    
print("**********************************************************************")    
print("*************** A N A L I S I S **************************************")    
print("**********************************************************************")    
print("**********************************************************************")    

print(instrumento)
Beneficio_Bruto = data.Capital[-1] - data.Capital[1]
print ('Beneficio Bruto : {:.2f} €  con una inverison de 100€'.format(Beneficio_Bruto))


# In[29]:


#Rentabilidad anual compuesta. Calculamos lo que la inversion se ha incrementado cada año con el interes compuesto
CAGR = analisis.CAGR(data.Retornos)
print ('CAGR : {:.2f}%'.format(CAGR * 100))


# In[30]:


#Ratio calculado restando una rentabilidad segura a nuestra rentabilidad de estrategia y dividido por el riego (=volatilidad)
data.Retornos=data.Retornos.replace(0,np.e)  #Quito los cero (no sepuede hacer logariotmo de cero), pero no se que poner
Sharpe = CAGR / (np.log(data.Retornos + 1).std(skipna=True) * 252 ** 0.5)
print ('Sharpe : {:.3f}'.format(CAGR ))

print ( "Sharpe: Se calcula dividiendo la rentabilidad de un fondo menos la tasa de interés sin riesgo entre la volatilidad o desviación standard de esa rentabilidad en el mismo periodo.")


# In[31]:


# Actualizo la excel con los economic
regreMedia.analisisEconomics(instrumento)


# ---
# 

# In[32]:


# 


# ### Cálculo esperanza matemática
#  
#  (%Aciertos * beneficioMedio )-(%Errores * perdidaMedia)
#  
#  Nos da idea el benefcio esperado por entrada

# In[33]:


print("Operaciones con beneficio ->", 
      data[data['ExitReason'] ==1]['ExitReason'].count()) 
print("Operaciones con perdidas ->", 
      data[data['ExitReason'] ==-1]['ExitReason'].count()) 
  
data[data['ExitReason']>0]['ExitReason'] 

#data[data['Senal']>0][1:10]
#data[data['Senal']>0].index[1]


# In[34]:


# ENTRADAS
print (data[(data['Senal']>0) & (data['Beneficio']>0)].index[0])
data[(data['Senal']>0) & (data['Beneficio']>0) ][0:5] 
# SALIDA PERDIDAS
print (data[(data['Senal'].shift(1) >0) & (data['ExitReason']== -1)].index[0])
data[(data['Senal'].shift(1) >0) & (data['ExitReason']== -1)][0:5]
# SALIDA GANANCIAS
data[(data['Senal'].shift(1) >0) & (data['ExitReason']== 1)][0:5]


# In[35]:


serieIndicesENTRADA=data[(data['Senal']>0) & (data['Beneficio']>0)].index

print(serieIndicesENTRADA.size)

serieIndicesENTRADA

serieIndicesEXIT=data[(data['ExitReason']==1) | (data['ExitReason']==-1)].index

print(serieIndicesEXIT.size)

#data['ExitReason'][serieIndicesEXIT[2]]


# In[36]:


serieIndicesENTRADA


# In[37]:


#Cálculo Esperanza Matemática
countGanando=0
countPerdiendo=0

bolsaGanando=0
bolsaPerdiendo=0

for i in range(serieIndicesEXIT.size):
    if(data['ExitReason'][serieIndicesEXIT[i]] == -1):
        ref1  = data['Price'][serieIndicesEXIT[i]]
        ref2 = data['Price'][serieIndicesENTRADA[i]]
        print ("-1",ref1, ref2)
        countPerdiendo= 1+countPerdiendo
        bolsaPerdiendo= bolsaPerdiendo + (ref1-ref2)

    
    if(data['ExitReason'][serieIndicesEXIT[i]] == 1):
        ref1  = data['Price'][serieIndicesEXIT[i]]
        ref2 = data['Price'][serieIndicesENTRADA[i]]
        print ("+1",ref1, ref2)
        countGanando= 1+countGanando
        bolsaGanando= bolsaGanando + (ref1-ref2)
    
#(%Aciertos * beneficioMedio )-(%Errores * perdidaMedia)

count=countGanando+countPerdiendo


print ("Ganado (€)--> ", bolsaGanando, " Número operaciones ganando   ", countGanando)   
print ("Perdiendo (€) -->", bolsaPerdiendo, " Número operaciones perdiendo", countPerdiendo) 
print (" Media perdiendo(€) -> ", (bolsaPerdiendo/countPerdiendo),"\n", "Media ganando(€) -> ", (bolsaGanando/countGanando)) 


esperanza = (countGanando/count *(bolsaGanando/countGanando))+(countPerdiendo/count *(bolsaPerdiendo/countPerdiendo))
print("")
print(instrumento)
print("ESPERANZA MATEMATICA ES: ", esperanza)


