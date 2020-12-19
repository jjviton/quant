#!/usr/bin/env python
# coding: utf-8

# # Backtest vectorizado y optimización de parametros con Pandas.

# ---

# En este Notebook vamos a realizar un backtest de una estrategia sencilla. Se trata de un cruce de medias, que se puede considerar el "Hello World!" de los sistemas automáticos.
# 
# Vamos a usar el módulo Pandas, para realizar un backtest vectorizado, es decir calcular el resultado del backtest sin iterar sobre las filas (barras) de la serie temporal.

# Posteriormente realizarmos una optimización de los parametros del sistema, y veremos como el calculo vectorizador nos permite hacer un gran número de backtests para la optimización en un tiempo muy breve.

# ---

# # IMPORTACIÓN DE MODULOS Y CARGA DE DATOS
# 

# Como es usual, importamos los módulos que vamos a necesitar para las distintas tareas, y preparamos Matplotlib para una mejor visualización de los gráficos en el notebook.
# 
# Se importa un modulo llamado **analisis**, en realidad se trata de un archivo .py con algunas funciones de apoyo para el trabajo, debe estar guardado en la misma carpeta que este notebook.

# In[2]:


import pandas as pd
import analisis
import numpy as np
import itertools
import seaborn as sns

#get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plt
plt.rcParams['figure.figsize'] = 18, 8
plt.style.use('ggplot')

from IPython.display import display, Markdown

from matplotlib import style
style.use ('ggplot')   #poner Spider in graph automatico

# Importamos el modulo **quandl** que nos proporcionará una descarga de los datos que vamos a necesitar, en este caso la cotización diaria de las acciones de Apple.  

# In[6]:


import quandl
quandl.ApiConfig.api_key = "_T1Kr-ySr5mkA3Za1bKb" # Para una descarga ocasional no necesitas la API KEY.
qd_data = quandl.get("WIKI/AAPL", start_date= "2000-01-01", end_date= "2018-06-15")


# Tambien puedes cargar los datos desde el archivo pickle.

# In[9]:


# qd_data = pd.read_pickle('apple_qd.pkl')


# Veamos la cabecera del dataframe que acabamos de crear con los datos descargados.

# In[10]:


print(qd_data.head())


# La tabla muestra que tenemos datos sin ajustar y ajustados. Tomaremos solo los datos OHLCV ajustados y el volumen, prescindiremos del resto de columnas, y eliminaremos el prefijo __Adj.__ para mas comodidad de uso.

# In[23]:


ajustadas = [f for f in qd_data.columns if f.startswith('Adj')]  #devuelve una lista con las cadenas de las columnas

qd_data = qd_data[ajustadas].copy()
print(qd_data.columns[5:])
qd_data.columns = [f[5:] for f in qd_data.columns]
qd_data.head()


# In[25]:


ajustadas   #type()
qd_data.head()
qd_data.tail()


# Para usarlo en nuestro backtest vamos a hacer una copia del dataframe pero solo hasta 2017.

# In[26]:


data = qd_data[:'2016'].copy()


# ---
# 

# # DEFINICION DEL SISTEMA

# Es importante tener clara la lógica del sistema, pues debemos plasmarla de forma sencilla y correcta en el dataframe para realizar el backtest del mismo.
# 
# Esta estrategia utiliza dos medias simples del precio de cierre, de 20 y 60 periodos. Calculemoslas y asignamos sus valores a nuevas columnas de nuestro dataframe.
# 
# Para ello usamos la función **rolling** de Pandas, que va _rodando_ una ventana de N valores, sobre la que realiza un calculo, en este caso la media.

# In[27]:


data['SMA_20'] = data.Close.rolling(20).mean()
data['SMA_60'] = data.Close.rolling(60).mean()


# Como lo que nos interesa es su cruce, para saber cuando se produce calcularemos la diferencia entre ambas medias para cada muestra. Y el signo de la diferencia será la señal para establecer la posición del sistema.
# 
# Así cuando la diferencia sea positiva, significará que la media de 20 periodos es mayor que la de 60 periodos, indicando una tendencia alcista y tomando una posición compradora. Con una diferencia negativa, la lógica es justo la inversa y tomaremos posicion vendedora.

# In[28]:


data['Dif_SMA'] = data.SMA_20 - data.SMA_60
data['Senal'] = np.sign(data.Dif_SMA)


# Para calcular los retornos del sistema, calculamos la diferencia relativativa entre el precio de cierre y el del día anterior. Para posteriormente multiplicarlo por la señal que del día anterior que nos indicaba la posición a tomar.

# In[29]:


data['Dif_Close'] = data.Close.pct_change()

data['Retornos'] = data.Dif_Close * data.Senal.shift(1)


# In[37]:


data.iloc[70:75,:]


# El capital, por comodidad, lo calcularemos en base 100, es decir como si iniciaramos la inversión con 100 unidades monetarias. Para su calculo arrastramos el producto acumulado de los retornos mas 1, multiplicados como dijimos por 100.

# In[38]:


data['Capital'] = (data.Retornos + 1).cumprod() * 100  #interesanta que no multiplica por 100 cada fila, solo una vez


# Veamos como queda la tabla, tras añadir estas columnas.
# 
# Observamos de la fila 58 en adelante, pues hasta que no existen 60 filas no es posible calcular el SMA_60, y por tanto no tenemos señal para tomar posición.

# In[40]:


data[58:68]


# Veamos gráficamente como evoluciona el precio y las dos medias.

# In[41]:


data[['Close','SMA_20','SMA_60']].plot(color=['0.7','r','g'])
plt.show()


# Pero para observar gráficamente la evolución del sistema necesitamos un gráfico con mas información. Para ello definimos una función que nos mostrará un gráfico con la evolución de nuestra estrategia, comparandola con la del activo. En un subgráfico se visualizará el drawdown del sistema, comparado de nuevo con el del activo. Y por útlimo las posiciones que toma el sistema.

# In[57]:


def grafico (df):
    estudio = df.copy()
    DD_bh, maxDD, maxDD_ini, maxDD_fin = analisis.DrawDown(estudio.Dif_Close[60:], info = True)  #buy&Hold
    DD, maxDD, maxDD_ini, maxDD_fin = analisis.DrawDown(estudio.Retornos.fillna(0), info = True) #muestraEstrategia

    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, sharex=True, figsize=(18, 12), gridspec_kw = {'height_ratios':[3, 1, 1]})
    fig.suptitle('Estrategia vs B & H', fontsize=20)

    ax1.plot(estudio.Capital.fillna(100))               # nuestra evoluion del capital con nuestra estrategia
    ax1.plot((estudio.Close) *100 / estudio.Close[0])  # estrategia buy and Hold
    ax1.set_title('Capital')
    ax1.legend(['Estrategia','Buy & Hold'])

    ax2.plot(DD*100, c='0.5')
    ax2.plot(DD_bh*100, c='y')
    ax2.fill_between(DD.index, 0, DD*100, color='0.7')
    ax2.set_title('Drawdown')
    ax2.legend(['Estrategia','Buy & Hold'])

    ax3.plot(estudio.Senal, c='orange')
    ax3.fill_between(estudio.index, 0, estudio.Senal*100, color='orange')
    ax3.set_title('Posición')

    plt.show()
    return


# In[58]:


grafico(data)


# ---

# In[59]:



# In[46]:


data['Dif_Open'] = data.Open.pct_change()
data['Posicion'] = data.Senal.shift(1)
data['Retornos'] = data.Posicion.shift(1) * data.Dif_Open
data['Capital'] = (data.Retornos.fillna(0) + 1).cumprod() * 100


# In[47]:


data[55:70]


# In[48]:


fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, figsize=(18, 12), gridspec_kw = {'height_ratios':[3, 1]})
ax1.plot(data.Capital)
ax1.plot(data.Close *100 / data.Close[0])
ax1.set_title('Estrategia vs B & H')
ax1.legend(['Estrategia','Buy & Hold'])
ax2.plot(data.Posicion, c='y')
ax2.fill_between(data.index, 0, data.Posicion*100, color='y')
ax2.set_title('Posición')
plt.show()


# In[ ]:





# In[ ]:





# In[ ]:





# ---

# # ANALISIS DEL SISTEMA

# In[49]:


Beneficio_Bruto = data.Capital[-1] - data.Capital[0]
print ('Beneficio Bruto : {:.2f}'.format(Beneficio_Bruto))


# In[50]:


CAGR = analisis.CAGR(data.Retornos)
print ('CAGR : {:.2f}%'.format(CAGR * 100))


# In[51]:


DD, maxDD, maxDD_ini, maxDD_fin = analisis.DrawDown(data.Retornos) 


# In[52]:


Sharpe = CAGR / (np.log(data.Retornos + 1).std(skipna=True) * 252 ** 0.5)
print ('Sharpe : {:.3f}'.format(CAGR ))


# ---

# # OPTIMIZACION DEL SISTEMA

# In[6]:


op_data = qd_data[:'2016'].copy()
op_data['Dif_Close'] = op_data.Close.pct_change()
op_data['Dif_Open'] = op_data.Open.pct_change()


# In[9]:


def estrategia_medias (df, periodo_rapido, periodo_lento):
    
    estr = df.copy()
    estr[f'SMA_{periodo_rapido}'] = estr.Close.rolling(periodo_rapido).mean()
    estr[f'SMA_{periodo_lento}'] = estr.Close.rolling(periodo_lento).mean()
    estr['Dif_SMA'] = estr[f'SMA_{periodo_rapido}'] - estr[f'SMA_{periodo_lento}']    
    estr['Senal'] = estr.Dif_SMA / estr.Dif_SMA.abs()
    estr['Posicion'] = estr.Senal.shift(1)    
    estr['Retornos'] = estr.Posicion.shift(1) * estr.Dif_Open    
    estr['Capital'] = (estr.Retornos+1).cumprod() * 100
    
    resultados = {'Rapida' : periodo_rapido, 'Lenta' : periodo_lento}
    resultados['Beneficio Bruto'] = round(estr.Capital[-1]-100,2)
    resultados['CAGR'] = analisis.CAGR(estr.Retornos) 
    resultados['Sharpe'] = resultados['CAGR'] / (np.log(estr.Retornos + 1).std(skipna=True) * 252 ** 0.5)
    resultados['Máximo Drawdown'] = (estr.Capital.div(estr.Capital.cummax()).sub(1)).min()
    
    resultados['Número de trades'] = (np.sign(estr.Posicion * estr.Posicion.shift(1)) == -1).sum() 
    
    return estr, resultados


# In[15]:


periodos_rapido = range (5,160,5)
periodos_lento = range (20,210,5)


# In[18]:


get_ipython().run_cell_magic('time', '', "\ncoleccion = {}\nresultados = {}\n\nfor periodo_rapido in periodos_rapido:\n    for periodo_lento in periodos_lento:\n\n        \n        if periodo_lento <= periodo_rapido:\n            continue\n        estr, resultado = estrategia_medias (op_data, periodo_rapido, periodo_lento)\n        nombre = f'estrategia_{periodo_rapido}_{periodo_lento}'\n        coleccion[nombre] = estr\n        resultados[nombre] = resultado")


# In[17]:


print ('Realizados {} backtests sobre una serie de {} muestras'.format(len(coleccion), op_data.shape[0]))


# In[38]:


clasificacion = pd.DataFrame(resultados).transpose()
clasificacion.head(25)


# In[39]:


pd.DataFrame(clasificacion['Beneficio Bruto'].sort_values(ascending=False).head(10))


# In[40]:


pd.DataFrame(clasificacion.Sharpe.sort_values(ascending=False).head(10))


# In[41]:


pd.DataFrame(clasificacion['Máximo Drawdown'].sort_values(ascending=False).head(10))


# In[42]:


clasificacion['Beneficio Bruto'].sort_values(ascending=False).plot(kind='bar')


# In[43]:


(clasificacion['Beneficio Bruto']/clasificacion['Número de trades']).sort_values(ascending=False).plot(kind='bar')


# In[44]:


ax=sns.heatmap(clasificacion.pivot('Rapida','Lenta','Máximo Drawdown'), annot=False, fmt=".3", linewidths=0, cmap=plt.cm.jet)


# In[45]:


# ax=sns.heatmap(clasificacion.pivot('Rapida','Lenta','Sharpe'), annot=True, fmt=".3f", cmap=plt.cm.jet)
ax=sns.heatmap(clasificacion.pivot('Rapida','Lenta','Sharpe'), annot=False, fmt=".1f", cmap=plt.cm.jet )


# In[46]:


analisis.trisurf_heatmap (clasificacion, 'Rapida', 'Lenta','Sharpe', v1=45, v2=45)


# In[47]:


analisis.trisurf_heatmap (clasificacion, 'Rapida', 'Lenta','Máximo Drawdown',v1= 45, v2=45)


# ---

# # REVISIÓN DE LOS PARÁMETROS SELECCIONADOS

# In[48]:


pd.DataFrame(clasificacion.loc['estrategia_5_140'])


# In[49]:


grafico(coleccion['estrategia_5_140'])


# ---
# 

# # PRUEBA FUERA DE LA MUESTRA

# In[50]:


periodo_rapido = 5

periodo_lento = 140

out_sample= qd_data[data.shape[0]:].copy()

out_sample['Dif_Close'] = out_sample.Close.pct_change()
out_sample['Dif_Open'] = out_sample.Open.pct_change()


out_estr, out_resultado = estrategia_medias (out_sample, periodo_rapido, periodo_lento)


# In[51]:


grafico(out_estr)


# ---
